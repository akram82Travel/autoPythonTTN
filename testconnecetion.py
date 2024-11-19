import pymssql
import psycopg2
import uuid
import os
import traceback

# Track the last processed doc_id in a file
LAST_PROCESSED_FILE = 'last_TTN.txt'
LAST_PROCESSED_FILE_XT = 'list_Xtitre.txt'
new_records = []
def set_list_xtitre(titre_num):
    with open(LAST_PROCESSED_FILE_XT, 'a') as file:
        file.write(str(titre_num) + '\n')

# Connection details
server_sql = '192.168.10.216'
database_sql = 'TESTMAS'

server_pg = '192.168.10.217'
database_pg = 'APP_TRANS_1'

try:
    # Establish connection to SQL Server for xtitre
    conn_sql = pymssql.connect(server=server_sql, database=database_sql, port=1433, user='sa', password='123')
    cursor_sql = conn_sql.cursor()

    # Fetch existing Titre_Num from xDeclaration
    cursor_sql.execute("SELECT Decla_Titre FROM xDeclaration")
    xtitre_rows_DeclaImp = cursor_sql.fetchall()

    # Fetch existing Titre_Num from SQL Server
    cursor_sql.execute("SELECT TitDecla FROM DeclartExport")
    xtitre_rows_DeclaExp = cursor_sql.fetchall()


    # Convert SQL Server titles to a set for quick lookup
    existing_xdeclaration = {row[0] for row in xtitre_rows_DeclaImp}
    # Convert SQL Server titles to a set for quick lookup
    existing_declaexport = {row[0] for row in xtitre_rows_DeclaExp}

    # Establish connection to PostgreSQL
    conn_pg = psycopg2.connect(dbname=database_pg, user='zedgres', password='zedgres', host=server_pg, port='5432', sslmode='disable')
    cursor_pg = conn_pg.cursor()

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
        LIMIT 10;

    '''

    cursor_pg.execute(select_query)

    # Fetch all rows from PostgreSQL
    pg_rows = cursor_pg.fetchall()

    # Prepare new records to insert that are not in existing_declarations_Import
    new_records_DeclImp = []
    for row in pg_rows:
        titre_num = row[0]  # Assuming num_domicialiation is in the first column
        if titre_num not in existing_xdeclaration:
            new_records_DeclImp.append(row)

    # Prepare new records to insert that are not in existing_declarations_Export
    new_records_DeclExp = []
    for row in pg_rows:
        titre_num = row[0]  # Assuming num_domicialiation is in the first column
        if titre_num not in existing_declaexport:
            new_records_DeclExp.append(row)


    ########## Insertion des Titres ###############

    ########## Insertion des declarations Import ######

    try:
        # Insert new records into XDECLARATION
        insert_query_DeclaImport = '''
                            INSERT INTO [dbo].[xDeclaration]
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
                            NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL
           ,NULL

                            )
                '''
        for record in new_records:
            key_titre = str(uuid.uuid4())  # Generate a unique KeyTitre
            titre_num = record[0]  # Titre_Num
            ndoss = record[1]  # NDoss
            nttn = record[2]  # NTTN
            type_doss = record[3]  # TypeDoss
            Tiers_Code = record[5]  # Tiers_Code
            fournisseur = record[6]  # Fournisseur
            date_domicilation = record[9]  # DateDomicilation
            titre_mnt = record[13]  # Titre_Mnt
            titre_devise = record[10]  # Titre_Devise
            fact_num = record[14]  # FactNum
            banque = record[16]  # Titre_Banque
            TypeDoss = record[20]  # TypeDoss
            NDOSS = record[15]  # NDOSS

            # Generate the query with actual values for debugging
            formatted_query = insert_query_DeclaImport % (
                key_titre, titre_num, date_domicilation, fact_num, Tiers_Code, fournisseur,
                banque, titre_mnt, titre_devise, 0,  TypeDoss, NDOSS, nttn, 'TTNAUTO'
            )

            # Print the formatted query
            print("Executing the following query:")
            print(formatted_query)

            # Execute the insert query
            cursor_sql.execute(insert_query_DeclaImport, (
                key_titre, titre_num, date_domicilation, fact_num, Tiers_Code, fournisseur,
                banque, titre_mnt, titre_devise, 0, TypeDoss, NDOSS, nttn, 'TTNAUTO'
            ))

            # Optionally store processed `Titre_Num` to avoid duplicates in future processing
            set_list_xtitre(insert_query_DeclaImport)
        # Commit the transaction after inserts
        conn_sql.commit()
    except pymssql.OperationalError as e:
        conn_sql.rollback()
        print(f"Error during insertion: {e}")
    ########## Insertion des declarations Export ######

    try:
        # Insert new records into DeclaExport
        insert_query_DeclaExport = '''
                            INSERT INTO [dbo].[DeclartExport]
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
                            NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL
                               ,NULL

                            )
                '''
        for record in new_records:
            key_titre = str(uuid.uuid4())  # Generate a unique KeyTitre
            titre_num = record[0]  # Titre_Num
            ndoss = record[1]  # NDoss
            nttn = record[2]  # NTTN
            type_doss = record[3]  # TypeDoss
            Tiers_Code = record[5]  # Tiers_Code
            fournisseur = record[6]  # Fournisseur
            date_domicilation = record[9]  # DateDomicilation
            titre_mnt = record[13]  # Titre_Mnt
            titre_devise = record[10]  # Titre_Devise
            fact_num = record[14]  # FactNum
            banque = record[16]  # Titre_Banque
            TypeDoss = record[20]  # TypeDoss
            NDOSS = record[15]  # NDOSS

            # Generate the query with actual values for debugging
            formatted_query = insert_query_DeclaExport % (
                key_titre, titre_num, date_domicilation, fact_num, Tiers_Code, fournisseur,
                banque, titre_mnt, titre_devise, 0,  TypeDoss, NDOSS, nttn, 'TTNAUTO'
            )

            # Print the formatted query
            print("Executing the following query:")
            print(formatted_query)

            # Execute the insert query
            cursor_sql.execute(insert_query_DeclaExport, (
                key_titre, titre_num, date_domicilation, fact_num, Tiers_Code, fournisseur,
                banque, titre_mnt, titre_devise, 0, TypeDoss, NDOSS, nttn, 'TTNAUTO'
            ))

            # Optionally store processed `Titre_Num` to avoid duplicates in future processing
            set_list_xtitre(insert_query_DeclaExport)
        # Commit the transaction after inserts
        conn_sql.commit()
    except pymssql.OperationalError as e:
        conn_sql.rollback()
        print(f"Error during insertion: {e}")

    # Close the connections
    cursor_pg.close()
    conn_pg.close()
    cursor_sql.close()
    conn_sql.close()
    print(f"Inserted {len(new_records)} new records into xtitre")
except Exception as e:
    print("An error occurred:", e)
    print(traceback.format_exc())