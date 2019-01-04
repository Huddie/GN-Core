"""Initialize Grade-Notifier               
"""

__author__      = "Ehud Adler & Akiva Sherman"
__copyright__   = "Copyright 2018, The Punk Kids"
__license__     = "MIT"
__version__     = "1.0.0"
__maintainer__  = "Ehud Adler & Akiva Sherman"
__email__       = "self@ehudadler.com"
__status__      = "Production"

import argparse
import constants
import time
import os
import requests
import getpass

from cunylogin import login, logout
from os.path import join, dirname
from dotenv import load_dotenv
from constants import log_path
from session import Session
from fileManager import create_dir

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

# Accessing variables.
account_pass = os.getenv('ACCOUNT_PASSWORD')

def run(username, password, school, phone, local):
    log_path = f'{constants.log_path(local)}/{username}{time.time()}'
    create_dir(constants.log_path(local))
    if local:
        print(f'python3 ./grade-notifier.py --username={username} --password={password} --school={school} --phone={phone} > {log_path}.txt 2>&1')
        os.system(f'python3 ./grade-notifier.py --username={username} --password={password} --school={school} --phone={phone} > {log_path}.txt 2>&1')
    else:
        os.system(f'echo "{account_pass}" | su -c "nohup setsid python3 /home/fa18/313/adeh6562/public_html/grade-notifier/Grade-Notifier/grade-notifier.py --username={username} --password={password} --school={school} --phone={phone} --prod=true" - adeh6562 > {log_path}.txt 2>&1 &')

def parse():
    parser = argparse.ArgumentParser(description='Specify commands for CUNY Grade Notifier Retriever v1.0')
    parser.add_argument('--school', default="QNS01")
    parser.add_argument('--list-codes', action='store_true')
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--phone')
    parser.add_argument('--filename')

    ## Production
    parser.add_argument('--prod') 

    ## Development
    parser.add_argument('--enable_phone')

    ## Testing 
    parser.add_argument('--test')
    parser.add_argument('--test_diff')
    parser.add_argument('--test_add_remove_instance')
    parser.add_argument('--test_message_contruction')
    return parser.parse_args()

def main():
    args = parse()
    try:

        s = requests.Session()
        s.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        username = input("Enter username: ") if not args.username else args.username
        password = getpass.getpass("Enter password: ") if not args.password else args.password
        number = input("Enter phone number: ") if not args.phone else args.phone
        prod  = False if not args.prod else True
        session = Session(s, username, password, number)
        did_log_in = login(session, username, password)
        if did_log_in:
            run(username, password, args.school.upper(), number, not prod)
        else:
            print("Invalid Credentials")
 

    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    main()