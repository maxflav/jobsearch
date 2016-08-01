import urllib2
from pyquery import PyQuery

INDEED_URL = "http://www.indeed.com/jobs?q=%28lawyer+or+attorney%29&l=San+Francisco%2C+CA&radius=20&sort=date"

# indeed links work by finding the job key
LINK_BASE = "http://www.indeed.com/viewjob?jk="

# job keys might end up being repeated from one page to the next. filter duplicates out.
seen_job_keys = set()

# returns a tuple (items, next_offset)
# items is a list where each item is a dictionary with title, company, description, link, date.
# next_offset is the next offset that should be sent for the next page of results.
# If next_offset is 0, there are no more results for this query.
def getItems(offset):
  url = INDEED_URL
  if offset > 0:
    url += "&start="+str(offset)

  print url

  try:
   response = urllib2.urlopen(url).read()
  except urllib2.HTTPError:
   return ([], 0)

  pq = PyQuery(response)
  nodes = pq('.result.row')

  items = []
  for node in nodes.items():
    anchor_tag = node('a[data-tn-element="jobTitle"]')
    title = anchor_tag.text()
    job_key = node.attr('data-jk')

    if job_key in seen_job_keys:
      continue
    seen_job_keys.add(job_key)

    link = LINK_BASE + job_key
    company = node('span.company').text()
    description = node('span.summary').text()
    date = node('span.date').text()
    
    items.append({
      'title': title,
      'description': company + '\n' + description,
      'link': link,
      'date': date,
    })

  if len(items) == 0:
    return ([], 0)

  # indeed seems to add 10 to the 'start' param every time, even if there weren't exactly 10 listings in this page
  return (items, offset + 10)
