#!/bin/sh
cd ../../../pythonlibs/embeddings/etnlp/src/codes/
export PYTHONPATH="$PYTHONPATH:$PWD"
INPUT_FILES="../../../../../../data/etnlp/Tiny_fasttext_wiki_subword.vec;../../../../../../data/etnlp/Tiny_fasttext_wiki.vec;../../../../../../data/etnlp/Tiny_glove.840B.300d.vec;../../../../../../data/etnlp/Tiny_W2V_google_news.vec"
python3 ./etnlp_api.py  -input $INPUT_FILES -args visualizer -port 8891
