import llm
import pytest

TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xa6\x00\x00\x01\x1a"
    b"\x02\x03\x00\x00\x00\xe6\x99\xc4^\x00\x00\x00\tPLTE\xff\xff\xff"
    b"\x00\xff\x00\xfe\x01\x00\x12t\x01J\x00\x00\x00GIDATx\xda\xed\xd81\x11"
    b"\x000\x08\xc0\xc0.]\xea\xaf&Q\x89\x04V\xe0>\xf3+\xc8\x91Z\xf4\xa2\x08EQ\x14E"
    b"Q\x14EQ\x14EQ\xd4B\x91$I3\xbb\xbf\x08EQ\x14EQ\x14EQ\x14E\xd1\xa5"
    b"\xd4\x17\x91\xc6\x95\x05\x15\x0f\x9f\xc5\t\x9f\xa4\x00\x00\x00\x00IEND\xaeB`"
    b"\x82"
)


@pytest.mark.vcr
def test_prompt():
    model = llm.get_model("claude-3-opus")
    model.key = model.key or "sk-..."  # don't override existing key
    response = model.prompt("Two names for a pet pelican, be brief")
    assert str(response) == "1. Pelly\n2. Beaky"
    response_dict = dict(response.response_json)
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


EXPECTED_IMAGE_TEXT = (
    "This image shows two simple rectangular blocks of solid colors stacked "
    "vertically. The top rectangle is a bright, vibrant red color, while the "
    "bottom rectangle is a bright, neon green color. The rectangles appear to "
    "be of similar width but may be slightly different in height. The colors "
    "are very saturated and create a striking contrast against each other."
)


@pytest.mark.vcr
def test_image_prompt():
    model = llm.get_model("claude-3.5-sonnet")
    model.key = (
        model.key
        or "sk-..."
    )
    response = model.prompt(
        "Describe image in three words",
        attachments=[llm.Attachment(content=TINY_PNG)],
    )
    assert str(response) == EXPECTED_IMAGE_TEXT
    response_dict = response.response_json
    response_dict.pop("id")  # differs between requests
    assert response_dict == {
        "content": [
            {
                "text": EXPECTED_IMAGE_TEXT,
                "type": "text",
            }
        ],
        "model": "claude-3-5-sonnet-20241022",
        "role": "assistant",
        "stop_reason": "end_turn",
        "stop_sequence": None,
        "type": "message",
        "usage": {"input_tokens": 76, "output_tokens": 75},
    }
