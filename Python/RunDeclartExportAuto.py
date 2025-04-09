import pymssql
import psycopg2
import uuid
import traceback
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
# Track the last processed doc_id in a file
LAST_PROCESSED_FILE = 'D\last_TTN.txt'
LAST_PROCESSED_FILE_XT = 'D:\list_Xtitre.txt'
# SMTP server details
smtp_server = "192.168.10.191"
smtp_port = 25
# Email details
sender_email = "informatique@mas-alu.com"
recipient_email = "khamdi@mas-alu.com"
subject = "Alert: Titre non inserrer: Client/Fournisseur Non Trouver"
body = ""

def set_list_xtitre(titre: str):
    with open(LAST_PROCESSED_FILE_XT, 'a') as file:
        file.write(str(titre) + '\n')
def normalize_supplier_name(name):
    """
    Normalize supplier name by cleaning and standardizing the format.
    """
    # Replace single quotes with double quotes for SQL safety
    name = name.replace("'", "''")
    # Remove extra whitespace
    name = ' '.join(name.split())
    return name
def generate_search_patterns(supplier_name):
    """
    Generate a list of search patterns for the supplier name.
    Return patterns formatted as SQL 'LIKE' clauses.
    """
    formattedWord = supplier_name.replace("'","''")
    words = formattedWord.split()
    patterns = []

    # Add exact match
    patterns.append(f"Tiers_rs LIKE '{formattedWord}'")

    if len(words) > 1:
        # Pattern with all words except the last
        patterns.append(f"Tiers_rs LIKE '{' '.join(words[:-1])}%'")

        if len(words) > 2:
            # Pattern with all words except the last two
            patterns.append(f"Tiers_rs LIKE '{' '.join(words[:-2])}%'")

            # Pattern with wildcards between words (for flexible matching)
            patterns.append(f"Tiers_rs LIKE ' {'%'.join(words[:-1])}%'")
    else:
        # Single word case
        patterns.append(f"Tiers_rs LIKE '{formattedWord}%'")

    return patterns

