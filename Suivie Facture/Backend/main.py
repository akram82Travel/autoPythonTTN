from typing import Union

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
import sqlalchemy
from dbConnection import Connection
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
conn = Connection()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
host_address = "192.168.10.216"
user = "sa"
password = "123"
database ="MAS"

# Define a Pydantic model for the request body
class DFRequest(BaseModel):
    FCT_num: str
class OFRequest(BaseModel):
    OF_num: str
# Request model for the incoming data
class SaveModePaiementFactRequest(BaseModel):
    Fact_num: str
    formData: dict
# @app.on_event("startup")
# async def startup_event():
conn.connect(host_address, user, password, database)
    # return {"message": "Connected to database"}
@app.get("/FactureTTN")
def getFactureTTN():
    output = []
    conn.connect(host_address, user, password, database)
    query = """
    select YEAR(Doc_Date) AS 'Year', xTitre.Fournisseur as 'Beneficiaire', Document.Doc_RS as 'Chantier',Doc_Num as 'Facture',
 xTitre.Fournisseur  as 'ModReglement', FORMAT(Doc_Date, 'dd/MM/yyyy') AS 'Date', 
 Doc_TTTC as 'Montant', 
 Titre_Num as 'TitreNum', 
 xTitre.Titre_Banque as 'Banque', 
 Titre_Devise as 'Devise', 
 ModRegFactExp.numFacture as 'isParam',
    CASE 
                WHEN xdeclaration.Decla_Num is not null THEN xdeclaration.Decla_Num
				 WHEN DeclartExport.NumDecl is not null THEN DeclartExport.NumDecl
                else ''
            END AS Decla_Num,
  CASE 
                WHEN xdeclaration.Decla_Num is not null THEN xdeclaration.Decla_Date
				 WHEN DeclartExport.NumDecl is not null THEN DeclartExport.DateDecl
                else ''
            END AS DateDecla
 from Document 
    inner join Tiers on Tiers.Tiers_code = Document.Tiers_code
    inner join xTitre on xTitre.FactNum = Document.Doc_Num
	left join xdeclaration on xdeclaration.decla_titre = xTitre.titre_num
	left join DeclartExport on DeclartExport.TitDecla = xTitre.titre_num
    left join ModRegFactExp on ModRegFactExp.numFacture = Document.Doc_Num
    where (Doc_nat like '1m' or Doc_nat = '2m' or Doc_Nat = '09') 
    order by Doc_Date desc
    """
    cursor = conn.get_conn().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    factureTTN = [{"Year": row[0],
                   "Beneficiaire": row[1], 
                   "Chantier": row[2], 
                   "Facture": row[3],
                   "ModReglement": row[4], 
                   "Date": row[5], 
                   "Montant": row[6], 
                   "TitreNum": row[7], 
                   "Banque": row[8], 
                   "Devise": row[9],
                   "isParam": row[10],
                   "Decla_Num": row[11],
                   "DateDecla": row[12],
                   } for row in data]
    return {"FactureTTN": factureTTN}

@app.get("/ModePaiement")
def getFactureTTN():
    output = []
    conn.connect(host_address, user, password, database)
    query = """
    select Type AS 'ModeReg_Code', Libelle as 'ModeReg_Libelle'
    from xxModeP 
    """
    cursor = conn.get_conn().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    modePaiement = [{"ModeReg_Code": row[0],
                   "ModeReg_Libelle": row[1], 
                   } for row in data]
    return {"ModePaiement": modePaiement}

@app.post("/ListModeReg/")
async def getListOF(FCT_num: DFRequest):
    output = []
    conn.connect(host_address, user, password, database)
    query = f"""
    select numFacture as 'numFacture', codeMode as 'codeMode', avance as 'avance', reception as 'reception', pose as 'pose', finmarche as 'finmarche', duree as 'duree'
    from ModRegFactExp 
    where numFacture = '{FCT_num.FCT_num}'
    """
    print(f'********{query}*****')
    cursor = conn.get_conn().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
   
    result = [{"numFacture": row[0], "codeMode": row[1], "avance": row[2], "reception": row[3], "pose": row[4], "finmarche": row[5], "duree": row[6]} for row in data]  # Extracting the first column from each row
    return {"ModePaiement": result}

@app.post("/SaveModePaiementFact/")
async def save_mode_paiement_fact(data: SaveModePaiementFactRequest):
    # Unpack the incoming data
    Fact_num = data.Fact_num
    form_data = data.formData

    # Retrieve values from formData
    codeMode = form_data.get("standardMethod")
    avance = form_data.get("advancePayment")
    duree = form_data.get("dureePayment")
    reception = form_data.get("receptionPayment")
    pose = form_data.get("postInstallationPayment")
    finmarche = form_data.get("endOfContractPayment")

    conn.connect(host_address, user, password, database)
    query = f"""
    INSERT INTO ModRegFactExp (numFacture, codeMode, avance, reception, pose, finmarche, duree)
    VALUES ('{Fact_num}', '{codeMode}', '{str(avance)}', '{str(reception)}', '{str(pose)}', '{str(finmarche)}', '{str(duree)}')
    """

    try:
        cursor = conn.get_conn().cursor()
        # Pass parameters as a dictionary
        cursor.execute(query)
        conn.get_conn().commit()  # Commit the transaction
    except Exception as e:
        conn.get_conn().rollback()  # Rollback in case of error
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(e)}")
    finally:
        cursor.close()

    return {"status": "Success", "message": "Data saved successfully"}


@app.post("/GetReglementFact/")
async def getListOF(FCT_num: DFRequest):
    output = []
    conn.connect(host_address, user, password, database)
    query = f"""
    select Reg_Num,RegD_Montant,RegD_Devise_Cours, Doc_Num, Devise_Code from reglementD where Doc_Num = '{FCT_num.FCT_num}'
    """
    print(f'********{query}*****')
    cursor = conn.get_conn().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
   
    result = [{"Reg_Num": row[0], "RegD_Montant": row[1], "RegD_Devise_Cours": row[2], "Doc_Num": row[3], "Devise_Code": row[4]} for row in data]  # Extracting the first column from each row
    return {"ModePaiement": result}

@app.post("/GetListeFag/")
async def getListOF(FCT_num: DFRequest):
    output = []
    conn.connect(host_address, user, password, database)
    query = f"""
    select dd1.Doc_Num, dd1.Doc_RS, dd1.Doc_Date, dd1.Doc_TTTC from DocumentD dd
    inner join Document dd1 on dd1.doc_num = dd.DocDOrigine
    where dd.Doc_Num = '{FCT_num.FCT_num}'
    group by dd1.Doc_Num, dd1.Doc_RS, dd1.Doc_Date, dd1.Doc_TTTC
    """
    print(f'********{query}*****')
    cursor = conn.get_conn().cursor()
    cursor.execute(query)
    data = cursor.fetchall()
   
    result = [{"Doc_Num": row[0], "Doc_RS": row[1], "Doc_Date": row[2], "Doc_TTTC": row[3]} for row in data]  # Extracting the first column from each row
    return {"ModePaiement": result}