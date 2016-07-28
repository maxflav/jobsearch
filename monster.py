import urllib2
from pyquery import PyQuery
import json
import html

MONSTER_URL = "http://www.monster.com/jobs/search/?q=attorney&where=San-Francisco__2C-CA&rad=20&sort=rv.dt.di"

# TODO: Allow multiple different queries, e.g.
#   "employment+labor",
#   "labor+law",
#   "lawyer",
#   "attorney"

# returns a tuple (items, next_offset)
# items is a list where each item is a dictionary with title, description, link, date.
# next_offset is the next offset that should be sent for the next page of results.
# If next_offset is 0, there are no more results for this query.
def getItems(offset):
  url = MONSTER_URL
  if offset > 0:
    url += "&page="+str(offset)

  print ""
  print "---"
  print url
  print "---"
  print ""

  try:
    response = urllib2.urlopen(url).read()
  except urllib2.HTTPError:
    return ([], 0)

  pq = PyQuery(response)
  nodes = pq('script[type="application/ld+json"]')

  items = []
  for node in nodes:
    try:
      obj = json.loads(node.text)
    except:
      continue

    if not "title" in obj:
      continue

    title = obj["title"]
    description = obj["description"]
    link = obj["url"]
    date = obj["datePosted"]

    items.append({
      'title': title,
      'description': description,
      'link': link,
      'date': date,
    })

  if len(items) == 0:
    return ([], 0)

  if offset == 0:
    next_offset = 2
  else:
    next_offset = offset + 1
  return (items, next_offset)
