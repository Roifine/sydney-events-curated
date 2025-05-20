#This files helps me learn how to scrape data from the web

#section 1 - How to get the web content (in HTML)

import requests

url = "https://whatson.cityofsydney.nsw.gov.au/?freeEvent=true"
response = requests.get(url)
html = response.text  # this is the HTML content


#print(html)


#section 2 - How to Parse the HTML - Get the info we need from it

from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')

# Think of soup as a nice Python object where you can now search elements like tags, classes, etc.

# for example: <h1 class="jsx-9e58d0d29c793919 event_header_info-title">Guitar/bass beginner &amp; intermediate group lessons</h1>










# <a title="Inner West Country Fest" class="event_tile-link" href="/events/inner-west-country-fest"><span class="jsx-ab8ddd651046bdf3 sr-only">Inner West Country Fest</span></a>


title_tag = soup.select_one('a.event_tile-link')
print(title_tag)

print(soup.prettify())


# title = soup.find('a', class_= "event_tile-link")
# print(title.text)         

# ticket_link = soup.find('a', title='event_tile-link')['href']
# print(ticket_link)
