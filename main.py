import argparse
import gdrive_utils
import json


def main():
    parser = argparse.ArgumentParser(description='Google Drive Tools.')

    parser.add_argument('--auth-url',
                        action='store_true',
                        help='Get authentication URL')

    parser.add_argument('--auth-code',
                        help='Specify authentication code')

    parser.add_argument('--create',
                        help='Create and share google document with specified name')

    args = parser.parse_args()

    creds = gdrive_utils.load_credentials()
    gdrive_utils.refresh_credentials(creds)
    gdrive_utils.save_credentials(creds)

    if args.auth_url:
        print(gdrive_utils.auth_url())
        return
    elif args.auth_code:
        creds = gdrive_utils.auth_code(args.auth_code)
        gdrive_utils.save_credentials(creds)
        return

    if not creds:
        print("Not authorized, use --auth-url and --auth-code")
        return
        
    if args.create:
        file = gdrive_utils.create_document(gdrive_utils.load_credentials(), args.create)
        gdrive_utils.share_file(gdrive_utils.load_credentials(), file.get("id"))
        print(json.dumps(file))


if __name__ == '__main__':
    main()
