"""Checks the Asyntai app on a real ownCloud 10, over HTTP.

The server runs in WSL (see wsl_setup.sh) on http://localhost:8023. The admin
account is the test rig's own account, made by wsl_setup.sh; it is not a real
credential. Settings are changed both with occ and through the app's own save
route, so the whole path an administrator uses is covered.
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.cookiejar import CookieJar

BASE = os.environ.get("OC_URL", "http://localhost:8023")
ADMIN_USER = os.environ.get("OC_ADMIN", "admin")
ADMIN_PASS = os.environ["OC_ADMIN_PASS"]
WIDGET_ID = "asyntai_000000000000"
DEFAULT_SCRIPT = "https://widget.asyntai.com/static/js/chat-widget.js"

failures = []


def check(name, ok):
    print(("  OK   " if ok else "  FAIL ") + name)
    if not ok:
        failures.append(name)


def occ(*args):
    """Runs an occ command inside WSL, the way an administrator would."""
    return subprocess.run(
        ["wsl", "-d", "Ubuntu-20.04", "-u", "root", "-e", "sudo", "-u", "www-data",
         "php", "/var/www/owncloud/occ", *args],
        capture_output=True, text=True,
    ).stdout.strip()


def set_value(key, value):
    if value == "":
        occ("config:app:delete", "asyntai", key)
    else:
        occ("config:app:set", "asyntai", key, "--value=" + value)


jar = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))


def get(path, headers=None):
    request = urllib.request.Request(BASE + path, headers=headers or {})
    with opener.open(request) as response:
        return response.read().decode("utf-8", "replace"), dict(response.headers)


def post_json(path, token, payload):
    request = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "requesttoken": token},
        method="POST",
    )
    try:
        with opener.open(request) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        return error.code, None


def meta(html, name):
    match = re.search(r'<meta name="' + name + r'" content="([^"]*)"', html)
    return match.group(1) if match else None


def loads_widget(html):
    return "asyntai-loader.js" in html and meta(html, "asyntai-widget-id") is not None


def csp_allows(headers):
    policy = headers.get("Content-Security-Policy", "")
    return all(
        "https://asyntai.com" in part and "https://widget.asyntai.com" in part
        for part in policy.split(";")
        if part.strip().startswith(("script-src", "connect-src", "img-src", "font-src", "media-src", "style-src"))
    ) and "script-src" in policy


def request_token(html):
    match = re.search(r'data-requesttoken="([^"]+)"', html)
    return match.group(1) if match else None


print("A visitor who is not logged in")
set_value("widget_id", WIDGET_ID)
set_value("show_logged_in", "yes")
set_value("show_public", "yes")
set_value("script_url", "")

login_page, login_headers = get("/index.php/login")
check("the login screen loads the widget", loads_widget(login_page))
check("the widget ID is handed over", meta(login_page, "asyntai-widget-id") == WIDGET_ID)
check("the standard script address is used", meta(login_page, "asyntai-script-url") == DEFAULT_SCRIPT)
check("the security policy lets the chat reach Asyntai", csp_allows(login_headers))

set_value("show_public", "no")
login_page, login_headers = get("/index.php/login")
check("no widget on the login screen when public pages are switched off", not loads_widget(login_page))
check("the security policy stays closed then", "asyntai.com" not in login_headers.get("Content-Security-Policy", ""))

set_value("show_public", "yes")
set_value("script_url", "https://cdn.example.com/w.js")
login_page, login_headers = get("/index.php/login")
check("another script address is handed over", meta(login_page, "asyntai-script-url") == "https://cdn.example.com/w.js")
check("that address is let through the security policy",
      "https://cdn.example.com" in login_headers.get("Content-Security-Policy", ""))
set_value("script_url", "")

set_value("widget_id", "")
login_page, _ = get("/index.php/login")
check("no widget at all without a widget ID", not loads_widget(login_page))
set_value("widget_id", WIDGET_ID)

print("Logging in as the administrator")
login_page, _ = get("/index.php/login")
token = request_token(login_page)
check("the login page carries a request token", token is not None)
form = urllib.parse.urlencode({
    "user": ADMIN_USER, "password": ADMIN_PASS, "requesttoken": token, "timezone-offset": "0",
}).encode()
request = urllib.request.Request(BASE + "/index.php/login", data=form, method="POST")
with opener.open(request) as response:
    after_login = response.read().decode("utf-8", "replace")
files_page, files_headers = get("/index.php/apps/files/")
check("the Files page shows a logged in user", 'data-user="' + ADMIN_USER + '"' in files_page)

print("A user who is logged in")
check("the Files page loads the widget", loads_widget(files_page))
check("the security policy lets the chat reach Asyntai", csp_allows(files_headers))

set_value("show_logged_in", "no")
files_page, _ = get("/index.php/apps/files/")
check("no widget for logged in users when that is switched off", not loads_widget(files_page))
login_page, _ = get("/index.php/login")
set_value("show_logged_in", "yes")

print("The settings screen")
settings_page, _ = get("/index.php/settings/admin?sectionid=asyntai")
check("the section is in the settings navigation", "sectionid=asyntai" in settings_page)
check("the panel draws", 'id="asyntai-admin"' in settings_page)
check("the panel shows the widget ID", 'value="' + WIDGET_ID + '"' in settings_page)
check("the panel loads its script", "asyntai-admin.js" in settings_page)
check("the panel loads its style", "asyntai-admin.css" in settings_page)
check("the icon is found", "/apps/asyntai/img/asyntai.svg" in settings_page)

print("Saving through the app's own route")
token = request_token(settings_page)
status, data = post_json("/index.php/apps/asyntai/settings", token, {
    "widgetId": '<script src="https://widget.asyntai.com/static/js/chat-widget.js" data-asyntai-id="asyntai_111111111111" async></script>',
    "scriptUrl": "",
    "showLoggedIn": True,
    "showPublic": False,
})
check("the save route answers 200", status == 200)
check("a pasted snippet becomes a bare widget ID", data and data.get("widgetId") == "asyntai_111111111111")
check("the stored value matches", occ("config:app:get", "asyntai", "widget_id") == "asyntai_111111111111")
check("the public switch is stored", occ("config:app:get", "asyntai", "show_public") == "no")
# A logged in administrator is sent away from the login screen, so a fresh
# visitor without cookies looks at it instead.
with urllib.request.urlopen(BASE + "/index.php/login") as response:
    fresh_login = response.read().decode("utf-8", "replace")
check("the login screen follows the saved settings at once", not loads_widget(fresh_login))

status, data = post_json("/index.php/apps/asyntai/settings", token, {
    "widgetId": "not an id", "scriptUrl": "javascript:alert(1)", "showLoggedIn": True, "showPublic": True,
})
check("rubbish is refused and reported", data and data.get("widgetIdRejected") is True and data.get("widgetId") == "")
check("a dangerous script address is not stored", data and data.get("scriptUrl") == DEFAULT_SCRIPT)

status, _ = post_json("/index.php/apps/asyntai/settings", "wrong-token", {"widgetId": WIDGET_ID})
check("a wrong request token is refused", status in (401, 403, 412))

status, data = post_json("/index.php/apps/asyntai/settings", token, {
    "widgetId": WIDGET_ID, "scriptUrl": "", "showLoggedIn": True, "showPublic": True,
})
check("the settings are put back", status == 200 and data.get("widgetId") == WIDGET_ID)

print("A public share link")
share_request = urllib.request.Request(
    BASE + "/ocs/v1.php/apps/files_sharing/api/v1/shares?format=json",
    data=urllib.parse.urlencode({"shareType": "3", "path": "/Documents"}).encode(),
    headers={"OCS-APIRequest": "true", "requesttoken": token},
    method="POST",
)
with opener.open(share_request) as response:
    share = json.loads(response.read().decode())
share_token = share["ocs"]["data"]["token"]
check("a share link was made", bool(share_token))

visitor = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
with visitor.open(BASE + "/index.php/s/" + share_token) as response:
    share_page = response.read().decode("utf-8", "replace")
    share_headers = dict(response.headers)
check("the share page loads the widget for a visitor", loads_widget(share_page))
check("the security policy lets the chat reach Asyntai there", csp_allows(share_headers))

set_value("show_public", "no")
with visitor.open(BASE + "/index.php/s/" + share_token) as response:
    share_page = response.read().decode("utf-8", "replace")
check("no widget on the share page when public pages are switched off", not loads_widget(share_page))
set_value("show_public", "yes")

print("Someone who is not an administrator")
outsider = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
request = urllib.request.Request(
    BASE + "/index.php/apps/asyntai/settings",
    data=json.dumps({"widgetId": "asyntai_222222222222"}).encode(),
    headers={"Content-Type": "application/json", "requesttoken": token},
    method="POST",
)
try:
    with outsider.open(request) as response:
        status = response.status
except urllib.error.HTTPError as error:
    status = error.code
check("cannot save the settings without a session", status in (401, 403, 412))
check("nothing was stored", occ("config:app:get", "asyntai", "widget_id") == WIDGET_ID)

log = subprocess.run(
    ["wsl", "-d", "Ubuntu-20.04", "-u", "root", "-e", "bash", "-c",
     "grep -c -i 'asyntai' /var/www/owncloud/data/owncloud.log 2>/dev/null; true"],
    capture_output=True, text=True,
).stdout.strip()
check("the ownCloud log holds no line about the app", log in ("", "0"))

print()
if failures:
    print("%d checks failed" % len(failures))
    sys.exit(1)
print("all checks passed")
