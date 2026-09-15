<?php

declare(strict_types=1);

namespace OCA\Asyntai\Controller;

use OCA\Asyntai\Config;
use OCP\AppFramework\Controller;
use OCP\AppFramework\Http\DataResponse;
use OCP\AppFramework\Http\TemplateResponse;
use OCP\IRequest;

/**
 * Only an administrator reaches these methods: ownCloud demands an admin for
 * every controller method that does not carry @NoAdminRequired, and checks the
 * request token for every method that does not carry @NoCSRFRequired.
 */
class SettingsController extends Controller
{
    /** @var Config */
    private $config;

    public function __construct(string $appName, IRequest $request, Config $config)
    {
        parent::__construct($appName, $request);
        $this->config = $config;
    }

    /** Draws the settings panel. */
    public function index(): TemplateResponse
    {
        return new TemplateResponse(Config::APP_ID, 'admin', [
            'widget_id' => $this->config->getWidgetId(),
            'script_url' => $this->config->getRawScriptUrl(),
            'default_script_url' => Config::DEFAULT_SCRIPT_URL,
            'show_logged_in' => $this->config->showForLoggedIn(),
            'show_public' => $this->config->showOnPublicPages(),
        ], 'blank');
    }

    /** Stores the settings. */
    public function save(
        string $widgetId = '',
        string $scriptUrl = '',
        bool $showLoggedIn = true,
        bool $showPublic = true
    ): DataResponse {
        $cleanWidgetId = $this->config->setWidgetId($widgetId);
        $cleanScriptUrl = $this->config->setScriptUrl($scriptUrl);
        $this->config->setShowForLoggedIn($showLoggedIn);
        $this->config->setShowOnPublicPages($showPublic);

        return new DataResponse([
            'widgetId' => $cleanWidgetId,
            'scriptUrl' => $cleanScriptUrl,
            'showLoggedIn' => $showLoggedIn,
            'showPublic' => $showPublic,
            // True when something was typed but nothing usable came out of it.
            'widgetIdRejected' => trim($widgetId) !== '' && $cleanWidgetId === '',
        ]);
    }
}
