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

First, set [an API key](https://console.anthropic.com/settings/keys) for Claude 3:
```bash
llm keys set claude
# Paste key here
```

Run `llm models` to list the models, and `llm models --options` to include a list of their options.

Run prompts like this:
```bash
llm -m claude-3.5-sonnet 'Fun facts about pelicans'
llm -m claude-3-opus 'Fun facts about squirrels'
llm -m claude-3-sonnet 'Fun facts about walruses'
llm -m claude-3-haiku 'Fun facts about armadillos'
```

## New Features

### Stop Sequences
Control when the model stops generating text:

```bash
llm -m claude-3-opus -o stop_sequences '["END", "STOP"]' 'Write a story'
```

### Prefill
Provide a starting point for the model to continue from:

```bash
llm -m claude-3-opus -o prefill "It was a dark and stormy night" 'Continue the story'
```

## Usage Examples

Get creative with Claude 3 models:

1. Basic prompt:
   ```bash
   llm -m claude-3-haiku 'Haiku about spring'
   ```

2. Using stop sequences:
   ```bash
   llm -m claude-3-sonnet -o stop_sequences '["THE END"]' 'Short mystery story'
   ```

3. With prefill:
   ```bash
   llm -m claude-3-opus -o prefill "In the year 2050" 'Describe the future'
   ```

4. Combining options:
   ```bash
   llm -m claude-3.5-sonnet -o stop_sequences '["DONE"]' -o prefill "Recipe for happiness:" 'Complete the recipe'
   ```

Explore all available options:
```bash
llm models --options
```

Remember to check the [Anthropic documentation](https://docs.anthropic.com) for detailed information on Claude 3 capabilities and best practices.

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