import os
import sys
from io import StringIO

from lsimg.app import App
from lsimg.app import Config


class TestApp:
    def test_run_get_terminal_size_error(self):
        config = Config(
            out=sys.stdin,
            errout=StringIO(),
            env={"TERM_PROGRAM": "iTerm.app"},
        )
        app = App(config)
        rc = app.run([])

        config.errout.seek(0)

        assert rc == 1
        assert config.errout.read().startswith(
            "ERROR: unable to obtain terminal window size"
        )

    def test_run_no_graphical_protocol_error(self):
        _, fd = os.openpty()
        with open(fd, "r") as out:
            config = Config(
                out=out,
                errout=StringIO(),
                env={"TERM": "", "TERM_PROGRAM": ""},
            )
            app = App(config)
            rc = app.run([])

        config.errout.seek(0)

        assert rc == 1
        assert config.errout.read().startswith(
            "ERROR: no suitable terminal graphics protocol found"
        )
