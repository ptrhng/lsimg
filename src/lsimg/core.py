import array
import fcntl
import io
import mimetypes
import termios
from pathlib import Path
from typing import Iterable
from typing import List
from typing import Tuple

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import UnidentifiedImageError


def is_image_file(fname: str) -> bool:
    """Return True if an image file."""
    file_type, _ = mimetypes.guess_type(fname)
    return file_type is not None and file_type.startswith("image/")


def find_image_files(root: Path) -> Iterable[Path]:
    """Return all immediate image files found in the path."""
    paths = [root]
    if root.is_dir():
        paths = list(root.iterdir())

    return [p for p in paths if is_image_file(p.name)]


def get_terminal_size(fd: int) -> Tuple[int, int]:
    """Return the size of the terminal window as (width, height) in pixels.

    Raises:
        OSError: if ioctl() call fails
    """
    buf = array.array("H", [0, 0, 0, 0])
    fcntl.ioctl(fd, termios.TIOCGWINSZ, buf)
    return buf[2], buf[3]


def find_best_fit(
    box_width: int, box_height: int, terminal_width: int
) -> Tuple[int, int, int]:
    """Find the best dimensions for the image fitting into terminal window.

    Returns:
        A tuple containing number of columns, adjusted box width and height.
    """
    num_cols = terminal_width // box_width
    adj = (terminal_width - num_cols * box_width) // num_cols
    box_width += adj
    box_height += adj
    return num_cols, box_width, box_height


class ImageRow:
    """ImageRow represents a row containing image thumbnails."""

    def __init__(self, box_width: int, box_height: int, padding: int, bg_color: str):
        self.box_width = box_width
        self.box_height = box_height
        self.padding = padding
        self.image_width = box_width - padding * 2
        self.image_height = self.image_width
        self.label_height = box_height - self.image_height
        self.bg_color = ImageColor.getrgb(bg_color)
        self.font = ImageFont.load_default(size=16)
        self.files: List[Path] = []

    def add(self, file: Path):
        """Add image file to a row."""
        self.files.append(file)

    def to_image(self) -> Image.Image:
        """Combine all image files into a single image.

        For an image file that cannot be opend and identified, only label text (along with blank
        box) is displayed.
        """
        row_width = self.box_width * len(self.files)
        row_height = self.box_height
        row = Image.new("RGB", size=(row_width, row_height), color=self.bg_color)

        for i, file in enumerate(self.files):
            try:
                with Image.open(file) as img:
                    img.thumbnail(size=(self.image_width, self.image_height))
                    img_x = (self.box_width - img.width) // 2 + self.box_width * i
                    img_y = (self.box_width - img.height) // 2
                    row.paste(img, box=(img_x, img_y))
            except UnidentifiedImageError:
                # TODO: log this error
                pass

            draw = ImageDraw.Draw(row)
            text_x = self.box_width * i + self.image_width / 2
            text_y = self.box_height - self.label_height + self.label_height / 2
            draw.text(xy=(text_x, text_y), text=file.name, font=self.font, anchor="mm")

        return row

    def to_bytes(self, format: str = "png") -> bytes:
        """Return row image as bytes."""
        img = self.to_image()
        f = io.BytesIO()
        img.save(f, format=format)
        f.seek(0)

        return f.read()
