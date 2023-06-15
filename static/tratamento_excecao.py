import sys, traceback

def tratamento_excecao() -> str:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lista_traceback = traceback.extract_tb(exc_traceback)
    
    lista_arquivo_next = []
    lista_linha_next = []
    lista_nome_next = []
    
    for contagem, dicionario in enumerate(lista_traceback):
        if contagem == 0:
            arquivo = dicionario.filename
            linha = dicionario.lineno
            nome = dicionario.name
            tipo_erro = str(exc_type.__name__)
            mensagem_erro = str(exc_value)
            arquivo = str(arquivo).split('\\')
            arquivo = arquivo[len(arquivo) - 1]
            
            detalhes_do_erro =  {
                                'arquivo' : arquivo,
                                'linha'  : linha,
                                'nome'    : nome,
                                'tipo_erro'    : tipo_erro,
                                'mensagem_erro' : mensagem_erro, # or see traceback._some_str()
                                }
        
        arquivo_next = dicionario.filename
        arquivo_next = str(arquivo_next).split('\\')
        arquivo_next = arquivo_next[len(arquivo_next) - 1]
        
        lista_arquivo_next.append(arquivo_next)
        lista_linha_next.append(dicionario.lineno)
        lista_nome_next.append(dicionario.name)
        
    detalhes_do_erro_next =  {
                                    'arquivo_next' : lista_arquivo_next,
                                    'linha_next'  : lista_linha_next,
                                    'nome_next' : lista_nome_next,
                                    }
        
    detalhes_do_erro = detalhes_do_erro | detalhes_do_erro_next
    
    
    colunas = detalhes_do_erro.keys()
    valores = ['{}:{}'.format(coluna, detalhes_do_erro[coluna]) for coluna in colunas]
    
    str_detalhes_do_erro = '|'.join(valores)
    return str_detalhes_do_erro