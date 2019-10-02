#!/bin/bash
URL=${1:-http://swcarpentry.github.io/shell-novice/data/data-shell.zip}
DOWNLOAD_NAME=${2:-data-shell.zip}
OUTPUT_FOLDER=${3:-elements_by_atomic_number}
# downloading the zip file
#curl http://swcarpentry.github.io/shell-novice/data/data-shell.zip -o data-shell.zip
curl $URL -o $DOWNLOAD_NAME
# unzipping
unzip data-shell.zip
# creating destination folder
#OUTPUT_FOLDER=elements_by_atomic_number
mkdir -p $OUTPUT_FOLDER
# counting how many xml files we have
initialFilesNumber=$(find data-shell -name *.xml | wc -l)
# loop over all the xml files to modify their names
for element in $(find data-shell -name *.xml)
do
# retreiving the atomic number
atomicNumber=$(cat $element | grep atomic-number | sed -e 's/<atomic-number>\(.*\)<\/atomic-number>/\1/')
# counting how many digits we have in the atomic number (to fill with 0 on the left if less than 3)
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
cp $element $OUTPUT_FOLDER/$newFileName
done
# removing unnecessary stuff
rm data-shell.zip
rm -r data-shell
# showing elements in the new folder
ls -1 elements_by_atomic_number
# counting how many xml files have been copied to the new folder
finalFilesNumber=$(ls -1 elements_by_atomic_number | wc -l)
echo ===========
if [ $finalFilesNumber -eq $initialFilesNumber ]; then
    echo All done!
else
    echo Something went wrong! :\'\(
fi
echo ===========
echo I am downloading the $URL url, unzipping it into the $DOWNLOAD_NAME folder, and copying the xml files, with the requested name, in $OUTPUT_FOLDER
echo ===========
echo You can change these settings by introducing different url, unzipping folder name, and output folder, when running this script, as:
echo bash elements.sh \<URL\> \<DOWNLOAD_NAME\> \<OUTPUT_FOLDER\>
echo e.g. 
echo bash elements.sh $URL $DOWNLOAD_NAME $OUTPUT_FOLDER
echo ===========
