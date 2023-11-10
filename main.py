import sys
import subprocess
import os
from decouple import config

database = config('DATABASE')
DIR = config('REPO_DIR')

if database == 'mysql':
    from db_connector.mysql import connect, execute, execute_from_file, getdata, close

connection = connect()


def currentversion():
    result = getdata(connection, "SHOW TABLES LIKE 'system_setting';")
    if len(result) == 0:
        return None
    try:
        return getdata(
            connection, 
            "SELECT value FROM system_setting WHERE `key` = 'db.version';"
        )[0][0]
    except IndexError:
        return None

def remoteversion():
    if os.path.exists(DIR):
        subprocess.call(["git", "pull", config('REPO_REMOTE'),
                        config('REPO_BRANCH'), "--quiet"])
    else:
        subprocess.call(["git", "clone", config('REPO_LINK'), "--quiet"])
    result = currentversion()
    if result == None:
        result = "1.0"
    while True:
        temp = f"{int(result.split('.')[0])}.{int(result.split('.')[-1])+1}"
        if not os.path.exists(f"{DIR}/alter/alter-{temp}.sql"):
            break
        result = temp
        
    return result

def syncdb():
    remote = remoteversion()
    current = currentversion()
    if current == None:
        print(f"Initializing database to {remote}")
        current = "1.0"
        if os.path.exists(f"{DIR}/alter/alter-{current}.sql"):
            execute_from_file(connection, f"{DIR}/alter/alter-{current}.sql")
        execute(
            connection,
            f'''INSERT INTO system_setting 
            (`key`, value, updated_at, created_at) 
            VALUES ('db.version', '1.0', now(), now());'''
        )
    if remote == current:
        print("Database is up to date")
    elif float(remote) > float(current):
        print(f"Updating database from {current} to {remote}")
        while True:
            current = f"{int(current.split('.')[0])}.{int(current.split('.')[-1])+1}"
            if os.path.exists(f"{DIR}/alter/alter-{current}.sql"):
                execute_from_file(connection, f"{DIR}/alter/alter-{current}.sql")
            else:
                break
        execute(
            connection,
            f'''UPDATE system_setting 
                SET value = {remote}, updated_at = now() 
                WHERE `key` = 'db.version';'''
        )
        print("Database updated")


if len(sys.argv) == 1:
    print("Usage: python main.py [command]")
    print("Commands:")
    print("  syncdb - Syncs the database")
    print("  currentversion - Prints the current version")
    print("  remoteversion - Prints the remote version")

elif sys.argv[1] == 'syncdb':
    syncdb()

elif sys.argv[1] == 'currentversion':
    version = currentversion()
    if version == None:
        print("Database is not initialized")
    else:
        print(f"Current version {version}")

elif sys.argv[1] == 'remoteversion':
    print(f"Remote version {remoteversion()}")


close(connection)
