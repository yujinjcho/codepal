#!/usr/bin/env python3

import os
import argparse
import openai

from codepal.openai import generate_code
from codepal.utils import get_conf, load_file

OPENAI_API_KEY_ENV_VAR = 'OPENAI_API_KEY'
OPENAI_MODEL_ENV_VAR = 'OPENAI_MODEL'
OPENAI_DEFAULT_MODEL = 'gpt-4'


def main():
    parser = argparse.ArgumentParser(description='Generate code using OpenAI API and update a target file.')
    parser.add_argument('file_name', help='The target file to be updated')
    parser.add_argument('prompt', help='The prompt for updating the file')
    parser.add_argument('-c', '--conf_filepath', default='~/.codepal/keys.conf', help='Filepath for the conf file')

    args = parser.parse_args()

    # load conf
    conf = get_conf(args.conf_filepath)
    if not conf:
        print('Invalid config file')
        exit(1)

    # set api key
    api_key = conf.get(OPENAI_API_KEY_ENV_VAR, None) or os.environ.get(OPENAI_API_KEY_ENV_VAR)
    if not api_key:
        print("Please provide an OpenAI API key either as an environment variable or in the config file.")
        exit(1)
    openai.api_key = api_key

    # ensure file exists
    if not os.path.isfile(args.file_name):
        print('This file does not exist')
        exit(1)

    model = conf.get(OPENAI_MODEL_ENV_VAR, OPENAI_DEFAULT_MODEL)

    with open(args.file_name, 'r') as f:
        file_contents = f.read()

    updated_code = generate_code(file_contents, args.prompt, model)
    if not updated_code:
        exit(1)

    with open(args.file_name, 'w') as f:
        f.write(updated_code)

if __name__ == '__main__':
    main()
