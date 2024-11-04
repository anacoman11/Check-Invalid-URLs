# Check-Invalid-URLs

This Python script checks markdown files for invalid URLs. The invalid URLs are saved in an Excel file.

## Requirements

> [!NOTE]
> Make sure that you have the VPN off before running the script.

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

## Step 2: Run the setup script 
### For Linux/macOS (Bash)

1. Navigate to the project directory:
```bash
cd Check-Invalid-URLs
```

2. Give execution permissions to the setup script (only needed the first time):
```bash
chmod +x setup_checkInvalidURL.sh
```

3. Run the Bash setup script:
```bash
./setup_checkInvalidURL.sh
```

4. Restart your terminal
   
After these steps, you can run the script from any directory by simply typing:
```bash
checkInvalidURL
```

### For Windows (PowerShell)

1. Navigate to the project directory:
```bash
cd Check-Invalid-URLs
```

2. Set the execution policy:
- Run the following command to allow script execution as Administrator 
```bash
Set-ExecutionPolicy RemoteSigned
```
- When prompted, you can press Yes to accept the change for all operations.

3. Run the PowerShell setup script
```bash
./setup_checkInvalidURL.ps1
```

4. Close and reopen PowerShell to apply the changes.
   
After these steps, you can run the script from any directory by simply typing:
```bash
checkInvalidURL
```
