CYPHER_AddCmpd = """
    CREATE (c:Compound)
    SET c.name = {name}, c.identifier = {identifier},
    c.license = 'CC BY-NC 4.0', c.source = 'DrugBank',
    c.inchi = {inchi}, c.inchikey = {inchikey}, c.url = {url},
    c.pref_name = {name}, c.drugbank_id = {identifier}, c.chembl_id = {chembl_id}
"""

CYPHER_VestigeCmpd = """
    MATCH (c:Compound) WHERE c.identifier = {cmpd_id}
    SET c.vestige = True
"""

CYPHER_ObtainCmpd = """
    MATCH (c:Compound) WHERE c.identifier contains '' and exists (c.drugbank_id)
    RETURN c.name as c_name, c.identifier as c_id, c.inchi as c_inchi, c.inchikey as c_inchikey,
    c.chembl_id as c_chembl
"""

CYPHER_UpdateCmpd = """
    MATCH (c:Compound) WHERE c.identifier = {identifier} SET c.name = {name}, c.inchi = {inchi}, c.inchikey = {inchikey}, c.chembl_id = {chembl_id}
"""

CYPHER_UpdateIdentifier = """
    MATCH (c:Compound) WHERE c.identifier = {old_id} SET c.identifier = {new_id}
"""

def main():
    from neo4j.v1 import GraphDatabase, basic_auth
    import gzip
    from gzip import GzipFile
    import shutil
    
##    with gzip.open('drugbank_all_full_database.xml.zip', 'rb') as f_in, open('drugbank_full_db.xml', 'wb') as f_out:
##        shutil.copyfileobj(f_in, f_out)
        
    print "Connecting to GraphDB"
    in_file = open('full_database.xml', 'r')
    driver = GraphDatabase.driver("bolt://127.0.0.1/:7687", auth=basic_auth("neo4j", "neo4j2"))
    session = driver.session()
    print "Connected to DB!"
    update_drugbank_cmpds(session, drugbank_process_xml(in_file))

def process_null(string):
    out_text = "None"
    if (string == "None"):
        out_text = "null"
    else:
        out_text = "'" + string + "'"
    return out_text

def drugbank_process_xml(in_file):
    import xml.etree.ElementTree as ET
    tree = ET.parse(in_file)
    root = tree.getroot()
    
    conv_dict = dict()
    drugbank_dict = dict()
    ns = "{http://www.drugbank.ca}"
    for drug in root.findall(ns + "drug"):
        if (str(drug.attrib["type"]) == "small molecule"):
            groups_arr = []
            for drug_group in drug.findall(ns + "groups/" + ns + "group"):
                groups_arr.append(drug_group.text)

            if (len(groups_arr) > 0):
                if "approved" in groups_arr:
                    conv_arr = []
                    for alternate_id in drug.findall(ns + "drugbank-id"):
                        if "DB" in alternate_id.text:
                            conv_arr.append(alternate_id.text)
                    drug_name = drug.findtext(ns + "name")
                    drug_id = drug.findtext(ns + "drugbank-id[@primary='true']")
                    conv_arr.remove(drug_id)
                    for conv_item in conv_arr:
                        conv_dict.update({conv_item:drug_id})
                    
                    inchi = "None"
                    inchikey = "None"
                    chembl_id = "None"

                    for prop in drug.findall(ns + "calculated-properties/" + ns + "property"):
                        if (prop.findtext(ns + "kind") == "InChI"):
                            inchi = prop.findtext(ns + "value")
                        if (prop.findtext(ns + "kind") == "InChIKey"):
                            inchikey = prop.findtext(ns + "value")

                    for ex_id in drug.findall(ns + "external-identifiers/" + ns + "external-identifier"):
                        if (ex_id.findtext(ns + "resource") == "ChEMBL"):
                            chembl_id = ex_id.findtext(ns + "identifier")
                    
                    if not (inchi == "None"):
                        single_dict = {drug_id: {"name":drug_name, "inchi":inchi, "inchikey":inchikey, "chembl_id":chembl_id}}
                        drugbank_dict.update(single_dict)
                    else:
                        continue

    print len(drugbank_dict)
    return drugbank_dict, conv_dict

