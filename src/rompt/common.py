import os
from pathlib import Path

_ENV = None


def ephemeral_dotenv():
    global _ENV
    if _ENV is None:
        env_file_path = Path.cwd() / ".env"
        _ENV = {}
        if env_file_path.exists():
            with open(env_file_path, "r", encoding="utf-8") as file:
                content = file.read()
                lines = content.split("\n")
                for line in lines:
                    key_value = line.split("=")
                    if len(key_value) == 2:
                        key, value = key_value
                        _ENV[key.strip()] = value.strip()
    return _ENV


def get_api_token():
    if "ROMPT_API_TOKEN" in os.environ:
        return os.environ["ROMPT_API_TOKEN"]
    else:
        _api_token = ephemeral_dotenv().get("ROMPT_API_TOKEN")
        if _api_token:
            return _api_token
        else:
            raise ValueError("ROMPT_API_TOKEN not found")


def debug_log(env, *messages):
    if env != "prod":
        print(*messages)
