import re
import flet as ft

# -----------------------------------------------------------------------------------------------------consts com os regex para a pesquisa das informações nos XML 

cpf_regex = re.compile(r"<cpfTrab>(.*?)</cpfTrab>", re.DOTALL)
matricula_regex = re.compile(r"<matricula>(.*?)</matricula>", re.DOTALL)
data_admissao_regex = re.compile(r"<dtAdm>(.*?)</dtAdm>", re.DOTALL)
data_atividade_regex = re.compile(r"<dtIniCondicao>(.*?)</dtIniCondicao>", re.DOTALL)

empregador_regex = re.compile(r"<ideEmpregador>\s+<tpInsc>[12]</tpInsc>\s+<nrInsc>(.*?)</nrInsc>", re.DOTALL)
local_de_trabalho_regex = re.compile(r"<localTrabGeral>\s+<tpInsc>[134]</tpInsc>\s+<nrInsc>(.*?)</nrInsc>", re.DOTALL)
local_de_trabalho_sistema_regex = re.compile(r"</dscSetor>\s+<tpInsc>[134]</tpInsc>\s+<nrInsc>(.*?)</nrInsc>", re.DOTALL)

sucessao_de_vinculo_Local_de_trabalho_regex = re.compile(r"<sucessaoVinc>\s+<tpInsc>[12]</tpInsc>\s+<nrInsc>(.*?)</nrInsc>", re.DOTALL)
sucessao_de_vinculo_matricula_regex = re.compile(r"<matricAnt>(.*?)</matricAnt>", re.DOTALL)
sucessao_de_vinculo_transferencia_regex = re.compile(r"<dtTransf>(.*?)</dtTransf>", re.DOTALL)


# -----------------------------------------------------------------------------------------------------Função principal que vai ser chamada como componente:

def comparador(a, b):
    esquerdo = conteiner(a)  
    direito = conteiner(b)
    
    resultado = verificador(esquerdo, direito)    
    print(f"teste do resultado dentro do comparador{resultado}")       

    return resultado

# -----------------------------------------------------------------------------------------------------Função que compara as informações dos dois XML:

def verificador(xml_esquerdo, xml_direito):
    divergentes = []
    texto = []
      

    # Itera sobre as chaves de xml_esquerdo
    for item in xml_esquerdo:        
        # Verifica se a chave existe em xml_direito
        if item in xml_direito:
            # Compara os valores das chaves correspondentes
            if xml_esquerdo[item] != xml_direito[item]:
                divergentes.append((item, xml_esquerdo[item], xml_direito[item]))
        else:
            # Se a chave não existe em xml_direito, considera como divergente
            divergentes.append((item, xml_esquerdo[item], None))

    # Itera sobre as chaves de xml_direito que não foram verificadas em xml_esquerdo
    for item in xml_direito:
        if item not in xml_esquerdo:
            divergentes.append((item, None, xml_direito[item]))

    if divergentes:        
        painel_esquerdo_dicionario = {}
        painel_direito_dicionario = {}
        
        painel_esquerdo_texto = ""
        painel_direito_texto = ""

        for item, val1, val2 in divergentes:
            painel_esquerdo_texto += f"\n- {item}: {val1}\n"#salva o texto dos itens diferntes para a exibição na tela
            painel_direito_texto += f"\n- {item}: {val2}\n" #salva o texto dos itens diferntes para a exibição na tela

            painel_esquerdo_dicionario[item] = val1 #salva os valores diferentes em um dicionário para poder trabalhar com eles mais fácil
            painel_direito_dicionario[item] = val2  #salva os valores diferentes em um dicionário para poder trabalhar com eles mais fácil         
    else:        
        painel_direito_texto = f"Os dois XML estão identicos"        
        painel_esquerdo_texto = f"Os dois XML estão identicos"
        painel_direito_dicionario = "Os dois XML estão identicos"       
        painel_esquerdo_dicionario = "Os dois XML estão identicos"       
               
    
    texto.append(painel_esquerdo_texto)
    texto.append(painel_direito_texto)
    texto.append(painel_esquerdo_dicionario)
    texto.append(painel_direito_dicionario)
    print(f"Texto enviado de retorno da comparação: {texto}")
    return texto
    
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
        if match1:
           data_admissao = match1.group(1)
        elif match2:
            data_admissao = match2.group(1)
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
            local = ""
    return local

def capturar_sucessao_matricula(xml):
    for item in xml:
        match = sucessao_de_vinculo_matricula_regex.search(item)
        if match:
           matricula = match.group(1)        
        else:
            matricula = ""
    return matricula

def capturar_sucessao_transf(xml):
    for item in xml:
        match = sucessao_de_vinculo_transferencia_regex.search(item)          
        if match:
           data_transf = match.group(1)                   
        else:
            data_transf = ""
    return data_transf