#!/usr/bin/env python3

import openai
import sys
import os
import configparser


CONFIG_DIR = os.getenv('XDG_CONFIG_HOME', os.path.expanduser('~/.config'))
API_KEYS_LOCATION = os.path.join(CONFIG_DIR, 'openaiapirc')


def create_template_ini_file():
    """
    If the ini file does not exist create it and add the organization_id and
    secret_key
    """
    if not os.path.isfile(API_KEYS_LOCATION):
        with open(API_KEYS_LOCATION, 'w') as f:
            f.write('[openai]\n')
            f.write('organization_id=\n')
            f.write('secret_key=\n')

        print('OpenAI API config file created at {}'.format(API_KEYS_LOCATION))
        # print('Please edit it and add your organization ID and secret key')
        print('Please edit it and add your secret key.')
        sys.exit(1)


def initialize_openai_api():
    """
    Initialize the OpenAI API
    """
    # Check if file at API_KEYS_LOCATION exists
    create_template_ini_file()
    config = configparser.ConfigParser()
    config.read(API_KEYS_LOCATION)

    openai.organization_id = config['openai']['organization_id'].strip('"').strip("'")
    openai.api_key = config['openai']['secret_key'].strip('"').strip("'")


initialize_openai_api()


SYSTEM_MESSAGE = \
'''
You are a chatbot with the purpose of programming for a user.
You can execute multiple different actions, which you can execute by writting a message starting with the action name in the format [<action name>].
The available actions are:
[message_user] <message to the user>
[read] <file path> <start line> <end line>   
[write] <file path> <start line> <end line> <text to write>
'''



def print_chat(messages):
    """
    Print the chat messages
    """
    for message in messages:
        if message['role'] == 'user':
            print('User: {}'.format(message['content']))
        elif message['role'] == 'assistant':
            print('Assistant: {}'.format(message['content']))
        elif message['role'] == 'system':
            print('System: {}'.format(message['content']))


def get_user_input():
    print('User: ', end='')
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)

    return contents




# messages = [{"role": "user", "content": user_input}]
messages = []


while True:
    # user_input = input("User: ")
    user_input = get_user_input()



    # messages = [{"role": "user", "content": user_input}]
    messages.append({"role": "system", "content": SYSTEM_MESSAGE})
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
      messages=messages,
    )

    response_text = response["choices"][0]["message"]['content']

    messages.append({"role": "assistant", "content": response_text})
    # print_chat(messages)
    print(f'Assistant: {response_text}')

