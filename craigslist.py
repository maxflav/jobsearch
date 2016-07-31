import urllib2
from xml.etree import ElementTree
from pyquery import PyQuery
import string

CRAIG_URL = "http://sfbay.craigslist.org/search/lgl?sort=date&search_distance=20&postal=94109&format=rss"

printableChars = set(string.printable)
# Gets rid of non-ASCII characters, which etree can't deal with
def removeBadStuff(text):
  return filter(lambda x: x in printableChars, text)

# returns a tuple (items, next_offset)
# items is a list where each item is a dictionary with title, description, link, date.
# next_offset is the next offset that should be sent for the next page of results.
# If next_offset is 0, there are no more results for this query.
def getItems(offset):
  url = CRAIG_URL
  if offset > 0:
    url += "&s="+str(offset)

  print url
  
  response = urllib2.urlopen(url).read()
  response = removeBadStuff(response)
  tree = ElementTree.fromstring(response)

  nodes = tree.findall(".//{http://purl.org/rss/1.0/}item")

  if len(nodes) == 0:
    return ([], 0)

  items = []
  for node in nodes:
    title = node.find('{http://purl.org/rss/1.0/}title').text
    description = node.find('{http://purl.org/rss/1.0/}description').text
    link = node.find('{http://purl.org/rss/1.0/}link').text
    date = node.find('{http://purl.org/dc/elements/1.1/}date').text

    items.append({
      'title': title,
      'description': description,
      'link': link,
      'date': date,
    })

  return (items, len(items) + offset)