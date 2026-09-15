# Asyntai AI Chatbot for ownCloud

Adds the [Asyntai](https://asyntai.com) AI assistant to every page of ownCloud
Server 10: the Files view, the settings, the login screen and public share
links. Users click the chat button and ask a question in their own words. The
assistant answers from your own content, in more than 80 languages.

Typical use: an internal help desk that never sleeps. "How do I share a folder
with someone outside the company?" "Where is the travel policy?" The assistant
answers, so your team does not have to.

## Install

1. Install **Asyntai AI Chatbot** from the ownCloud Marketplace, or unpack the
   `asyntai` folder into the `apps` folder of your server and enable it under
   **Settings → Apps**.
2. In your Asyntai dashboard, open **Install** and copy the snippet.
3. In ownCloud, open **Settings → Admin → Asyntai AI Chatbot**, paste the
   snippet or the widget ID, and press **Save**.

Full guide: https://asyntai.com/documentation/integrations/owncloud/

## Settings

- **Asyntai widget ID**: leave it empty to switch the chat off.
- **Show to users who are logged in**.
- **Show on the login screen and on public share pages**.
- **Script address**: only for a self hosted copy of the widget.

## Requirements

ownCloud Server 10.11 or newer on PHP 7.4, and an Asyntai account (the free
plan works).

## Development

The app is plain PHP and JavaScript, no build step. `tests/` holds the checks
that ran against a real ownCloud 10.16 (`tests/README.md`).

## Licence

AGPL-3.0. Support: hello@asyntai.com
