import base64
from typing import Iterable


class ITerm2Encoder:
    def encode(self, d: bytes) -> Iterable[str]:
        """Encode image data in iTerm2 image format"""
        opts = {
            "preserveAspectRatio": 1,
            "inline": 1,
        }
        args = ";".join(f"{k}={opts[k]}" for k in sorted(opts.keys()))
        data = base64.standard_b64encode(d).decode()
        encoded = f"\033]1337;File={args}:{data}\a"

        yield encoded
