#!/usr/bin/env python3

import json
import os
import re
import requests
import pandas as pd
import platform
from pathlib import Path
from appscript import app, k
from mactypes import Alias

def get_workshop_title(manifest_path):
    with open(manifest_path, "r", encoding='utf-8') as file:
        manifest_data = json.load(file)
    return manifest_data.get("workshoptitle")

def get_wms_id_and_emails(workshop_title):
    df = pd.read_excel("All Workshops Report.xlsx")
    wms_id_row = df[df["Title"] == workshop_title]

    if not wms_id_row.empty:
        wms_id = wms_id_row["Workshop Id"].values[0]
        owner_email = wms_id_row["Workshop Owner Email"].values[0]
        support_contact_email = wms_id_row["Support Contact Email"].values[0]
        return wms_id, owner_email, support_contact_email
    else:
        return None, None, None


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
    if system in ['Windows', 'Darwin', 'Linux']:
        return os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        raise EnvironmentError("Unsupported operating system")

def extract_first_name_from_email(email):
    email_username = email.split('@')[0]

    first_name = email_username.split('.')[0]

    first_name = first_name.replace('-', ' ').title().replace(' ', '-')

    return first_name


def create_message_with_attachment(manifest_title, to_recip, attachment_path=None):
    client = app('Microsoft Outlook')

    subject = f"{manifest_title}: Invalid URLs"

    if len(to_recip) > 1:
        greetings = [f"{extract_first_name_from_email(email)}" for email in to_recip]
        greeting = "Hi " + " and ".join(greetings)
    else:
        first_name = extract_first_name_from_email(to_recip[0])
        greeting = f"Hi {first_name}"

    greeting += ",\n\n"
    attachment_info = "Find attached the Excel with invalid URLs to fix them in your workshop.\n\n"
    closing = "Thank you"

    body = greeting + attachment_info + closing

    msg = client.make(
        new=k.outgoing_message,
        with_properties={k.subject: subject, k.content: body})

    unique_recipients = set(to_recip)
    for email in unique_recipients:
        msg.make(new=k.to_recipient, with_properties={k.email_address: {k.address: email}})

    if attachment_path:
        p = Path(attachment_path)
        if not p.exists():
            raise FileNotFoundError(f"The file at {p} does not exist.")
        p = Alias(str(p))
        msg.make(new=k.attachment, with_properties={k.file: p})

    msg.send()

    if len(to_recip) == 1:
        print(f"Email sent successfully to {extract_first_name_from_email(to_recip[0])}!")
    else:
        names = [extract_first_name_from_email(email) for email in unique_recipients]
        print(f"Email sent successfully to {', '.join(names)}!")


def check_urls_in_directory(directory, manifest_path):
    markdown_files = find_markdown_files(directory)
    all_invalid_urls = []

    workshop_title = get_workshop_title(manifest_path)

    wms_id, owner_email, support_contact_email = get_wms_id_and_emails(workshop_title)

    if not wms_id:
        print(f"Could not find WMS ID for workshop title: {workshop_title}")
        return

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

        recipients = [email for email in (owner_email, support_contact_email) if pd.notna(email)]
        if recipients:
            create_message_with_attachment(
                manifest_title=workshop_title,
                to_recip=recipients,
                attachment_path=full_path
            )
        else:
            print("No recipients found for the email.")
    else:
        print("No invalid URLs found.")


def main():
    directory = input("Please enter the directory path containing markdown files: ")
    manifest_path = input("Please enter the path to the manifest.json file: ")

    check_urls_in_directory(directory, manifest_path)

if __name__ == "__main__":
    main()
