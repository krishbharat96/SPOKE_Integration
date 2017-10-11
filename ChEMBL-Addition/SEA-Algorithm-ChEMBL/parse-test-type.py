Func_types = ["AC50", "GI50", "LD50", "ED50", "ID50", "pD'2", "pD2", "pA2", "Log AC50", "Log GI50", "Log LD50", "-Log AC50", "-Log GI50", "-Log LD50"]
Func_data = ["identity", "identity", "identity", "identity", "identity", "minus_log", "minus_log", "minus_log", "plus_log", "plus_log", "plus_log", "minus_log", "minus_log", "minus_log"]
FUNCTIONAL_TYPES = zip(Func_types, Func_data)
FUNCTIONAL_TYPES_ACT = dict(FUNCTIONAL_TYPES)
SU_TYPES = {'IC60' : 'identity', 'IC70' : 'identity'}
print SU_TYPES
BOUNDING_TYPES = {'IC60':'identity', 'IC70':'identity', 'IC80':'identity', 'IC90':'identity', 'IC95':'identity', 'IC99':'identity', 'Log IC60':'plus_log', 'Log IC70':'plus_log', 'Log IC80':'plus_log', 'Log IC90':'plus_log', 'Log IC95':'plus_log', 'Log IC99':'plus_log', '-Log IC60':'minus_log', '-Log IC70':'minus_log', '-Log IC80':'minus_log', '-Log IC90':'minus_log', '-Log IC95':'minus_log', '-Log IC99':'minus_log'}
STD_TYPES = {'Ki':'identity', 'Kd':'identity', 'IC50':'identity', 'pKi':'minus_log', 'pKd':'minus_log', 'pIC50':'minus_log', '-Log Ki':'minus_log', '-Log Kd': 'minus_log', '-Log IC50': 'minus_log', '-Log KD': 'minus_log', 'Log 1/Ki': 'minus_log', 'Log 1/Kd': 'minus_log', 'Log 1/IC50': 'minus_log', 'log(1/Ki)': 'minus_log', 'log(1/Kd)': 'minus_log', 'log(1/IC50)': 'minus_log', 'Log Ki': 'plus_log', 'Log Kd': 'plus_log', 'Log IC50': 'plus_log', 'logKi': 'plus_log', 'logKd': 'plus_log', 'logIC50': 'plus_log', 'EC50': 'identity', 'pEC50': 'minus_log', '-Log EC50': 'minus_log', 'Log 1/EC50': 'minus_log', 'log(1/EC50)': 'minus_log', 'Log EC50': 'plus_log', 'logEC50': 'plus_log'}

COMBINED_TYPE = {}
COMBINED_TYPE.update(FUNCTIONAL_TYPES_ACT)
COMBINED_TYPE.update(STD_TYPES)
COMBINED_TYPE.update(BOUNDING_TYPES)

def commacatenate(param1, param2):
    return param1 + "," + param2

i = open('assays-mod6-act.tsv', 'r')
o = open('assays-mod7.csv', 'w+')

for line in i.readlines():
    cols = line.split(',')
    if line:
        if cols[4] in COMBINED_TYPE:
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





        
