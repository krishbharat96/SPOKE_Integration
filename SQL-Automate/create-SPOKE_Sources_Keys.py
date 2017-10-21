import mysql.connector

cnx = mysql.connector.connect(user='root', password='')
cursor = cnx.cursor(buffered=True)

cursor.execute("USE SPOKE_Try_Sources;")
cursor.execute("ALTER TABLE Ref_Sources ADD PRIMARY KEY (Source_ID);")
cursor.execute("ALTER TABLE Node_Props_Ref ADD PRIMARY KEY (Node_PK_ID);")
cursor.execute("ALTER TABLE Rel_Props_Ref ADD PRIMARY KEY (Rel_PK_ID);")
cursor.execute("ALTER TABLE Rel_Keys_Sources ADD FOREIGN KEY (Rel_PK_ID) REFERENCES Rel_Props_Ref(Rel_PK_ID);")
cursor.execute("ALTER TABLE Rel_Keys_Sources ADD FOREIGN KEY (Source_ID) REFERENCES Ref_Sources(Source_ID);")
cursor.execute("ALTER TABLE Node_Keys_Sources ADD FOREIGN KEY (Node_PK_ID) REFERENCES Node_Props_Ref(Node_PK_ID);")
cursor.execute("ALTER TABLE Node_Keys_Sources ADD FOREIGN KEY (Source_ID) REFERENCES Ref_Sources(Source_ID);")

cnx.commit()
cnx.close()

