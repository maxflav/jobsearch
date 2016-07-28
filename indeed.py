import urllib2
from pyquery import PyQuery
import json
import html

INDEED_URL = "http://www.indeed.com/jobs?q=%28lawyer+or+attorney%29&l=San+Francisco%2C+CA&radius=20&sort=date"
LINK_BASE = "http://www.indeed.com"

# returns a tuple (items, next_offset)
# items is a list where each item is a dictionary with title, company, description, link, date.
# next_offset is the next offset that should be sent for the next page of results.
# If next_offset is 0, there are no more results for this query.
def getItems(offset):
  url = INDEED_URL
  if offset > 0:
    url += "&start="+str(offset)

  print ""
  print "---"
  print url
  print "---"
  print ""

  #try:
  #  response = urllib2.urlopen(url).read()
  #except urllib2.HTTPError:
  #  return ([], 0)

  response = open('indeed.html', 'r').read()
  pq = PyQuery(response)
  nodes = pq('.result.row')

  items = []
  for node in nodes.items():
    anchor_tag = node('a[itemprop="title"]')
    title = anchor_tag.text()
    link = LINK_BASE + anchor_tag.attr('href')
    company = node('span[itemprop="name"]').text()
    description = node('span[itemprop="description"]').text()
    date = node('span.date').text()

    print title
    print link
    print company
    print description
    print date

    print ""
  #  try:
  #    obj = json.loads(node.text)
  #  except:
  #    continue

  #  if not "title" in obj:
  #    continue

  #  title = obj["title"]
  #  description = obj["description"]
  #  link = obj["url"]
  #  date = obj["datePosted"]

  #  items.append({
  #    'title': title,
  #    'description': description,
  #    'link': link,
  #    'date': date,
  #  })

  #if len(items) == 0:
  #  return ([], 0)

  #if offset == 0:
  #  next_offset = 2
  #else:
  #  next_offset = offset + 1
  return (items, 0)
