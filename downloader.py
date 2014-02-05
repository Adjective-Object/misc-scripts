import requests, sys, os
from xml.etree import ElementTree
from time import sleep

api_key = ""

def get_download_url(track_id):
	response_track = requests.get(
		"https://api.soundcloud.com/tracks/%s.format?consumer_key=%s" %(track_id, api_key)
	)
	tree = ElementTree.fromstring(response_track.text)
	return tree.iter("download-url").next().text+"?consumer_key=%s"%(api_key)

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
	if(track["dl"]):
		sys.stdout.write("Downloading \"%s\"%s "%(tempname, filler) )
		
		local_filename = track["title"]+".mp3"
		url = get_download_url(track["id"])

		#print track["id"]

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
		return f.name

	else:
		sys.stdout.write("Downloading \"%s\"%s DOWNLOADS DISABLED"%(tempname, filler) )

def fix_metadata(path, meta):
	pass

def main():
	username = None
	destination = "."
	if len(sys.argv) > 1:
		username = sys.argv[1]
		if(len(sys.argv) > 2):
			destination = sys.argv[2]
	else:
		username = raw_input("Username?: ")

	print("Getting tracklist for user \"%s\""%(username))
	tracklist = get_track_list(username)

	print("Discovered %s Tracks" % (len(tracklist)))


	if not os.path.exists(destination):
	    os.makedirs(destination)

	filepaths_and_meta = [ (download_track(track, folder=destination), track) for track in tracklist]

	for pair in filepaths_and_meta
		fix_metadata(pair[0], pair[1])

if __name__ == "__main__":
	main()