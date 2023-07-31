# Codepal

Codepal is a cli tool that allows you to specify a file and instructions for updating the file.

Changes will automatically be applied. Please use version contol.

## Installation
```
pip3 install -e .
```

## Usage
```
codepal FILE_PATH 'Some prompt'
```

## Configuration

Supports the following environment variables:
- OPENAI_API_KEY
- OPENAI_MODEL

Alternatively, these could be set in `~./codepal/keys.conf` e.g.
```
OPENAI_API_KEY=YOUR_KEY
OPENAI_MODEL=gpt-4
```

