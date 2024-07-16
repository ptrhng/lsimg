import os
import sys
from typing import Tuple

import click

from lsimg import core
from lsimg import version


@click.command()
@click.argument("args", metavar="FILE", nargs=-1)
@click.version_option(version.__version__)
def main(args: Tuple[str]):
    """\"ls\" command for iamges"""
    if not args:
        args = (os.getcwd(),)

    rc = core.run(args, sys.stdout, sys.stderr)
    sys.exit(rc)
