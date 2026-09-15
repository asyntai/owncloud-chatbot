<?php

declare(strict_types=1);

/**
 * Runs on every request once the app is enabled.
 *
 * ownCloud loads every enabled app before it draws a page, for the login
 * screen and for public share links as well as for the normal interface. So
 * this one file decides, for every page, whether the chat belongs on it.
 */

use OCA\Asyntai\AppInfo\Application;

$app = new Application();
$app->addWidgetToPage();
