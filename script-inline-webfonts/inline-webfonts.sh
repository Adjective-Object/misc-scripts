#!/usr/bin/env bash

stylesheet=$(curl -s $1)
files=$( echo $stylesheet| grep 'url' | grep -o 'http[^)]*')

for filename in $files; do
  format="${filename##*.}"

  # encode font and strip newlines
  encodedFont=$(curl -s $filename | base64 | sed s/\n//g)
  encodedFont=$(echo -n $encodedFont)

  # replace original url with data-encoded one
  encodedUrl="'data:application/x-font-$format;charset=utf-8;base64\,$encodedFont'";
  stylesheet=$(echo "$stylesheet" | sed "s,$filename,$encodedUrl,1")
done

# echo replaced stylesheet
echo "$stylesheet"

