/**
 * Loads the Asyntai chat widget.
 *
 * The widget is fetched only after the page has finished loading, so ownCloud
 * is drawn first and page speed does not change. The script runs once per tab.
 * The widget ID and the script address come from two <meta> tags that the app
 * writes into the page head. ownCloud prints those tags after its script tags,
 * so they are read only once the page has loaded.
 */
(function () {
	'use strict'

	if (window.__asyntaiRequested) {
		return
	}
	window.__asyntaiRequested = true

	var read = function (name) {
		var tag = document.querySelector('meta[name="' + name + '"]')
		return tag ? tag.getAttribute('content') || '' : ''
	}

	var load = function () {
		var widgetId = read('asyntai-widget-id')
		if (!/^asyntai_[A-Za-z0-9]{6,64}$/.test(widgetId)) {
			return
		}

		var scriptUrl = read('asyntai-script-url')
		if (!/^https?:\/\//i.test(scriptUrl)) {
			return
		}

		var script = document.createElement('script')
		script.src = scriptUrl
		script.async = true
		script.setAttribute('data-asyntai-id', widgetId)
		document.head.appendChild(script)
	}

	if (document.readyState === 'complete') {
		load()
	} else {
		window.addEventListener('load', load)
	}
})()
