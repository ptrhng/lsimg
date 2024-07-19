from lsimg import encoder


class TestITerm2Encoder:
    def test_encode(self):
        enc = encoder.ITerm2Encoder()
        data = list(enc.encode(b"lsimg"))

        assert data == ["\033]1337;File=inline=1;preserveAspectRatio=1:bHNpbWc=\a"]


class TestKittyEncoder:
    def test_encode(self):
        enc = encoder.KittyEncoder()
        data = list(enc.encode(b"lsimg"))

        assert data == ["\033_Ga=T,f=100,m=0;bHNpbWc=\033\\"]


def test_get_graphics_encoder_iterm():
    enc = encoder.get_graphics_encoder(
        {
            "TERM_PROGRAM": "iTerm.app",
            "TERM": "xterm-256color",
        }
    )
    assert isinstance(enc, encoder.ITerm2Encoder)


def test_get_graphics_encoder_kitty():
    enc = encoder.get_graphics_encoder(
        {
            "TERM_PROGRAM": "iTerm.app",
            "TERM": "xterm-kitty",
        }
    )
    assert isinstance(enc, encoder.KittyEncoder)


def test_get_graphics_encoder_unsupported():
    enc = encoder.get_graphics_encoder(
        {
            "TERM_PROGRAM": "Apple_Terminal",
            "TERM": "xterm-256color",
        }
    )
    assert enc is None
