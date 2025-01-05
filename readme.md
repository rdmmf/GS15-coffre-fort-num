# GS15 Coffre-Fort Numérique

## Description
GS15 Coffre-Fort Numérique is a secure digital vault application designed to store and manage sensitive information such as passwords, documents, and personal data.

## Features
- Secure storage of sensitive information
- User authentication and authorization
- Data encryption
- Easy-to-use interface
- Backup and restore functionality

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/rdmmf/GS15-coffre-fort-num.git
    ```
2. Navigate to the project directory:
    ```bash
    cd GS15-coffre-fort-num
    ```
3. Install requirements
    ```bash
        pip install -r requirements.txt
    ```
4. Launch main.py script
    ```bash
    python3 main.py -h
    ```
## Example
1. Create an account:
    ```bash
    python3 main.py -c user:pass
    ```
2. Connect to an account and list files on the vault:
    ```bash
    python3 main.py -u user:pass -l
    ```
3. Connect to an account and save a local file:
    ```bash
    python3 main.py -u user:pass -s somefile
    ```
4. Connect to an account and get a file from the vault:
    ```bash
    python3 main.py -u user:pass -g somefile -o outputfile
    ```
5. Connect to an account and get all files:
    ```bash
    python3 main.py -u user:pass -ga outputdirectory
    ```
