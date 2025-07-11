import flet as ft
import re
from controls import comparar

#local onde ficam as pesquisas Regex, para poder localizar as informações divergentes nos XML e trocar a cor para vermelho----------------------------------------------------------------------------

cpf_regex = re.compile(r"<cpfTrab>(.*?)</cpfTrab>", re.DOTALL)
matricula_regex = re.compile(r"<matricula>(.*?)</matricula>", re.DOTALL)
data_admissao_regex = re.compile(r"<dtAdm>(.*?)</dtAdm>", re.DOTALL)
data_atividade_regex = re.compile(r"<dtIniCondicao>(.*?)</dtIniCondicao>", re.DOTALL)
data_inicio_regex = re.compile(r"<dtInicio>(.*?)</dtInicio>", re.DOTALL)

empregador_regex = re.compile(r"<ideEmpregador>\s+<tpInsc>[12]</tpInsc>\s+<nrInsc>(.*?)</nrInsc>", re.DOTALL)
local_de_trabalho_regex = re.compile(r"<localTrabGeral>\s+<tpInsc>[134]</tpInsc>\s+<nrInsc>(.*?)</nrInsc>", re.DOTALL)
local_de_trabalho_sistema_regex = re.compile(r"</dscSetor>\s+<tpInsc>[134]</tpInsc>\s+<nrInsc>(.*?)</nrInsc>", re.DOTALL)

sucessao_de_vinculo_Local_de_trabalho_regex = re.compile(r"<sucessaoVinc>\s+<tpInsc>[12]</tpInsc>\s+<nrInsc>(.*?)</nrInsc>", re.DOTALL)
sucessao_de_vinculo_matricula_regex = re.compile(r"<matricAnt>(.*?)</matricAnt>", re.DOTALL)
sucessao_de_vinculo_transferencia_regex = re.compile(r"<dtTransf>(.*?)</dtTransf>", re.DOTALL)


#Função que divide o XML em linhas e manda para a extrura do modal----------------------------------------------------------------------------

def modal_separado_por_linhas(xml_esquerdo, xml_direito, divergentes):

    # Variavel para o texto na parte de cima do modal
    header = ft.Text(
        f"Aqui você consegue ver o local onde ficam as informações divergentes nos XML\n", 
        size=20, 
        text_align="Center", 
        color=ft.colors.ORANGE_700
    )         

    # Separar os textos em linhas
    xml_esquerdo_separado_em_linhas = xml_esquerdo[0].splitlines()

    xml_direito_separado_em_linhas = xml_direito[0].splitlines()   
    
    # Tratamento da lista de divergentes, para poder fazer a comparação
    divergencias_no_painel_esquerdo = divergentes[0]
    divergencias_no_painel_direito = divergentes[1]
  

    # cria lista com pesquisa Regex e o resultado dela para comparar no conteiner de texto
    lista_regex_vermelho_esquerda = []
    lista_regex_vermelho_direita = [] 

    conteiner_regex_esquerdo = conteiner(xml_esquerdo)  
    conteiner_regex_direito = conteiner(xml_direito)
    
    
    # Adiciona os valores capturados às listas de divergentes
    for chave, valor in conteiner_regex_esquerdo.items():
        if chave in divergencias_no_painel_esquerdo:
            lista_regex_vermelho_esquerda.append(valor)
            print("Print com os valores", lista_regex_vermelho_esquerda)

    for chave, valor in conteiner_regex_direito.items():
        if chave in divergencias_no_painel_direito:                        
            lista_regex_vermelho_direita.append(valor)
            print("Print com os valores", lista_regex_vermelho_direita)

    # Tags que vão ser coloridas
    tags_desejadas = ["<cpfTrab>", "<matricula>", "<dtAdm>", "<nrInsc>", "<dtTransf>", "<matricAnt>", "<dtIniCondicao>", "<dtInicio>"]

    # Cria containers para cada texto
    conteudo_esquerdo = []
    conteudo_direito = []

    for item in xml_esquerdo_separado_em_linhas:
        if any(tag in item for tag in tags_desejadas):
            if any(valor in item for valor in lista_regex_vermelho_esquerda):
                conteudo_esquerdo.append(ft.Text(item, color=ft.colors.RED))
            else:
                conteudo_esquerdo.append(ft.Text(item,  color=ft.colors.BLACK))  # adiciona normalmente se tag existe, mas não é divergente
        else:
            conteudo_esquerdo.append(ft.Text(item,  color=ft.colors.BLACK))  # adiciona normalmente se não tem tag

    # mesmo para o lado direito:
    for item in xml_direito_separado_em_linhas:
        if any(tag in item for tag in tags_desejadas):
            if any(valor in item for valor in lista_regex_vermelho_direita):
                conteudo_direito.append(ft.Text(item, color=ft.colors.RED))
            else:
                conteudo_direito.append(ft.Text(item,  color=ft.colors.BLACK))
        else:
            conteudo_direito.append(ft.Text(item,  color=ft.colors.BLACK))
    
    
    # Estrutura da exibição do texto no modal
    esquerdo = ft.ListView(
        conteudo_esquerdo,
        spacing=5,
        expand=True,
        width=200,  
        height=700,  
    )
    
    direito = ft.ListView(
        conteudo_direito,
        spacing=5,        
        expand=True,
        width=200,  
        height=700,       
    )
        
    corpo = ft.ListView(        
        [
        ft.Container(
        content = ft.Row([esquerdo, direito], expand=True),
        border_radius=20,
        padding=5,
        expand=True,
        bgcolor=ft.colors.WHITE,                        
        )
    ],
    )

    # variavel principal do modal
    modal_completo = ft.AlertDialog(
        modal=True,
        title=header,
        content=corpo,
        bgcolor=ft.colors.BLUE_GREY_900,                
    )
    
    return modal_completo

