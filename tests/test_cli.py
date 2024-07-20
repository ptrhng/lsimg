from click.testing import CliRunner

from lsimg.cli import main
from lsimg.version import __version__


def test_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output

    result = runner.invoke(main, ["-v"])
    assert result.exit_code == 0
    assert __version__ in result.output
