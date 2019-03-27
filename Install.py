import argparse
from datetime import date
import hashlib
import random
import requests
import json
import os

parser = argparse.ArgumentParser(description='Add new node to your account.')
parser.add_argument('--name',
                    metavar='NODE_NAME',
                    type=str,
                    default='Auto-'+str(date.today()),
                    help='Name of the node.')
parser.add_argument('--host',
                    metavar='HOSTNAME',
                    type=str,
                    default='http://127.0.0.1:5000',
                    help='Host of the web app.')
parser.add_argument('--email',
                    metavar='EMAIL',
                    type=str,
                    default='jorgefrancoibanez@gmail.com',
                    help='User that make the request. Valid account is required.')
args = parser.parse_args()


def do_hash():
    if os.path.isfile('hashnode'):
        with open('hashnode') as f:
            h = [line for line in f]
    else:
        h = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
        f = open("hashnode", "w")
        f.write(h)
        f.close()
    return h


try:
    user = requests.post(args.host+"/users", data=args.email)
    data = {"name": args.name, "hash": do_hash()}
    add_node = requests.post(args.host+"/nodes/"+user.text, data=json.dumps(data))
    print(add_node.text)

except Exception as ex:
    print(ex)
