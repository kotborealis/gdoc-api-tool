# gdoc-api-tool

```shell script
C:\kotborealis\gdoc-api-tool>python main.py --help
usage: main.py [-h] [--auth-url] [--auth-code AUTH_CODE] [--create CREATE]

Google Drive Tools.

optional arguments:
  -h, --help            show this help message and exit
  --auth-url            Get authentication URL
  --auth-code AUTH_CODE
                        Specify authentication code
  --create CREATE       Create and share google document with specified name
```

## Setup

* Recommended python version >=3.5
* [Create a new Cloud Platform project and enable the Drive API](https://developers.google.com/drive/api/v3/quickstart/python)
* Download client configuration from Google Cloud Platform
* Place credentials.json into project directory
* Install dependencies from `requirements.txt`
* Running: `python3 main.py <args>`
    


## Auth

Use `--auth-url` to get OAuth2 url, open it, allow access to GDrive, 
copy auth code and pass it into a program via `--auth-code <code>`.

## Creating document

Use `--create <name>` to create new publicly shared Google Document and get JSON w/ it's name, id and url.