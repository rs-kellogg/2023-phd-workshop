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

app = typer.Typer()


logging.basicConfig(filename='openai-response.log', encoding='utf-8', level=logging.INFO)
model_name = "gpt-3.5-turbo"
encoding_name = "cl100k_base"
max_token_len = 4097
prompt = "Read through the newspaper text and identify the following: environmental movement organization (EMO) involved, action taken by EMO, target of the action, which of the following strategies is being used- verbal statements, political tactic, education/raising awareness, juridicial tactics, disruptive protests, lifestyle/culture tactics, direct environmental protection, nondisruptive protest, and affecting business-, whether it is collaborative or contentious action, and where the event/interaction is happening. Answer in the following format. EMO: ; action: ; target: ; strategy: ; collaborative/contentious: ; city: ; county: ; state: . If the article is an advertisement, editorial, or opinions, or if it reports multiple unrelated events or non-local, international ones, return NA and specify why. Newspaper text: "


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def chat_complete(text: str):
    try:
        return completion_with_backoff(
          model=model_name,
          messages=[
                {"role": "user", "content": prompt + " " + text},
            ]
        )
    except openai.InvalidRequestError as e:
        return str(e)
    except openai.error.RateLimitError as e:
        return str(e)
    except Exception as e:
        return str(e)

def _count_tokens(text: str):
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens

@app.command()
def count_tokens(
    filename: str, 
    outdir: str = ".",
):
    df = pd.read_csv(filename)
    texts = list(df['text'])
    counts = []
    for i in tqdm(range(len(texts))):
        counts.append(_count_tokens(texts[i]))
    df['count'] = counts
    df.to_csv(
        f"{outdir}/{filename}_counts.csv",
        quoting=csv.QUOTE_ALL
    )


@app.command()
def process(
    openai_api_key: str,
    filename: str, 
    outdir: str = ".",
    ):
    
    openai.api_key = openai_api_key 
    df = pd.read_csv(filename)
    indices = list(df.index)
    texts = list(df['text'])
    counts = list(df['count'])
    responses = []
    for i in tqdm(range(len(texts))):
        if counts[i] > max_token_len:
            responses.append("TOO_LONG")
        else:
            responses.append(str(chat_complete(texts[i]))
        logging.info(f"{indices[i]}: {responses[i]}
    df['responses'] = responses
    df.to_csv(
        f"{outdir}/{filename}_responses.csv",
        quoting=csv.QUOTE_ALL
    )


if __name__ == "__main__":
    app()
