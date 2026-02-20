import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import unicodedata
import shutil
from PIL import Image
from funcao_erros import validar

# --- CONFIGURAÇÕES DE NOMES E PASTAS ---
# Usamos apenas o nome do arquivo. O segredo está no os.chdir abaixo.
NOME_ARQUIVO_EXCEL = "Salas_cinema_versao_sem_erro.xlsx" 
PASTA_RESUMO = "resumo"
PASTA_IMAGENS = "imagens"
PASTA_BACKUP = "backup"

# Força o script a rodar de dentro da pasta onde ele está salvo
diretorio_do_script = os.path.dirname(os.path.abspath(__file__))
os.chdir(diretorio_do_script)

# Agora criamos as pastas dentro de 'projeto_10810' automaticamente
os.makedirs(PASTA_RESUMO, exist_ok=True)
os.makedirs(PASTA_IMAGENS, exist_ok=True)
os.makedirs(PASTA_BACKUP, exist_ok=True)

def realizar_backup():
    """Cria uma cópia exata do arquivo original na pasta backup"""
    if os.path.exists(NOME_ARQUIVO_EXCEL):
        caminho_backup = os.path.join(PASTA_BACKUP, NOME_ARQUIVO_EXCEL)
        shutil.copy2(NOME_ARQUIVO_EXCEL, caminho_backup)
        print(f"Backup realizado com sucesso em: {caminho_backup}")
    else:
        # Listar arquivos para ajudar no diagnóstico se der erro
        print(f"Erro: Arquivo {NOME_ARQUIVO_EXCEL} não encontrado.")
        print(f"Arquivos na pasta atual: {os.listdir('.')}")
        

def salvar_como_jpg(nome_arquivo):
    caminho_temp = os.path.join(PASTA_IMAGENS, "temp_plot.png")
    caminho_final = os.path.join(PASTA_IMAGENS, nome_arquivo)
    plt.savefig(caminho_temp)
    plt.close()
    img = Image.open(caminho_temp)
    rgb_img = img.convert('RGB')
    rgb_img.save(caminho_final, "JPEG")
    if os.path.exists(caminho_temp):
        os.remove(caminho_temp)

def limpar_para_estatistica(df_input):
    df_clean = df_input.copy()
    df_clean['ocupacao'] = pd.to_numeric(df_clean['ocupacao'], errors='coerce')
    df_clean = df_clean.dropna(subset=['ocupacao'])
    return df_clean

# --- INÍCIO DO PROCESSO ---

realizar_backup()

# 1. Executar Validação
tabelas, houve_erros = validar()
if not tabelas:
    print("Nenhum dado válido encontrado.")
    exit()

# 2. Preparação e Normalização
df_total = pd.concat(tabelas, ignore_index=True)
df_total.columns = [
    unicodedata.normalize("NFKD", c).encode("ascii", "ignore").decode("utf-8")
    .strip().lower().replace(" ", "") for c in df_total.columns
]

if 'semana.1' in df_total.columns:
    df_total = df_total.drop(columns=['semana.1'])

id_vars_ajustados = ["ano", "mes", "semana"]
col_salas = [c for c in df_total.columns if c.startswith("sala")]

df_long = df_total.melt(
    id_vars=id_vars_ajustados, 
    value_vars=col_salas, 
    var_name="sala", 
    value_name="ocupacao"
)

df_estat = limpar_para_estatistica(df_long)

# --- ANÁLISES SEM DECIMAIS E COM ORDENAÇÃO ---

# 1. OCUPAÇÃO TOTAL ANUAL (Sem .0)
res_ano = df_estat.groupby("ano")["ocupacao"].sum().reset_index()
with open(os.path.join(PASTA_RESUMO, "Ocupacao_Total_Anual.txt"), "w", encoding='utf-8') as f:
    df_out = res_ano.copy()
    df_out["ocupacao"] = df_out["ocupacao"].astype(int)
    f.write(df_out.rename(columns={"ano":"Ano", "ocupacao":"Ocupação"}).to_string(index=False))

plt.figure(figsize=(10, 6))
plt.bar(res_ano["ano"].astype(str), res_ano["ocupacao"], color="skyblue", edgecolor="black")
plt.title("Ocupação Total Acumulada por Ano")
plt.tight_layout()
salvar_como_jpg("1_grafico_anual_total.jpg")

# 2. HEATMAP (Sala 10 por último e sem .0)
res_sala_ano = df_estat.groupby(["sala", "ano"])["ocupacao"].sum().unstack("ano").fillna(0)
res_sala_ano = res_sala_ano.iloc[res_sala_ano.index.str.extract('(\d+)', expand=False).astype(int).argsort()]

