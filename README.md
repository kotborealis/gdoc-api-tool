# gdoc-api-tool

```shell script
usage: main.py [-h] [--auth-url] [--auth-code AUTH_CODE] [--create FILE_NAME]
               [--type {spreadsheet,document}]

Google Drive Tools.

optional arguments:
  -h, --help            show this help message and exit
  --auth-url            Call Google OAuth and show authentication URL
  --auth-code AUTH_CODE
                        Send authentication code to Google OAuth to obtain new
                        token
  --create FILE_NAME    Create and share Google Drive file with specified name
  --type {spreadsheet,document}
                        Document type
```

## Setup

* Recommended python version >=3.5
* [Create a new Cloud Platform project and enable the Drive API](https://developers.google.com/drive/api/v3/quickstart/python)
* Download client configuration from Google Cloud Platform
* Place credentials.json into working directory
* Install dependencies from `requirements.txt`; try one of these:
    * `pip3 install -r requirements.txt`
    * `python3 -m pip3 install -r requirements.txt`
    * `python3 -m pip install -r requirements.txt`
    * `pip install -r requirements.txt`
    * `python -m pip install -r requirements.txt`
* Running: `python3 main.py <args>`

## Auth

Use `--auth-url` to get OAuth2 url, open it, allow access to GDrive, 
copy auth code and pass it into a program via `--auth-code <code>`.
```shell script
# Get auth URL via --auth-url argument
$ python3 main.py --auth-url
https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=...
# Open auth URL in browser and allow access to your google drive
# Google will show you auth code, use it with --auth-code argument
$ python3 main.py --auth-code 4/1wH1kz...
```

## Creating document

Use `--create <name>` to create new publicly shared Google Drive file and get JSON with it's name, id and url.
By default, creates Google Document. You can specify other types (`spreadsheet`, `document`) via `--type` argument. 
Examples:
```shell script
# Creates Google Document named `g_document`
$ python3 main.py --create g_document 
...

# Creates Google Document named `g_document`
$ python3 main.py --create g_document --type document
...
 
# Creates Google Document named `g_spreadsheet`
$ python3 main.py --create g_spreadsheet --type spreadsheet
... 
```