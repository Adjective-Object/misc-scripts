import requests, sys, os
from xml.etree import ElementTree
from time import sleep
import urllib
import mutagen, mutagen.easyid3, mutagen.id3


api_key = ""


def get_track_info(track_id):
	response_track = requests.get(
		"https://api.soundcloud.com/tracks/%s.format?consumer_key=%s" %(track_id, api_key)
	)
	tree = ElementTree.fromstring(response_track.text)
	meta = {}

	meta["download-url"] = tree.find("download-url").text+"?consumer_key=%s"%(api_key)
	meta["format"] = tree.find("original-format").text

	meta["username"] = tree.find("user").find("username").text
	meta["title"] = tree.find("title").text
	meta["description"] = tree.find("description").text

	if tree.find("artwork-url") != None:
		meta["artwork-url"] = tree.find("artwork-url").text.replace("-large.jpg","-t500x500.jpg")
	return meta

def get_track_list(username, verbose=True):
	response_user = requests.get(
		"https://api.soundcloud.com/users.format?consumer_key=apigee&q=%s" %(username)
	)
	tree = ElementTree.fromstring(response_user.text)
	uid = tree.iter("id").next().text
	if(verbose):
		print("user id is %s"%(uid))
		print("getting tracks...")
	response_tracks = 	response_tracks = requests.get(
		"https://api.soundcloud.com/users/%s/tracks.format?consumer_key=apigee"%(uid)
	)
	tree = ElementTree.fromstring(response_tracks.text)
	track_elements = tree.iter("track")

	return [ {
					"title":elem.find("title").text,
					"id":elem.find("id").text,
					"dl":(elem.find("downloadable").text == "true"),
			} for elem in track_elements]


def download_track(track, folder=".", tries=0):
	tempname =  track["title"] if len(track["title"])<20 else track["title"][0:17]+"...";
	filler = (20-len(track["title"]))*" "
	sys.stdout.write("\n")
	
	#print track["id"]
	
	if(track["dl"]):
		sys.stdout.write("Downloading \"%s\"%s "%(tempname, filler) )
		sys.stdout.flush()

		meta = get_track_info(track["id"])
		local_filename = track["title"]+"."+meta["format"]
		url = meta["download-url"]

		#actual file download
		f = file(
			(folder[0:-1] if folder[-1] == "/" else folder) + "/" + local_filename, "wb")
		r = requests.get(url, stream=True) #Stream download file
		total_length = r.headers.get('content-length')

		if total_length is None: # no content length header
			f.write(response.content)
		else:
			printed = 0
			dl = 0
			total_length = int(total_length)
			for chunk in r.iter_content(chunk_size=1024):
				dl += len(chunk)
				f.write(chunk)
				done = int(20 * (1.0 * dl / total_length))
				sys.stdout.write("#"*(done-printed))
				sys.stdout.flush()
				printed = done

		f.close()
		if r.status_code != 200:
			if r.status_code == 401:
				sys.stdout.write("PERMISSION DENIED")
				return None
			elif r.status_code == 504 & tries<3:
				sys.stdout.write("TIMEOUT, Trying again")
				return download_track(track, folder, tries+1)
			elif r.status_code == 504 & tries>=3:
				sys.stdout.write("TIMEOUT, I give up on this file")
				return None
			else:
				sys.stdout.write("HTTP ERROR %s"%(r.status_code))
				return None
		else:
			fix_metadata(f.name, meta)
		return f.name

	else:
		sys.stdout.write("Downloading \"%s\"%s DOWNLOADS DISABLED"%(tempname, filler) )


def fix_metadata(path, meta, artwork=True):
	#sys.stdout.write("\nfixing metadata for %s 		"%(path,) )
	#sys.stdout.flush()
	f = None

	try:
		f = mutagen.File(path, easy=True)
	except:
		print "can't operate on file %s metadata - mutagen, why?"%(path,)

	if f is not None:

		f["title"]=meta["title"]
		f["artist"]=meta["username"]
		f["comment"]=meta["description"]

		#only know how to do MP3 artwork
		if(artwork and ("artwork-url" in meta) and meta["format"]=="mp3"):
			f.save()
			f = mutagen.File(path)
			f.tags.add(mutagen.id3.APIC(
			        encoding=3, # 3 is for utf-8
			        mime='image/'+("png" if meta["artwork-url"].split(".")[-1].split("?")[0] == "png" else "jpeg"), # image/jpeg or image/png
			        type=3, # 3 is for the cover image
			        desc=u'Cover',
			        data=urllib.urlopen(meta['artwork-url']).read()
			    ))

		f.save()
	#sys.stdout.write("...done\n");
	#sys.stdout.flush()

def main():
	username = None
	destination = "."
	if len(sys.argv) > 1:
		username = sys.argv[1]
		if(len(sys.argv) > 2):
			destination = sys.argv[2]
		else:
			destination = "./"+sys.argv[1]
	else:
		username = raw_input("Username?: ")

	print("Getting tracklist for user \"%s\""%(username))
	tracklist = get_track_list(username)

	print("Discovered %s Tracks" % (len(tracklist)))


	if not os.path.exists(destination):
	    os.makedirs(destination)

	filepaths_and_meta = [download_track(track,destination) for track in tracklist]


if __name__ == "__main__":

	mutagen.easyid3.EasyID3.RegisterTextKey("comment","COMM")
	main()