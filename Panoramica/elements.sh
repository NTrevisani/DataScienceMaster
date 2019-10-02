#!/bin/bash
# downloading the zip file
curl http://swcarpentry.github.io/shell-novice/data/data-shell.zip -o data-shell.zip
# unzipping
unzip data-shell.zip
# creating destination folder
outputFolder=elements_by_atomic_number
mkdir -p $outputFolder
# counting how many xml files we have
initialFilesNumber=$(find data-shell -name *.xml | wc -l)
# loop over all the xml files to modify their names
for element in $(find data-shell -name *.xml)
do
# retreiving the atomic number
atomicNumber=$(cat $element | grep atomic-number | sed -e 's/<atomic-number>\(.*\)<\/atomic-number>/\1/')
# counting how many digits in the atomic number (to fill with 0 if less than 3)
characterNumber=$(echo -n $atomicNumber | wc -c)
# retreiving the element name
elementName=$(cat $element | grep "<element name" | sed -e 's/<element name="\(.*\)"\/>/\1/' )
# now making all the atomic number have 3 digits
if [ $characterNumber -eq 1 ]; then
    newAtomicNumber=$(echo $atomicNumber | sed -e 's/^/00/')
fi
if [ $characterNumber -eq 2 ]; then
    newAtomicNumber=$(echo $atomicNumber | sed -e 's/^/0/')
fi
if [ $characterNumber -eq 3 ]; then
    newAtomicNumber=$(echo $atomicNumber)
fi
# creating the new file name
newFileName=$newAtomicNumber\_$elementName.xml
# copying the file in the new folder with the new name
cp $element $outputFolder/$newFileName
done
# removing unnecessary stuff
rm data-shell.zip
rm -r data-shell
# showing elements in the new folder
ls -1 elements_by_atomic_number
# counting how many xml files have been copied to the new folder
finalFilesNumber=$(ls -1 elements_by_atomic_number | wc -l)
if [ $finalFilesNumber -eq $initialFilesNumber ]; then
    echo All done!
else
    echo Something went wrong! :\'\(
fi