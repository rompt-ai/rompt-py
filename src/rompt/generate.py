import json
import os
from typing import Optional, List, Union, TypedDict
from rompt.bindings import TemplateObject, Prompts, FlattenedItem, GeneratedPrompt

file_to_prompts: Prompts = {}


def is_aws_lambda_env():
    return (
        "AWS_LAMBDA_FUNCTION_NAME" in os.environ
        or "AWS_LAMBDA_FUNCTION_VERSION" in os.environ
    )


class GenerateSettings(TypedDict):
    promptFilePath: str
    version: Union["latest", int]


def generate(
    prompt_name: str,
    template_object: Optional[TemplateObject] = None,
    options: Optional[GenerateSettings] = None,
) -> GeneratedPrompt:
    if options is None:
        options = {}

    prompt_file_path = options.get("promptFilePath", "prompts.json")
    version = options.get("version", "latest")
    formatted_template_object = format_variable_keys_with_curlies(template_object)

    if prompt_file_path not in file_to_prompts:
        try:
            with open(prompt_file_path, "r", encoding="utf-8") as f:
                file_to_prompts[prompt_file_path] = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Could not find prompts file at {prompt_file_path}. Please run `npx rompt pull`."
            )

    prompt_data = file_to_prompts[prompt_file_path][prompt_name]
    branch_id, prompt_id, versions = (
        prompt_data["branchId"],
        prompt_data["id"],
        prompt_data["versions"],
    )

    if version == "latest":
        version_number = max(int(k) for k in versions.keys())
    else:
        version_number = version

    parts = versions[str(version_number)]["parts"]

    return {
        "prompt": generate_string(parts, formatted_template_object),
        "metadata": {
            "branchId": branch_id,
            "promptId": prompt_id,
            "version": version_number,
            "template": formatted_template_object,
        },
    }


def format_variable_keys_with_curlies(
    input_dict: Optional[TemplateObject],
) -> TemplateObject:
    formatted_output = {}

    for key, value in input_dict.items():
        formatted_key = key

        if not formatted_key.startswith("{"):
            formatted_key = "{" + formatted_key

        if not formatted_key.endswith("}"):
            formatted_key = formatted_key + "}"

        formatted_output[formatted_key] = value

    return formatted_output


def generate_string(items: List[FlattenedItem], variables: TemplateObject) -> str:
    result = ""

    for item in items:
        if item["type"] == "text":
            result += item["content"]
        elif item["type"] == "variable":
            variable_value = variables.get(item["content"])
            if variable_value is not None:
                result += variable_value
        elif item["type"] == "paragraph":
            result += "\n"

    return result
