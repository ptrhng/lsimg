import base64
from pathlib import Path
import itertools
import io
import mimetypes

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from PIL import UnidentifiedImageError


def encode(d: bytes, w: str, h: str) -> str:
    encoded = base64.standard_b64encode(d).decode()
    msg = f'\033]1337;File=width={w};height={h};preserveAspectRatio=1;inline=1:{encoded}\a'

    return msg


def is_image_file(fname: str) -> bool:
    file_type, _ = mimetypes.guess_type(fname)
    return file_type is not None and file_type.startswith('image/')


def run(path: Path):
    # TODO: os.get_terminal_size to find the size of terminal
    # and compute the number of columns
    num_cols = 8

    image_width = 200
    image_height = 200
    image_spacing = 10
    label_height = 20
    label_spacing = 1

    fpaths = []
    if path.is_dir():
        for fpath in path.iterdir():
            if fpath.is_file():
                fpaths.append(fpath)
    else:
        fpaths.append(path)

    fpaths = [v for v in fpaths if is_image_file(v.name)]
    background_color = ImageColor.getrgb('black')
    font = ImageFont.load_default(size=label_height - label_spacing * 2)

    for batch in itertools.batched(fpaths, num_cols):
        frame = Image.new('RGB', size=((image_width + image_spacing) * len(batch), image_height + label_height,), color=background_color)

        for i, fpath in enumerate(batch):
            fname = fpath.name

            try:
                with Image.open(fpath) as img:
                    background = Image.new('RGB', size=(image_width, image_height + label_height), color=background_color)
                    draw = ImageDraw.Draw(background)
                    _, _, x, _ = draw.textbbox((0, 0,), fname, font=font)
                    draw.text(((image_width - x) // 2, image_height + label_spacing,), fname, font=font)
                    img.thumbnail((image_width, image_height,))
                    background.paste(img, box=(0, 0))
            except UnidentifiedImageError:
                # TODO: log this error
                continue

            frame.paste(background, box=((image_width + image_spacing) * i, 0,))

        f = io.BytesIO()
        frame.save(f, format='png')
        f.seek(0)

        pct = 100 / num_cols * len(batch)
        msg = encode(f.read(), f'{pct}%', 'auto')
        print(msg)

