import cardsharp as cs
from re import sub, search

ids = ['ID12701','ID12702','ID12703','ID12704','ID12705','ID12706','ID12707','ID12708','ID12709','ID12710','ID12711','ID12712',
       'ID12713','ID12714','ID12715','ID12716','ID12717','ID12718','ID12719','ID12720','ID12721','ID12722','ID12723','ID12724',
       'ID12725','ID12726','ID12727','ID12728','ID12729','ID12730','ID12731','ID12732','ID12733','ID12734','ID12735','ID12736',
       'ID12737','ID12738','ID12739','ID12740','ID12741','ID12742','ID12743','ID12744','ID12745','ID12746','ID12747','ID12748',
       'ID12749','ID12750','ID12751','ID12752','ID12753','ID12754','ID12755','ID12756','ID12757','ID12758','ID12759','ID12760',
       'ID12761','ID12762','ID12763','ID12764','ID12765','ID12766','ID12767','ID12768','ID12769','ID12770','ID12771','ID12772',
       'ID12773','ID12774','ID12775','ID12776','ID12777','ID12778','ID12779','ID12780','ID12781','ID12782','ID12783','ID12784',
       'ID12785','ID12786','ID12787','ID12788','ID12789','ID12790','ID12791','ID12792','ID12793','ID12794','ID12795','ID12796',
       'ID12797','ID12798','ID12799','ID12800','ID12801','ID12802','ID12803','ID12804','ID12805','ID12806','ID12807','ID12808',
       'ID12809','ID12810','ID12811','ID12812','ID12813','ID12814','ID12815','ID12816','ID12817','ID12818','ID12819','ID12820',
       'ID12821','ID12822','ID12823','ID12824','ID12825','ID12826','ID12827','ID12828','ID12829','ID12830','ID12831','ID12832',
       'ID12833','ID12834','ID12835','ID12836','ID12837','ID12838','ID12839','ID12840','ID12841','ID12842','ID12843','ID12844',
       'ID12845','ID12846','ID12847','ID12848','ID12849','ID12850','ID12851','ID12852','ID12853','ID12854','ID12855','ID12856',
       'ID12857','ID12858','ID12859','ID12860','ID12861','ID12862','ID12863','ID12864','ID12865','ID12866','ID12867','ID12868',
       'ID12869','ID12870','ID12871','ID12872','ID12873','ID12874','ID12875','ID12876','ID12877','ID12878','ID12879','ID12880',
       'ID12881','ID12882','ID12883','ID12884','ID12885','ID12886','ID12887','ID12888','ID12889','ID12890','ID12891','ID12892',
       'ID12893','ID12894','ID12895','ID12896','ID12897','ID12898','ID12899','ID12900']

from itertools import izip
rows = {}
with open(r'D:\school\ect584\assign3\out-new.txt', 'r') as f:
    for line in f.readlines():
        
        if search('inst#[ ]*actual[ ]*predicted[ ]*error[ ]*prediction', line):
            results = cs.Dataset (['id', 'instance', 'actual', 'predicted', 'error'])
        
        if search('\d+', line):
            data = search('[ ]*(\d+)[ ]*(\d+:\?)[ ]*(\d+:[a-z]+)[ ]*(\d+\.\d+|\d+)', line.lower())
            rows[ids.pop(0)] = ([data.groups()[x] for x in range(4)])

bank = cs.load(filename = r'D:\school\ect584\assign3\bank-new.csv', format = 'csv')

bank.variables.append('error')
cs.wait()

for row in bank:
    row[11] = rows[row[0]][2][2:]
    row[12] = rows[row[0]][3]
count = 0
for row in bank:
    if row[11] == 'yes':
        count += 1

print count