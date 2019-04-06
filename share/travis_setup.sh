#!/bin/bash
set -evx

mkdir ~/.genixcore

# safety check
if [ ! -f ~/.genixcore/.genix.conf ]; then
  cp share/genix.conf.example ~/.genixcore/genix.conf
fi
