import json
import os
from typing import Optional
import requests
from rompt.common import get_api_token, debug_log


def pull(
    branch: Optional[str],
    destination: str,
    api_token: Optional[str],
    _env: Optional[str],
    _dry: bool,
):
    root_api = f"api-{_env}.aws.rompt.ai" if _env else "api.aws.rompt.ai"
    api_token = api_token or get_api_token()

    debug_log(
        _env,
        f"Pulling prompts from branch {branch}.",
        json.dumps(
            {
                "branch": branch,
                "destination": destination,
                "env": _env,
                "apiToken": api_token,
                "rootApi": root_api,
                "cwd": os.getcwd(),
            },
            indent=2,
        ),
    )

    if not api_token:
        raise Exception(
            "You must provide an API token in your env or `--token`. You can get one from https://rompt.ai."
        )

    response = requests.post(
        f"https://{root_api}/pull",
        json=(
            {
                "apiToken": api_token,
                "branch": branch,
            }
            if branch
            else {
                "apiToken": api_token,
            }
        ),
    )

    pull_result = response.json()

    if not _dry:
        with open(
            os.path.join(os.getcwd(), destination), "w", encoding="utf-8"
        ) as outfile:
            json.dump(pull_result, outfile, indent=2)

        print(
            f"Done! Your prompts are in {destination}."
            + "\n\nNext, install the `@romptai/client` package then use it in your code like this:"
            + '\n\n\nconst romptData = generate("your-prompt-name", {\n  NAME: "Michael",\n  DIRECTION: "Generate a Tweet",\n  SENTIMENT: `Make the Tweet about ${myOtherVariable}`\n})'
            + "\n\nconst { prompt } = romptData;"
            + "\n\n// Your generated prompt is in `prompt`"
            + "\n\n// Example with OpenAI:"
            + "\n\nconst gptResponse = await openai.createCompletion({\n  prompt,\n  //...\n});",
        )

    return pull_result
