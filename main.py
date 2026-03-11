import argparse
import json
import os



def store_cred(service, username, password, filename='./data/vault.json'):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        data = {}

    data[service] = {
        "username": username, 
        "password": password
    }

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)



def get_cred(service, filename='./data/vault.json'):
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            vault= json.load(f)
    else:
        vault = {}

    if service in vault:
        print("Username:", vault[service]['username'])
        print("Password:", vault[service]['password'])
    else:
        print("No service")



def get_list(filename='./data/vault.json'):
    with open(filename, 'r') as f:
        data = json.load(f)

        print("Stored Services" + '\n')
        for el in data:
            print(el)





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