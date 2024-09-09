

LLM plugin providing access to Claude 3 models via the Anthropic API with prompt caching support.



Install this plugin in the same environment as [LLM](https://llm.datasette.io/):

```bash
llm install llm-claude-3
```



You'll need an Anthropic API key. Obtain one from [https://console.anthropic.com](https://console.anthropic.com), then configure it like this:

```bash
llm keys set anthropic
```



This plugin adds support for the following Claude 3 models:

- claude-3-opus-20240229
- claude-3-sonnet-20240229
- claude-3-haiku-20240229

To use them:

```bash
llm -m claude-3-opus-20240229 "Your prompt here"
llm -m claude-3-sonnet-20240229 "Another prompt"
llm -m claude-3-haiku-20240229 "Yet another prompt"
```



This plugin now supports prompt caching to improve performance and reduce costs for repetitive tasks or prompts with large amounts of context. Use the following options:

- `--system-cache`: Cache system instructions
- `--prompt-cache`: Cache user prompt content
- `--context-cache`: Cache additional context

Example usage:

```bash
llm -m claude-3-sonnet-20240229   --system-cache "You are an AI assistant specialized in analyzing literature."   --context-cache "Full text of Pride and Prejudice: ..."   --prompt-cache "Provide a brief summary of the major themes."   "What are the key relationships in the novel?"
```

Cached content has a 5-minute lifetime and is automatically refreshed when used.



All Claude 3 models support the following options:

- `-o temperature 0.7`: Controls randomness (0.0 to 1.0)
- `-o top_p 0.9`: Nucleus sampling parameter (0.0 to 1.0)
- `-o top_k 10`: Limits vocabulary to top K options
- `-o max_tokens 250`: Maximum number of tokens to generate

Example:

```bash
llm -m claude-3-sonnet-20240229 -o temperature 0.8 -o max_tokens 100 "Write a short poem"
```



To set up this plugin locally:

```bash
git clone https://github.com/your-username/llm-claude-3
cd llm-claude-3
python3 -m venv venv
source venv/bin/activate
pip install -e '.[test]'
```

To run the tests:

```bash
pytest
```



Contributions are welcome! Please feel free to submit a Pull Request.
