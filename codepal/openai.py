import re

import openai
import tiktoken

START_TAG = "<START>"
END_TAG = "<END>"
RESPONSE_PATTERN = re.compile(f"{START_TAG}(.*?){END_TAG}", re.DOTALL)


def generate_code(file_contents, prompt, model):
    """Use openai chat completion api."""

    messages = [
        {'role': 'system', 'content': 'You are an amazing pair programmer'},
        {'role': 'system',
         'content': 'You are given instructions on editing an existing file. To the best of your abilities, generate what the updated file should be. Please prefix the code with <START> and end the code with <END>. Everything in between should be able to be written as a new file. If the prompt does not make sense, please just respond with <NO_RESPONSE>'},
        {'role': 'user',
         'content': f'Here are the contents of the current file: {file_contents}. Update the file based on the provided prompt: {prompt}'}
    ]

    encoding = tiktoken.encoding_for_model(model)
    tokens = sum([len(encoding.encode(msg['content'])) for msg in messages])

    print(f"Prompt tokens: {tokens}")
    print(f'Model: {model}')
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    usage = response['usage']
    print(f'Response usage {usage}')

    response_content = response['choices'][0]['message']['content']
    updated_code_match = RESPONSE_PATTERN.search(response_content)

    if not updated_code_match:
        print('Could not generate code')
        return

    updated_code = updated_code_match.group(1)
    if not updated_code:
        print('Could not generate code')
        return

    return updated_code
