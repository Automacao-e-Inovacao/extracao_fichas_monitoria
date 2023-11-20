import sys
import os

caminho_relativo = os.path.dirname(__file__)
caminho_relativo = os.path.dirname(caminho_relativo)
sys.path.append(caminho_relativo)
ordem_das_etapas = ['static', 'insercao_datamart', 'extracao_site', 'venv']
for etapa in ordem_das_etapas:
    sys.path.append(os.path.join(caminho_relativo, etapa))

from extracao_site.main import main as site
from insercao_datamart.main import main as insercao
from static.tratamento_excecao import tratamento_excecao
from static.registrar_consultar import registers
import time
import datetime

multiplicador = 30
data_atual = datetime.datetime.now()
numero_meses = 6
for numero_mes_anterior in range(0, numero_meses, 1):
    if numero_mes_anterior == 0:
        numero_mes_anterior = 1
    else:
        numero_mes_anterior = numero_mes_anterior * multiplicador
    data_extracao = data_atual - datetime.timedelta(days=numero_mes_anterior)

    tabela = 'public.hist_bases'
    nome_do_relatorio = 'optimus_monitoria_site'

    dicionario = {
        'carimbo_tempo': datetime.datetime.now(),
        'nome_do_relatorio': nome_do_relatorio,
        'tempo_de_extracao_seg': time.time()
    }

    inst_main_extracao = site(data_extracao=data_extracao)

    inst_registers = registers()

    if inst_registers.procurar_historico_execucao(nome_do_relatorio=nome_do_relatorio):
        dicionario['tentativa'] = inst_registers.qtd_tentativa
        try:
            inst_main_extracao.extracao_site_optimus()
            dicionario['tempo_de_extracao_seg'] = time.time() - dicionario['tempo_de_extracao_seg']
            dicionario['concluido'] = True
            # inst_registers.registro_sucesso(dicionario=dicionario, tabela=tabela)
        except:
            str_erro = tratamento_excecao()
            dicionario['tempo_de_extracao_seg'] = time.time() - dicionario['tempo_de_extracao_seg']
            dicionario['msg_erro'] = str_erro
            dicionario['tentativa'] = inst_registers.qtd_tentativa + 1
            inst_registers.registro_sucesso(dicionario=dicionario, tabela=tabela)

    tabela = 'public.hist_bases'
    nome_do_relatorio = 'fichas_importacao'

    dicionario = {
        'carimbo_tempo': datetime.datetime.now(),
        'nome_do_relatorio': nome_do_relatorio,
        'tempo_de_extracao_seg': time.time()
    }

    inst_main_extracao = insercao(data_extracao=inst_main_extracao.data_extracao)

    inst_registers = registers()

    if inst_registers.procurar_historico_execucao(nome_do_relatorio=nome_do_relatorio):
        dicionario['tentativa'] = inst_registers.qtd_tentativa
        try:
            inst_main_extracao.run()
            dicionario['tempo_de_extracao_seg'] = time.time() - dicionario['tempo_de_extracao_seg']
            dicionario['concluido'] = True
            inst_registers.registro_sucesso(dicionario=dicionario, tabela=tabela)
        except:
            str_erro = tratamento_excecao()
            dicionario['tempo_de_extracao_seg'] = time.time() - dicionario['tempo_de_extracao_seg']
            dicionario['msg_erro'] = str_erro
            dicionario['tentativa'] = inst_registers.qtd_tentativa + 1
            # inst_registers.registro_sucesso(dicionario=dicionario, tabela=tabela)
