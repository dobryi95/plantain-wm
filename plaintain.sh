#!/usr/bin/env bash
set -e
nfc-mfclassic r a ./dumps/dumpIn.mfd ./dumps/dump0.mfd f
printf "Dump successfully downloaded. Enter amount: "
read amount
python3 ./dumpEdit.py -a ${amount}
nfc-mfclassic w b ./dumps/dumpOut.mfd ./dumps/dumpIn.mfd f
