from req_handler import TestHandler, UserGenerator
from loguru import logger
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument("-n", "--Name", help="Api name")

args = parser.parse_args()
api_name = args.Name

if api_name not in ('fast', 'robyn', 'gin'):
    logger.error("Could not support this api type.")
    sys.exit(1)

# tester = TestHandler(api_name)
# tester.home()

user1 = UserGenerator()
message1 = user1.create_message()
print(message1)
user1.delete_message(message1)
