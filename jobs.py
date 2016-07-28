import craigslist, monster, indeed
import re

MUST_HAVE_ONE = [
  "\\battorneys?\\b",
  "\\bemployment\\b",
  "\\bfirm\\b",
  "\\blabor\\b",
  "\\blaw\\b",
  "\\blegal\\b",
  "\\blitigation\\b",
  "\\blitigators?\\b",
  "\\blitigates?\\b",
  "\\bcounsels?\\b",
]

# search queries:
# for craigslist, empty string ""
# for monster, try:
#   "employment+labor",
#   "labor+law",
#   "lawyer",
#   "attorney"

def textContainsAny(text, words):
  for word in words:
    if re.search(word, text, re.IGNORECASE) != None:
      return True
  return False

filter_words = open('filter_words', 'r').read().splitlines()
ignore_links = open('ignore_links', 'r').read().splitlines()

offset = 0
while True:
  items, next_offset = indeed.getItems(offset)
  for item in items:
    text = (item['description'] + item['title'])

    if not textContainsAny(text, MUST_HAVE_ONE):
      continue
    if textContainsAny(text, filter_words):
      continue
    if item['link'] in ignore_links:
      continue

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