# -----------------------------------------------------------------------------------------------------conteiner com as informações:

def conteiner(xml):
    empregador = capturar_empregador(xml)
    local_de_trabalho = capturar_local_de_trabalho(xml)
    cpf = capturar_cpf(xml)    
    matricula = capturar_matricula(xml)
    data_admissao = capturar_data_admissao(xml)
    transf_sucessao = capturar_sucessao_transf(xml)
    mat_sucessao = capturar_sucessao_matricula(xml)
    local_sucessao = capturar_sucessao_local(xml)

    dados = {"Cpf":cpf, 
             "Matricula":matricula, 
             "Empresa Empregadora":empregador, 
             "Data de Início do Empregado":data_admissao, 
             "Empresa do Local de Trabalho":local_de_trabalho, 
             "Data da transferência":transf_sucessao, 
             "Matricula Antes da Transferência":mat_sucessao,
             "Empresa Antes da Transferência":local_sucessao,
             }
    
    return dados

# -----------------------------------------------------------------------------------------------------funções para capturar as informações dos XML:

def capturar_empregador(xml):
    for item in xml:
        match = empregador_regex.search(item)
        if match:
           empregador = match.group(1)
        else:
            empregador = "Erro ao capturar empregador"
    return empregador

def capturar_local_de_trabalho(xml):
    for item in xml:
        match1 = local_de_trabalho_regex.search(item)
        match2 = local_de_trabalho_sistema_regex.search(item)        
        if match1:
           local_de_trabalho = match1.group(1)
        elif match2:
           local_de_trabalho = match2.group(1)
        
        else:
            local_de_trabalho = "Erro ao capturar local_de_trabalho"
    return local_de_trabalho

def capturar_cpf(xml):
    for item in xml:
        match = cpf_regex.search(item)
        if match:
           cpf = match.group(1)
        else:
            cpf = "Erro ao capturar CPF"
    return cpf

def capturar_matricula(xml):
    for item in xml:
        match = matricula_regex.search(item)
        if match:
           matricula = match.group(1)
        else:
            matricula = "Erro ao capturar matricula"
    return matricula

def capturar_data_admissao(xml):
    for item in xml:
        match1 = data_admissao_regex.search(item)
        match2 = data_atividade_regex.search(item)
        match3 = data_inicio_regex.search(item)
        if match1:
            data_admissao = match1.group(1)
        elif match2:
            data_admissao = match2.group(1)
        elif match3:
            data_admissao = match3.group(1)
        else:
            data_admissao = "Erro ao capturar data_admissao"

    return data_admissao


# -----------------------------------------------------------------------------------------------------funções para capturar as informações de sucessão de vínculo dos XML:

def capturar_sucessao_local(xml):
    for item in xml:
        match = sucessao_de_vinculo_Local_de_trabalho_regex.search(item)
        if match:
           local = match.group(1)
        else:
            local = "Não encontrada sucessão de vinculo"
    return local

def capturar_sucessao_matricula(xml):
    for item in xml:
        match = sucessao_de_vinculo_matricula_regex.search(item)
        if match:
           matricula = match.group(1)        
        else:
            matricula = "Não encontrada sucessão de vinculo"
    return matricula

def capturar_sucessao_transf(xml):
    for item in xml:
        match = sucessao_de_vinculo_transferencia_regex.search(item)          
        if match:
           data_transf = match.group(1)                   
        else:
            data_transf = "Não encontrada sucessão de vinculo"
    return data_transf