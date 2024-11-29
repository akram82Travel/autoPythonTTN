import pymssql
import psycopg2
import uuid
import traceback
from datetime import datetime
# Track the last processed doc_id in a file
LAST_PROCESSED_FILE = 'D:\last_TTN.txt'
LAST_PROCESSED_FILE_XT = 'D:\list_Xtitre.txt'


def set_list_xtitre(titre: str):
    with open(LAST_PROCESSED_FILE_XT, 'a') as file:
        file.write(str(titre) + '\n')


def count_partial_matching_words(string1, string2):
    # Split both strings into lists of words (convert to lowercase for case-insensitive comparison)
    words1 = string1.lower().split()
    words2 = string2.lower().split()

    # Count matches based on partial or exact matches
    match_count = 0
    for word1 in words1:
        for word2 in words2:
            if word1 in word2 or word2 in word1:  # Partial match condition
                match_count += 1
                break  # Avoid counting the same word twice

    return match_count
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
                 SELECT 
            t.num_domicialiation AS Titre_Num,
            g.num_dossier AS NDoss,
            t.num_dossier_ttn AS NTTN,
            g.type_transaction AS TypeDoss,
            t.type_transaction,
            g.code_frs AS Tiers_Code,
            f.rs_frs AS Fournisseur,
            t.rs_exportateur AS FournisseurExp,
            t.rs_importateur AS FournisseurImp,
            g.date_signat_declarant AS DateDomicilation,
            g.code_devise_ptfn,
            g.code_incoterme,
            g.fob_mont_devise AS Titre_Devise,
            g.ptfn AS Titre_Mnt,
            t.num_contrat AS FactNum,
            t.num_demande AS NDOSS,
            t.emetteur AS Titre_Banque,
            t.code_devise_reglement,
            t.cours_conversion,
            t.designation_code_org_domicialiation,
            CASE 
                WHEN t.type_transaction = 'IMPORT' THEN 'TCE'
                else 'FDE'
            END AS TypeDoss -- Change the alias to avoid confusion with existing TypeDoss
        FROM 
            dossier_g g
        INNER JOIN 
            fournisseur f ON g.code_frs = f.code_frs
        LEFT JOIN 
            document_tce2 t ON g.num_dossier = t.num_dossier
        WHERE 
            (g.type_transaction = 1 OR g.type_transaction = 2) 
            AND t.num_domicialiation != '' 
        ORDER BY 
            g.num_dossier DESC, g.date_signat_declarant 
        LIMIT 1;
    '''

    cursor_pg.execute(select_query)

    # Fetch all rows from PostgreSQL
    pg_rows = cursor_pg.fetchall()

    # Prepare new records to insert that are not in existing_xtitre
    new_records = []
    for row in pg_rows:
        titre_num = row[0]  # Assuming num_domicialiation is in the first column
        TypeDoss = row[3]  # Extract TypeDoss for this row
        FournisseurExp = row[7]  # Extract FournisseurExp
        FournisseurImp = row[8]  # Extract FournisseurImp
        database_sql = 'MAS'

        if TypeDoss == 1:
            if FournisseurImp == 'SOCIETE POLYBAT':
                database_sql = 'POLYBAT'
                print(database_sql)
            elif FournisseurImp == 'STE ((MAS))':
                database_sql = 'MAS'
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
                database_sql = 'MAS'
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
        # Fetch existing Titre_Num from xtitre
        cursor_sql.execute("SELECT Titre_Num FROM xtitre")
        xtitre_rows = cursor_sql.fetchall()

        # Fetch existing Titre_Num from xDeclaration
        cursor_sql.execute("SELECT Decla_Titre FROM xDeclaration")
        xtitre_rows_DeclaImp = cursor_sql.fetchall()

        # Fetch existing Titre_Num from SQL Server
        cursor_sql.execute("SELECT TitDecla FROM DeclartExport")
        xtitre_rows_DeclaExp = cursor_sql.fetchall()

        # Convert SQL Server titles to a set for quick lookup
        existing_xtitre = {row[0] for row in xtitre_rows}
        # Convert SQL Server titles to a set for quick lookup
        existing_xdeclaration = {row[0] for row in xtitre_rows_DeclaImp}
        # Convert SQL Server titles to a set for quick lookup
        existing_declaexport = {row[0] for row in xtitre_rows_DeclaExp}

        # FIND client by name
        existing_Tiers = {row[0] for row in xtitre_rows}

        if titre_num not in existing_xtitre:
            new_records.append(row)
    # Insertion des Titres ###############

        # Insert new records into xtitre
        insert_query = '''
                    INSERT INTO [dbo].[xtitre]
                        ([KeyTitre]
                   ,[Titre_Num]
                   ,[DateDomicilation]
                   ,[FactNum]
                   ,[Tiers_Code]
                   ,[Fournisseur]
                   ,[Titre_Banque]
                   ,[Titre_Mnt]
                   ,[Titre_Devise]
                   ,[ModePaiement]
                   ,[DelaisReg]
                   ,[DateBL]
                   ,[DateEcheance]
                   ,[Etat_Titre]
                   ,[TypeDoss]
                   ,[NDoss]
                   ,[NTTN]
                   ,[ID_XReleveH]
                   ,[NumPiece]
                   ,[BureauDouane]
                   ,[DelaiPaiement]
                   ,[IncotermeTTN]
                   ,[ListeBanques]
                   ,[LstDocReg]
                   ,[TRSTModePaiement]
                   ,[RegimeStat]
                   ,[TypeDDM]
                   ,[User_Id_Create])
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
        			   NULL, 
                       NULL,
        			   NULL,
        				NULL, 
        				%s,
        				%s,
        				%s, 
        				%s, 
        				NULL, 
        				NULL, 
                        NULL, 
        				NULL, 
        				NULL, 
        				NULL, 
        				NULL, 
        				NULL, 
        				NULL, 
        				NULL,
        				%s

                    )
        '''
        for record in new_records:
            # Execute Find Tiers
            # Get the original string from record[6]
            original_string = record[6]  # Nom fournisseur
            print("Result of original_string:", original_string)
            # Optionally store processed `Titre_Num` to avoid duplicates in future processing
            set_list_xtitre(original_string)

            # Split the string by whitespace and remove the last word
            words = original_string.split()

            if original_string != record[6]:
                if len(words) > 1:
                    modified_string = ' '.join(words[:-1]) + '%'  # Join all words except the last one
                    set_list_xtitre("words + 1"+modified_string)
                    if len(words) > 2:
                        modified_string = ' %'.join(words[:-2]) + '%'  # Join all words except the last one
                        set_list_xtitre("words + 2"+modified_string)
            else:
                if len(words) > 1:
                    modified_string = ' %'.join(words[:-1]) + '%'  # Join all words except the last one
                    # modified_string = original_string
                    set_list_xtitre("words == "+modified_string)

            # Fetch existing Tiers from SQL Server
            queryFindTiers = "SELECT * FROM tiers " \
                                    "WHERE (Tiers_Type = '07' or Tiers_Type = '02' or Tiers_Type = '01') AND Tiers_rs LIKE '%s'"
            # Generate the query with actual values for debugging
            formatted_query2 = queryFindTiers % modified_string

            print("Result of FindTiersExecute:", formatted_query2)
            # Optionally store processed `Titre_Num` to avoid duplicates in future processing
            set_list_xtitre(formatted_query2)
            # Execute the insert query
            cursor_sql.execute(formatted_query2)
            # search_value = modified_string + '%'  # Append '%' to match any characters after
            # cursor_sql.execute(queryFindTiers, (search_value,))
            FindTiersExecute = cursor_sql.fetchall()
            print("Result of len FindTiersExecute:", FindTiersExecute[0][2])
            # Optionally store processed `Titre_Num` to avoid duplicates in future processing
            set_list_xtitre(FindTiersExecute[0][2])
            # Check if the third row exists in FindTiersExecute and get "fournisseur"
            if len(FindTiersExecute) > 0:
                fournisseur = FindTiersExecute[0][2]  # Assuming this row has "fournisseur" data
                Tiers_Code = FindTiersExecute[0][0]  # Tiers_Code
            else:
                fournisseur = record[6]  # Default or fallback if the third row doesn't exist
                Tiers_Code = record[5]  # Tiers_Code
            print("Result of Tiers_Code:", Tiers_Code)
            # Optionally store processed `Titre_Num` to avoid duplicates in future processing
            set_list_xtitre(Tiers_Code)

            # Execute Find Banque
            # Get the original string from record[6]
            original_string_Banque = record[16]  # Nom fournisseur
            # Split the string by whitespace and remove the last word
            words_Banque = original_string_Banque.split()
            if len(words_Banque) > 0:
                modified_string_banque = ' '.join(word[:3] for word in words_Banque) + '%'
                print("Result of modified_string_banque:", words_Banque)
                # Optionally store processed `Titre_Num` to avoid duplicates in future processing
                set_list_xtitre(words_Banque)
                # Fetch existing Tiers from SQL Server
                queryFindBanque = "select distinct Banque_XRT from Banque " \
                                          "where Banque_XRT is not null AND Banque_XRT LIKE '%s'"
                # Generate the query with actual values for debugging
                formatted_query_banque = queryFindBanque % modified_string_banque
                print("Result of queryFindBanque:", queryFindBanque)
                # Optionally store processed `Titre_Num` to avoid duplicates in future processing
                set_list_xtitre(queryFindBanque)
                # Execute the insert query
                cursor_sql.execute(formatted_query_banque)
                # search_value = modified_string + '%'  # Append '%' to match any characters after
                # cursor_sql.execute(queryFindTiers, (search_value,))
                FindBanqueExecute = cursor_sql.fetchall()
                # print("Result of len FindTiersExecute:", FindBanqueExecute[0][0])
                # Check if the third row exists in FindTiersExecute and get "fournisseur"
                if len(FindTiersExecute) > 0:
                    banque = FindBanqueExecute[0][0] + '01'  # Assuming this row has "fournisseur" data
                else:
                    banque = record[16]

            key_titre = str(uuid.uuid4())  # Generate a unique KeyTitre
            titre_num = record[0]  # Titre_Num
            ndoss = record[1]  # NDoss
            nttn = record[2]  # NTTN
            type_doss = record[3]  # TypeDoss
            # Tiers_Code = record[5]  # Tiers_Code
            # fournisseur = record[6]  # Fournisseur
            date_domicilation = record[9]  # DateDomicilation
            titre_mnt = record[13]  # Titre_Mnt
            titre_devise = record[10]  # Titre_Devise
            fact_num = record[14]  # FactNum
            # banque = record[16]  # Titre_Banque
            TypeDoss = record[20]  # TypeDoss
            NDOSS = record[15]  # NDOSS
            # Generate the query with actual values for debugging
            formatted_query = insert_query % (
                key_titre, titre_num, date_domicilation, fact_num, Tiers_Code, fournisseur,
                banque, titre_mnt, titre_devise, 1,  TypeDoss, NDOSS, nttn, 'TTNAUTO'
            )
            # Print the formatted query
            print("Executing the following query:")
            print(formatted_query)
            # Optionally store processed `Titre_Num` to avoid duplicates in future processing
            set_list_xtitre(formatted_query)
            # Execute the insert query
            cursor_sql.execute(insert_query, (
                key_titre, titre_num, date_domicilation, fact_num, Tiers_Code, fournisseur,
                banque, titre_mnt, titre_devise, 1, TypeDoss, NDOSS, nttn, 'TTNAUTO'
            ))

        # Commit the transaction after inserts
        conn_sql.commit()

    # Close the connections
    cursor_pg.close()
    conn_pg.close()
    cursor_sql.close()
    conn_sql.close()
    set_list_xtitre(f"------ Inserted {len(new_records)} new records into xtitre ------")

except Exception as e:
    print("An error occurred:", e)
    print(traceback.format_exc())
