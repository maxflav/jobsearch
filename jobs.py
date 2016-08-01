import craigslist, monster, indeed, linkedin
import re, sys

MUST_HAVE_ONE = [
  "\\battorneys?\\b",
  "\\bcounsels?\\b",
  "\\bemployment\\b",
  "\\bfirm\\b",
  "\\blabor\\b",
  "\\blaw\\b",
  "\\blawyers?\\b",
  "\\blegal\\b",
  "\\blitigation\\b",
  "\\blitigators?\\b",
  "\\blitigates?\\b",
  "\\bl ?\\W ?e\\b",    # "L & E", "L+E" etc.
]

def textContainsAny(text, words):
  for word in words:
    if re.search(word, text, re.IGNORECASE) != None:
      return True
  return False

sites_map = {
  "craigslist": craigslist,
  "c": craigslist,
  "monster": monster,
  "m": monster,
  "indeed": indeed,
  "i": indeed,
  "linkedin": linkedin,
  "l": linkedin,
}
if len(sys.argv) < 2 or sys.argv[1] not in sites_map:
  print "Usage:", sys.argv[0], "|".join(sorted(sites_map.keys())), "[starting offset] [max results]"
  exit(-1)

site = sys.argv[1]
module = sites_map[sys.argv[1]]


offset = 0
if len(sys.argv) > 2:
  offset = int(sys.argv[2])

max_results = -1
if len(sys.argv) > 3:
  max_results = int(sys.argv[3])

max_pages = -1
if len(sys.argv) > 4:
  max_pages = int(sys.argv[4])

filter_words = open('filter_words', 'r').read().splitlines()
ignore_links = open('ignore_links', 'r').read().splitlines()

num_results = 0
page = 0

while True:
  if max_results >= 0 and num_results > max_results:
    break

  page += 1
  if max_pages >= 0 and page > max_pages:
    break

  items, next_offset = module.getItems(offset)
  for item in items:
    text = (item['description'] + " " + item['title'])

    if not textContainsAny(text, MUST_HAVE_ONE):
      continue
    if textContainsAny(text, filter_words):
      continue
    if item['link'] in ignore_links:
      continue

    num_results += 1
    if max_results > 0 and num_results > max_results:
      break

    print ""
    print "*****"
    print item['title']
    print item['description']
    print item['link']
    print item['date']
    print "*****"
    print ""

  if next_offset == 0:
    break

  offset = next_offset