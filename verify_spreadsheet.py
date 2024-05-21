import pandas as pd
import os
import requests

def download_spreadsheet(url, file_path):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)

def verify_data(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        issues = []
        if df['Date'].isnull().any():
            issues.append('Há datas ausentes na planilha.')
        if df.duplicated().any():
            issues.append('Há registros duplicados na planilha.')
        if (df['Value'] < 0).any():
            issues.append('Há valores negativos na planilha.')
        return issues
    except pd.errors.ParserError as e:
        print(f"Erro de análise: {e}")
        return []

def generate_report(issues, report_path):
    with open(report_path, 'w') as file:
        if issues:
            file.write("Problemas encontrados:\n")
            for issue in issues:
                file.write(f"- {issue}\n")
        else:
            file.write("Nenhum problema encontrado.")

spreadsheet_url = 'https://drive.google.com/uc?export=download&id=14bOzCd_cD6IDMu9_9gGLLqKaBL-_gqaA'
spreadsheet_path = '/mnt/c/Users/tpaul/Downloads/consultas_previas.csv' # Mude esse caminho para o caminho onde ficará o arquivo.
report_path = 'relatorio.txt'

download_spreadsheet(spreadsheet_url, spreadsheet_path)
issues = verify_data(spreadsheet_path)
generate_report(issues, report_path)

os.remove(spreadsheet_path)
