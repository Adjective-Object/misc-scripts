#!/usr/bin/env bash
mkdir -p out
X=$(cat out.log | grep 'url:' | sed 's/url: //')

for url in $X; do
    curl -k "$url" > "./out/`basename $url`";
done
