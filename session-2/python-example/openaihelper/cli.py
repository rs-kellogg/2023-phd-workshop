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


app = typer.Typer()
if __name__ == "__main__":
    app()


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
    ids = list(df["id"])

    # Count tokens and write results to csv file
    out_csv = open(f"{outdir}/{data_file_path.stem}_counts.csv", "a")
    writer = csv.writer(out_csv)
    writer.writerow(["id", "count"])
    for i in tqdm(range(len(texts))):
        n_tokens = F.count_tokens(texts[i], encoding_name)
        writer.writerow([ids[i], n_tokens])
        out_csv.flush()
        logging.info(f"Data point {ids[i]} has {n_tokens} tokens")
    out_csv.close()


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

    # Complete prompt and write results to csv file
    out_csv = open(f"{outdir}/{data_file_path.stem}_responses.csv", "a")
    writer = csv.writer(out_csv)
    writer.writerow(["id", "response"])
    for i in tqdm(range(len(texts))):
        n_tokens = F.count_tokens(texts[i], encoding_name)
        if (n_tokens + n_prompt_tokens) > max_token_len:
            writer.writerow([ids[i], "TOO_LONG"])
            logging.warn(f"Data point {ids[i]} not completed")
        else:
            response = str(
                F.chat_complete(texts[i], model_name=model_name, prompt=prompt)
            )
            writer.writerow([ids[i], response])
            valid = F.validate_result(response)
            if valid:
                logging.info(f"Data point {ids[i]} completed")
            else:
                logging.warn(f"Data point {ids[i]} not completed")
        out_csv.flush()
    out_csv.close()
