lsimg
=====

lsimg is "ls" command for images, displaying images in a directory.

![lsimg in action](./demo.gif)


### Installation

```bash
# To install the latest version
$ LSIMG_VERSION=$(git ls-remote \
--tags \
--sort '-v:refname' \
https://github.com/ptrhng/lsimg.git \
| head -n1 \
| cut -d '/' -f 3)
$ pip install https://github.com/ptrhng/lsimg/archive/refs/tags/$LSIMG_VERSION.tar.gz

# To install the latest unreleased code
$ pip install https://github.com/ptrhng/lsimg/archive/refs/heads/main.zip
```
