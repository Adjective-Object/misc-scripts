import random, time, urllib, sys, threading, os, socket, signal, select
#self-modifying script to shitpost into the CSSU

# shitposting to CSSU office
baseurl = "http://www.merccoder.com/push.php?video=www.youtube.com/watch?v="

# line of this file the database starts at
thisfilename = "shitposting.py"

server_address = "./shitposting_socket_uds"
insertline = 13

shit = [
	"0ALG1YMG-0", # menu test
	"IyYnnUcgeMc", # bootylicious
	"mJl7U07c9As", # RIP in Peace Kim Jong Il
	"i9uGtQK9Qgs", # Ron Paul smokes weed every day
	# "9BuNdj5lyk0", # Pringles.jpg
	"MTk5XPzLa_U", # THe Maple Leaves have a 3 goal lead
	# "V2LxDGI2FRk" # dark and edgy spongebob
	# "sBh5nCxNteY", # 5'9" penismobile
	"yZKb_-MwM0w", # whale man
	"NLU9a4AS5eA", # More bagel bites
	"7QNfbjh3hog", # it's all suicide
	"bBQ68kPySQI", # ggggggggggggg
	"rWqhyg2G3HI", # les coucougnettes
	# "5sEfFCQoY3U", # corn malt liquor
	# "aSz8NOA3oGI", # Spongebob is #1 pussy eater
	"NF-XMtNEudQ", # Tim Allen Morrowind
	"b3_lVSrPB6w", # correct horse
	"p9zcfow3AcU", # r u tough
	# "CcnzvIM5XX0", # I love jesus
	"qn-aQ4qokDs", # Pillowy mounds of mashed potatoes
	# "sqn_z9PDUwM", # Porn Plot Twist
	"-CQrSsrctQc", # jimmy neutron butt
	"hGin0d0CK10", # American cheeto
	# "PWe4xi5jsQM", # harry_potter.wmv
	"6-E6N7sXoZI", # LoZ Menu Rap
	"M97VkS_YpOA", # Tomas da tankeng
	"Q3zwPX98HUw", # Dorito shell taco
	"0R-TKTsIU2w", # Those kids from gifs in animoo
	"sc6nByNHKXI", # Pro Meat Slicer
	"jdRCNM2k42o", # Gnawing on human bones
	"JbepN4dKLbU", # Pure vanilla sweetness, that's a 10
	"DqVonexxNBU", # Dog trumpet
	"OGbhJjXl9Rk", # garfeld
	"jgnG2wvykSE", # highly inappropriate technomasterbation
	"KHfMsTvtaCw", # Only 90's gamers
	"TVc4nS6_XY0", # Closing a window in win95
	"I2nLiVo74IQ", # JESUS
	"yKvgCELrXCo", # Garlic bread tribute
	"Zc-a-U2BJnM", # Rev up those friers
	"T-Wl4L2YJb0", # Say What
	"oUc0vbSlanM", # Black actors on friends (semi-alphabetical)
	"LZgeIReY04c", # NEVER ILLEGALLY DOWNLOAD
	"sRTdzGtu3yA" # Pringles
	"8ZCysBT5Kec", # Fix it Fry
	"lFQ4h-Im54E", # A Message to all Gas N' Fuel employees
	"Ae1AiFNKFBk", # Starwars reenactment by euro dudes
	"8Z5xb9GjCY0", # I love michael cera
	"PT6uH31wQeE", # Antikid
	"W9Eio5JmyPQ", # Italo Disco
	"VQFl_WLmNTU", # Castlevania x Old Spice
	"24Eh2-DZTgQ", # Bonkirumiku japanese scout-kun
	"ysg0WZ_XmSU", # Octagon collab
	"2C1iFVFktR4", # Octagon vs Masked Hexagon
	"R9Yd4Fyq1qo", # Gaben delayed the precious thing
	"dBqMxvqLQuw", # Nichismoke
	"o2TO5atI4rU", # Nichijoint
	"gm2E24jSAfI", # Jack Smokes Weed Every Day
	"8coX8VkUKY8", # Intensive Gaston Unit
	"xpKxtTPQ1Q8", # Most Brutal Metal Scream
	"y9K18CGEeiI", # DOG
	"Y9YAPBhk7yo", # JANTRAN SPOOKS
	"RuX-foAwPCk", # Waxvac is quiet
	"9C_HReR_McQ", # Don't hug me #1
	"vtkGtXtDlQA", # Don't hug me #2
	"rflvwYArWew", # Good advice from mario
	"gvdf5n-zI14", # nope.avi
	"TBsdWW7MOew", # you need me
	"xtXaKsd7jm4", # shinjii gratz
	"lgWgEoaAYDY" # smell yo dick
 ]


