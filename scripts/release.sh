#!/usr/bin/env bash

set -eou pipefail

RELEASE_VERSION=$(git-cliff --bumped-version)

poetry version $RELEASE_VERSION
git-cliff --bump -o CHANGELOG.md
git add CHANGELOG.md pyproject.toml
git commit -m "release: $RELEASE_VERSION"
git tag $RELEASE_VERSION
