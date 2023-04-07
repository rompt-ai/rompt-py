from rompt.pull import pull
from rompt.generate import generate
from rompt.track import track
from rompt.common import ephemeral_dotenv


def test():
    env = ephemeral_dotenv()

    print("CLI Pull")
    pulled_prompts = pull(
        _env="staging",
        _dry=False,
        branch=None,
        api_token=env["ROMPT_API_TOKEN"],
        destination="prompts.json",
    )

    if pulled_prompts.get("_errors", False):
        raise Exception("Failed to pull prompts.")

    print("Generate Prompt With No Input")
    generated_prompt = generate(
        prompt_name="test",
        template_object={},
    )

    if (
        generated_prompt.get("prompt")
        != "This prompt is for testing the client packages. The current package is "
    ):
        raise Exception(
            "Failed to Generate Prompt With No Input.",
            generated_prompt.get("prompt"),
            "This prompt is for testing the client packages. The current package is ",
        )

    print("Generate Prompt With Input")
    generated_prompt = generate(
        prompt_name="test",
        template_object={"LANG": "Python"},
    )

    if (
        generated_prompt.get("prompt")
        != "This prompt is for testing the client packages. The current package is Python"
    ):
        raise Exception(
            "Failed to Generate Prompt With Input.",
            generated_prompt.get("prompt"),
            "This prompt is for testing the client packages. The current package is Python",
        )

    print("Track Prompt Without Response")
    response = track(
        generated_prompt, None, {"apiToken": env["ROMPT_API_TOKEN"], "_env": "staging"}
    )

    if not response.json().get("success"):
        raise Exception("Failed to track prompt without response.", response.text)

    print("Track Prompt With Chat Completion Response")
    exampleChatCompletionResponse = {
        "id": "chatcmpl-72PitcHpPRqrVKE0drqPdLS1UZW7m",
        "object": "chat.completion",
        "created": 1680809891,
        "model": "gpt-3.5-turbo-0301",
        "usage": {"prompt_tokens": 11, "completion_tokens": 9, "total_tokens": 20},
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I assist you today?",
                },
                "finish_reason": "stop",
                "index": 0,
            }
        ],
    }
    response = track(
        generated_prompt,
        exampleChatCompletionResponse,
        {"apiToken": env["ROMPT_API_TOKEN"], "_env": "staging"},
    )

    if not response.json().get("success"):
        raise Exception(
            "Failed to Track Prompt With Chat Completion Response.", response.text
        )

    print("Track Prompt With Completion Response")
    exampleCompletionResponse = {
        "id": "cmpl-72PhEls2MoIttCcpfKlfIw9yrysVX",
        "object": "text_completion",
        "created": 1680809788,
        "model": "text-davinci-003",
        "choices": [
            {
                "text": "\n\nHello! It's great to hear from you. How are you doing",
                "index": 0,
                "logprobs": None,
                "finish_reason": "length",
            }
        ],
        "usage": {"prompt_tokens": 2, "completion_tokens": 16, "total_tokens": 18},
    }
    response = track(
        generated_prompt,
        exampleCompletionResponse,
        {"apiToken": env["ROMPT_API_TOKEN"], "_env": "staging"},
    )

    if not response.json().get("success"):
        raise Exception(
            "Failed to Track Prompt With Completion Response.", response.text
        )


if __name__ == "__main__":
    raise SystemExit(test())
