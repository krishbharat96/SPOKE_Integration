from neo4j.v1 import GraphDatabase, basic_auth

def concatenate(pchembl):
    return 'MATCH (n:Compound) where n.chembl_id = "' + pchembl + '" return n.identifier as id'

countf = 0
countnf = 0

f = open('assays-mod6-act.tsv', 'r')

driver = GraphDatabase.driver("bolt://msgap1.ucsf.edu/:7687", auth=basic_auth("kbharat96", "tejas320"))
session = driver.session()

for line in f.readlines():
    cols = line.split(',')
    if line:
        su = "false"
        cmd = concatenate(cols[1].strip())
        result = session.run(cmd)
        for record in result:
            su = "true"
            tmp = record["id"]
            countf = countf + 1
            print "Found! " + str(cols[1])
        result.consume()
        if (su == "false"):
            print "Not Found! " + str(cols[1])
            countnf = countnf + 1

        if (countf%1000 == 0):
            print "Number Found: " + str(countf)
            print "Number Not Found: " + str(countnf)

print "Found " + str(countf)
print "Not Found " + str(countnf)
