# llm-claude-3

[![PyPI](https://img.shields.io/pypi/v/llm-claude-3.svg)](https://pypi.org/project/llm-claude-3/)
[![Changelog](https://img.shields.io/github/v/release/simonw/llm-claude-3?include_prereleases&label=changelog)](https://github.com/simonw/llm-claude-3/releases)
[![Tests](https://github.com/simonw/llm-claude-3/actions/workflows/test.yml/badge.svg)](https://github.com/simonw/llm-claude-3/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/llm-claude-3/blob/main/LICENSE)

LLM access to Claude 3 by Anthropic

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
git clone -b prompt-caching https://github.com/irthomasthomas/llm-claude-3-caching.git
cd llm-claude-3-caching
llm install -e .
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

## Prompt Caching

This plugin now supports Anthropic's Prompt Caching feature, which can significantly improve performance and reduce costs for certain types of queries.

### How It Works

Prompt Caching allows you to store and reuse context within your prompt. This is especially useful for:

- Prompts with many examples
- Large amounts of context or background information
- Repetitive tasks with consistent instructions
- Long multi-turn conversations

The cache has a 5-minute lifetime, refreshed each time the cached content is used.

### Usage

To enable Prompt Caching, use the following options:

- `-o cache_prompt 1`: Enables caching for the user prompt.
- `-o cache_system 1`: Enables caching for the system prompt.

Example:
```bash
llm -m claude-3-sonnet -o cache_prompt 1 'Analyze this text: [long text here]'
llm -m claude-3-sonnet -o cache_prompt 1 -o cache_system 1 'Analyze this text: [long text here]' --system '[long system prompt here]'

llm -c # continues from cached prompt, if available
```

### Benefits

- Reduced latency: Can improve response times by over 2x.
- Cost savings: Up to 90% reduction in costs for repetitive tasks.
- Improved consistency: Helps maintain context across multiple queries.

### Caching Behavior

- The system checks if the prompt prefix is already cached from a recent query.
- If found, it uses the cached version, reducing processing time and costs.
- Otherwise, it processes the full prompt and caches the prefix for future use.

### Supported Models

Prompt Caching is currently supported on:

- Claude 3.5 Sonnet
- Claude 3 Haiku
- Claude 3 Opus

### Performance Tracking

You can monitor cache performance using these fields in the API response:

- `cache_creation_input_tokens`: Number of tokens written to the cache when creating a new entry.
- `cache_read_input_tokens`: Number of tokens retrieved from the cache for this request.
  
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
