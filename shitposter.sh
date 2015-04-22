#!/bin/bash

boards=(a c w m cgl c f n jp vp v vg vr co g tv k o an tg sp asp sci int out\
toy biz i po p ck ic wg mu fa 3 gd diy wsg trv fit x lit adv lgbt mlp b r r9k\
pol soc s4s s hc hm h e u d y t hr gif)
if [ "$#" -gt 0 ];
then
	board="$1"
else 
	board=${boards[RANDOM % ${#boards[@]}]}
fi

echo $board $1

wget -O board.html "http://boards.4chan.org/$board/"
xmllint --html --xmlout board.html 2>/dev/null > board.xml

payload=$(xqilla shitposter.xq)

payload="${payload//\$board/$board}"

curl -X POST --data-urlencode "$payload" "$SLACK_SHITPOST_HOOK"
rm board.html
rm board.xml
