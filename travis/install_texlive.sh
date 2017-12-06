#!/usr/bin/env bash
set -e

export PATH=/tmp/texlive/bin/x86_64-linux:$PATH

# See if there is a cached version of TL available
if ! command -v latexmk > /dev/null 2>&1; then
  wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
  tar -xzf install-tl-unx.tar.gz
  cd install-tl-20*
  ./install-tl --profile=../texlive.profile
fi

# Keep no backups (smaller cache)
tlmgr option -- autobackup 0

# Update the TL install but add nothing new
tlmgr update --self --all --no-auto-install