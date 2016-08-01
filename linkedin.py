import urllib2
import json
import lxml
from pyquery import PyQuery

LINKEDIN_URL = "https://www.linkedin.com/jobs/search?keywords=attorney&distance=25.0&locationId=PLACES.us.7-1-0-38-1"

def stripHTML(text):
  return lxml.html.fromstring(text).text_content()

# returns a tuple (items, next_offset)
# items is a list where each item is a dictionary with title, description, link, date.
# next_offset is the next offset that should be sent for the next page of results.
# If next_offset is 0, there are no more results for this query.
def getItems(offset):
  url = LINKEDIN_URL
  if offset > 0:
    url += "&start="+str(offset)

  print url

  try:
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'br')
    response = urllib2.urlopen(request).read()
  except urllib2.HTTPError:
    return ([], 0)

  pq = PyQuery(response)
  script = pq("code#decoratedJobPostingsModule").html()

  # find the first { and last }. json blob is between those.
  blob = script[script.find("{"):-script[::-1].find("}")]
  obj = json.loads(blob)

  items = []
  elements = obj["elements"]
  for element in elements:
    posting = element["decoratedJobPosting"]

    company = posting["companyName"]
    description = stripHTML(posting["formattedDescription"])
    date = stripHTML(posting["formattedListDate"])
    title = posting["jobPosting"]["title"]
    link = element["viewJobCanonicalUrl"]

    items.append({
      'title': title,
      'description': company + '\n' + description,
      'link': link,
      'date': date,
    })

  if len(items) == 0:
    return ([], 0)

  return (items, offset + len(items))
