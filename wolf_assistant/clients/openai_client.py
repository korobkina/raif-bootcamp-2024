"""OpenAI Customized Client."""

import typing
from io import BytesIO
from loguru import logger

from openai import OpenAI, APIConnectionError
from openai.types.audio.transcription import Transcription
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_content_part_image_param import ChatCompletionContentPartImageParam, ImageURL
from openai.types.chat.chat_completion_content_part_text_param import ChatCompletionContentPartTextParam
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam
import tiktoken

from wolf_assistant.clients import prompts
from wolf_assistant.settings import GPT_VERSION, OPENAI_API_KEY, MAX_TOKENS_DICT


CLIENT: OpenAI = OpenAI(
    api_key=OPENAI_API_KEY,
)


def openapi_exception(func: typing.Callable) -> typing.Callable:
    """
    Decorator for exceptions
    Args:
        func: decorable function

    Returns: decorated function

    """

    def internal_func(*args, **kwargs):
        """
        Internal function
        Args:
            *args: args
            **kwargs: kwargs

        Returns: decorated function

        """
        try:
            return func(*args, **kwargs)
        except APIConnectionError as err:
            logger.error(err)
            return f"{str(err)} Please check `OPENAI_API_KEY` or VPN or Internet Connection"
       
    return internal_func


def format_message(response: ChatCompletion) -> str:
    """Format GPT response.

    Args:
        response (ChatCompletion): GPT response

    Returns:
        str: formatted message
    """
    text = response.choices[0].message.content
    if text is not None:
        message = text.strip()
    else:
        message = "None"
    return message


@openapi_exception
def generate_response(text: str) -> str:
    """Generate response from text.

    Args:
        text (str): text

    Returns:
        str: generated text
    """

    formatted_text: str
    if text:
        formatted_text = text
    else:
        formatted_text = "text"

    response = CLIENT.chat.completions.create(
        model=GPT_VERSION,
        messages=[
            ChatCompletionUserMessageParam(
                role="user", content=[ChatCompletionContentPartTextParam(type="text", text=formatted_text)]
            )
        ],
        max_tokens=1024,
        temperature=0.5,
    )
    message: str = format_message(response)
    return message


@openapi_exception
def generate_transcription(input_bytes: BytesIO) -> str:
    """Generate transcription.

    Args:
        audio_bytes (bytes): audio bytes

    Returns:
        str: generated text
    """
    transcription: Transcription = CLIENT.audio.transcriptions.create(
        model="whisper-1", file=("audio.oga", input_bytes, "audio/ogg")
    )
    return transcription.text.strip()


@openapi_exception
def generate_video_response(
    transcription: str, video_frames: list[bytes], max_tokens: int = 200, caption: typing.Optional[str] = None
) -> str:
    """Generate video response from text.

    Args:
        text (str): text

    Returns:
        str: generated text
    """

    text: str
    if caption:
        text = transcription
    else:
        text = "text"

    content_fragment: list[ChatCompletionContentPartTextParam] = [
        ChatCompletionContentPartTextParam(type="text", text=text)
    ]

    if caption:
        content_fragment.append(ChatCompletionContentPartTextParam(type="text", text=caption))

    # обработка видео openai
    response = CLIENT.chat.completions.create(
        model=GPT_VERSION,
        messages=[
            ChatCompletionUserMessageParam(
                role="user",
                content=[
                    *content_fragment,
                    *map(lambda x: {"image": x, "resize": 768}, video_frames[0::300]),  # type: ignore
                ],
            ),
        ],
        max_tokens=max_tokens,
    )

    message: str = format_message(response)
    return message


@openapi_exception
def generate_file_response(url: str, caption: typing.Optional[str] = None, max_tokens: int = 300) -> str:
    """Generate file response.

    Args:
        url (str): url
        caption (typing.Optional[str], optional): caption

    Returns:
        str: generated text
    """

    text: str
    if caption:
        text = caption
    else:
        text = "text"

    response = CLIENT.chat.completions.create(
        model=GPT_VERSION,
        messages=[
            ChatCompletionUserMessageParam(
                role="user",
                content=[
                    ChatCompletionContentPartTextParam(type="text", text=text),
                    ChatCompletionContentPartImageParam(type="image_url", image_url=ImageURL(url=url)),
                ],
            ),
        ],
        max_tokens=max_tokens,
    )
    message: str = format_message(response)
    return message


def prepare_prompt(input_text: str, input_format: typing.Literal["text", "image", "audio", "video"]) -> str:
    """Prepare prommpt

    Args:
        input_text (str): input text from chat bot
        input_format (typing.Literal["text", "image", "audio", "video"]): input format

    Returns:
        prompt for ChatGPT
    """
    if input_format == "text":
        prompt = "\n".join([prompts.CODE_DESC_TASK, prompts.TEXT_EXAMPLE, prompts.CODE_DESC_BODY.substitute(input_text=input_text)])
    else:
        logger.warning(f"Please develope prompt for {input_format}, input_text is used as prompt")
        prompt = input_text

    return prompt

def check_tokens_length(prompt: str) -> bool:
    """_summary_

    Args:
        prompt (str): _description_

    Returns:
        bool: _description_
    """
    encoding = tiktoken.encoding_for_model(GPT_VERSION)
    tokens = encoding.encode(prompt)
    max_tokens_length = MAX_TOKENS_DICT.get(GPT_VERSION, 4096)
    logger.debug(f"Number of tokens: {len(tokens)}, Max tokens: {max_tokens_length}")
    return len(tokens) < max_tokens_length
