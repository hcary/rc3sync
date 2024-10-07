#!/usr/bin/env python3

import requests
import argparse
import os
import urllib3
import sys
from tqdm import tqdm  # Used to show the progress bar
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

# Disable the SSL warnings from requests (for lab environment)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Chunk size in bytes for the file upload
CHUNK_SIZE = 1024 * 1024  # 1MB per chunk

def upload_file(file_path, server_url):
    file_size = os.path.getsize(file_path)  # Get the total size of the file

    with open(file_path, 'rb') as file:
        # Create a MultipartEncoder
        encoder = MultipartEncoder(fields={'file': (os.path.basename(file_path), file, 'application/octet-stream')})

        # Create a progress bar using tqdm
        with tqdm(total=file_size, unit='B', unit_scale=True, desc='Uploading', ncols=100) as progress_bar:

            # Callback function to update progress bar
            def progress_callback(monitor):
                progress_bar.update(monitor.bytes_read - progress_bar.n)

            # Wrap the encoder with MultipartEncoderMonitor to add progress tracking
            monitor = MultipartEncoderMonitor(encoder, progress_callback)

            try:
                # Upload the file
                response = requests.post(
                    server_url,
                    data=monitor,
                    headers={'Content-Type': monitor.content_type},
                    verify=False  # Ignore certificate warnings (for lab)
                )

                # Check the response status code
                if response.status_code == 200:
                    print(f"\nFile uploaded successfully: {response.text}")
                    sys.exit(0)
                else:
                    print(f"\nFailed to upload file. Status code: {response.status_code}")
                    print(f"Response content: {response.text}")  # Output the server's response for debugging
                    sys.exit(100)

            except Exception as e:
                print(f"An error occurred: {e}")
                sys.exit(200)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Upload a file to the server with progress tracking.')
    parser.add_argument('file_path', type=str, help='Path to the file to upload')
    parser.add_argument('--server_url', type=str, default='https://10.10.1.40:443/upload',
                        help='URL of the server where the file will be uploaded (default: https://10.10.1.40:443/upload)')
    
    # Parse arguments
    args = parser.parse_args()

    # Call the function to upload the file
    upload_file(args.file_path, args.server_url)

if __name__ == '__main__':
    main()
