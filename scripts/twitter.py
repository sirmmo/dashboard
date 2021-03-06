"""
Access the latest status messages (the timeline) of a Twitter user
and save it to a database table. 

This cannot be simply done using an RSS or Atom feed, since Twitter 
is apparently phasing out these interfaces. And while a user timeline
RSS still works one needs to know the user ID to access it like this
for the user "okfn":

  http://twitter.com/statuses/user_timeline/okfn.rss
  http://twitter.com/statuses/user_timeline/16143105.rss
  
The tweepy package helps with finding that ID and much more.
"""

import logging

from common import make_activity
import tweepy


log = logging.getLogger(__name__)


def gather(database, source, config):
    # url should be like "http(s)://twitter.com/okfn" or simply "okfn"
    username = source.url[source.url.rfind('/') + 1:]
    user = tweepy.api.get_user(username)
    user_id = user.id
    user_realname = user.name
    statuses = tweepy.api.user_timeline(user_id, count=20)

    log.info("%s: %s" % (source.type, username))
    
    table = database['activity']
    for s in statuses:
        author = s.author.screen_name
        text = s.text
        dt = s.created_at
        url = "http://twitter.com/#!/%s/statuses/%d" % (username, s.id)
        data = {
            'author': user_realname,
            'title': text,
            'source_url': url,
            'description': text
            }
        data = make_activity(data, dt, source)
        table.writerow(data,
            unique_columns=['author', 'title', 'source_url'])

