#!/usr/bin/env python3

import os
import re
import requests
import pandas as pd
import platform


def extract_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    url_pattern = r'\[.*?\]\((https?://[^\s<>\)\]]+)\)'
    urls = re.findall(url_pattern, content)

    html_url_pattern = r'href="(https?://[^\s<>\)\"]+)"'
    urls += re.findall(html_url_pattern, content)

    cleaned_urls = [url.strip(').,<>;') for url in urls]
    return cleaned_urls


def check_url_status(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return 0


def find_files_with_urls(directory):
    files_with_urls = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') or file.endswith('.html'):
                files_with_urls.append(os.path.join(root, file))
    return files_with_urls


def get_download_folder_path():
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    elif system == 'Darwin':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    elif system == 'Linux':
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        raise EnvironmentError("Unsupported operating system")


def check_urls_in_directory(directory):
    files_with_urls = find_files_with_urls(directory)
    all_invalid_urls = []

    for file_path in files_with_urls:
        print(f"\nChecking file: {file_path}")
        urls = extract_urls_from_file(file_path)

        if not urls:
            print(f"No URLs found in {file_path}.")
            continue

        for url in urls:
            status_code = check_url_status(url)

            if "bit.ly" in url or status_code != 200:
                print(f"{url} is invalid or returned an error (status code: {status_code})")
                all_invalid_urls.append({
                    'File': file_path,
                    'Invalid URL': url
                })

    if all_invalid_urls:
        directory_name = os.path.basename(os.path.normpath(directory))
        output_file = os.path.join(directory, f"{directory_name}_Invalid_URLs.xlsx")
        df = pd.DataFrame(all_invalid_urls)
        df.to_excel(output_file, index=False)
        full_path = os.path.abspath(output_file)
        print(f"\nInvalid URLs saved successfully to {full_path}")
    else:
        print("No invalid URLs found.")


def main():
    directory = os.getcwd()
    check_urls_in_directory(directory)


if __name__ == "__main__":
    main()
