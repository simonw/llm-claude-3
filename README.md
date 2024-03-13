# llm-claude-3

[![PyPI](https://img.shields.io/pypi/v/llm-claude-3.svg)](https://pypi.org/project/llm-claude-3/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-claude-3?include_prereleases&label=changelog)](https://github.com/simonw/llm-claude-3/releases)
[![Tests](https://github.com/simonw/llm-claude-3/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-claude-3/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-claude-3/blob/main/LICENSE)

LLM access to Claude 3 by Anthropic

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-claude-3
```
## Usage

First, set an API key for Claude 3:
```bash
llm keys set claude
# Paste key here
```

Run `llm models` to list the models, and `llm models --options` to include a list of their options.

Run prompts like this:
```bash
llm -m claude-3-opus 'Fun facts about pelicans'
llm -m claude-3-sonnet 'Fun facts about walruses'
llm -m claude-3-haiku 'Fun facts about armadillos'
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-claude-3
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
