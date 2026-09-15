<?php

declare(strict_types=1);

namespace OCA\Asyntai\AppInfo;

use OCA\Asyntai\Config;
use OCP\AppFramework\App;
use OCP\AppFramework\Http\EmptyContentSecurityPolicy;
use OCP\Util;

class Application extends App
{
    public const APP_ID = Config::APP_ID;

    /** Where the chat sends questions and gets answers. */
    private const API_ORIGIN = 'https://asyntai.com';

    public function __construct(array $urlParams = [])
    {
        parent::__construct(self::APP_ID, $urlParams);
    }

    /**
     * Puts the loader on the page when the settings say so.
     *
     * The widget ID and the script address travel in two <meta> tags in the
     * page head, and the loader script reads them from there. ownCloud escapes
     * every attribute it writes, so nothing typed by an administrator can
     * break out of the tag.
     */
    public function addWidgetToPage(): void
    {
        $server = $this->getContainer()->getServer();

        /** @var Config $config */
        $config = $this->getContainer()->query(Config::class);

        $loggedIn = $server->getUserSession()->isLoggedIn();

        if (!$config->shouldShow($loggedIn)) {
            return;
        }

        Util::addHeader('meta', [
            'name' => 'asyntai-widget-id',
            'content' => $config->getWidgetId(),
        ]);
        Util::addHeader('meta', [
            'name' => 'asyntai-script-url',
            'content' => $config->getScriptUrl(),
        ]);
        Util::addScript(self::APP_ID, 'asyntai-loader');

        $this->openContentSecurityPolicy($config);
    }

    /**
     * Opens the content security policy just wide enough for the chat.
     *
     * ownCloud blocks every outside address by default, which is right.
     * Without this the widget draws itself but cannot reach the Asyntai
     * service, so it shows an empty window. Only the Asyntai addresses are
     * added, and only while the chat is switched on.
     */
    private function openContentSecurityPolicy(Config $config): void
    {
        $origins = [self::API_ORIGIN];

        // The administrator may point the app at another copy of the widget.
        $scriptOrigin = self::originOf($config->getScriptUrl());
        if ($scriptOrigin !== '' && !in_array($scriptOrigin, $origins, true)) {
            $origins[] = $scriptOrigin;
        }

        $policy = new EmptyContentSecurityPolicy();

        foreach ($origins as $origin) {
            $policy->addAllowedScriptDomain($origin);
            $policy->addAllowedConnectDomain($origin);
            $policy->addAllowedImageDomain($origin);
            $policy->addAllowedMediaDomain($origin);
            $policy->addAllowedFontDomain($origin);
            $policy->addAllowedStyleDomain($origin);
        }

        $this->getContainer()->getServer()->getContentSecurityPolicyManager()->addDefaultPolicy($policy);
    }

    /** "https://widget.asyntai.com/static/js/x.js" becomes "https://widget.asyntai.com". */
    public static function originOf(string $url): string
    {
        $parts = parse_url($url);

        if (!is_array($parts) || empty($parts['scheme']) || empty($parts['host'])) {
            return '';
        }

        $origin = $parts['scheme'] . '://' . $parts['host'];

        if (!empty($parts['port'])) {
            $origin .= ':' . $parts['port'];
        }

        return $origin;
    }
}
