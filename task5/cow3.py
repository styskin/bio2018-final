#!/usr/bin/env python

import sys
import itertools

header = dict()

def get_index(name):
    global header
    return header[name]
    
def read_table(fname, delim = '\t'):
    data = []
    for line in file(fname):
        line = line.strip()
        ll = line.split(delim)
        if line.find("total") >= 0:
            global header
            for i in xrange(0, len(ll)):
                header[ll[i]] = i
        else:
            data.append(ll)
    return data

def read_population(cows, father, mother, f, m, ppairs):
    start = read_table('test3.txt')
    sex_index = get_index("sex")
    for c in start:
        cows[c[0]] = c
        if c[sex_index] == "male":
            father[c[0]] = c[0]
        else:
            mother[c[0]] = c[0]

    maxiter = 0
    for iterc in xrange(1, 50):
        try:
            pairs = read_table('cow_' + str(iterc), ' ')
            cur   = read_table('res_' + str(iterc) + ".txt")
            L = len(pairs)
            for i in xrange(0, L):
                curc = cur[i]
                curp = pairs[i]
                cows[curc[0]] = curc
                father[curc[0]] = father[curp[0]]
                f[curc[0]] = curp[0]
                mother[curc[0]] = mother[curp[1]]
                m[curc[0]] = curp[1]

                ppairs[(curp[0], curp[1])] = 1
            maxiter = iterc
        except:
            print sys.exc_info()[0]
            ""
    return maxiter


def bullrank(bull):
    if bull[get_index("sex")] == 'male':
        return float(bull[get_index("weight")])
    else:
        return -1

def cowrank(cow):
    if cow[get_index("sex")] == 'female':
        return float(cow[get_index("total milk production")])
    else:
        return -1

def get_top(cows, func, top_size):
    return list(map(lambda x: x[1], itertools.islice(sorted(map(lambda x: (-func(x), x), cows.itervalues())), top_size)))
    

def pair_rank(b, c, topg):
    return topg[b[0]] if b[0] in topg else 0. + topg[c[0]] if c[0] in topg else 0.
#    return float(b[get_index("weight")]) + float(c[get_index("total milk production")])
#    return 0 * float(b[get_index("weight")]) + 5 * float(c[get_index("milk production yearly")])


cows = dict()
father = dict()
mother = dict()
f = dict()
m = dict()
ppairs = dict()
maxiter = read_population(cows, father, mother, f, m, ppairs)


#print cows
#print father
#print mother

# Range best cows
cs = get_top(cows, cowrank, 50)

topg = dict()

ind = 1
for c in cs:
    #print f[c[0]], m[c[0]], c
    if f[c[0]] in topg:
        topg[f[c[0]]] += 1./(1 + ind)
    else:
        topg[f[c[0]]] = 1./(1 + ind)
    if m[c[0]] in topg:
        topg[m[c[0]]] += 1./(1 + ind)
    else:
        topg[m[c[0]]] = 1./(1 + ind)
    ind += 1

print topg

# Range best bulls
bs = get_top(cows, bullrank, 30)

# Create possible pairs and range them
# with group by cow

pairs = []
for i in xrange(0, len(cs)):
    for j in xrange(0, len(bs)):
        c = cs[i]
        b = bs[j]
        # check mother and father
        if (c[0] not in mother or b[0] not in mother or mother[c[0]] != mother[b[0]]) \
            and \
           (c[0] not in father or b[0] not in father or father[c[0]] != father[b[0]]) \
           :
#           and \
#           (b[0], c[0]) not in ppairs:
            pairs.append( (-pair_rank(b, c, topg), b[0], c[0]))

maxiter += 1
ccount = dict()
bcount = dict()
ind = 0
print len(pairs)
with open('cow_' + str(maxiter), 'w') as f:
    # with group by cow
    for p in sorted(pairs):
        if p[1] in bcount:
            bcount[p[1]] += 1
        else:
            bcount[p[1]] = 1
        if p[2] in ccount:
            ccount[p[2]] += 1
        else:
            ccount[p[2]] = 1

        if ccount[p[2]] <= 4:
            print >> f, p[1], p[2]
            ind += 1
            if ind >= 20:
                print "FULL"
                break

print "NOTHING"
