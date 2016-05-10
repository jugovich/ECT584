import cardsharp as cs

ds = cs.load(filename = r'd:\school\ect584\assign2_part2.txt', format = 'text')

freq, trans_m = {}, {}
for row in ds:
    for var in row[0].split(','):
        for page in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
            if page == var:
                freq[page] = freq[page] + 1 if page in freq else 1
    for trans in ['A,B', 'A,C', 'B,C', 'B,D', 'C,D', 'C,E', 'C,F', 'D,E', 'E,G', 'F,G']:
        if trans in row[0]:
            freq[trans] = freq[trans] + 1 if trans in freq else 1
            
for k, v in freq.iteritems():
    if len(k) > 1:
        key = k[0]
        trans_m[k[2] + '|' + k[0]] =  round((float(v) / float(freq[key])), 2)
            
for k,v in freq.iteritems():
    print k + ' : ' + str(v)
    
print trans_m