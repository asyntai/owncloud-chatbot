<?php

declare(strict_types=1);

/** @var array $_ */
/** @var \OCP\IL10N $l */

script('asyntai', 'asyntai-admin');
style('asyntai', 'asyntai-admin');
?>

<div id="asyntai-admin" class="section">
    <h2><?php p($l->t('Asyntai AI Chatbot')); ?></h2>
    <p class="settings-hint">
        <?php p($l->t('Adds a chat assistant to every page. Users ask a question and get an answer from your own content.')); ?>
    </p>

    <div class="asyntai-field">
        <label for="asyntai-widget-id"><?php p($l->t('Asyntai widget ID')); ?></label>
        <input type="text" id="asyntai-widget-id" maxlength="512"
               placeholder="asyntai_xxxxxxxxxxxx"
               value="<?php p($_['widget_id']); ?>">
        <p class="asyntai-hint">
            <?php p($l->t('Paste the snippet from your Asyntai dashboard, or only the widget ID. Leave the field empty to switch the chat off.')); ?>
        </p>
    </div>

    <div class="asyntai-field">
        <input type="checkbox" id="asyntai-show-logged-in" class="checkbox"
            <?php if ($_['show_logged_in']) {
                print_unescaped('checked');
            } ?>>
        <label for="asyntai-show-logged-in"><?php p($l->t('Show to users who are logged in')); ?></label>
    </div>

    <div class="asyntai-field">
        <input type="checkbox" id="asyntai-show-public" class="checkbox"
            <?php if ($_['show_public']) {
                print_unescaped('checked');
            } ?>>
        <label for="asyntai-show-public"><?php p($l->t('Show on the login screen and on public share pages')); ?></label>
    </div>

    <div class="asyntai-field">
        <label for="asyntai-script-url"><?php p($l->t('Script address (optional)')); ?></label>
        <input type="text" id="asyntai-script-url" maxlength="255"
               placeholder="<?php p($_['default_script_url']); ?>"
               value="<?php p($_['script_url']); ?>">
        <p class="asyntai-hint">
            <?php p($l->t('Leave this field empty to use the standard address.')); ?>
        </p>
    </div>

    <button id="asyntai-save" class="button primary"><?php p($l->t('Save')); ?></button>
    <span id="asyntai-message" class="asyntai-message" role="status"></span>

    <p class="asyntai-hint asyntai-help">
        <?php p($l->t('Need help?')); ?>
        <a href="https://asyntai.com/documentation/integrations/owncloud/" target="_blank" rel="noreferrer noopener"><?php p($l->t('Setup guide')); ?></a>
        &middot;
        <a href="mailto:hello@asyntai.com">hello@asyntai.com</a>
    </p>
</div>
