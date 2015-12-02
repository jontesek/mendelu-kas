from bs4 import BeautifulSoup

# Given html
html_doc = """
<span style="font-family:Arial">T</span><span style="font-family:Arial">h</span><span style="font-family:Arial">e</span><span style="font-family:Arial">r</span><span style="font-family:Arial">e</span><span style="font-family:Arial"> </span><span style="font-family:Times">a</span><span style="font-family:Arial">r</span><span style="font-family:Times">e</span><span style="font-family:Arial"> </span><span style="font-family:Arial">8</span><span style="font-family:Arial"> </span><span style="font-family:Arial">t</span><span style="font-family:Arial">a</span><span style="font-family:Arial">s</span><span style="font-family:Arial">k</span><span style="font-family:Times">s</span><span style="font-family:Times"> </span><span style="font-family:Arial">f</span><span style="font-family:Arial">o</span><span style="font-family:Times">r</span><span style="font-family:Arial"> </span><span style="font-family:Arial">t</span><span style="font-family:Times">h</span><span style="font-family:Arial">i</span><span style="font-family:Times">s</span><span style="font-family:Arial"> </span><span style="font-family:Arial">w</span><span style="font-family:Times">o</span><span style="font-family:Times">r</span><span style="font-family:Times">k</span><span style="font-family:Arial">s</span><span style="font-family:Arial">h</span><span style="font-family:Arial">o</span><span style="font-family:Arial">p</span><span style="font-family:Arial">.</span><span style="font-family:Times"> </span><span style="font-family:Arial">T</span><span style="font-family:Arial">r</span><span style="font-family:Arial">y</span><span style="font-family:Arial"> </span><span style="font-family:Times">t</span><span style="font-family:Times">o</span><span style="font-family:Arial"> </span><span style="font-family:Arial">c</span><span style="font-family:Arial">o</span><span style="font-family:Arial">m</span><span style="font-family:Times">p</span><span style="font-family:Times">l</span><span style="font-family:Arial">e</span>te
"""

# Create a soup Find all spans
soup = BeautifulSoup(html_doc, 'html.parser')
# Find all spans
spans = soup.find_all('span');
print ''.join([x.contents[0] for x in spans])
# Process spans
msg_letters = [];
print len(spans)
for span in spans:
    if span.get('style').strip() == 'font-family:Arial':
        msg_letters.append('A')
    else:
        msg_letters.append('B')
# Print letters
print ''.join(msg_letters)
# Then use http://www.whaddayaknowabout.com/baconiancipher/ to decipher it: alanturing

