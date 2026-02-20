import pandas as pd
import os
import numpy as np

# --- CONFIGURAÇÕES DINÂMICAS ---
# Detecta a pasta onde este arquivo .py está salvo
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
NOME_ARQUIVO_EXCEL = "Salas_cinema_versao_sem_erro.xlsx" 
HEADER_LINHA = 2
LIMITE_MAX = 200

# Define a pasta resumo dentro do diretório do projeto
PASTA_RESUMO = os.path.join(DIRETORIO_ATUAL, "resumo")
os.chdir(DIRETORIO_ATUAL)

def validar():
    # Garante que a pasta resumo exista
    os.makedirs(PASTA_RESUMO, exist_ok=True)
    FICHEIRO_ERROS = os.path.join(PASTA_RESUMO, "erros.txt")
    
    erros = []
    tabelas = []

    # --- CORREÇÃO AQUI: Em vez de listar a pasta, usamos apenas o arquivo alvo ---
    caminho = os.path.join(DIRETORIO_ATUAL, NOME_ARQUIVO_EXCEL)
    
    if not os.path.exists(caminho):
        print(f"Erro: O arquivo {NOME_ARQUIVO_EXCEL} não foi encontrado.")
        return [], False

    try:
        # Lemos apenas o arquivo específico definido nas configurações
        df = pd.read_excel(caminho, header=HEADER_LINHA)
        df = df.dropna(axis=1, how="all")
        
        colunas_salas = [c for c in df.columns if str(c).startswith("Sala")]

        for col in colunas_salas:
            valores_num = pd.to_numeric(df[col], errors="coerce")
            
            # Máscaras de erro
            invalidos = valores_num.isna() & df[col].notna()
            negativos = valores_num < 0
            grandes = valores_num > LIMITE_MAX
            
            todos_erros = invalidos | negativos | grandes

            # Registar erros
            for idx in df[todos_erros].index:
                linha_excel = idx + HEADER_LINHA + 2
                valor_errado = df.loc[idx, col]
                erros.append(f"Arquivo: {NOME_ARQUIVO_EXCEL} | Linha: {linha_excel} | Coluna: {col} | Valor: {valor_errado}")

            # Limpeza
            df.loc[todos_erros, col] = np.nan 

        tabelas.append(df)
        
    except Exception as e:
        erros.append(f"Erro crítico no arquivo {NOME_ARQUIVO_EXCEL}: {e}")
    # --- FIM DA CORREÇÃO ---

    # Escreve o log de erros
    with open(FICHEIRO_ERROS, "w", encoding="utf-8") as f:
        if erros:
            for erro in erros:
                f.write(erro + "\n")
        else:
            f.write("Nenhum erro encontrado no arquivo.")
    
    return tabelas, len(erros) > 0