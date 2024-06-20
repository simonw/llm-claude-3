import llm
import pytest


@pytest.mark.vcr
def test_prompt():
    model = llm.get_model("claude-3-opus")
    model.key = model.key or "sk-..."  # don't override existing key
    response = model.prompt("Two names for a pet pelican, be brief")
    assert str(response) == "1. Pelly\n2. Beaky"
    response_dict = response.response_json
    response_dict.pop("id")  # differs between requests
    assert response_dict == {
        "content": [{"text": "1. Pelly\n2. Beaky", "type": "text"}],
        "model": "claude-3-opus-20240229",
        "role": "assistant",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "type": "message",
        "usage": {"input_tokens": 17, "output_tokens": 15},
    }
