# Code to process Assay Data obtained from ChEMBL
clist = {}

from statistics import mean, median, stdev

def hyphenatenate(ptarget, compound, p3): # Concatenates Protein-Target ChEMBL ID, Compound ChEMBL ID, and Assay Type (i.e. Ki, IC50, EC50 etc.)
    return ptarget + '-' + compound + '-' + p3 # Sets up a Unique 'ID' for the assay when it is added to the python dictionary

def colonatenate(oldparam, param): # Concatenates multiple values for a Target-Compound-Assay tuple since ChEMBL tends to generate randomly arranged records that are not found together for multiple assays for the same target/compounds
    return oldparam + ';' + param

z = open('assays-mod9.csv', 'r') # Contains Assay Data (Refer to SEA Algorithm files for further details within this repo)
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

# Print the values within the data dictionary "clist" to file
# Process the mean, median and standard deviation as there are multiple assays for a single uid tuple
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