timerThread = None

def do_cleanup(signal, frame):
	print("cleaning threads")
	if (timerThread != None):
		timerThread.alive = False

	if(os.path.exists(server_address)):
		os.remove(server_address)
	sys.exit()

class TimerThread(threading.Thread):

	def run(self):
		posts = shit
		self.alive = True
		while(self.alive):
			s = random.choice(posts)
			posts.remove(s)

			if(len(shit) == 0):
				posts = shit

			print("\ntimer opening "+s)

			enqueue(s)

			#hackish, but python has no easy signaling to threads
			for i in range(int(24*60*60*(0.5+0.5*random.random()))):
				time.sleep(1)
				if(not self.alive):
					break
		print "timer thread closing"

def enqueue(shorturl):
	urllib.urlopen(baseurl+shorturl)


def selfcestmod(shorturl, comment):
	if(not shorturl in shit):
		f = open(thisfilename)
		lines = f.readlines()
		f.close()
		if comment != "":
			lines.insert(insertline, "	\"%s\", # %s\n"%(shorturl, comment))
		else:
			lines.insert(insertline, "	\"%s\",\n"%(shorturl))

		f=open(thisfilename,"w")
		f.write("".join(lines))
		f.close()

def modThroughServer(shorturl, comment):
		
	# Create a UDS socket
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	print 'connecting to %s' % server_address
	try:
		sock.connect(server_address)
	except socket.error, msg:
		print(msg)
		sys.exit(1)

	print shorturl, comment
	sock.send("%s\r\n%s\r\n"%(shorturl, comment))
	sock.close()
	print "sent"

if (__name__ == "__main__"):

	posts = shit

	#this is the server
	if (len(sys.argv) == 1 or "server" in sys.argv):
		if os.path.exists(server_address):
			print("socket already exists, assumed to be from previous instance")
			#print("exiting")
			#sys.exit()
			print("removing..")
			os.remove(server_address);
		
		#create the server
		servsock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

		servsock.bind(server_address)	
		servsock.listen(1)

		#establish signal handlers
		signal.signal(signal.SIGINT, do_cleanup)

		#not even remotely thread safe
		timerThread = TimerThread()
		timerThread.start()

		connections = {}

		selectbase = [servsock] 
		seletout = []

		try:

			while True:
				(rable, wable, eable) = select.select(selectbase, [], selectbase)

				for rsoc in rable:
					if rsoc == servsock:
						conn, cliaddr = servsock.accept()
						connections[conn] = {
								"socket":conn,
								"addr":cliaddr,
								"onmsg":True,
								"msgbuffr":"",
								"commentbuffr":""
								}
						selectbase.append(conn)

					else:
						if (connections[rsoc]["onmsg"]):
							connections[rsoc]["msgbuffr"] += rsoc.recv(2048)
							prev = ''
							for i in range(1,len(connections[rsoc]["msgbuffr"])):
								if connections[rsoc]["msgbuffr"][i-1:i+1] == "\r\n":
									if i< len(connections[rsoc]["msgbuffr"])-1:
										connections[rsoc]["commentbuffr"] = connections[rsoc]["msgbuffr"][i+1:]
									connections[rsoc]["msgbuffr"] = connections[rsoc]["msgbuffr"][0:i]
									connections[rsoc]["onmsg"] = False
									break
								prev = i
						else:
							connections[rsoc]["commentbuffr"] += rsoc.recv(2048)
							if(connections[rsoc]["commentbuffr"][-2:] == "\r\n"):
								complete = connections[rsoc]
								connections.pop(rsoc)
								selectbase.remove(rsoc)
								rsoc.close()

								selfcestmod(complete["msgbuffr"][0:-2], complete["commentbuffr"][0:-2])
								enqueue(complete["msgbuffr"])

				for esocket in eable:
					selectbase.remove(esocket)
		except socket.error, msg:
			print("ERROR", msg)
			do_cleanup(None, None)

	#This is the client
	else:
		if(len(sys.argv)>2):
			#get comment from args
			comment = reduce( lambda a,b: a+" "+b, sys.argv[2:])
		else:
			comment = ""

		#get yourube url shortform
		urllong = sys.argv[1]
		urlshort = ""
		active = False
		for i in range(1,len(urllong)):
			if active:
				if urllong[i] == '&':
					break
				else:
					urlshort += urllong[i]
			if(urllong[i-1:i+1] == 'v='):
				active = True
		
		if(urlshort == ""):
			urlshort = urllong

		modThroughServer(urlshort, comment)
