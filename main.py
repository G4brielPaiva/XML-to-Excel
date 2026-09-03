import xmltodict
import os
import pandas as pd

def get_info(file_name, values):
    with open(f'XMLtoXLSX/nfs/{file_name}', "rb") as xml_file:
        dic_files = xmltodict.parse(xml_file)
        
        if "NFe" in  dic_files:
            infos_nf = dic_files["NFe"]["infNFe"]
        else:
            infos_nf = dic_files["nfeProc"]["NFe"]["infNFe"]

        nf_id = infos_nf["@Id"]
        company = infos_nf["emit"]["xNome"]
        client_name = infos_nf["dest"]["xNome"]
        address = infos_nf["dest"]["enderDest"]
        if "vol" in infos_nf["transp"]:
            weight = infos_nf["transp"]["vol"]["pesoB"]
        else:
            weight = "Não Informado"
        values.append([nf_id, company, client_name, address, weight])
        

files_list = os.listdir("XMLtoXLSX/nfs")

columns = ["File_ID", "Company", "client_name", "Address", "Weight"]
values = []

print(files_list)

for file_name in files_list:
    get_info(file_name, values)

table = pd.DataFrame(columns=columns, data=values)
print(table)
table.to_excel("Nfs.xlsx", index=False)