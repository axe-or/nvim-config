#!/usr/bin/env sh

set -eu
echo 'Compacting'
tar czvf nvim-config.tgz init.lua pack
