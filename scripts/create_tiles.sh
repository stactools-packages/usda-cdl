#!/usr/bin/env sh

set -e

for file in tests/data-files/*.tif; do
    stac usda-cdl tile "$file" tests/data-files/tiles --size 500
done
