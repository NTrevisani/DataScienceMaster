#!/bin/bash
# curl http://swcarpentry.github.io/shell-novice/data/data-shell.zip -o data-shell.zip
# unzip data-shell.zip
mkdir -p elements_by_atomic_number
#find data-shell -name *.xml
#elements=$(find data-shell -name *.xml)
#echo $elements
for element in $(find data-shell -name *.xml)
do
#echo $element | sed -e 's/data-shell\/data\/elements\// /' | sed -e 's/.xml/ /'
atomicNumber=$(cat $element | grep atomic-number | sed -e 's/<atomic-number>\(.*\)<\/atomic-number>/\1/')
echo $atomicNumber
elementName=$(cat $element | grep "<element name" | sed -e 's/<element name="\(.*\)"\/>/\1/' )
echo $elementName
done

