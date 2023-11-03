import os.path

import pandas as pd
import re



# Defina o número de linhas a serem puladas para ignorar o cabeçalho
num_header_rows = 4  # Por exemplo, se as primeiras 7 linhas são o cabeçalho
caminho = os.path.join("modelos/planilhas/GlobalRamosExtratos2018.csv")

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

filtered_df['Operation'] = filtered_df['Description'].str.extract(r'(CALL|PUT)', flags=re.IGNORECASE)
filtered_df['Strike'] = filtered_df['Description'].str.split('@').str[1].str.replace('OPTION', '')


print(filtered_df.columns)

# Exibe o DataFrame com as colunas renomeadas e a coluna excluída
print(filtered_df)

output_filename = "GlobalRamosYearEndReport2018_cleaned.xlsx"
filtered_df.to_excel(output_filename, index=False, engine="openpyxl")

print(f"Dados filtrados foram salvos em {output_filename}")
