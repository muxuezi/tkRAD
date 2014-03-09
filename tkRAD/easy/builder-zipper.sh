#!/bin/bash

cd $(dirname "$0")

XML="builder-example.xml"

B1="builder"
P1="pydoc3"
F1="$P1-$B1.html"
D1="builder-python3"

B2="builder2"
P2="pydoc"
F2="$P2-$B2.html"
D2="builder-python2"

#---

$P1 -w "$B1"
$P2 -w "$B2"

mv -fv "$B1.html" "$F1"
mv -fv "$B2.html" "$F2"

rm -v *.pyc

mkdir -pv "$D1" "$D2"

cp -v "$B1.py" "$D1/"
cp -v "$XML" "$D1/"
cp -v "$F1" "$D1/"
mv -fv "$F1" doc/
zip -r "$D1" "$D1"
rm -rfv "$D1"

cp -v "$B2.py" "$D2/"
cp -v "$XML" "$D2/"
cp -v "$F2" "$D2/"
mv -fv "$F2" doc/
zip -r "$D2" "$D2"
rm -rfv "$D2"

sleep 1

mv -fv *.zip ../

exit 0
