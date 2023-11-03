import os.path

import pandas as pd
import shutil
import re


# Defina o número de linhas a serem puladas para ignorar o cabeçalho
num_header_rows = 1  # Por exemplo, se as primeiras 7 linhas são o cabeçalho

caminho = os.path.join("modelos/planilhas/GlobalRamosYearEndReport2022.csv")

# Leia o arquivo CSV, pulando as linhas do cabeçalho
df = pd.read_csv(caminho, thousands=",", engine='python')
print(df.columns)

# extract_option(df)


# Agora, o DataFrame contém apenas os dados reais, sem as linhas do cabeçalho
df_cleaned = df.dropna(how='all').dropna(axis=1, how='all')


#COMBINA AS COLUNAS
df['Combined_Description'] = df['Transactions in Date Sequence (continued)'].fillna('') + ' ' + df['Unnamed: 1'].fillna('')


# procura call & put
filtered_df = df[df['Combined_Description'].str.contains('call|put', case=False, na=False)].copy()

columns_to_drop = ["Transactions in Date Sequence (continued)", "Unnamed: 1", "Unnamed: 4"]
filtered_df.drop(columns=columns_to_drop, inplace=True)


filtered_df.rename(columns={
    'Unnamed: 2': 'Quantity',
    'Unnamed: 3': 'Price',
    'Unnamed: 5': 'Amount',
    'Unnamed: 6': 'Currency'
}, inplace=True)

filtered_df[['Process Settement Date',
             'Trade Transaction Date',
             'Activity Type',
             ]] = filtered_df['Combined_Description'].str.split(' ', n=2, expand=True).replace('YOUR', "")


filtered_df[['Action', 'Quantity', 'Description', 'Values']] = filtered_df['Activity Type'].str.split(',', n=3, expand=True)


# Exclui a coluna original 'Activity Type'
# df.drop(columns=['Activity Type'], inplace=True)

filtered_df.drop(columns=['Activity Type', 'Combined_Description'], inplace=True)

filtered_df['Combined_Quantity'] = filtered_df['Price'].fillna('') + ' ' + filtered_df['Description'].fillna('')
filtered_df.drop(columns=['Price', 'Description'], inplace=True)

filtered_df[['Price', 'Amount_Currency']] = filtered_df['Values'].str.split(',', n=1, expand=True)



# Exibe o DataFrame com as colunas renomeadas e a coluna excluída

output_filename = "2022_cleaned.xlsx"
filtered_df.to_excel(output_filename, index=False, engine="openpyxl")


if output_filename not in os.path.join("."):
    shutil.move(output_filename, "relatorios")
else:
    print("here")


print(f" Os  Dados filtrados  foram salvos em {output_filename}")

print(os.listdir("relatorios/"))