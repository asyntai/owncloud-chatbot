<?php

declare(strict_types=1);

namespace OCA\Asyntai\Panels;

use OCA\Asyntai\AppInfo\Application;
use OCA\Asyntai\Config;
use OCA\Asyntai\Controller\SettingsController;
use OCP\AppFramework\Http\TemplateResponse;
use OCP\Settings\ISettings;

class AdminPanel implements ISettings
{
    /** @var Application */
    private $app;

    public function __construct(Application $app)
    {
        $this->app = $app;
    }

    public function getPriority()
    {
        return 50;
    }

    public function getPanel(): TemplateResponse
    {
        /** @var SettingsController $controller */
        $controller = $this->app->getContainer()->query(SettingsController::class);

        return $controller->index();
    }

    public function getSectionID()
    {
        return Config::APP_ID;
    }
}
