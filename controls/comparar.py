import re

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
    print(resultado)       

    return resultado

def verificador(dict1, dict2):
    divergentes = []  

    # Itera sobre as chaves de dict1
    for key in dict1:
        # Verifica se a chave existe em dict2
        if key in dict2:
            # Compara os valores das chaves correspondentes
            if dict1[key] != dict2[key]:
                divergentes.append((key, dict1[key], dict2[key]))
        else:
            # Se a chave não existe em dict2, considera como divergente
            divergentes.append((key, dict1[key], None))

    # Itera sobre as chaves de dict2 que não foram verificadas em dict1
    for key in dict2:
        if key not in dict1:
            divergentes.append((key, None, dict2[key]))

    if divergentes:
        texto = []
        painel_esquerdo = ""
        painel_direito = ""
        for key, val1, val2 in divergentes:
            painel_esquerdo += f"\n- {key}: {val1}\n"                      
            painel_direito += f"\n- {key}: {val2}\n"            
    else:        
        painel_direito +="Os dois estão identicos"        
        painel_esquerdo +="Os dois estão identicos"        
    
    texto.append(painel_esquerdo)
    texto.append(painel_direito)                                  
    return texto
    
# -----------------------------------------------------------------------------------------------------conteiner com as informações:

def conteiner(a):
    empregador_esquerdo = capturar_empregador(a)
    local_de_trabalho_esquerdo = capturar_local_de_trabalho(a)
    cpf_esquerdo = capturar_cpf(a)    
    matricula_esquerda = capturar_matricula(a)
    data_admissao_esquerda = capturar_data_admissao(a)
    transf_sucessao = capturar_sucessao_transf(a)
    mat_sucessao = capturar_sucessao_matricula(a)
    local_sucessao = capturar_sucessao_local(a)

    dados = {"Cpf":cpf_esquerdo, 
             "Matricula":matricula_esquerda, 
             "Empregador":empregador_esquerdo, 
             "Data":data_admissao_esquerda, 
             "Local":local_de_trabalho_esquerdo, 
             "Data da transferência":transf_sucessao, 
             "Matricula antes da transferência":mat_sucessao,
             "Empresa antes da transferência":local_sucessao,
             }
    return dados       


# -----------------------------------------------------------------------------------------------------funções para capturar as informações dos XML:

def capturar_empregador(xml):
    for item in xml:
        match = empregador_regex.search(item)
        if match:
           empregador = match.group(1)
        else:
            empregador = "Erro ao capturar o empregador"
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
            local_de_trabalho = "Erro ao capturar o local_de_trabalho"
    return local_de_trabalho

def capturar_cpf(xml):
    for item in xml:
        match = cpf_regex.search(item)
        if match:
           cpf = match.group(1)
        else:
            cpf = "Erro ao capturar o CPF"
    return cpf

def capturar_matricula(xml):
    for item in xml:
        match = matricula_regex.search(item)
        if match:
           matricula = match.group(1)
        else:
            matricula = "Erro ao capturar o matricula"
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
            data_admissao = "Erro ao capturar o data_admissao"

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