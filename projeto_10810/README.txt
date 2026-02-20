INFORMAÇÕES DO PROJETO E CUIDADOS
1. Objetivo do Script:

- O código realiza a leitura, limpeza e análise estatística de dados de ocupação de salas de cinema.
- Gera automaticamente um backup, relatórios de texto (resumo/) e gráficos de desempenho (imagens/).

2. Requisitos de Execução:

- Ficheiro Alvo: O ficheiro Excel deve ser alterado na funcao_erros.py e no estatisticas.py
- Ficheiro: Existem os ficheiros 'Salas_cinema_versao_final.xlsx' e o sem erro 'Salas_cinema_versao_sem_erro.xlsx'
- Estrutura do Excel: Os dados devem começar na Linha 3 (Header na linha 2 do Python).
- Colunas: O script procura colunas que comecem com o nome "Sala" (ex: Sala 1, Sala 2).

3. Tratamento de Dados (Limpeza):

- Valores Inválidos: Textos em colunas numéricas, valores negativos ou acima de 200 (limite máximo) são ignorados nas estatísticas.
- Log de Erros: Qualquer inconsistência encontrada no Excel é registada no ficheiro resumo/erros.txt com a indicação exata da linha e coluna.

4. Saídas Geradas:

- backup/: Cópia de segurança do arquivo original.
- resumo/: Relatórios de ocupação anual, mensal, média por sala e ranking.
- imagens/: Heatmaps e gráficos de linha/barra para visualização de tendências.

5. Resumo das análises geradas:

- Ocupação Total Anual: Permite identificar o crescimento ou queda global do volume de público ao longo dos anos.
- Heatmap (Evolução por Sala/Ano): Visualiza rapidamente quais salas são mais rentáveis e identifica padrões de sazonalidade através do contraste de cores.
- Média de Ocupação por Sala: Avalia o desempenho real de cada sala, normalizando os dados para comparar salas grandes e pequenas de forma justa.
- Estatística Mensal por Ano: Identifica os meses de "pico" (estreias e feriados) versus meses de baixa procura para planeamento estratégico.
- Ranking da Melhor Sala: Destaca a sala "vencedora" de cada ano, facilitando a análise de qual infraestrutura ou localização interna gera mais retorno.