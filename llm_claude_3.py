from anthropic import Anthropic
import llm
from pydantic import Field, field_validator
from typing import Optional, List


@llm.hookimpl
def register_models(register):
    # https://docs.anthropic.com/claude/docs/models-overview
    register(ClaudeMessages("claude-3-opus-20240229"), aliases=("claude-3-opus",))
    register(ClaudeMessages("claude-3-sonnet-20240229"), aliases=("claude-3-sonnet",))


class ClaudeMessages(llm.Model):
    needs_key = "claude"
    key_env_var = "ANTHROPIC_API_KEY"
    can_stream = True

    class Options(llm.Options):
        max_tokens: int = Field(
            description="The maximum number of tokens to generate before stopping",
            default=4096,
        )
        user_id: Optional[str] = Field(
            description="An external identifier for the user who is associated with the request",
            default=None,
        )

    def __init__(self, model_id):
        self.model_id = model_id

    def build_messages(self, prompt, conversation) -> List[dict]:
        messages = []
        if conversation:
            for response in conversation.responses:
                messages.extend(
                    [
                        {
                            "role": "user",
                            "content": response.prompt.prompt,
                        },
                        {"role": "assistant", "content": response.text()},
                    ]
                )
        messages.append({"role": "user", "content": prompt.prompt})
        return messages

    def execute(self, prompt, stream, response, conversation):
        client = Anthropic(api_key=self.get_key())

        kwargs = {
            "model": self.model_id,
            "messages": self.build_messages(prompt, conversation),
            "max_tokens": prompt.options.max_tokens,
        }
        if prompt.options.user_id:
            kwargs["metadata"] = {"user_id": prompt.options.user_id}

        if prompt.system:
            kwargs["system"] = prompt.system

        usage = None
        if stream:
            with client.messages.stream(**kwargs) as stream:
                for text in stream.text_stream:
                    yield text
                # This records usage and other data:
                response.response_json = stream.get_final_message().model_dump()
        else:
            completion = client.messages.create(**kwargs)
            yield completion.content[0].text
            response.response_json = completion.model_dump()

    def __str__(self):
        return "Anthropic Messages: {}".format(self.model_id)
