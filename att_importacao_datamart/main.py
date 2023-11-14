# %%
import sys
import os

caminho_relativo = os.path.dirname(__file__)
caminho_relativo = os.path.dirname(caminho_relativo)
sys.path.append(caminho_relativo)
ordem_das_etapas = ['static', 'insercao_datamart', 'extracao_site', 'venv']
for etapa in ordem_das_etapas:
    sys.path.append(os.path.join(caminho_relativo, etapa))

import datetime
from static.registrar_consultar import registers
import pandas

inst_register = registers()

fichas = inst_register.consultar_notas('select * from monitoria.fichas')
registro_coluna = inst_register.consultar_notas('select * from monitoria.registro_coluna')
colunas = inst_register.consultar_notas('select * from monitoria.colunas')
registros = inst_register.consultar_notas('select * from monitoria.registros')

colunas = pandas.DataFrame(colunas)
registros = pandas.DataFrame(registros)
fichas = pandas.DataFrame(fichas)
registro_coluna = pandas.DataFrame(registro_coluna)

# %%
caminho_fichas_excel = r'\\55aspdcarq01\55atende\Administrativo\06 - Gerência Contact Center\03 - Call Center Sao Luis\02 - Monitoria de Qualidade\10.BASES'
data_atual = datetime.date.today() - datetime.timedelta(days=1)
lista_de_arquivos = os.listdir(caminho_fichas_excel)
lista_de_arquivos = [os.path.join(caminho_fichas_excel, linha) for linha in lista_de_arquivos if linha.endswith('.xls') and linha.startswith('{:02d}-{:04d}'.format(data_atual.month,data_atual.year))]


def inserir_valor(ficha_dataframe, num_monitoria_fk):
    for indice, linha in ficha_dataframe.iterrows():
        if registros.empty:
            registro_fk = inst_register.registro_sucesso(
            dicionario= {
                'num_monitoria': linha[num_monitoria_fk],
                'ficha_fk': ficha_fk
            }, tabela='monitoria.registros'
            )
        else:
            resultado_busca = registros.loc[(registros['ficha_fk'] == ficha_fk) & (registros['num_monitoria'] == linha[num_monitoria_fk])]
            if resultado_busca.empty:
                registro_fk = inst_register.registro_sucesso(
                dicionario= {
                    'num_monitoria': linha[num_monitoria_fk],
                    'ficha_fk': ficha_fk
                }, tabela='monitoria.registros'
                )
            else:
                registro_fk = resultado_busca.values[0][0]
    
        for coluna_fk_valor, valor in linha.items():
            if registro_coluna.empty:
                inst_register.registro_sucesso(
                dicionario= {
                    'coluna_fk': coluna_fk_valor,
                    'registro_fk': registro_fk,
                    'valor': valor
                }, tabela='monitoria.registro_coluna'
                )
            else:
                resultado_busca = registro_coluna.loc[(registro_coluna['coluna_fk'] == coluna_fk_valor) & (registro_coluna['registro_fk'] == registro_fk)]
                if resultado_busca.empty:
                    inst_register.registro_sucesso(
                    dicionario= {
                        'coluna_fk': coluna_fk_valor,
                        'registro_fk': registro_fk,
                        'valor': valor
                    }, tabela='monitoria.registro_coluna'
                    )


def leitura_excel(caminho, ficha_fk):
    ficha_dataframe = pandas.read_html(caminho, keep_default_na=False, decimal=',', thousands='.')
    if len(ficha_dataframe) != 1:
        raise AssertionError('Pandas leu o excel mas o tamanho de planilha foi diferente de 1')

    ficha_dataframe = ficha_dataframe[0]
    
    colunas_excel = ficha_dataframe.columns.values.tolist()

    for coluna in colunas_excel:
        if colunas.empty:
            coluna_fk = inst_register.registro_sucesso(
            dicionario= {
                'nome_coluna': coluna,
                'ficha_fk': ficha_fk
            }, tabela='monitoria.colunas'
            )
        else:
            resultado_busca = colunas.loc[(colunas['ficha_fk'] == ficha_fk) & (colunas['nome_coluna'] == coluna)]
            if resultado_busca.empty:
                coluna_fk = inst_register.registro_sucesso(
                dicionario= {
                    'nome_coluna': coluna,
                    'ficha_fk': ficha_fk
                }, tabela='monitoria.colunas'
                )
            else:
                coluna_fk = resultado_busca.values[0][0]
        if coluna == 'NUM_MONITORIA':
            num_monitoria_fk = coluna_fk
        ficha_dataframe.rename(columns={coluna: coluna_fk}, inplace=True)
        
    return (ficha_dataframe, num_monitoria_fk)

# %%
for indice_lista_arquivos, ficha in enumerate(lista_de_arquivos):
    split_ficha = ficha.split('\\')
    ficha = split_ficha[len(split_ficha) - 1]
    ficha = ficha.replace('.xls', '')
    ficha = ficha.replace('{:02d}-{:04d}'.format(data_atual.month,data_atual.year), '')
    ficha = ficha.strip()
    if fichas.empty:
        ficha_fk = inst_register.registro_sucesso(
            dicionario= {
                'nome_ficha': ficha
            }, tabela='monitoria.fichas'
            )
    else:
        resultado_busca = fichas.loc[(fichas['nome_ficha'] == ficha) & (fichas['mes'] == data_atual.month) & (fichas['ano'] == data_atual.year)]
        if resultado_busca.empty:
            ficha_fk = inst_register.registro_sucesso(
                dicionario= {
                    'nome_ficha': ficha,
                    'mes': data_atual.month,
                    'ano': data_atual.year
                }, tabela='monitoria.fichas'
                )
        else:
            ficha_fk = resultado_busca.values[0][0]
        
    (dataframe, num_monitoria_fk) = leitura_excel(caminho=lista_de_arquivos[indice_lista_arquivos], ficha_fk=ficha_fk)
    
    inserir_valor(ficha_dataframe=dataframe, num_monitoria_fk=num_monitoria_fk)
