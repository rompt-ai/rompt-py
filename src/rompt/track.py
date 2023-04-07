import requests
import json
from typing import Optional, List, Any
from rompt.bindings import TemplateObject, GeneratedPrompt
from rompt.common import get_api_token


class Metadata:
    branchId: str
    promptId: str
    version: int
    template: TemplateObject


class TrackOptions:
    apiToken: Optional[str]


class Response:
    model: str
    choices: str
    responseType: str


class GeneratedPromptWithResponse:
    prompt: str
    metadata: Metadata
    response: Optional[Response]


def is_response_chat_completion(response: Any) -> bool:
    if isinstance(response.get("choices"), list):
        first_choice = response["choices"][0]
        return bool(first_choice.get("message"))
    return False


def is_response_completion(response: Any) -> bool:
    if isinstance(response.get("choices"), list):
        first_choice = response["choices"][0]
        return bool(first_choice.get("text"))
    return False


def send_track_arr(
    generated_prompts_with_response_arr: List[GeneratedPromptWithResponse],
    api_token: str,
    _env: Optional[str] = None,
) -> requests.Response:
    url = (
        f"https://api-{_env}.aws.rompt.ai/track"
        if _env
        else "https://api.aws.rompt.ai/track"
    )

    return requests.post(
        url,
        json={
            "apiToken": api_token,
            "tracks": generated_prompts_with_response_arr,
        },
    )


def track(
    generated_prompt: GeneratedPrompt,
    response: Any = None,
    options: TrackOptions = {"apiToken": None},
) -> requests.Response:
    stripped_response: Optional[Response] = None

    if response:
        if is_response_chat_completion(response):
            stripped_response = {
                "model": response["model"],
                "choices": json.dumps(response["choices"]),
                "responseType": "openai.chatCompletion",
            }
        elif is_response_completion(response):
            stripped_response = {
                "model": response["model"],
                "choices": json.dumps(response["choices"]),
                "responseType": "openai.completion",
            }

    generated_prompt_with_response: GeneratedPromptWithResponse = (
        {
            **generated_prompt,
            "response": stripped_response,
        }
        if stripped_response
        else generated_prompt
    )

    return send_track_arr(
        [generated_prompt_with_response],
        options.get("apiToken") or get_api_token(),
        options.get("_env"),
    )
