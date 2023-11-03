import pandas as pd
import re



# Defina o número de linhas a serem puladas para ignorar o cabeçalho
num_header_rows = 4  # Por exemplo, se as primeiras 7 linhas são o cabeçalho

# Leia o arquivo CSV, pulando as linhas do cabeçalho
df = pd.read_csv("GlobalRamosYearEndReport2019.csv",  thousands=",", engine='python')

# # Agora, o DataFrame contém apenas os dados reais, sem as linhas do cabeçalho

colunmname = df.iloc[:, 0]

# Dividir a coluna "Transactions" em 8 colunas usando vírgulas como delimitador
split_data = df['Transactions in Date Sequence (continued),,,,,,,'].str.split(',', expand=True)

# Criar 8 novas colunas
df['Activity Type'] = split_data[0]
df['Description'] = split_data[1]
df['Quantity'] = split_data[2]
df['Price'] = split_data[3]
df['ex'] = split_data[4]
df['Accrued Interest'] = split_data[5]
df['Amount'] = split_data[6]
df['Currency'] = split_data[7]

# Excluir a coluna original "Transactions in Date Sequence (continued),,,,,,,,"
df.drop(columns=['Transactions in Date Sequence (continued),,,,,,,'], inplace=True)

df[['Process Settement Date', 'Trade Transaction Date', 'Activity']] = df['Activity Type'].str.split(' ', n=2, expand=True).replace('YOUR', "")

df.drop(columns=['Activity Type'], inplace=True)


filtered_df = df[df['Description'].str.contains('CALL|PUT', case=False, na=False)]
filtered_df['Operation'] = filtered_df['Description'].str.extract(r'(CALL|PUT)', flags=re.IGNORECASE)
filtered_df['Strike'] = filtered_df['Description'].str.split('@').str[1].str.replace('OPTION', '')


# Exibir o DataFrame resultante
print(df)

output_filename = "GlobalRamosYearEndReport2019_cleaned.xlsx"
df.to_excel(output_filename, index=False, engine="openpyxl")
print(f"Dados filtrados foram salvos em {output_filename}")





