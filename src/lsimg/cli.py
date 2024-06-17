import os
from pathlib import Path
from typing import Tuple

import click

from lsimg import core
from lsimg import version

@click.command()
@click.argument(
    'files',
    metavar='FILE',
    nargs=-1)
@click.version_option(version.__version__)
def main(files: Tuple[str]):
    """\"ls\" command for iamges"""
    # TODO: handle multiple file arguments
    path = Path(files[0]) if files else Path(os.getcwd())
    out = core.run(path)

    click.echo(out)
