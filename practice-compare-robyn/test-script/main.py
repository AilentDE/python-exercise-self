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

# Prepare
user1 = UserGenerator(api_name)
message1 = user1.create_message()

user2 = UserGenerator(api_name)
message2 = user2.create_message()
user2.subscribe_user(user1.user_id)


# Test
tester = TestHandler(api_name)
tester.home()

tester.visit_message(user2.access_token, message1)

tester.delete_message(user1.access_token, message1)
