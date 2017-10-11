clist = {}

from statistics import mean, median, stdev

def hyphenatenate(p1, p2, p3):
    return p1 + '-' + p2 + '-' + p3

def colonatenate(oldparam, param):
    return oldparam + ';' + param

z = open('assays-mod9.csv', 'r')
o = open('output-file-values2.csv', 'w+')

su = ""

for line in z.readlines():
    cols = line.split(',')
    if line:
        uid = hyphenatenate(cols[0], cols[1], cols[4])
        val = str(float(cols[3]))
        print "Still Processing: " + uid
        su = "False"
        
        if uid in clist:
            su = "True"
            newval = colonatenate(clist[uid], val)
            clist[uid] = newval

        if (su == "False"):
            clist.update({uid : val})

for k, v in clist.iteritems():
    arr = v.split(';')
    arract = []
    for i in arr:
        arract.append(float(i))
    
    mean_arr = mean(arract)
    median_arr = median(arract)
    
    if (len(arract) > 1):
        stdev_arr = stdev(arract)
    else:
        stdev_arr = 0
    print k, v, mean_arr, median_arr, stdev_arr
    o.write(k + ',' + v + ',' + str(mean_arr) + ',' + str(median_arr) + ',' + str(stdev_arr))
    o.write('\n')



