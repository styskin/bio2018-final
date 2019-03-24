#!/usr/bin/env python

slices = []

for line in file("test6.fasta"):
    line = line.strip()
    if line[0] == '>':
        name = line[1:]
    else:
        slices.append((name, line))


common = dict()
M = 15
L = len(slices)
for i in xrange(0, L):
    s = slices[i][1]
    for j in xrange(0, len(s) / M):
        cc = s[j * M: j * M + M]
        if cc in common:
            common[cc] += 1
        else:
            common[cc] = 1
            
sr = list(sorted(map(lambda x: (-x[1], x[0]), common.iteritems())))

clasters = []
for i in xrange(0, L):
    clasters.append([])

for i in xrange(0, 50):
    for j in xrange(0, L):
        s = slices[j][1]
        if s.find(sr[i][1]) >= 0:
            clasters[j].append(i)

max_claster_id = 0

clasterization = [0] * L

# clasterize vectors
for i in xrange(0, L):
    for j in xrange(i+1, L):
        sa = set(clasters[i])
        ss = sa.intersection(set(clasters[j]))
        #print len(ss), " of ", len(clasters[i]), ", ", len(clasters[j])
        if 4 * len(ss) > len(clasters[i]) + len(clasters[j]) and len(ss) > 2:
            # in the same claster
            if clasterization[i] > 0 or clasterization[j] > 0:
                clasterization[i] = max(clasterization[i], clasterization[j])
                clasterization[j] = max(clasterization[i], clasterization[j])
            else:
                max_claster_id += 1
                clasterization[i] = max_claster_id
                clasterization[j] = max_claster_id

for i in xrange(0, L):
    if clasterization[i] == 0:
        max_claster_id += 1
        clasterization[i] = max_claster_id
    print slices[i][0], clasterization[i]




