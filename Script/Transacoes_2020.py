import os.path

import pandas as pd
import shutil
import re



# Defina o número de linhas a serem puladas para ignorar o cabeçalho
num_header_rows = 4  # Por exemplo, se as primeiras 7 linhas são o cabeçalho

caminho = os.path.join("modelos/planilhas/GlobalRamosYearEndReport2020.csv")
# Leia o arquivo CSV, pulando as linhas do cabeçalho
df = pd.read_csv(caminho,  thousands=",", engine='python')

print(df.columns)
df.drop(columns=['Unnamed: 4'], inplace=True)

# Agora, o DataFrame contém apenas os dados reais, sem as linhas do cabeçalho


df_cleaned = df.dropna(how='all').dropna(axis=1, how='all')
# Renomeia as colunas
df_cleaned.rename(columns={
    'Transactions in Date Sequence': 'Datas',
    'Unnamed: 1': 'Description',
    'Unnamed: 2': 'Quantity',
    'Unnamed: 3': 'Price',
    'Unnamed: 5': 'Amount',
    'Unnamed: 6': 'Currency'
}, inplace=True)

df_cleaned[['Process Settement Date', 'Trade Transaction Date', 'Activity Type']] = df_cleaned['Datas'].str.split(' ', n=2, expand=True).replace('YOUR', "")

df_cleaned.drop(columns=['Datas'], inplace=True)

filtered_df = df_cleaned[df_cleaned['Description'].str.contains('CALL|PUT', case=False, na=False)].copy()

print(filtered_df.columns)

# Exibe o DataFrame com as colunas renomeadas e a coluna excluída
print(filtered_df)

output_filename = "2020_cleaned.xlsx"
filtered_df.to_excel(output_filename, index=False, engine="openpyxl")

print(f"Dados filtrados foram salvos em {output_filename}")


if output_filename not in os.listdir("."):
    shutil.move("2020_cleaned.xlsx", "relatorios/")
else:
    os.remove("2020_cleaned.xlsx")
    print("O arquivo já estáva no local e foi removido")

print(os.listdir("relatorios"))



