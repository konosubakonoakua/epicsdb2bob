import subprocess
import sys

import pytest

from epicsdb2bob import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "epicsdb2bob", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__


@pytest.mark.parametrize(
    "args",
    [
        [],
        ["input.db"],
        ["output/"],
    ],
)
def test_cli_missing_args(args: list[str]):
    cmd = [sys.executable, "-m", "epicsdb2bob"] + args
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)


# def test_cli_creates_bobfile(tmp_path, default_config):
#     cmd = [
#         sys.executable,
#         "-m",
#         "epicsdb2bob",
#         "tests/inputs/db_with_readbacks.db",
#         str(tmp_path),
#         "-r",
#         "_RBV",
#     ]
#     subprocess.check_output(cmd)
#     generated_bobfile = tmp_path / "db_with_readbacks.bob"
#     assert generated_bobfile.exists()
#     with open(generated_bobfile, "r") as f:
#         with open("tests/expected/db_with_readbacks.bob", "r") as ef:
#             assert f.read() == ef.read()
