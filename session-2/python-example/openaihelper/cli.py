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
)
from typing import Dict
from openaihelper import functions as F


app = typer.Typer()


logging.basicConfig(filename="openai-helper.log", encoding="utf-8", level=logging.INFO)

# model_name = "gpt-3.5-turbo"
# encoding_name = "cl100k_base"
# max_token_len = 4097
# prompt = "Read through the newspaper text and identify the following: environmental movement organization (EMO) involved, action taken by EMO, target of the action, which of the following strategies is being used- verbal statements, political tactic, education/raising awareness, juridicial tactics, disruptive protests, lifestyle/culture tactics, direct environmental protection, nondisruptive protest, and affecting business-, whether it is collaborative or contentious action, and where the event/interaction is happening. Answer in the following format. EMO: ; action: ; target: ; strategy: ; collaborative/contentious: ; city: ; county: ; state: . If the article is an advertisement, editorial, or opinions, or if it reports multiple unrelated events or non-local, international ones, return NA and specify why. Newspaper text: "


@app.command()
def count_tokens(
    data_file_path: Path = typer.Argument(..., help="Data file path name"),
    config_file_path: Path = typer.Argument(..., help="Config file path name"),
    outdir: Path = typer.Option(Path("."), help="Output directory"),
):
    assert data_file_path.exists()
    assert config_file_path.exists()
    if not outdir.exists():
        outdir.mkdir(parents=True)

    config = F.config(config_file_path)
    encoding_name = config["encoding_name"]
    max_token_len = config["max_token_len"]

    df = pd.read_csv(data_file_path)
    assert "id" in df.columns
    assert "text" in df.columns
    texts = list(df["text"])

    out_df = df[["id"]].copy()
    counts = []
    for i in tqdm(range(len(texts))):
        counts.append(F.count_tokens(texts[i], encoding_name))
    out_df["count"] = counts
    out_df.to_csv(
        f"{outdir}/{data_file_path.stem}_counts.csv", 
        quoting=csv.QUOTE_ALL,
        index=False,
    )


@app.command()
def process(
    data_file: str,
    openai_api_key_file: str,
    outdir: str = ".",
):
    openai.api_key = Path(openai_api_key_file).read_text()
    df = pd.read_csv(data_file)
    indices = list(df.index)
    texts = list(df["text"])
    counts = list(df["count"])
    responses = []
    for i in tqdm(range(len(texts))):
        if counts[i] > max_token_len:
            responses.append("TOO_LONG")
        else:
            responses.append(
                str(F.chat_complete(texts[i], model_name=model_name, prompt=prompt))
            )
        logging.info(f"{indices[i]}: {responses[i]}")
    df["responses"] = responses
    df.to_csv(f"{outdir}/{data_file}_responses.csv", quoting=csv.QUOTE_ALL)


if __name__ == "__main__":
    app()
