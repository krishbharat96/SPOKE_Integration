import math
from decimal import Decimal as D

# Overall/Combined script for extracting the assay data from ChEMBL for the purposes of the SEA algorithm

EXCLUDE_SOURCES = ['7', '15'] # Source IDs within ChEMBL to exclude
WEAK_CURATION = ['Autocuration'] # Exclude Autocurated assays
UNITS2NM = {'M': 1e9, 'mM': 1e6, 'uM': 1e3, 'nM':1, 'pM':1e-3, 'fM':1e-6, 'fmol/ml':1e-3, 'pmol/ml':1, 'nmol/ml': 1e3, 'umol/ml':1e9, 'mmol/ml':1e12, 'M-1':1e-9, 'NULL':1} # Only contains acceptable units for the purposes of SEA
WEAK_CONFIDENCE = ['0', '1', '2', '3', '4', '6', '8'] # Exclude certain confidence scores. 0-3 are poor confidences; 4, 6, and 8 have to do with Homologous Proteins and should be excluded

Func_types = ["AC50", "GI50", "LD50", "ED50", "ID50", "pD'2", "pD2", "pA2", "Log AC50", "Log GI50", "Log LD50", "-Log AC50", "-Log GI50", "-Log LD50"]
Func_data = ["identity", "identity", "identity", "identity", "identity", "minus_log", "minus_log", "minus_log", "plus_log", "plus_log", "plus_log", "minus_log", "minus_log", "minus_log"]
FUNCTIONAL_TYPES = zip(Func_types, Func_data)
FUNCTIONAL_TYPES_ACT = dict(FUNCTIONAL_TYPES)
BOUNDING_TYPES = {'IC60':'identity', 'IC70':'identity', 'IC80':'identity', 'IC90':'identity', 'IC95':'identity', 'IC99':'identity', 'Log IC60':'plus_log', 'Log IC70':'plus_log', 'Log IC80':'plus_log', 'Log IC90':'plus_log', 'Log IC95':'plus_log', 'Log IC99':'plus_log', '-Log IC60':'minus_log', '-Log IC70':'minus_log', '-Log IC80':'minus_log', '-Log IC90':'minus_log', '-Log IC95':'minus_log', '-Log IC99':'minus_log'}
STD_TYPES = {'Ki':'identity', 'Kd':'identity', 'IC50':'identity', 'pKi':'minus_log', 'pKd':'minus_log', 'pIC50':'minus_log', '-Log Ki':'minus_log', '-Log Kd': 'minus_log', '-Log IC50': 'minus_log', '-Log KD': 'minus_log', 'Log 1/Ki': 'minus_log', 'Log 1/Kd': 'minus_log', 'Log 1/IC50': 'minus_log', 'log(1/Ki)': 'minus_log', 'log(1/Kd)': 'minus_log', 'log(1/IC50)': 'minus_log', 'Log Ki': 'plus_log', 'Log Kd': 'plus_log', 'Log IC50': 'plus_log', 'logKi': 'plus_log', 'logKd': 'plus_log', 'logIC50': 'plus_log', 'EC50': 'identity', 'pEC50': 'minus_log', '-Log EC50': 'minus_log', 'Log 1/EC50': 'minus_log', 'log(1/EC50)': 'minus_log', 'Log EC50': 'plus_log', 'logEC50': 'plus_log'}

COMBINED_TYPE = {}
COMBINED_TYPE.update(FUNCTIONAL_TYPES_ACT)
COMBINED_TYPE.update(STD_TYPES)
COMBINED_TYPE.update(BOUNDING_TYPES) # Contains the results of the various acceptable types of assays for SEA. The functions corresponding to the way they are processed are listed below (ie minus_log, plus_log, and identity)

def minus_log(x):
    return 10**(9-x)

def plus_log(x):
    if x > 2:
	x = -x
    return 10**(9+x)

def identity(x):
    return x

def commacatenate(param1, param2):
    return param1 + "," + param2

z = open('assays_outfile.tsv', 'r')

dict_a = {}

for line in z.readlines():
    cols = line.split('\t')
    if line:
        if not '\N' in cols:
            if not cols[6].strip() in EXCLUDE_SOURCES and not cols[8].strip() in WEAK_CURATION and cols[2].strip() in UNITS2NM and not cols[7].strip() in WEAK_CONFIDENCE and cols[9].strip() in COMBINED_TYPE:
                conv_units = float(cols[3].strip())*float(UNITS2NM[cols[2].strip()])
                conv_type = COMBINED_TYPE[cols[9].strip()]
                final_val = 0
                if (conv_type == 'minus_log'):
                    final_val = minus_log(conv_units)
                elif (conv_type == 'plus_log'):
                    final_val = plus_log(conv_units)
                else:
                    final_val = identity(conv_units)

                val_M = final_val * 1e-9
                val_neg_log = -(D(val_M).log10())
                
                uid = cols[0].strip() + "-" + cols[1].strip() + "-" + cols[9].strip()
                cat_val = str(final_val) + "|nM|" + cols[4].strip() + "|" + str(float(val_neg_log))
                
                if not uid in dict_a:
                    dict_a.update({uid : cat_val})
                else:
                    val_from_dict = dict_a[uid]
                    new_val = val_from_dict + ";" + cat_val
                    dict_a[uid] = new_val


o = open('parsed_outfile.csv', 'w+')
for k, v in dict_a.iteritems():
    o.write(k + "," + v)
    o.write("\n")
    


