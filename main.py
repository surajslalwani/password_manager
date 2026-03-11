import argparse
import json
import os

vault_file = "./data/vault_example.json"


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


def store_cred(service, username, password):
    data = load_vault()
    if data is not None:
        data[service] = {
            "username": username, 
            "password": password
        }
        os.makedirs("data", exist_ok=True)
        with open(vault_file, 'w') as f:
            json.dump(data, f, indent=4)



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

args = parser.parse_args()


if args.command == 'add':
    username = input("Username: ")
    password = input("Password: ")

    store_cred(args.service, username, password)
elif args.command == 'get':
    get_cred(args.service)
elif args.command == 'list':
    get_list()