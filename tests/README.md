# Tests

These checks ran against a real ownCloud Server 10.16.0 on 2026-09-14. They all
pass.

## Prepare

ownCloud refuses to run on Windows, so the test server lives in WSL Ubuntu
20.04, which ships PHP 7.4. `wsl_setup.sh` copies the server from
`C:\laragon\www\owncloud10`, installs it with SQLite, and serves it with Apache
on http://localhost:8023. Choose an admin password for the rig and pass it in
`OC_ADMIN_PASS`.

```
wsl -d Ubuntu-20.04 -u root -e bash -c 'OC_ADMIN_PASS=<your rig password> bash /mnt/c/Users/tomku/PycharmProjects/asyntai/plugins/owncloud/tests/wsl_setup.sh'
```

Copy the app in and enable it (repeat the copy after every edit):

```
wsl -d Ubuntu-20.04 -u root -e bash -c 'rm -rf /var/www/owncloud/apps/asyntai; cp -r /mnt/c/Users/tomku/PycharmProjects/asyntai/plugins/owncloud/asyntai /var/www/owncloud/apps/; chown -R www-data:www-data /var/www/owncloud/apps/asyntai; sudo -u www-data php /var/www/owncloud/occ app:enable asyntai'
```

## Run

```
OC_ADMIN_PASS=<your rig password> python test_pages.py
```

38 checks: the login screen, the Files view and a public share link load the
widget and open the security policy; every switch turns it off again; the
settings panel draws with its section and icon; the save route cleans a pasted
snippet, refuses rubbish, and refuses a wrong request token or no session.

## Checked by hand in Chrome

- The chat button and greeting draw on the login screen, zero console errors.
- The settings panel draws in the Admin section, the Save button stores the
  switches, and "Settings saved." appears.
- A question in the chat gets an answer.

## Two ownCloud traps

- ownCloud prints custom `<meta>` headers **after** its script tags, and puts
  app scripts in the page head. So the loader reads the meta tags at `load`,
  and the admin script waits for `DOMContentLoaded`.
- The `?v=` hash on script URLs comes from the app versions, so an edited
  script stays cached in the browser until the cache is refreshed.
