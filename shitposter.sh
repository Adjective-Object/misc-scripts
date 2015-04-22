#!/bin/bash

apply_shell_expansion() {
    declare file="$1"
    declare data=$(< "$file")
    declare delimiter="__apply_shell_expansion_delimiter__"
    declare command="cat <<$delimiter"$'\n'"$data"$'\n'"$delimiter"
    eval "$command"
}

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
api_hook='https://hooks.slack.com/services/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'

payload="${payload//\$board/$board}"

echo "$payload"

curl -X POST --data-urlencode "$payload" "$api_hook"
rm board.html
rm board.xml
