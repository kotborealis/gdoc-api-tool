import argparse
import gdrive_utils
import json


def main():
    """gdoc-api-tool entrypoint"""

    # Arguments parser
    parser = argparse.ArgumentParser(description='Google Drive Tools.')

    parser.add_argument('--auth-url',
                        action='store_true',
                        help='Call Google OAuth and show authentication URL')

    parser.add_argument('--auth-code',
                        help='Send authentication code to Google OAuth to obtain new token')

    parser.add_argument('--create',
                        dest='file_name',
                        help='Create and share Google Drive file with specified name')

    parser.add_argument('--type',
                        dest='file_type',
                        default='document',
                        choices=gdrive_utils.mime_types.keys(),
                        help='Document type')

    args = parser.parse_args()

    # Load, refresh & save credentials
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

    # Check if credentials are valid
    if not creds:
        print("Not authorized, use --auth-url and --auth-code")
        return

    if args.file_name:
        # Create new file with specified name
        file = gdrive_utils.create_file(
            gdrive_utils.load_credentials(),
            args.file_name,
            args.file_type
        )

        # Share created file
        gdrive_utils.share_file(gdrive_utils.load_credentials(), file.get("id"))

        print(json.dumps(file))


if __name__ == '__main__':
    main()
