<?php

declare(strict_types=1);

namespace OCA\Asyntai\Panels;

use OCA\Asyntai\Config;
use OCP\IL10N;
use OCP\Settings\ISection;

class Section implements ISection
{
    /** @var IL10N */
    private $l;

    public function __construct(IL10N $l)
    {
        $this->l = $l;
    }

    public function getID()
    {
        return Config::APP_ID;
    }

    public function getName()
    {
        return $this->l->t('Asyntai AI Chatbot');
    }

    public function getPriority()
    {
        return 80;
    }

    /** ownCloud looks for img/<name>.svg inside the app. */
    public function getIconName()
    {
        return 'asyntai';
    }
}
