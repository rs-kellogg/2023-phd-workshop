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


def check_args(
    data_file_path: Path,
    config_file_path: Path,
    outdir: Path,
):
    assert data_file_path.exists()
    assert config_file_path.exists()
    if not outdir.exists():
        outdir.mkdir(parents=True)


@app.command()
def count_tokens(
    data_file_path: Path = typer.Argument(..., help="Data file path name"),
    config_file_path: Path = typer.Argument(..., help="Config file path name"),
    outdir: Path = typer.Option(Path("."), help="Output directory"),
):
    """
    Count tokens in a data file and write output to a csv file.
    """
    check_args(data_file_path, config_file_path, outdir)

    # Read config file
    config = F.config(config_file_path)
    encoding_name = config["encoding_name"]
    max_token_len = config["max_token_len"]

    # Read data file
    df = pd.read_csv(data_file_path)
    assert "id" in df.columns
    assert "text" in df.columns
    texts = list(df["text"])

    # Count tokens
    out_df = df[["id"]].copy()
    counts = []
    for i in tqdm(range(len(texts))):
        counts.append(F.count_tokens(texts[i], encoding_name))
    out_df["count"] = counts

    # Write output
    out_df.to_csv(
        f"{outdir}/{data_file_path.stem}_counts.csv", 
        quoting=csv.QUOTE_ALL,
        index=False,
    )


@app.command()
def complete_prompt(
    data_file_path: Path = typer.Argument(..., help="Data file path name"),
    config_file_path: Path = typer.Argument(..., help="Config file path name"),
    outdir: Path = typer.Option(Path("."), help="Output directory"),
):
    """
    Complete a prompt in a data file and write output to a csv file.
    """
    check_args(data_file_path, config_file_path, outdir)

    # Read config file and setup OpenAI
    config = F.config(config_file_path)
    api_key = Path(config["openai_api_key_file"]).read_text()
    encoding_name = config["encoding_name"]
    max_token_len = config["max_token_len"]
    model_name = config["model_name"]
    prompt = config["prompt"]
    n_prompt_tokens = F.count_tokens(prompt, encoding_name)
    openai.api_key = api_key

    # Read data file
    df = pd.read_csv(data_file_path)
    assert "id" in df.columns
    assert "text" in df.columns
    texts = list(df["text"])
    ids = list(df["id"])

    # Process texts
    out_df = df[["id"]].copy()
    responses = []
    for i in tqdm(range(len(ids))):
        n_tokens = F.count_tokens(texts[i], encoding_name)
        if (n_tokens + n_prompt_tokens) > max_token_len:
            responses.append("TOO_LONG")
        else:
            responses.append(
                str(F.chat_complete(texts[i], model_name=model_name, prompt=prompt))
            )
        logging.info(f"Data point {ids[i]} completed")
    out_df["response"] = responses

    # Write output
    out_df.to_csv(
        f"{outdir}/{data_file_path.stem}_response.csv", 
        quoting=csv.QUOTE_ALL,
        index=False,
    )


if __name__ == "__main__":
    app()
