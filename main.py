import random
adjlist = dict()    # adjacency list
alias = dict()      # stores the reirect titles
nodeid = dict()     # hash of page titles to unique integer
nodename = dict()   # hash from unique integer to page title
allnodes = dict()   # list of all nodes
visits = dict()     # number of visits for pagerank
aliasfile = open('alias.txt', 'r')
edgefile = open('edges.txt', 'r')


def init():     # loads the graph into memory
    print('loading graph into memory')
    aliascount = 0
    while True:     # links pages that redirect to another page
        title = aliasfile.readline().strip()
        if title == '':
            break
        rdtitle = aliasfile.readline().strip()
        alias[title] = rdtitle      # hashing the redirect title
        aliascount += 1
        if aliascount % 10000 == 0:     # progress update
            print('alias count: ' + str(aliascount))
    print('loading edges...')
    cnt = 0
    last = 0
    while True:     # loads edges into memory
        u = edgefile.readline().strip()
        if u == '':
            break
        if alias.get(u) is not None:    # if page redirects to another page
            u = alias[u]
        if nodeid.get(u) is None:   # assigning unique id to page for performance
            nodeid[u] = last
            nodename[last] = u
            last += 1
        cnt += 1
        u = nodeid[u]
        if adjlist.get(u) is None:
            adjlist[u] = []
        v = edgefile.readline().strip()
        cnt += 1
        while '###' not in v:   # no more edges for current node
            if cnt % 100000 == 0:   # progress update
                print('Edges added: ' + str(cnt))
            if v == '':     # ignoring blank lines
                cnt += 1
                v = edgefile.readline().strip()
                continue
            if alias.get(v) is not None:    # if page redirects to another page
                v = alias[v]
            if nodeid.get(v) is None:    # assigning unique id to page for performance
                nodeid[v] = last
                nodename[last] = v
                last += 1
            v = nodeid[v]
            adjlist[u].append(v)    # adding edge to adjacency list
            v = edgefile.readline().strip()
            cnt += 1
    aliasfile.close()
    edgefile.close()
    global allnodes
    allnodes = [c for c, c1 in adjlist.items()]     # list of all nodes


def randomwalk(maxhops):    # runs a random walk of 'maxhops' steps
    hops = 0
    cur = random.choice(allnodes)   # starting node
    if visits.get(cur) is None:     # visit counter for page rank
        visits[cur] = 1
    else:
        visits[cur] += 1
    while hops < maxhops:
        if random.random() < 0.9:   # goes to a neighbour
            if adjlist.get(cur) is None or len(adjlist[cur]) == 0:
                cur = random.choice(allnodes)
            else:   # if cur has no children
                cur = random.choice(adjlist[cur])
        else:   # goes to a random node
            cur = random.choice(allnodes)
        if visits.get(cur) is None:     # counting visits
            visits[cur] = 1
        else:
            visits[cur] += 1
        hops += 1
        if hops % 1000000 == 0:     # progress tracker
            print(str(round((hops / maxhops * 100), 2)) + ' %')
    print('random walk completed')


def printlinks(ab):
    ab = ab.lower().strip()     # cleaning the input
    if alias.get(ab) is not None:   # if page redirects to another page
        ab = alias[ab]
    if adjlist.get(nodeid[ab]) is None:
        print('page not found')
        return
    for c in adjlist[nodeid[ab]]:       # prints all the links
        print(nodename[c])


def main():
    init()
    while True:
        print('''Menu:
        1 : Run a random walk of X hops
        2 : Print the top K pages
        3 : See all links of a particular page
        Q : Quit'''
        )
        ip = input()
        if ip == '1':
            print('Enter number of hops: ')
            maxhops = int(input())
            randomwalk(maxhops)
        elif ip == '2':
            print('Enter number of top pages to be displayed')
            k = int(input())
            for a, b in sorted(visits.items(), key=lambda vk: (vk[1], vk[0]), reverse=True)[0:k]:
                print(nodename[a])
        elif ip == '3':
            print('Enter page name to look for: ')
            printlinks(input())
        elif ip == 'Q':
            print('Exiting')
            break
        else:
            print('Invalid input')
main()
