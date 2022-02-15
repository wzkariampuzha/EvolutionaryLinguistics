#!/bin/bash
# Downloads the Google unigrams dataset
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

set -e

# Configure download location
DOWNLOAD_PATH="$UNIGRAMS_DATA"
if [ "$UNIGRAMS_DATA" == "" ]; then
    echo "UNIGRAMS_DATA not set; downloading to default path ('data')."
    DOWNLOAD_PATH="./unigram_data"
fi
DOWNLOAD_PATH_TAR="$DOWNLOAD_PATH.tar.gz"

# Download dataset
for in 
do
	wget
done
   
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1cGqvAm9IZ_86C4Mj7Zf-w9CFilYVDl8j' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1cGqvAm9IZ_86C4Mj7Zf-w9CFilYVDl8j" -O "$DOWNLOAD_PATH_TAR" && rm -rf /tmp/cookies.txt
tar -xvzf "$DOWNLOAD_PATH_TAR"
rm "$DOWNLOAD_PATH_TAR"

echo "BioBERT dataset download done!"