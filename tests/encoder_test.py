from lsimg.encoder import ITerm2Encoder


class TestITerm2Encoder:
    def test_encode(self):
        encoder = ITerm2Encoder()
        data = list(encoder.encode(b"lsimg"))

        assert data == ["\033]1337;File=inline=1;preserveAspectRatio=1:bHNpbWc=\a"]
