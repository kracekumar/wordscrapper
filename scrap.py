#! /usr/bin/env python
"""
    Program to get all gre words and their meaning form http://www.gredics.com.

    Program Flow
    ------------
    http://www.gredic.com/index_a.html =>contains list of all words starting 
    with a.

    Eg. abacus, abandon.

    Then http://www.gredic.com/{word}
    http://www.gredic.com/abacus will have meaning for the word abacus.

    <h2 id="word">{word } /h2>
    ...
    <li id="barron"> meaning of the word from barron will be here </li>

    First fetch list of all words for an alphabet and build the url like
    http://www.gredisc.com/{word} and fetch the page using requests.
    Parse the page using Beautifulsoup and use findAll('tag') to find list
    of all tags in the page and do the check .

    More explanation is coming in each function.
"""
from BeautifulSoup import BeautifulSoup
import requests 
URL = "http://www.gredic.com/"

def build_starting_point():
    """ Builds the base url to fetch list of words alphabetically """
    return ( URL + "index_" + chr(no) + ".html" for no in xrange(97, 123) )

def scrap_the_words():
    """
       All the words in the particular alphabet is scraped here.
    """
    indexes = build_starting_point()
    for index in indexes:
        print ("Fetching words from", index)
        html_content = requests.get(index)
        content = BeautifulSoup(html_content.content)
        contents = content.findAll("a")
        """
        Example for alphabet y:

        [<a href="/">
                            GREdic<span id="title-dotcom">.com</span><br />
         <span class="hidden">-</span>
         <span id="subtitle">The Ultimate GRE Word List &amp; Dictionary</span>
         </a>,
         <a href="/" title="GREdic.com Home">home</a>,
         <a href="/hotlist.html" title="GREdic.com Hot List">hot list</a>,
         <a href="/references.html" title="GREdic.com References">references</a>,
         <a href="http://astore.amazon.com/gredic-20" title="GREdic.com Amazon Store">store</a>,
         <a href="/about.html" title="About GREdic.com">about</a>,
         <a href="mailto:webmaster@gredic.com" title="Contact">contact</a>,
         <a href="yarn">yarn</a>,
         <a href="yen">yen</a>,
         <a href="yeoman">yeoman</a>,
         <a href="yield">yield</a>,
         <a href="yoke">yoke</a>,
         <a href="yokel">yokel</a>,
         <a href="yore">yore</a>,
         <a href="/" title="GREdic.com Home">home</a>,
         <a href="/hotlist.html" title="GREdic.com Hot List">hot list</a>,
         <a href="/references.html" title="GREdic.com References">references</a>,
         <a href="http://astore.amazon.com/gredic-20" title="GREdic.com Amazon 
         Store">store</a>,
         <a href="/about.html" title="About GREdic.com">about</a>,
         <a href="mailto:webmaster@gredic.com" title="Contact">contact</a>,
         <a href="http://validator.w3.org/check?uri=referer">
         <img src="http://www.w3.org/Icons/valid-xhtml10-blue" 
         alt="Valid XHTML 1.0 Transitional" height="31" width="88" /></a>]

        All the words appears as a link in the page we need find only the words.
        Should elliminate items starting with '/', 'http', 'mailto'
        """
        words = [item.contents[0] for item in contents \
                      if not item['href'].startswith(("/",'http', 'mailto'))]
        yield words

def fetch_word_meaning():
    file_name = "words.txt"
    words = scrap_the_words()
    word_s = words.next()#generator 
    for word in word_s:
        print word
        link = URL + word 
        print(link)
        page_content = requests.get(link)
        content = BeautifulSoup(page_content.content)
        """ 
            content = requests.get("http://www.gredic.com/abacus")
            c = BeautifulSoup.BeautifulSoup(content.content)
            meanings = c.findAll('li')
            [<li id="taisha">an instrument for performing calculations by 
             sliding counters along rods or in grooves 
             <span class="referencelink">[Taisha]</span></li>,
             <li id="oleg">frame with balls for calculating 
             <span class="referencelink">[Smirnov]</span></li>]

             Here we need to get the content of the li tag
            >>> for meaning in meanings:
                 if meaning['id'] == 'taisha' or meaning['id'] == 'barron':
                     print meaning.contents[0]
                     
            an instrument for performing calculations by sliding counters along rods or in grooves 
        """
        meanings = content.findAll('li')
        print_to_file = word + ": " 
        for meaning in meanings:
            if meaning['id'] == 'taisha' or meaning['id'] == 'barron':
                for m in meaning.contents:
                    m = unicode(m)
                    if not m.startswith('<'):
                        print m
                        print_to_file += m
                        print_to_file += "\n"
            print(print_to_file,)
            with open(file_name, "a") as f:
                f.writelines(print_to_file)
            print("is written to file")

if __name__ == "__main__":
    fetch_word_meaning()
