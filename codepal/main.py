#!/usr/bin/env python3

import os
import re
import argparse
import openai

start_tag = "<START>"
end_tag = "<END>"
pattern = re.compile(f"{start_tag}(.*?){end_tag}", re.DOTALL)

def get_conf():
    config_file_path = os.path.expanduser('~/.codepal/keys.conf')

    if not os.path.isfile(config_file_path):
        print("Config file not found")  # Debug: print a message if the config file is not found
        return None

    conf = {}

    with open(config_file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            conf[key] = value

    return conf


def generate_code(file_name, instructions, model):
    with open(file_name, 'r') as f:
        contents = f.read()

    print(f'Model {model}')
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role':'system', 'content': 'You are an amazing pair programmer'},
            {'role':'system', 'content': 'You are given instructions on editing an existing file. To the best of your abilities, generate what the updated file should be. Please prefix the code with <START> and end the code with <END>. Everything in between should be able to be written as a new file. If the prompt does not make sense, please just respond with <NO_RESPONSE>'},
            {'role':'user', 'content': f'Here are the contents of the current file: {contents}. Update the file based on the provided prompt: {instructions}'}
        ]
    )

    response_content = response['choices'][0]['message']['content']
    updated_code_match = pattern.search(response_content)

    if not updated_code_match:
        print('Did not have matching code')

    updated_code = updated_code_match.group(1)
    if not updated_code:
        print('Did not have matching code group')

    with open(file_name, 'w') as f:
        f.write(updated_code)


def main():
    parser = argparse.ArgumentParser(description='Generate code using OpenAI API and update a target file.')
    parser.add_argument('file_name', help='The target file to be updated')
    parser.add_argument('instructions', help='The instructions for generating the new code')
    parser.add_argument('--api_key', help='The OpenAI API key', default=os.environ.get("OPENAI_API_KEY"))

    args = parser.parse_args()

    conf = get_conf()

    api_key = args.api_key or conf.get('OPENAI_API_KEY', None) or os.environ.get("OPENAI_API_KEY")

    if not api_key:
        print("Please provide an OpenAI API key either as an environment variable or as a command line argument.")
        exit(1)

    openai.api_key = api_key

    if not os.path.isfile(args.file_name):
        print('This file does not exist')
        exit(1)

    model = conf.get('OPENAI_MODEL', 'gpt-4')

    generate_code(args.file_name, args.instructions, model)

if __name__ == '__main__':
    main()
