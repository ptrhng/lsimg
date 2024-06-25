import base64
import io
import itertools
import mimetypes
from pathlib import Path
from typing import Iterable

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import UnidentifiedImageError


def encode(d: bytes, w: str, h: str) -> str:
    encoded = base64.standard_b64encode(d).decode()
    msg = f"\033]1337;File=width={w};height={h};preserveAspectRatio=1;inline=1:{encoded}\a"

    return msg


def is_image_file(fname: str) -> bool:
    file_type, _ = mimetypes.guess_type(fname)
    return file_type is not None and file_type.startswith("image/")


def find_image_files(root: Path) -> Iterable[Path]:
    paths = [root]
    if root.is_dir():
        paths = list(root.iterdir())

    return [p for p in paths if is_image_file(p.name)]


def run(files: Iterable[Path]) -> Iterable[str]:
    # TODO: os.get_terminal_size to find the size of terminal
    # and compute the number of columns
    num_cols = 8

    image_width = 200
    image_height = 200
    image_spacing = 10
    label_height = 20
    font_size = 16

    background_color = ImageColor.getrgb("black")
    font = ImageFont.load_default(size=font_size)

    for batch in itertools.batched(files, num_cols):
        frame = Image.new(
            "RGB",
            size=(
                (image_width + image_spacing) * len(batch),
                image_height + label_height,
            ),
            color=background_color,
        )

        for i, file in enumerate(batch):
            fname = file.name
            background = Image.new(
                "RGB",
                size=(image_width, image_height + label_height),
                color=background_color,
            )
            draw = ImageDraw.Draw(background)
            _, _, x, y = draw.textbbox(
                (
                    0,
                    0,
                ),
                fname,
                font=font,
            )
            draw.text(
                (
                    (image_width - x) // 2,
                    image_height + (label_height - y),
                ),
                fname,
                font=font,
            )

            try:
                with Image.open(file) as img:
                    img.thumbnail(
                        (
                            image_width,
                            image_height,
                        )
                    )
                    background.paste(img, box=(0, 0))
            except UnidentifiedImageError:
                # TODO: log this error
                pass

            frame.paste(
                background,
                box=(
                    (image_width + image_spacing) * i,
                    0,
                ),
            )

        f = io.BytesIO()
        frame.save(f, format="png")
        f.seek(0)

        pct = 100 / num_cols * len(batch)
        yield encode(f.read(), f"{pct}%", "auto")
