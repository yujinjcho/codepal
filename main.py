import os
import re

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

start_tag = "<START>"
end_tag = "<END>"
pattern = re.compile(f"{start_tag}(.*?){end_tag}", re.DOTALL)

if __name__ == '__main__':

    while True:
        file_name = input('Target filename > ')

        if not os.path.isfile(file_name):
            print('This file does not exist')
            continue


        with open(file_name, 'r') as f:
            contents = f.read()

        print(f'Contents: {contents}')

        instructions = input('Instructions > ')


        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {'role':'system', 'content': 'You are an amazing pair programmer'},
                {'role':'system', 'content': 'You are given instructions on editing and existing file. To the best of your abilities generate what the updated file should be. Please prefix the code with <START> and end the code with <END>. Everything inbetween should be able to be written as a new file. If the prompt does not make sense please just respond with <NO_RESPONSE>'},
                {'role':'user', 'content': f'Here are the contents of the current file: {contents}. Update the file based on the provided prompt: {instructions}'}
            ]
        )
        print(response)

        response_content = response['choices'][0]['message']['content']
        updated_code_match = pattern.search(response_content)

        if not updated_code_match:
            print('Did not have matching code')

        updated_code = updated_code_match.group(1)
        if not updated_code:
            print('Did not have matching code group')


        with open(file_name, 'w') as f:
            f.write(updated_code)

