/**
 * The admin settings screen: reads the four fields and saves them.
 *
 * ownCloud puts app scripts in the page head, before the panel exists, so the
 * work waits for the document to be ready.
 */
(function () {
	'use strict'

	var setUp = function () {
		var button = document.getElementById('asyntai-save')
		if (!button) {
			return
		}

		var widgetIdField = document.getElementById('asyntai-widget-id')
		var scriptUrlField = document.getElementById('asyntai-script-url')
		var loggedInField = document.getElementById('asyntai-show-logged-in')
		var publicField = document.getElementById('asyntai-show-public')
		var message = document.getElementById('asyntai-message')

		var show = function (text, isError) {
			message.textContent = text
			message.className = 'asyntai-message' + (isError ? ' asyntai-message--error' : ' asyntai-message--ok')
		}

		button.addEventListener('click', function () {
			button.disabled = true
			show(t('asyntai', 'Saving…'), false)

			var url = OC.generateUrl('/apps/asyntai/settings')

			fetch(url, {
				method: 'POST',
				credentials: 'same-origin',
				headers: {
					'Content-Type': 'application/json',
					requesttoken: OC.requestToken,
				},
				body: JSON.stringify({
					widgetId: widgetIdField.value,
					scriptUrl: scriptUrlField.value,
					showLoggedIn: loggedInField.checked,
					showPublic: publicField.checked,
				}),
			})
				.then(function (response) {
					if (!response.ok) {
						throw new Error('HTTP ' + response.status)
					}
					return response.json()
				})
				.then(function (data) {
					// The server cleans the values, so show back what was stored.
					widgetIdField.value = data.widgetId
					scriptUrlField.value = data.scriptUrl

					if (data.widgetIdRejected) {
						show(t('asyntai', 'That is not a valid Asyntai widget ID. The chat is switched off.'), true)
						return
					}

					show(t('asyntai', 'Settings saved.'), false)
				})
				.catch(function () {
					show(t('asyntai', 'Could not save the settings.'), true)
				})
				.then(function () {
					button.disabled = false
				})
		})
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', setUp)
	} else {
		setUp()
	}
})()
