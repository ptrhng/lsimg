import os
from pathlib import Path
from typing import Tuple

import click

from lsimg import core
from lsimg import version


@click.command()
@click.argument(
    'args',
    metavar='FILE',
    nargs=-1)
@click.version_option(version.__version__)
def main(args: Tuple[str]):
    """\"ls\" command for iamges"""
    if not args:
        args = (os.getcwd(),)

    for arg in args:
        click.secho(f'{arg}:', fg='white')
        fpaths = sorted(core.find_image_files(Path(arg)))
        out = core.run(fpaths)
        click.echo(out)
