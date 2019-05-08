#!/bin/sh
cd ../../../pythonlibs/embeddings/etnlp/src/codes/
export PYTHONPATH="$PYTHONPATH:$PWD"
INPUT_FILES="../../../../../../data/etnlp/Tiny_fasttext_wiki_subword.vec;../../../../../../data/etnlp/Tiny_fasttext_wiki.vec;../../../../../../data/etnlp/Tiny_glove.840B.300d.vec;../../../../../../data/etnlp/Tiny_W2V_google_news.vec"
# python ./visualizer/visualizer_sbs.py  -input $INPUT_FILES -args visualizer
python3 ./visualizer/visualizer_sbs.py $INPUT_FILES
