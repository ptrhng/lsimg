import os
import sys
from typing import Tuple

import click

from lsimg import version
from lsimg.app import App
from lsimg.app import Config


@click.command()
@click.argument("args", metavar="FILE", nargs=-1)
@click.version_option(version.__version__, "-v", "--version")
def main(args: Tuple[str]):
    """\"ls\" command for iamges"""
    if not args:
        args = (os.getcwd(),)

    app = App(Config(out=sys.stdout, errout=sys.stderr, env=os.environ.copy()))
    rc = app.run(args)
    sys.exit(rc)
