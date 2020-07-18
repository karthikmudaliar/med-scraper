#requests library to get the HTML content of the website
import requests 
#urllib library to parse the URL links
from urllib.parse import urlparse, urljoin
#HTMLParser library is used to parse the HTML content scraped using requests
from html.parser import HTMLParser

internal_urls = set()
hrefs = []

#since all anchor tags are not valid, this function will make sure that proper scheme and domain name exists in the URL.
def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

#handle_starttag parses the HTML content to take anchor tag data. hrefs is a list that contains all the URLs in it. 
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag != 'a':
            return
        attr = dict(attrs)
        href = attr["href"]
        hrefs.append(href)

#This function returns all URLs that is found on `url` in which it belongs to the same website
def get_all_website_links(url):
    # all URLs of `url
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc

    html = requests.get(url)
    parser = MyHTMLParser()
    parser.feed(html.text)
    
    for href in hrefs:

        if href == "" or href is None:
            # href empty tag
            continue
        #Since not all links are absolute join the URL if it's relative
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            continue

        urls.add(href)
        internal_urls.add(href)
        
        #file that stores all the internal links 
        f = open("links.txt", "a")
        f.write(href+'\n')
        f.close()
        
    return urls

# number of urls visited so far will be stored here
total_urls_visited = 0

#this function gets all the links of the first page and then call itself recursively to follow all the links extracted previously.
def crawl(url, max_urls=50):

    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)
        
if __name__ == "__main__":
    crawl("https://www.medium.com")
       
    