with open(os.path.join(PASTA_RESUMO, "Evolucao_Anual_por_Sala.txt"), "w", encoding="utf-8") as f:
    f.write(res_sala_ano.astype(int).reset_index().rename(columns={"sala":"Sala/Ano"}).to_string(index=False))

# Gráfico Heatmap
plt.figure(figsize=(14, 8))
im = plt.imshow(res_sala_ano, aspect="auto", cmap="YlGnBu")
plt.colorbar(im)
plt.xticks(range(len(res_sala_ano.columns)), res_sala_ano.columns)
plt.yticks(range(len(res_sala_ano.index)), res_sala_ano.index)
for i in range(len(res_sala_ano.index)):
    for j in range(len(res_sala_ano.columns)):
        v = int(res_sala_ano.iloc[i, j])
        plt.text(j, i, str(v), ha="center", va="center", color="black" if v < (res_sala_ano.max().max()/2) else "white")
salvar_como_jpg("2_heatmap_ocupacao_sala_ano.jpg")

# 3. MÉDIA DE OCUPAÇÃO POR SALA
res_media_sala_ano = (
    df_estat
    .groupby(["sala", "ano"])["ocupacao"]
    .mean()
    .unstack("ano")
)

# Ordenação Natural
res_media_sala_ano = res_media_sala_ano.iloc[
    res_media_sala_ano.index.str.extract('(\d+)', expand=False).astype(int).argsort()
]

res_media_sala_ano_excel = res_media_sala_ano.reset_index()
res_media_sala_ano_excel = res_media_sala_ano_excel.rename(columns={"sala": "Sala/Ano"})

with open(os.path.join(PASTA_RESUMO, "Ocupacao_Media_Sala_por_Ano.txt"), "w", encoding="utf-8") as f:
    f.write(res_media_sala_ano_excel.to_string(index=False, float_format="%.2f"))

plt.figure(figsize=(12, 6))
res_media_sala_ano.T.plot(marker="o", ax=plt.gca())
plt.title("Média de Ocupação por Sala ao Longo dos Anos")
plt.legend(title="Sala", bbox_to_anchor=(1.05, 1))
plt.tight_layout()
salvar_como_jpg("3_grafico_media_ocupacao_linhas.jpg")

# 4. ESTATÍSTICA MENSAL
res_mensal_ano = (
    df_estat
    .groupby(["mes", "ano"])["ocupacao"]
    .sum()
    .unstack("ano")
    .fillna(0)
    .astype(int)
)

res_mensal_ano_final = res_mensal_ano.reset_index()
res_mensal_ano_final = res_mensal_ano_final.rename(columns={"mes": "Mês/Ano"})
res_mensal_ano_final.columns.name = None

with open(os.path.join(PASTA_RESUMO, "Estatisticas_Mensais_por_Ano.txt"), "w", encoding="utf-8") as f:
    f.write(res_mensal_ano_final.to_string(index=False))

anos_disponiveis = sorted(df_estat['ano'].unique())
fig, axes = plt.subplots(nrows=(len(anos_disponiveis) + 2) // 3, ncols=3, figsize=(18, 10))
axes = axes.flatten()
cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

for i, ano in enumerate(anos_disponiveis):
    ax = axes[i]
    dados_grafico = res_mensal_ano[ano]
    ax.plot(dados_grafico.index, dados_grafico.values, marker='o', color=cores[i % 5], linewidth=2)
    for x, y in zip(dados_grafico.index, dados_grafico.values):
        ax.annotate(f'{int(y)}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center')
    ax.set_title(f"Ano {ano}", fontweight='bold', color=cores[i % 5])
    ax.set_xticks(range(1, 13))
    ax.grid(True, linestyle='--', alpha=0.3)

for j in range(i + 1, len(axes)): fig.delaxes(axes[j])
plt.tight_layout()
salvar_como_jpg("4_grafico_mensal_por_ano.jpg")

# 5. RANKING ANUAL
ranking = df_estat.groupby(["ano", "sala"])["ocupacao"].sum().reset_index()
ranking_final = ranking.sort_values(["ano", "ocupacao"], ascending=[True, False]).groupby("ano").first().reset_index()
ranking_final["ocupacao"] = ranking_final["ocupacao"].astype(int)
ranking_final = ranking_final.rename(columns={"ano": "Ano", "sala": "Sala", "ocupacao": "Ocupacao"})

with open(os.path.join(PASTA_RESUMO, "Ranking_Melhor_Sala_por_Ano.txt"), "w", encoding="utf-8") as f:
    f.write(ranking_final.to_string(index=False))

plt.figure(figsize=(10, 6))
plt.bar(ranking_final["Ano"].astype(str), ranking_final["Ocupacao"], edgecolor="black")
plt.title("Sala com Maior Ocupação em Cada Ano")
salvar_como_jpg("5_grafico_melhor_sala_por_ano.jpg")

print("\nPROCESSO CONCLUÍDO!")