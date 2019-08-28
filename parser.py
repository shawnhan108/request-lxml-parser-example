from html.parser import HTMLParser

import lxml.html
import requests


class MyHTMLParser(HTMLParser):
    """
    Parse a block of HTML code and returns every url in the structure of <a href='example.url'></a>
    """

    def handle_starttag(self, tag, attrs):
        # Only accepts 'anchor' <a> tag.
        if tag == "a":
            for name, value in attrs:
                # If href is a defined attribute, extract it and append it at the end of list.
                if name == "href":
                    url_list.append(value)


# Initialize local storage and require input
url_list = []
string_input = input('Enter the html code here:')

# Reformat html code to a proper string using lxml.html
html = lxml.html.fromstring('''%s''' % (string_input))
html_string = str(lxml.html.tostring(html))

# Initialize parser and parse the string -> populates/returns a global list of urls (url_list).
parser = MyHTMLParser()
parser.feed(html_string)

# Second section: parse each page from the url list.
# Writing scraped data (question + answer) to a .txt file
f = open("AWS_Questions.txt", "w+")
for i in range(1, len(url_list)):
    url = url_list[i]

    # Obtain page html source code
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)

    # extracts the text in a <div> that has classname "entry-content" (all the question choices)
    #                   or a <p> that has classname "rightAnswer"
    data = tree.xpath(
        '//div[@class="entry-content"]/p/text() | //div[@class="entry-content"]/p[@class="rightAnswer"]/font/text()')
    answer = tree.xpath('//div[@class="entry-content"]/p[@class="rightAnswer"]/font/text()')

    # write data to file
    f.write(str(i + 1) + '.')
    for i in range(len(data)):
        if (data[i] != '\t\t\t\n\t\t\t'): # To handle undesired scraped data
            f.write(data[i])
    f.write("Answer:")
    for i in range(len(answer)):
        f.write(answer[i])
    f.write('\n')
f.close()
