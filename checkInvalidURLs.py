#!/usr/bin/env python3

import json
import os
import re
import requests
import pandas as pd
import platform

def get_workshop_title(manifest_path):
    with open(manifest_path, "r", encoding='utf-8') as file:
        manifest_data = json.load(file)
    return manifest_data.get("workshoptitle")

def get_wms_id(workshop_title):
    df = pd.read_excel("All Workshops Report.xlsx")
    wms_id_row = df[df["Title"] == workshop_title]
    if not wms_id_row.empty:
        return wms_id_row["Workshop Id"].values[0]
    else:
        return None

def extract_urls_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    url_pattern = r'\[.*?\]\((https?://[^\s<>\)\]]+)\)'
    urls = re.findall(url_pattern, content)

    cleaned_urls = [url.strip(').,<>;') for url in urls]
    return cleaned_urls

def check_url_status(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
        return response.status_code
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return 0

def find_markdown_files(directory):
    markdown_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

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

def check_urls_in_directory(directory, manifest_path):
    markdown_files = find_markdown_files(directory)
    all_invalid_urls = []

    workshop_title = get_workshop_title(manifest_path)

    wms_id = get_wms_id(workshop_title)

    for file_path in markdown_files:
        print(f"\nChecking file: {file_path}")
        urls = extract_urls_from_file(file_path)
        invalid_urls = []

        for url in urls:
            status_code = check_url_status(url)

            if status_code != 200:
                print(f"{url} is invalid or returned an error (status code: {status_code})")
                invalid_urls.append({
                    'WMS ID': wms_id,
                    'Markdown File': file_path,
                    'Invalid URL': url
                })

        all_invalid_urls.extend(invalid_urls)

    if all_invalid_urls:
        download_folder = get_download_folder_path()
        output_file = os.path.join(download_folder, "Invalid_URLs.xlsx")
        df = pd.DataFrame(all_invalid_urls)
        df.to_excel(output_file, index=False)
        full_path = os.path.abspath(output_file)
        print(f"\nInvalid URLs saved successfully to {full_path}")
    else:
        print("No invalid URLs found.")

def main():
    directory = input("Please enter the directory path containing markdown files: ")
    manifest_path = input("Please enter the path to the manifest.json file: ")

    check_urls_in_directory(directory, manifest_path)

if __name__ == "__main__":
    main()
