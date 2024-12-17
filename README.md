# llm-anthropic

[![PyPI](https://img.shields.io/pypi/v/llm-anthropic.svg)](https://pypi.org/project/llm-anthropic/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-anthropic?include_prereleases&label=changelog)](https://github.com/simonw/llm-anthropic/releases)
[![Tests](https://github.com/simonw/llm-anthropic/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-anthropic/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-anthropic/blob/main/LICENSE)

LLM access to models by Anthropic, including the Claude series

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-anthropic
```

## Usage

First, set [an API key](https://console.anthropic.com/settings/keys) for Anthropic:
```bash
llm keys set anthropic
# Paste key here
```

You can also set the key in the environment variable `ANTHROPIC_API_KEY`

Run `llm models` to list the models, and `llm models --options` to include a list of their options.

Run prompts like this:
```bash
llm -m anthropic/claude-3.5-sonnet 'Fun facts about pelicans'
llm -m anthropic/claude-3.5-haiku 'Fun facts about armadillos'
llm -m anthropic/claude-3-opus 'Fun facts about squirrels'
```
Images are supported too, for models other than Claude 3.5 Haiku:
```bash
llm -m anthropic/claude-3.5-sonnet 'describe this image' -a https://static.simonwillison.net/static/2024/pelicans.jpg
llm -m anthropic/claude-3-haiku 'extract text' -a page.png
```
Claude 3.5 Sonnet can handle PDF files:
```bash
llm -m anthropic/claude-3.5-sonnet 'extract text' -a page.pdf
```
The plugin sets up `claude-3.5-sonnet` and similar as aliases, usable like this:
```bash
llm -m claude-3.5-sonnet 'Fun facts about pelicans'
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-anthropic
python3 -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
llm install -e '.[test]'
```
To run the tests:
```bash
pytest
```

This project uses [pytest-recording](https://github.com/kiwicom/pytest-recording) to record Anthropic API responses for the tests.

If you add a new test that calls the API you can capture the API response like this:
```bash
PYTEST_ANTHROPIC_API_KEY="$(llm keys get claude)" pytest --record-mode once
```
You will need to have stored a valid Anthropic API key using this command first:
```bash
llm keys set claude
# Paste key here
```