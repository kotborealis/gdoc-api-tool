# Setup

* [create a new Cloud Platform project and enable the Drive API](https://developers.google.com/drive/api/v3/quickstart/python)
* download client configuration
* place credentials.json into working directory

## Auth

Use `--auth-url` to get OAuth2 url, open it, allow access to GDrive, 
copy auth code and pass it into a program via `--auth-code <code>`.

## Creating document

Use `--create <name>` to create new publicly shared Google Document and get JSON w/ it's name, id and url.