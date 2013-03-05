import urllib2
import feedparser

def get_unread_msgs(user, passwd):
	auth_handler = urllib2.HTTPBasicAuthHandler()
	auth_handler.add_password(
		realm='New mail feed',
		uri='https://mail.google.com',
		user='%s@gmail.com' % user,
		passwd=passwd
	)
	opener = urllib2.build_opener(auth_handler)
	urllib2.install_opener(opener)
	feed = urllib2.urlopen('https://mail.google.com/mail/feed/atom')
	return feed.read()

feed = get_unread_msgs('user','password')
atom = feedparser.parse(feed)

print len(atom.entries)
print atom.feed.title.encode('utf-8')

for i in xrange(len(atom.entries)):
	print atom.entries[i].title.encode('utf-8'), atom.entries[i].author.encode('utf-8')
