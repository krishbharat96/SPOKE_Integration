import mysql.connector

cnx = mysql.connector.connect(user='root', password='')
cursor = cnx.cursor()

def basicatenate(param1, param2):
    return param1 + ', ' + param2

def elim_param(param1):
    act_tbl1 = str(param1).replace("u'", "")
    act_tbl2 = act_tbl1.replace("(", "")
    act_tbl3 = act_tbl2.replace(")", "")
    act_tbl4 = act_tbl3.replace(" ", "")
    act_tbl5 = act_tbl4.replace("',", "")
    return act_tbl5.strip()

cursor.execute('USE chembl23;')
cursor.execute('SHOW TABLES;')

tables_arr = []
for tbl in cursor:
    tables_arr.append(elim_param(tbl))

for tabl in tables_arr:
    print tabl
    col_arr = []
    cursor.execute("select column_name from information_schema.columns where table_name = " + "'" + str(tabl) + "';")
    for cols in cursor:
        col_arr.append(elim_param(cols))
    
    s = col_arr[0]
    s2 = "'" + str(col_arr[0]) + "'"
    
    for c in range(len(col_arr)):
        if not (c == 0):
            tmp = basicatenate(s, col_arr[c])
            s = tmp

            c_act = "'" + str(col_arr[c]) + "'"
            tmp2 = basicatenate(s2, c_act)
            s2 = tmp2

    cursor.execute("select " + s2 + " UNION ALL select " + s + " from " + tabl + " INTO OUTFILE '/Users/kbharat/Documents/ChEMBL-Commons/" + tabl + ".tsv';")
    print "select " + s2 + " UNION ALL select " + s + " from " + tabl + " INTO OUTFILE '/Users/Documents/ChEMBL-Commons/" + tabl + ".tsv';"
        
cnx.close()
    
