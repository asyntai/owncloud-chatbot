<?php

declare(strict_types=1);

namespace OCA\Asyntai;

use OCP\IConfig;

/**
 * Reads and writes the app settings, and cleans up what an administrator types.
 */
class Config
{
    public const APP_ID = 'asyntai';

    public const KEY_WIDGET_ID = 'widget_id';
    public const KEY_SCRIPT_URL = 'script_url';
    public const KEY_SHOW_LOGGED_IN = 'show_logged_in';
    public const KEY_SHOW_PUBLIC = 'show_public';

    public const DEFAULT_SCRIPT_URL = 'https://widget.asyntai.com/static/js/chat-widget.js';

    /** @var IConfig */
    private $config;

    public function __construct(IConfig $config)
    {
        $this->config = $config;
    }

    /**
     * People paste the whole snippet from the Asyntai dashboard, so accept that
     * as well as a bare widget ID. Returns an empty string when there is none.
     */
    public static function readWidgetId(?string $raw): string
    {
        $value = trim((string)$raw);

        if ($value === '') {
            return '';
        }

        if (preg_match('/data-asyntai-id\s*=\s*["\']([^"\']+)["\']/', $value, $matches) === 1) {
            $value = trim($matches[1]);
        }

        return preg_match('/^asyntai_[A-Za-z0-9]{6,64}$/', $value) === 1 ? $value : '';
    }

    /** Only a plain http or https address is accepted. Anything else falls back. */
    public static function normalizeScriptUrl(?string $raw): string
    {
        $value = trim((string)$raw);

        if ($value === '' || preg_match('#^https?://#i', $value) !== 1) {
            return self::DEFAULT_SCRIPT_URL;
        }

        return $value;
    }

    public function getWidgetId(): string
    {
        return self::readWidgetId($this->config->getAppValue(self::APP_ID, self::KEY_WIDGET_ID, ''));
    }

    public function setWidgetId(?string $raw): string
    {
        $clean = self::readWidgetId($raw);
        $this->config->setAppValue(self::APP_ID, self::KEY_WIDGET_ID, $clean);

        return $clean;
    }

    public function getScriptUrl(): string
    {
        return self::normalizeScriptUrl($this->config->getAppValue(self::APP_ID, self::KEY_SCRIPT_URL, ''));
    }

    /** The stored value, which is empty when the standard address is used. */
    public function getRawScriptUrl(): string
    {
        return (string)$this->config->getAppValue(self::APP_ID, self::KEY_SCRIPT_URL, '');
    }

    public function setScriptUrl(?string $raw): string
    {
        $value = trim((string)$raw);
        $clean = $value === '' ? '' : self::normalizeScriptUrl($value);
        $this->config->setAppValue(self::APP_ID, self::KEY_SCRIPT_URL, $clean);

        return $clean;
    }

    public function showForLoggedIn(): bool
    {
        return $this->config->getAppValue(self::APP_ID, self::KEY_SHOW_LOGGED_IN, 'yes') === 'yes';
    }

    public function showOnPublicPages(): bool
    {
        return $this->config->getAppValue(self::APP_ID, self::KEY_SHOW_PUBLIC, 'yes') === 'yes';
    }

    /**
     * The single rule for whether the chat belongs on a page.
     *
     * @param bool $loggedIn true for the normal interface, false for the login
     *                       screen and for public share pages.
     */
    public function shouldShow(bool $loggedIn): bool
    {
        if ($this->getWidgetId() === '') {
            return false;
        }

        return $loggedIn ? $this->showForLoggedIn() : $this->showOnPublicPages();
    }

    public function setShowForLoggedIn(bool $show): void
    {
        $this->config->setAppValue(self::APP_ID, self::KEY_SHOW_LOGGED_IN, $show ? 'yes' : 'no');
    }

    public function setShowOnPublicPages(bool $show): void
    {
        $this->config->setAppValue(self::APP_ID, self::KEY_SHOW_PUBLIC, $show ? 'yes' : 'no');
    }
}
