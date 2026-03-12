import argparse
import json
import os
import getpass
import sys
import hashlib


vault_file = "./data/vault_example.json"
password_file = "./data/master.hash"


def load_vault():
    try:
        with open(vault_file, 'r') as f:
            vault_data = json.load(f)
    except json.JSONDecodeError:
        if os.path.getsize(vault_file) == 0:
            return dict()
        else:
            print("Vault file corrupted")
            return
    except FileNotFoundError:
        return dict()
    return vault_data



def authenticate_user():
    input_pass = getpass.getpass("Enter Master Password: ")
    h = hashlib.sha256()
    h.update(input_pass.encode('utf-8'))
    os.makedirs("data", exist_ok=True)
    if os.path.exists(password_file) and os.path.getsize(password_file) > 0:
        with open(password_file, "r") as f:
            master_pass = f.read()
        if master_pass != h.hexdigest():
            sys.exit("Incorrect Password")
    else:
        with open(password_file, 'w') as f:
            f.write(h.hexdigest())
        print("Master password set successfully")




def store_cred(service, username, password):
    data = load_vault()
    if data is not None:
        os.makedirs("data", exist_ok=True)

        if service in data:
            ans = input("Service already exists. Overwrite? (y/n):").lower()
            if ans in ['n','no']:
                print("Operation Cancelled")
                return
                
        data[service] = {
            "username": username, 
            "password": password
        }
        with open(vault_file, 'w') as f:
            json.dump(data, f, indent=4)
        print("Credentials stored successfully")



def get_cred(service):
    vault = load_vault()
    if vault is not None:
        if service in vault:
            print("Username:", vault[service]['username'])
            print("Password:", vault[service]['password'])
        else:
            print("Service Not Found")



def get_list():
    data = load_vault()
    if data is not None:
        if len(data) == 0:
            print("No Services stored")
        else:
            print("Stored Services" + '\n')
            for service in data:
                print(service)






parser = argparse.ArgumentParser()
subparser = parser.add_subparsers(dest='command', help='Available Commands', required=True)


parser_add = subparser.add_parser('add', help="Add a new Service")
parser_get = subparser.add_parser('get', help="Get creds")
parser_list = subparser.add_parser('list', help="Get a list of Services")


parser_add.add_argument('service', type=str, help="Name of The Service")
parser_get.add_argument('service', type=str, help="Name of The Service")


authenticate_user()

args = parser.parse_args()

if args.command == 'add':
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    store_cred(args.service, username, password)
elif args.command == 'get':
    get_cred(args.service)
elif args.command == 'list':
    get_list()