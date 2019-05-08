#!/bin/sh
cd ../../../pythonlibs/embeddings/etnlp/src/codes/
export PYTHONPATH="$PYTHONPATH:$PWD"
INPUT_FILES="../../../../../../data/etnlp/Ti_ft_wi_sub.vec;../../../../../../data/etnlp/Ti_ft_wi.vec;../../../../../../data/etnlp/Ti_gl.vec;../../../../../../data/etnlp/Ti_W2V.vec"
python3 ./etnlp_api.py  -input $INPUT_FILES -args visualizer -port 8891
