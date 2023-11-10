# SyncSQL - Sync your Local Database with Production Database

SyncSQL is a cli tool designed to sync your local database with production database. It can also be used sync production database with backup database. Needed a github repository that contains updated sql scripts with version number as file name and env file for keeping your database credentials.

## Features

- Sync Database with one command
- Easy to manage
- Can be used for Different Services

## Steps

- ```bash 
    pip install -r requirements.txt
    ```
- create a .env file from .env.sample
- A repo with sql script must have a folder alter/ which contains alter scripts with version numbers
- ```bash
    python main.py currentversion
    ``` 
    to view current version of local database
- ```bash
    python main.py remoteversion
    ``` 
    to view remote version of production database
- ```bash
    python main.py syncdb
    ```
     to sync local db with production
    
## Limitations

- Only support MySQL as of now
- Slow for higher changes need Optimization
- Simple version numbering is allowed complex may broke the system
