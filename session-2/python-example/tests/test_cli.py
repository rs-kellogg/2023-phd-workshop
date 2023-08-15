import os
import tempfile
from typer.testing import CliRunner
from openaihelper.cli import *
import pytest

runner = CliRunner()

dir_path = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.skip(reason="not working")
def test_cli(tmpdir):
    result = runner.invoke(
        app,
        ["count-tokens", "sample-100.csv", "config.yml", "--outdir", str(tmpdir)],
    )
    assert result.exit_code == 0
    assert result.stdout.count("processing file:") == 100
