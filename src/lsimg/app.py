import itertools
import os
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Dict
from typing import Iterable
from typing import TextIO

from lsimg.core import ImageRow
from lsimg.core import find_best_fit
from lsimg.core import find_image_files
from lsimg.core import get_terminal_size
from lsimg.encoder import get_graphics_encoder


@dataclass
class Config:
    """App configuration."""

    out: TextIO
    errout: TextIO
    env: Dict[str, str] = field(repr=False)

    box_width: int = 200
    box_height: int = 220
    padding: int = 5


class App:
    def __init__(self, config: Config):
        self.config = config

    def write(self, s: str):
        self.config.out.write(s)
        self.config.out.flush()

    def write_line(self, s: str | None = None):
        if s is not None:
            self.config.out.write(s)
        self.config.out.write(os.linesep)
        self.config.out.flush()

    def write_error_line(self, s: str):
        self.config.errout.write(f"ERROR: {s}")
        self.config.errout.write(os.linesep)

    def run(self, args: Iterable[str]) -> int:
        """Render images found in paths specified.

        Returns:
            rc (int): exit status code.
        """
        encoder = get_graphics_encoder(self.config.env)
        if encoder is None:
            self.write_error_line("no suitable terminal graphics protocol found")
            return 1

        try:
            terminal_width, _ = get_terminal_size(self.config.out.fileno())
        except OSError as e:
            self.write_error_line(f"unable to obtain terminal window size: {e}")
            return 1

        num_cols, box_width, box_height = find_best_fit(
            self.config.box_width, self.config.box_height, terminal_width
        )

        for arg in args:
            self.write_line(f"{arg}:")
            files = sorted(find_image_files(Path(arg)))
            for chunk in itertools.batched(files, num_cols):
                row = ImageRow(
                    box_width, box_height, self.config.padding, bg_color="black"
                )
                for file in chunk:
                    row.add(file)

                for data in encoder.encode(row.to_bytes()):
                    self.write(data)
                self.write_line()

        return 0
