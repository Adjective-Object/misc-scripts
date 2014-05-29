Shitposting.py
==============

A self-modifying script made to shitpost videos periodically to the CSSU monitor.

Can be run as either server or client. The server will push a video from the list every 45 minutes (+/- 10 minutes), to second precision.

Client causes the server to immediately push the video, and puts it on the list

There are some pretty terrible hacks to get around Python's lack of Thread signaling. May rewrite in C to give myself a headache later, though that would require either recompiling the applicaion from source for each additional file or 

PLS
