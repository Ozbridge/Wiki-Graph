import xml.etree.ElementTree as ET
import re
import bz2


def parser(xmlInput):   # extracts pageid, title and text
    myroot = ET.fromstring(xmlInput)
    pageid, title, text = '', '', ''
    for x in myroot:
        if x.tag == 'revision':         # inside tag revision
            for y in x:
                if y.tag == 'text':     # inside tag text
                    text = y.text
                    break;
        elif x.tag == 'id':             # inside tag id
            pageid = x.text
        elif x.tag == 'title':          # inside tag title
            title = x.text
    return pageid, title.strip().lower(), text


def parserRedirect(xmlInput):   # extracts redirect title if it exists
    myroot = ET.fromstring(xmlInput)
    title, redtitle = '', '#####'
    for x in myroot:    # traversing xml tree
        if x.tag == 'redirect':         # in tag redirect
            for y, z in x.attrib.items():
                if y == 'title':        # in attribute title
                    redtitle = z
                    break
        elif x.tag == 'title':          # in tag title
            title = x.text
    return title.strip().lower(), redtitle.strip().lower()


def getLinksList(text):     # extracts wikilink references from text
    if text is None:
        return []
    ret = re.findall("\[\[[^\[\]\{\}:\\\/]+]]", text)    # matches [[pagename]], pagename does not contain ':', '\', '/'
    actret = []     # list to return
    for i in range(len(ret)):
        temp = ''
        for ch in ret[i]:
            if ch in ['|', ',', '#']:   # ignoring text after these because page title is complete
                break
            if ch != '[' and ch != ']':     # ignoring [[]]
                temp += ch
        temp = temp.lower().replace('\n', ' ')      # cleaning up the link
        temp = ' '.join(temp.split())
        if temp != '':
            actret.append(temp)
    return actret


alias = dict()      # stores redirect titles
aliasfile = open('alias.txt', 'w')      # wrties output here
fd = bz2.open('./data/enwiki-latest-pages-articles.xml.bz2', 'r')
startpoint = 0
while '<page>' not in fd.readline().decode():
    startpoint += 1
fd.close()
fd = bz2.open('./data/enwiki-latest-pages-articles.xml.bz2', 'r')
for i in range(startpoint):      # skips to where the dump starts
    fd.readline()
edgefile = open('edges.txt', 'w')
cnt = 0
aliascount = 0
lines = 0
pagenumber = dict()
while True:     # adds all edges to edges.txt
    xml = ''
    line = fd.readline().decode()
    if '<page>' not in line:    # end of file reached
        break
    while '</page>' not in line :       # closing tag of page
        xml += line.strip()+'\n'
        line = fd.readline().decode()
    xml += line.strip()+'\n'
    pageid, title, text = parser(xml)
    title, rdtitle = parserRedirect(xml)  # processing xml of the current page
    if re.fullmatch("[^\[\]\{\}:\\\/]+", title) is None:     # check if current page is valid
        continue

    links = getLinksList(text)  # get all links of the page
    edgefile.write(title+'\n')  # write the current page once
    lines += 1
    for link in links:  # write all children
        edgefile.write(link+'\n')
        lines += 1
    edgefile.write('###\n')     # current node done
    lines += 1

    if title != '' and rdtitle != '' and rdtitle != '#####':  # page redirects to another page
        aliascount += 1
        alias[title] = rdtitle
        aliasfile.write(title + '\n' + rdtitle + '\n')      # write to alias.txt
    if cnt % 10000 == 0:    # progress update
        print(cnt, lines, aliascount)
    cnt += 1
fd.close()
edgefile.close()
print('execution complete')
