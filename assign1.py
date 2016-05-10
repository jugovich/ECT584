import cardsharp as cs
from decimal import *
import math
from itertools import izip

def mean(vector):
    return Decimal(math.fsum([Decimal(v) for v in vector])) / Decimal(len(vector))
    
def stdev(vector):
    return Decimal(math.sqrt((Decimal(math.fsum(([math.pow(x, 2) for x in ([v - mean(vector) for v in vector])]))))/(Decimal(len(vector) - 1.0))))

def zscore(value, vector):
    return Decimal((Decimal(value) - mean(vector)) / stdev(vector))

#load the excel data
ds = cs.load(r'd:/school/ect584/Video_Store_S11.xls', format = 'excel')

#create container datasets

std_vars = [('cust_id', 'integer'), ('male', 'integer'), ('female', 'integer'), ('income', 'integer'), 
            ('age', 'integer'), ('rentals', 'integer'), ('avg_per_visit', 'decimal'), 
            ('incidentals_y', 'integer'), ('incidentals_n', 'integer'), ('action', 'integer'),
            ('comedy', 'integer'), ('drama', 'integer'), ('rentals_bin_smooth', 'float'),
            ('income_min_max', 'decimal'), ('age_z_score', 'decimal'), ('young', 'integer'),
            ('mid_age', 'integer'), ('old', 'integer')]

ds_std = cs.Dataset(std_vars)

ds_good_cust = cs.Dataset(std_vars)

#convert the original excel data
ds['rentals'].convert('integer')
ds['cust_id'].convert('integer')
ds['income'].convert('integer')
ds['avg_per_visit'].convert('decimal', 26)
ds['age'].convert('integer')
cs.wait()

#add new variables
ds.variables.append(('rentals_bin_smooth', 'float'))
ds.variables.append(('income_min_max', 'decimal'))
ds.variables.append(('age_z_score', 'decimal'))
ds.variables.append('age_cat')

#create variable containers for transformation
trans = []
for row in ds:
    trans.append((row['cust_id'], row['gender'], row['income'], row['age'], row['rentals'], 
                  row['avg_per_visit'], row['incidentals'], row['genre']))

#part a - smooth by bins
c = 0
b = 0
bins = {}
bins[0] = []

for i in sorted(trans, key=lambda r: r[4]):
    if c < 4:
        bins[b].append(i)
        c += 1
    else:
        b += 1
        bins[b] = []
        bins[b].append(i)
        c = 1

rental_replace = {}

for v in bins.itervalues():
    avg = sum(([val[4] for val in v ])) / float(len(v))
    for t in v:
        rental_replace[t[0]] = avg

#part b
min_income = float(min(([i[2] for i in trans])))
max_income = float(max(([i[2] for i in trans])))
new_min = 1.0
new_max = 5.0
        
ds1_vars = {}
male, female = {}, {}

def init_cont(d, l):
    for item in l:
        d[item] = 0

init_cont(male, ['action', 'comedy', 'drama'])
init_cont(female, ['action', 'comedy', 'drama'])

for row in ds:
    row['rentals_bin_smooth'] = rental_replace[row['cust_id']] 
    row['income_min_max'] = Decimal(((row['income'] - min_income)/(max_income - min_income)) * (new_max - new_min) + new_min)
    row['age_z_score'] = zscore(row['age'], ([i[3] for i in trans]))
    
    #Discretize the (original) Age attribute based on the following categories: 
    #Young = 1-20; MidAge = 21-40; Old = 41+.
    if row['age'] < 21:
        row['age_cat'] = 'Young'
    elif row['age'] < 41:
        row['age_cat'] = 'MidAge'
    else:
        row['age_cat'] = 'Old'
    
    for var in ['cust_id', 'income', 'age', 'avg_per_visit', 'rentals', 'rentals_bin_smooth',
                'income_min_max', 'age_z_score']:
        ds1_vars[var] = row[var]

    ds1_vars['male'] = 1 if 'm' == row['gender'].lower() else 0
    ds1_vars['female'] = 1 if 'f' == row['gender'].lower() else 0
    ds1_vars['incidentals_y'] = 1 if 'yes' == row['incidentals'].lower() else 0
    ds1_vars['incidentals_n'] = 1 if 'no' == row['incidentals'].lower() else 0
    ds1_vars['action'] = 1 if 'action' == row['genre'].lower() else 0
    ds1_vars['comedy'] = 1 if 'comedy' == row['genre'].lower() else 0
    ds1_vars['drama'] = 1 if 'drama' == row['genre'].lower() else 0
    ds1_vars['young'] = 1 if 'young' == row['age_cat'].lower() else 0
    ds1_vars['mid_age'] = 1 if 'midage' == row['age_cat'].lower() else 0
    ds1_vars['old'] = 1 if 'old' == row['age_cat'].lower() else 0
    
    std_vars = ([ds1_vars[v] for v in ['cust_id', 'male', 'female', 'income', 'age', 'rentals', 
                                        'avg_per_visit', 'incidentals_y', 'incidentals_n', 'action', 
                                        'comedy', 'drama', 'rentals_bin_smooth', 'income_min_max',
                                        'age_z_score', 'young', 'mid_age', 'old']])
        
    ds_std.add_row(std_vars)
    
    if row['rentals'] >= 30:
        ds_good_cust.add_row(std_vars)
    
    if row['gender'].lower() == 'm' and row['genre'].lower() == 'action':
        male['action'] += 1
    if row['gender'].lower() == 'm' and row['genre'].lower() == 'comedy':
        male['comedy'] += 1
    if row['gender'].lower() == 'm' and row['genre'].lower() == 'drama':
        male['drama'] += 1
    if row['gender'].lower() == 'f' and row['genre'].lower() == 'action':
        female['action'] += 1
    if row['gender'].lower() == 'f' and row['genre'].lower() == 'comedy':
        female['comedy'] += 1
    if row['gender'].lower() == 'f' and row['genre'].lower() == 'drama':
        female['drama'] += 1
        
    
mean_orig, mean_good = {}, {}

def get_var_means(d):
    means = {}
    for row in d:
        c = -1
        for val, var in izip(row, d.variables):
            c += 1
            if var.name in means:
                means[c] += val
            else:
                means[c] = val

    for k, v in mean_orig.iteritems():
        means[k] = float(float(v)/float(len(d.rows)))
    
    return means

mean_orig = get_var_means(ds_std)
mean_good = get_var_means(ds_good_cust)

#save the datasets
ds.save(filename = 'd:/school/ect584/assign1_output.xls', format = 'excel', overwrite = True)
cs.wait()
ds_std.save(filename = 'd:/school/ect584/assign1_output.xls', format = 'excel', overwrite = True, dataset = 'standardizied')
ds_std.save(filename = 'd:/school/ect584/assign1_std.sav', format = 'spss', overwrite = True)
cs.wait()
ds_good_cust.save(filename = 'd:/school/ect584/assign1_output.xls', format = 'excel', overwrite = True, dataset = 'good_cust_data')
ds_good_cust.save(filename = 'd:/school/ect584/assign1_output.sav', format = 'spss', overwrite = True)