
let $d := fn:doc("board.xml")

let $shitposts :=
	for $thread in $d//div[
		@class="thread" 
		and fn:not(.//img[@alt="Sticky"])]
	return <thread>{$thread}</thread>

let $top := $shitposts[1]

let $text := ($top//blockquote)[1]

let $imgurl := ($top//a[@class="fileThumb"]/img/@src)[1]
let $link := ($top//span[contains(@class, "postNum")]/a/@href)[1]

let $t := 	fn:replace(
			fn:replace(
				fn:string-join(data($text), "\n"),
				"'", "'"),
				'"', '\\\\"')
let $titt := fn:string-join(($top//span[@class="subject"])[1]/text())
let $tit := fn:concat(fn:substring(fn:string-join($t), 0, 25), "...")
let $i := fn:concat("http:", $imgurl)
let $l := fn:concat("http://boards.4chan.org/$board/", $link)


let $title := if (string-length($titt)>0) then $titt else $tit
return fn:string-join(('payload={"text": "",
	"attachments": [{
		"title": "', $title, '",
		"author_name": "Anonymous $board",
		"author_icon": "http://www.faviconer.com/uploads/21/823/favicon.png",
		"author_link": "', $l, '",
		"title_link": "', $l, '",
		"fallback": "', $l, '",
		"text": "',$t, '",
		"image_url": "', $i, '"
	}]}'))

