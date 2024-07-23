#!/usr/bin/env bash

set -euo pipefail

# find the latest version
LSIMG_VERSION=$(git ls-remote \
	--tags \
	--sort '-v:refname' \
	https://github.com/ptrhng/lsimg.git |
	head -n1 |
	cut -d '/' -f 3)

pip install --upgrade "https://github.com/ptrhng/lsimg/archive/refs/tags/$LSIMG_VERSION.tar.gz"
