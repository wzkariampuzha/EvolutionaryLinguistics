#!/bin/bash

FOLDERS="amer_unigram_data brit_unigram_data"

for FOLDER in $FOLDERS
do
	echo "***** " $FOLDER " Preprocessing Start *****"
	DATA_DIR=C:\Users\wzkar\Documents\GitHub\EvolutionaryLinguistics\Ngrams\amer_unigram_data/$FOLDER/
	# Preprocess
	python preprocess.py $DATA_DIR
	echo "***** " $ENTITY " Preprocessing Done *****"
done