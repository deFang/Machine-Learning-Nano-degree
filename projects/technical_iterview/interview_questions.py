from collections import Counter
## For Q1&Q2 run python -m doctest -v interview_questions.py to see test case results
def Q1(s,t):
    """Determinn whether some anagram of t is 
    a substring of s.

    >>> Q1('udacity','ad')
    True
    >>> Q1('daniel','nailed')
    True
    >>> Q1('python','hop')
    False
    """
    if len(t)>len(s) or t==None:
        return False
    t = Counter(t)
    for i in range(len(s)-len(t)+1):
        if Counter(s[i:len(t)+1]) == t:
            return True
    return False

def Q2 (a):
    """Return the longest palindromic substring of a

    >>> Q2('reviver')
    'reviver'
    >>> Q2('jonno')
    'onno'
    >>> Q2('')
    ''
    """
    if len(a)==0:
        return ''
    length = len(a)
    for i in range(length):
        for j in range(i+1):
            part = a[j:j+length-i+1]
            if part == part[::-1]:
                return part

    return None



def Q3 (G):
    MST = {}
    sortedE = sortedEdges(G)
    for i in range(len(sortedE)):
        a = sortedE[i][0]
        b = sortedE[i][1]
        val = sortedE[i][2]
        if a in MST and b in MST:
            continue
        elif a in MST:
            MST[a].append((b,val))
            MST[b] = [(a,val)]
        elif b in MST:
            MST[b].append((a,val))
            MST[a] = [(b,val)]
        else:
            MST[a] = [(b,val)]
            MST[b] = [(a,val)]
    return MST

def sortedEdges (G):
    alledge = []
    for v in G:
        edges = G[v]
        for edge in edges:
            v2, val = edge
            if v<v2:
                alledge.append((v,v2,val))
            else:
                alledge.append((v2,v,val))
                
    alledge = list(set(alledge))
    alledge = sorted(alledge, key = lambda x: x[2])
    return alledge

a = {'A': [('B', 2)],
    'B': [('A', 2), ('C', 5)], 
    'C': [('B', 5),('A',3)]}
print Q3(a)
print "expected output is: {'A': [('B', 2), ('C', 3)], 'B': [('A', 2)], 'C': [('A', 3)]}"

b = {'A': [('B',10),('C',20),('D',40)],
    'B':[('A',10)],
    'C':[('A',20)],
    'D':[('A',40),('E',10)]
    }
print Q3(b)
print "expected output is: {'A': [('B', 10), ('C', 20)], 'B': [('A', 10)], 'C': [('A', 20)], 'D': [('E', 10)], 'E': [('D', 10)]}"

c = {'A': [('B',10)],
    'B':[('A',10),('C',30),('C',40)],
    'C':[('B',40),('B',30),('D',10)],
    'D':[('C',10),('A',20)]
    }
print Q3(c)
print "expected output is: {'A': [('B', 10)], 'B': [('A', 10)], 'C': [('D', 10)], 'D': [('C', 10)]}"

## Q4 cannot understand the question.
## What does this sentence mean:" where T is the tree represented as a matrix, 
## where the index of the list is equal to the integer stored in that node 
## and a 1 represents a child node"?

class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None
    
def Q5(ll, m):
    length = 0
    pointer = ll
    item = ll
    while pointer != None:
        length += 1
        pointer = pointer.next
    loc = length-m
    
    for i in range(loc):
        item = item.next
    return item.data

a = Node('first')
b = Node('second')
c = Node('third')
a.next = b
b.next = c
print Q5(a,1)
print "expected output is 'third' "
