#!/bin/bash
curl http://swcarpentry.github.io/shell-novice/data/data-shell.zip -o data-shell.zip
unzip data-shell.zip
outputFolder=elements_by_atomic_number
mkdir -p $outputFolder
for element in $(find data-shell -name *.xml)
do
atomicNumber=$(cat $element | grep atomic-number | sed -e 's/<atomic-number>\(.*\)<\/atomic-number>/\1/')
characterNumber=$(echo -n $atomicNumber | wc -c)
elementName=$(cat $element | grep "<element name" | sed -e 's/<element name="\(.*\)"\/>/\1/' )
if [ $characterNumber -eq 1 ]; then
    newAtomicNumber=$(echo $atomicNumber | sed -e 's/^/00/')
fi
if [ $characterNumber -eq 2 ]; then
    newAtomicNumber=$(echo $atomicNumber | sed -e 's/^/0/')
fi
if [ $characterNumber -eq 3 ]; then
    newAtomicNumber=$(echo $atomicNumber)
fi
newFileName=$newAtomicNumber\_$elementName.xml
cp $element $outputFolder/$newFileName
done
rm data-shell.zip
rm -r data-shell
ls -lrt elements_by_atomic_number
echo All done!