def update_drugbank_cmpds(session, new_cp):
    import time
    new_cps = new_cp[0]
    conv_dict = new_cp[1]
    cp_new = 0
    cp_same = 0
    cp_vestige = 0
    
    cp_update = 0
    diff_name = 0
    diff_inchi = 0
    diff_inchikey = 0
    diff_chembl = 0
    
    result_1 = session.run(CYPHER_ObtainCmpd)
    old_cps = {}
    old_ids = []
    print "Updating Mappings ..."
    for r_id in result_1:
        old_ids.append(str(r_id["c_id"]))

    to_be_conv = list(set(old_ids) - (set(old_ids) - set(conv_dict.keys())))
    for old_id in to_be_conv:
        try:
            session.run(CYPHER_UpdateIdentifier.format(old_id="'" + old_id + "'", new_id="'" + conv_dict[old_id] + "'"))
        except:
            continue

    result_2 = session.run(CYPHER_ObtainCmpd)
    for r in result_2:
        single_dict = {str(r["c_id"]):{"name":str(r["c_name"]), "inchi":str(r["c_inchi"]), "inchikey":str(r["c_inchikey"]), "chembl_id":str(r["c_chembl"])}}
        old_cps.update(single_dict)

    time.sleep(2)

    vestige_arr = list(set(old_cps.keys()) - set(new_cps.keys()))
    add_arr = list(set(new_cps.keys()) - set(old_cps.keys()))
    for old_item in vestige_arr:
        session.run(CYPHER_VestigeCmpd.format(cmpd_id="'" + old_item + "'"))
        cp_vestige = cp_vestige + 1
        old_cps.pop(old_item)

    for new_item in add_arr:
        cp_new = cp_new + 1
        if (str(new_cps[new_item]["chembl_id"]) == "None"):
            url_drug = "http://www.drugbank.ca/drugs/" + str(new_item)
            session.run(CYPHER_AddCmpd.format(name="'" + str(new_cps[new_item]["name"]) + "'",
                                              identifier= "'" + new_item + "'", inchi=process_null(str(new_cps[new_item]["inchi"])),
                                              inchikey=process_null(str(new_cps[new_item]["inchikey"])), url="'" + url_drug + "'", chembl_id=process_null(str(new_cps[new_item]["chembl_id"]))))
        else:
            session.run("MATCH (c:Compound {identifier:'" + str(new_cps[new_item]["chembl_id"]) + "'}) SET c.drugbank_id = '" + new_item + "'")
        new_cps.pop(new_item)

    for key in new_cps.keys():
        if not (sorted(old_cps[key]) == sorted(new_cps[key])):
            cp_update = cp_update + 1
            session.run(CYPHER_UpdateCmpd.format(name="'" + str(new_cps[key]["name"]) + "'",
                                                 identifier= "'" + key + "'", inchi=process_null(str(new_cps[key]["inchi"])),
                                                 inchikey=process_null(str(new_cps[key]["inchikey"])), chembl_id=process_null(str(new_cps[key]["chembl_id"]))))
            if not (old_cps[key]["name"] == new_cps[key]["name"]):
                diff_name = diff_name + 1
            if not (old_cps[key]["chembl_id"] == new_cps[key]["chembl_id"]):
                diff_chembl = diff_chembl + 1
            if not (old_cps[key]["inchi"] == new_cps[key]["inchi"]):
                diff_inchi = diff_inchi + 1
            if not (old_cps[key]["inchikey"] == new_cps[key]["inchikey"]):
                diff_inchikey = diff_inchikey + 1
                                            
    print "Updated! Look below for stats regarding Update:"
    print "Number New : " + str(cp_new)
    print "Number Same : " + str(cp_same)
    print "Number Vestige : " + str(cp_vestige)
    print "Number Update : " + str(cp_update)
    print "   Diff_Name : " + str(diff_name)
    print "   Diff_InchI : " + str(diff_inchi)
    print "   Diff_ChEMBL : " + str(diff_chembl)
    print "   Diff_InChIKey : " + str(diff_inchikey)
main()
