from ReddiWrap import ReddiWrap
from re import match
from time import sleep, time
from getpass import getpass
import smtplib
import datetime

def main():
    #get startup info
    
    while True:
        try:
            Guser = raw_input("Gmail username :")
            Gpass = getpass("Gmail password :")
            print("connecting to smtp.gmail.com")
            myCellEmail = raw_input("SMS email address?")
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.ehlo()
            mail.login(Guser,Gpass)
            mail.quit()
            break
        except smtplib.SMTPConnectError:
            print("cannot connect to smtp.gmail.com:587")
        except smtplib.SMTPAuthenticationError:
            print("cannot authenticate. doublecheck the Username/password")
    
    
    subreddit = raw_input("monitor reddit.com/r/")
    
    #Logging posts on the subreddit
    recordedPosts=[] 
    reddit = ReddiWrap()
    
    startPosts = reddit.get("/r/%s/new" % subreddit )
    for post in startPosts:
        recordedPosts.append(post.id)
    
    #the main check loop, refreshes once per second
    while(True):
        newPosts=reddit.get("/r/%s" % subreddit+"/new/?count=0")
        mailToSend = []
        for post in newPosts:
            if (not post.id in recordedPosts):
                mailToSend.append(post)
                recordedPosts.append(post.id)
        if (len(mailToSend)>0):
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.ehlo()
            mail.login(Guser,Gpass)
            for newpost in mailToSend:
                seconds = (datetime.datetime.now()-datetime.datetime.fromtimestamp(newpost.created-7*60*60)).seconds
                print("(Posted %s:%s minutes ago): \"%s\"" %( seconds/60, (seconds%60/10==0)*"0"+str(seconds%60) , newpost.title) )
                mail.sendmail("RedditMonitor indev", [myCellEmail], newpost.title+"\r\n"+newpost.selftext*post.is_self+newpost.url*(not newpost.is_self))
            mail.quit()
        
        sleep(1)

main()
