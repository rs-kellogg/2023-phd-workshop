from pathlib import Path
from tqdm import tqdm
import pandas as pd
import openai
import time
import csv
import typer
import math
import tiktoken
import logging
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)


def chat_complete(text: str, model_name: str, prompt: str):
    try:
        return completion_with_backoff(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt + " " + text},
            ],
        )
    except openai.InvalidRequestError as e:
        return str(e)
    except openai.error.RateLimitError as e:
        return str(e)
    except Exception as e:
        return str(e)


def count_tokens(text: str, encoding_name: str):
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens
