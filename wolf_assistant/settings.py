import os
import typing
import pathlib

from dotenv import load_dotenv


load_dotenv()

def wrap_env_var(val: typing.Optional[str], default_val: str) -> str:
    """Wrap variable

    Args:
        val (typing.Optional[str]): variable value
        default_val (str): default value

    Returns:
        str: formatted value
    """
    if val is None:
        new_val = default_val
    else:
        new_val = val
    return new_val


TELEGRAM_BOT_TOKEN: str = wrap_env_var(os.getenv("TELEGRAM_BOT_TOKEN"), "")
OPENAI_API_KEY: str = wrap_env_var(os.getenv("OPENAI_API_KEY"), "")
GPT_VERSION: str = wrap_env_var(os.getenv("GPT_VERSION"), "gpt-4o")

MAX_TOKENS_DICT: dict[str, int] = {"gpt-4o": 4192}


MEMES_DIR: pathlib.Path = pathlib.Path(__file__).parent / "data" / "memes"