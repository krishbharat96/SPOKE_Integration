EXCLUDE_SOURCES = ['7', '15']
WEAK_CURATION = ['Autocuration']

def commacatenate(param1, param2):
    return param1 + "," + param2


z = open('assays-outfile6.tsv', 'r')
o = open('assays-mod6-actual.tsv', 'w+')

for line in z.readlines():
    cols = line.split('\t')
    if line:
        if not 'Autocuration' in cols[9]:
            if not cols[7] in EXCLUDE_SOURCES:
                array = []
                for j in range(10):
                    array.append(cols[j])
                var = array[0]
                for i in range(len(array)):
                    if (i == 0):
                        continue
                    else:
                        var = commacatenate(var, array[i])
                print var.strip()        
                o.write(var.strip())
                o.write('\n')
        
