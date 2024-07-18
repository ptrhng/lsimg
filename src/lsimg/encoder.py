import base64
from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Iterable


class Encoder(ABC):
    @abstractmethod
    def encode(self, d: bytes) -> Iterable[str]:
        raise NotImplementedError


class ITerm2Encoder(Encoder):
    def encode(self, d: bytes) -> Iterable[str]:
        """Encode image data in iTerm2 image format.

        For more details about iTerm2 image protocol, see
        https://iterm2.com/documentation-images.html
        """
        opts = {
            "preserveAspectRatio": 1,
            "inline": 1,
        }
        args = ";".join(f"{k}={opts[k]}" for k in sorted(opts.keys()))
        data = base64.standard_b64encode(d).decode()
        encoded = f"\033]1337;File={args}:{data}\a"

        yield encoded


class KittyEncoder(Encoder):
    def encode(self, d: bytes) -> Iterable[str]:
        """Encode image data in Kitty image format.

        For more details about Kitty image protocol, see
        https://sw.kovidgoyal.net/kitty/graphics-protocol/
        """
        limit = 4096
        data = base64.standard_b64encode(d)

        is_first_chunk = True
        while data:
            opts: Dict[str, str | int] = {"m": 1}
            if is_first_chunk:
                opts["a"] = "T"
                opts["f"] = 100
                is_first_chunk = False

            chunk, data = data[:limit], data[limit:]
            if not data:
                opts["m"] = 0

            args = ",".join(f"{k}={opts[k]}" for k in sorted(opts.keys()))
            encoded = f"\033_G{args};{chunk.decode()}\033\\"
            yield encoded


def get_graphics_encoder(env: Dict[str, str]) -> Encoder | None:
    """Return image encoder suitable for user's terminal."""
    term = env.get("TERM", "").lower()
    if "kitty" in term:
        return KittyEncoder()

    term_program = env.get("TERM_PROGRAM", "").lower()
    if "iterm" in term_program:
        return ITerm2Encoder()

    return None
