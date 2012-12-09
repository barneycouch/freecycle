from bs4 import BeautifulSoup
import urllib, itertools, re

#harvest different groups in London
def find_freecycle_group_urls(home_url):
	page = urllib.urlopen(home_url).read()
	soup = BeautifulSoup(page)
	#cut off first few and last link - these are signups etc so irrelevant
	groups = soup.find_all('a')[12:(len(soup.find_all('a'))-1)]
	#a tweaked function of that below
	def extract_name_url(listings):
		title = listings.string
		link = listings['href']
		return str(title), str(link)
	return dict(map(extract_name_url, groups))



def make_listings_from_groups_url(group_url):
	return str(group_url + "/posts/all")




#!!!!!pages contains invalid homepages, eg lambeth, brent
pages = map(make_listings_from_groups_url, find_freecycle_group_urls("http://www.freecycle.org/group/UK/London").values())


#this could help solve it?
def check_valid_group(url):
	try:
		if len(BeautifulSoup(urllib.urlopen(url).read()).find_all(text=re.compile("OFFER"))) != 0:
			print "This group is alright"
	except:
		pass		

print map(check_valid_group,pages)



#make a list of the adverts
def extract_listings(url):
	page = urllib.urlopen(url).read()
	soup = BeautifulSoup(page)
	return soup.find_all('tr')

#extract the "offered" posts, return the titles and urls
def extract_name_title_url(listings):
	if listings.find("img")['alt'] == "OFFER":
		title = listings.find("strong").find("a").string
		link = listings.find("strong").find("a")['href']
		return str(title), str(link)

#amalgamise the two functions
def extract_offers(www):
	listings = extract_listings(www)
	offers = map(extract_name_title_url, listings)
	return offers[2:]

#itertools.chain flattens a [[]] list, see http://stackoverflow.com/questions/716477/join-list-of-lists-in-python?lq=1
print list(itertools.chain(*map(extract_offers, pages)))