server_sql = '192.168.10.216'
server_pg = '192.168.10.217'
database_pg = 'APP_TRANS_1'
modified_string = ''
Tiers_Code: str = ''
fournisseur: str = ''
banque: str = ''
try:
    # Establish connection to PostgreSQL
    conn_pg = psycopg2.connect(dbname=database_pg, user='zedgres', password='zedgres', host=server_pg, port='5432', sslmode='disable')
    cursor_pg = conn_pg.cursor()
    set_list_xtitre('----------------------------------')
    set_list_xtitre(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    # Fetch data from PostgreSQL where num_domicialiation is not in existing_xtitre
    select_query = '''
        select  distinct
        dc.type_declaration || ' ' || douane_data.num_enreg_ddm AS NumDecaration, 
        t.type_transaction,
        dc.date_declaration as datedeclaration,
        douane_data.cours_convers_dev_fact as cours,
        cm.numero_domiciliation AS Titre_Num,
        g.code_frs AS Tiers_Code,
        f.rs_frs AS Fournisseur,
        t.rs_exportateur AS FournisseurExp,
        t.rs_importateur AS FournisseurImp,
        g.date_signat_declarant AS DateDomicilation,
        douane_data.code_devise_montant_devise as Devise,
        g.code_incoterme,
        g.fob_mont_devise AS Titre_Devise,
        g.ptfn AS Titre_Mnt,
        t.num_contrat AS FactNum,
        t.num_demande AS NDOSS,
        t.emetteur AS Titre_Banque,
        g.type_transaction AS TypeDoss
        --t.cours_conversion
        from document dc
        INNER JOIN douane_data on douane_data.id_doc = dc.id_doc
        LEFT JOIN marchadise_decv on marchadise_decv.id_doc= douane_data.id_doc
        INNER JOIN complement_marchandise cm on douane_data.id_doc = cm.id_doc
        INNER JOIN dossier_g g on cm.num_dossier = g.num_dossier
        INNER JOIN fournisseur f ON g.code_frs = f.code_frs
        INNER JOIN  document_tce2 t ON cm.numero_domiciliation = t.num_domicialiation
        where douane_data.num_enreg_ddm <> '' and cm.numero_domiciliation <> ''  and g.type_transaction  = 2
        order by g.date_signat_declarant desc 
        LIMIT 1;
    '''
    cursor_pg.execute(select_query)
    # Fetch all rows from PostgreSQL
    pg_rows = cursor_pg.fetchall()

    # Prepare new records to insert that are not in existing_xtitre
    new_records = []
    i = 0
    hasFindTiers = False
    isNewTitre = bool
    for row in pg_rows:
        print(i)
        Decla_num = row[0]  # Assuming num_domicialiation is in the first column
        TypeDoss = row[17]  # Extract TypeDoss for this row
        FournisseurExp = row[7]  # Extract FournisseurExp
        FournisseurImp = row[8]  # Extract FournisseurImp
        database_sql = 'TESTMAS6'
        if TypeDoss == 1:
            if FournisseurImp == 'SOCIETE POLYBAT':
                database_sql = 'POLYBAT'
                print(database_sql)
            elif FournisseurImp == 'STE ((MAS))':
                database_sql = 'TESTMAS6'
                print(database_sql)
            elif FournisseurImp == 'MAS INTERNATIONALE':
                database_sql = 'MASMETAL'
                print(database_sql)
            elif FournisseurImp == 'POLYCOFFRE':
                database_sql = 'POLYCOFFRE'
                print(database_sql)
            elif FournisseurImp == '"MAS INTERNATIONALE SENEGAL"':
                database_sql = '"MASINTERNATIONALSN"'
                print(database_sql)
        elif TypeDoss == 2:
            if FournisseurExp == 'SOCIETE POLYBAT':
                database_sql = 'POLYBAT'
                print(database_sql)
            elif FournisseurExp == 'STE ((MAS))':
                database_sql = 'TESTMAS6'
                print(database_sql)
            elif FournisseurExp == 'MAS INTERNATIONALE':
                database_sql = 'MASMETAL'
                print(database_sql)
            elif FournisseurImp == 'POLYCOFFRE':
                database_sql = 'POLYCOFFRE'
                print(database_sql)
            elif FournisseurImp == '"MAS INTERNATIONALE SENEGAL"':
                database_sql = '"MASINTERNATIONALSN"'
                print(database_sql)
        # Establish connection to SQL Server for xtitre
        conn_sql = pymssql.connect(server=server_sql, database=database_sql, port='1433', user='sa', password='123')
        cursor_sql = conn_sql.cursor()
        # Fetch existing Decla_num from xtitre
        cursor_sql.execute("SELECT NumDecl FROM DeclartExport where NumDecl = '" + Decla_num + "'")
        xtitre_rows = cursor_sql.fetchall()

        # Convert SQL Server titles to a set for quick lookup
        existing_xtitre = {row[0] for row in xtitre_rows}

        if Decla_num not in existing_xtitre:
            isNewTitre = 1
            print("Nouveau Titre: " + Decla_num + " (" + database_sql + ")")
            new_records = []
            new_records.append(row)
        else:
            print("Titre Existant")
            isNewTitre = 0
        i = i + 1
        # Insert new records into xtitre
        insert_query = '''
                        INSERT INTO [dbo].[xtitre]
                            ([KeyDecl]
                           ,[NumDecl]
                           ,[DateDecl]
                           ,[TitDecla]
                           ,[CodeClt]
                           ,[Client]
                           ,[Mt_Tit]
                           ,[Mt_Decl]
                           ,[BQ]
                           ,[Devise]
                           ,[TTN]
                           ,[NFact]
                           ,[Mt_Fcat]
                           ,[DossDecl]
                           ,[CoursDecl]
                           ,[Etat_Decla])
                         VALUES (
                        %s, 
            			   %s, 
            			   %s, 
            			   %s, 
            			   %s, 
            			   %s, 
            			   %s, 
            			   %s, 
            			   %s, 
            			   %s, 
                           %s,
            			   %s,
            				%s, 
            				%s,
            				%s,
            				%s

                        )
            '''
        if Decla_num not in existing_xtitre:
            for record in new_records:

                # Execute Find Tiers
                original_string = generate_search_patterns(record[6])  # Nom fournisseur
                # Fetch existing Tiers from SQL Server
                queryFindTiers = "SELECT * FROM tiers WHERE (Tiers_Type = '07' OR Tiers_Type = '02' OR Tiers_Type = '01') AND (" + " OR ".join(
                    original_string) + ")"
                print("Query For Find Tiers:", queryFindTiers)
                # Execute the insert query
                cursor_sql.execute(queryFindTiers)
                FindTiersExecute = cursor_sql.fetchall()
                if len(FindTiersExecute) > 0 and len(FindTiersExecute[0]) > 2:
                    print("Result of len Find Tiers:", FindTiersExecute[0][2])
                    # Check if the third row exists in FindTiersExecute and get "fournisseur"
                    if len(FindTiersExecute) > 0:
                        hasFindTiers = True
                        fournisseur = FindTiersExecute[0][2]  # Assuming this row has "fournisseur" data
                        Tiers_Code = FindTiersExecute[0][0]  # Tiers_Code
                    else:
                        hasFindTiers = False
                        print("Error Finding Tiers:", FindTiersExecute[0][2])
                        fournisseur = record[6]  # Default or fallback if the third row doesn't exist
                        Tiers_Code = record[5]  # Tiers_Code

                # Execute Find Banque
                # Get the original string from record[6]
                original_string_Banque = record[16]  # Nom banque

                if ("STEMASS1" == original_string_Banque):
                    original_string_Banque = "ATB"
                # Split the string by whitespace and remove the last word
                words_Banque = original_string_Banque.split()
                if len(words_Banque) > 0:
                    modified_string_banque = ' '.join(word[:3] for word in words_Banque) + '%'
                    # Fetch existing Tiers from SQL Server
                    queryFindBanque = "select distinct Banque_XRT from Banque " \
                                      "where Banque_XRT is not null AND Banque_XRT LIKE '%s'"

                    # Generate the query with actual values for debugging
                    formatted_query_banque = queryFindBanque % modified_string_banque
                    # Execute the insert query
                    cursor_sql.execute(formatted_query_banque)
                    FindBanqueExecute = cursor_sql.fetchall()
                    # Check if the third row exists in FindTiersExecute and get "fournisseur"

                    if len(FindTiersExecute) > 0:
                        banque = FindBanqueExecute[0][0] + '01'  # Assuming this row has "fournisseur" data
                    else:
                        banque = record[16]

                key_titre = str(uuid.uuid4())  # Generate a unique KeyTitre
                titre_num = record[0]  # Titre_Num
                nttn = record[5]  # NTTN
                type_doss = record[3]  # TypeDoss
                date_domicilation = record[9]  # DateDomicilation
                titre_mnt = record[13]  # Titre_Mnt
                titre_devise = record[10]  # Titre_Devise
                fact_num = record[15]  # FactNum
                TypeDoss = ""  # TypeDoss
                NDOSS = record[15]  # NDOSS
                Cours = record[4]


                if hasFindTiers == True and isNewTitre == 1:
                    # Execute the insert query
                    # Values to be inserted
                    values = (
                        key_titre, titre_num, date_domicilation, Tiers_Code, fournisseur, titre_mnt, titre_mnt,
                        banque, titre_devise, nttn, fact_num, titre_mnt, NDOSS, Cours, 0
                    )
                    # Manually format the query for debugging
                    formatted_query = insert_query % tuple(
                        repr(value) for value in values
                    )

                    # Print the formatted query
                    print("Executing query:", formatted_query)

                    cursor_sql.execute(insert_query, values)

                    # Commit the transaction after inserts
                    conn_sql.commit()
                else:
                    print(f"-----Tiers finding = {int(hasFindTiers)}  ------")
                    # Create the email message
                    message = MIMEMultipart()
                    message["From"] = sender_email
                    message["To"] = recipient_email
                    message["Subject"] = subject + record[6] + " (" + database_sql + " )"

                    # Attach the email body
                    message.attach(MIMEText("Client/Fourniseur Non trouver" + record[
                        6] + " (" + database_sql + " )\nTitre Non inserrer Num:" + titre_num + "\n" + "Type Dossier:" + TypeDoss,
                                            "plain"))

                    try:
                        # Connect to the SMTP server and send the email
                        #with smtplib.SMTP(smtp_server, smtp_port) as server:
                            #server.sendmail(sender_email, recipient_email, message.as_string())
                        print("Email alert sent successfully.")
                    except Exception as e:
                        print(f"Failed to send email: {e}")
                    print(f"-----is New Titre = {int(isNewTitre)} ------")

    # Close the connections
    cursor_pg.close()
    conn_pg.close()
    cursor_sql.close()
    conn_sql.close()
    set_list_xtitre(f"------ Inserted {len(new_records)} new records into xtitre in {database_sql} ------")

except Exception as e:
    print("An error occurred:", e)
    print(traceback.format_exc())