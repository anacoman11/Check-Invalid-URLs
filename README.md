# Check-Invalid-URLs

This Python script checks markdown files for invalid URLs. The invalid URLs are saved in an Excel file.

## Requirements

Before running the script, make sure you have the following installed:

- Python 3.12
- Required libraries: You can install them using the following command:

```bash
pip install pandas requests openpyxl
```

## How to run the script 

## Step 1: Clone the Repository

You can clone the repository using either Git or GitHub Desktop:

## Using Git
Clone the repository to your local machine using Git:

```bash
git clone <repository-url>
```

## Using GitHub Desktop
1. Open GitHub Desktop.
2. Go to File > Clone repository.
3. In the Clone a repository dialog, enter the URL of your repository or select it from the list if you have previously connected your GitHub account.
4. Choose the local path where you want to clone the repository.
5. Click Clone.

## Step 2: Navigate to the Project Directory
Navigate to the project directory:

```bash
cd Check-Invalid-URLs
```

## Step 3: Run the Script
Run the script using Python. The script will prompt you to provide:

Directory Path: The directory containing markdown (.md) files.

Manifest Path: The path to the manifest.json file.

```bash
python3 checkInvalidURLs.py
```

