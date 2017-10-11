UNITS2NM = {'M': 1e9, 'mM': 1e6, 'uM': 1e3, 'nM':1, 'pM':1e-3, 'fM':1e-6, 'fmol/ml':1e-3, 'pmol/ml':1, 'nmol/ml': 1e3, 'umol/ml':1e9, 'mmol/ml':1e12, 'M-1':1e-9, 'NULL':1}

def commacatenate(param1, param2):
    return str(param1) + "," + str(param2)

i = open('assays-mod7.csv', 'r')
o = open('assays-mod9.csv', 'w+')

for line in i.readlines():
    cols = line.split(',')
    if line:
        if cols[2] in UNITS2NM:
            array = []
            newcols3 = float(float(UNITS2NM[cols[2]])*float(cols[3]))
            array.append(cols[0])
            array.append(cols[1])
            array.append('nM')
            array.append(newcols3)
            array.append(cols[4])
            array.append(cols[5])
            array.append(cols[6])
            array.append(cols[7])
            array.append(cols[8])
            array.append(cols[9])
            
            var = array[0]
            
            for i in range(len(array)):
                if (i == 0):
                    continue
                else:
                    var = commacatenate(var, array[i])
            
            print var.strip()        
            o.write(var.strip())
            o.write('\n')





        
