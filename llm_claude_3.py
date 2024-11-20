from anthropic import Anthropic
import llm
from pydantic import Field, field_validator, model_validator
from typing import Optional, List


@llm.hookimpl
def register_models(register):
    # https://docs.anthropic.com/claude/docs/models-overview
    register(ClaudeMessages("claude-3-opus-20240229"), aliases=("claude-3-opus",))
    register(ClaudeMessages("claude-3-sonnet-20240229"), aliases=("claude-3-sonnet",))
    register(ClaudeMessages("claude-3-haiku-20240307"), aliases=("claude-3-haiku",))
    register(ClaudeMessagesLong("claude-3-5-sonnet-20240620"), aliases=("claude-3.5-sonnet",))
    register(ClaudeMessagesLong("claude-3-5-haiku-latest"), aliases=("claude-3.5-haiku",))


class ClaudeOptions(llm.Options):
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate before stopping",
        default=4_096,
    )

    temperature: Optional[float] = Field(
        description="Amount of randomness injected into the response. Defaults to 1.0. Ranges from 0.0 to 1.0. Use temperature closer to 0.0 for analytical / multiple choice, and closer to 1.0 for creative and generative tasks. Note that even with temperature of 0.0, the results will not be fully deterministic.",
        default=1.0,
    )

    top_p: Optional[float] = Field(
        description="Use nucleus sampling. In nucleus sampling, we compute the cumulative distribution over all the options for each subsequent token in decreasing probability order and cut it off once it reaches a particular probability specified by top_p. You should either alter temperature or top_p, but not both. Recommended for advanced use cases only. You usually only need to use temperature.",
        default=None,
    )

    top_k: Optional[int] = Field(
        description="Only sample from the top K options for each subsequent token. Used to remove 'long tail' low probability responses. Recommended for advanced use cases only. You usually only need to use temperature.",
        default=None,
    )

    user_id: Optional[str] = Field(
        description="An external identifier for the user who is associated with the request",
        default=None,
    )

    cache_prompt: Optional[bool] = Field(
        description="Whether to cache the user prompt for future use",
        default=None,
    )

    cache_system: Optional[bool] = Field(
        description="Whether to cache the system prompt for future use",
        default=None,
    )

    @field_validator("max_tokens")
    @classmethod
    def validate_max_tokens(cls, max_tokens):
        real_max = cls.model_fields["max_tokens"].default
        if not (0 < max_tokens <= real_max):
            raise ValueError(f"max_tokens must be in range 1-{real_max}")
        return max_tokens

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, temperature):
        if not (0.0 <= temperature <= 1.0):
            raise ValueError("temperature must be in range 0.0-1.0")
        return temperature

    @field_validator("top_p")
    @classmethod
    def validate_top_p(cls, top_p):
        if top_p is not None and not (0.0 <= top_p <= 1.0):
            raise ValueError("top_p must be in range 0.0-1.0")
        return top_p

    @field_validator("top_k")
    @classmethod
    def validate_top_k(cls, top_k):
        if top_k is not None and top_k <= 0:
            raise ValueError("top_k must be a positive integer")
        return top_k

    @model_validator(mode="after")
    def validate_temperature_top_p(self):
        if self.temperature != 1.0 and self.top_p is not None:
            raise ValueError("Only one of temperature and top_p can be set")
        return self

class ClaudeMessages(llm.Model):
    needs_key = "claude"
    key_env_var = "ANTHROPIC_API_KEY"
    can_stream = True

    class Options(ClaudeOptions): ...

    def __init__(self, model_id, claude_model_id=None, extra_headers=None):
        self.model_id = model_id
        self.claude_model_id = claude_model_id or model_id
        self.extra_headers = extra_headers

    def build_messages(self, prompt, conversation) -> List[dict]:
        messages = []
        cache_control_count = 0
        max_cache_control_blocks = 2  # Leave one for the current prompt and system prompt

        if conversation:
            for response in reversed(conversation.responses):
                user_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": response.prompt.prompt,
                        }
                    ],
                }
                
                if prompt.options.cache_prompt is not False and cache_control_count < max_cache_control_blocks:
                    user_message["content"][0]["cache_control"] = {"type": "ephemeral"}
                    cache_control_count += 1

                messages.insert(0, user_message)
                messages.insert(1, {"role": "assistant", "content": response.text()})

        current_prompt = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt.prompt,
                }
            ]
        }

        if prompt.options.cache_prompt:
            current_prompt["content"][0]["cache_control"] = {"type": "ephemeral"}

        messages.append(current_prompt)
        return messages

    def execute(self, prompt, stream, response, conversation):
        client = Anthropic(api_key=self.get_key(), default_headers={"anthropic-beta": "prompt-caching-2024-07-31"})
        kwargs = {
            "model": self.claude_model_id,
            "messages": self.build_messages(prompt, conversation),
            "max_tokens": prompt.options.max_tokens,
        }
        if prompt.options.user_id:
            kwargs["metadata"] = {"user_id": prompt.options.user_id}

        if prompt.options.top_p:
            kwargs["top_p"] = prompt.options.top_p
        else:
            kwargs["temperature"] = prompt.options.temperature

        if prompt.options.top_k:
            kwargs["top_k"] = prompt.options.top_k

        if prompt.system:
            kwargs["system"] = [
                {
                    "type": "text",
                    "text": prompt.system,
                    "cache_control": {"type": "ephemeral"} if prompt.options.cache_system else None
                }
            ]

        if stream:
            with client.messages.stream(**kwargs) as stream:
                for text in stream.text_stream:
                    yield text
                # This records usage and other data:
                response.response_json = stream.get_final_message().model_dump()
        else:
            completion = client.beta.prompt_caching.messages.create(**kwargs)
            yield completion.content[0].text
            response.response_json = completion.model_dump()

    def __str__(self):
        return f"Anthropic Messages: {self.model_id}"

class ClaudeMessagesLong(ClaudeMessages):
    class Options(ClaudeOptions):
        max_tokens: Optional[int] = Field(
            description="The maximum number of tokens to generate before stopping",
            default=4_096 * 2,
        )
