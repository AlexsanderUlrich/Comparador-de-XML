import flet as ft


def modal(xml_esquerdo, xml_direito):
    header = ft.Text("Aqui você consegue ver o local onde ficam as informações divegerentes nos XML", size=20, text_align="Center", color=ft.colors.ORANGE_700)    


    esquerdo = ft.Text(
        xml_esquerdo,               
        expand=True,
        overflow=ft.TextOverflow.VISIBLE,           
    )

    direito = ft.Text(
        xml_direito,         
        expand=True,
        overflow=ft.TextOverflow.VISIBLE,                
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

    modal_completo = ft.AlertDialog(
        modal=True,
        title=header,
        content=corpo,
        bgcolor=ft.colors.BLUE_GREY_900,
        content_padding=10,        
        
    )
    

    return modal_completo

def modal_separado_por_linhas(xml_esquerdo, xml_direito, comparacao_e, comparacao_d):

    header = ft.Text(
        "Aqui você consegue ver o local onde ficam as informações divergentes nos XML", 
        size=20, 
        text_align="Center", 
        color=ft.colors.ORANGE_700
    )         

    # Separar os textos em linhas
    linhas_esquerdo = xml_esquerdo[0]
    texto_normalizado_esquerdo = linhas_esquerdo.replace('\n', ' ')
    linhas_esquerdo = texto_normalizado_esquerdo.split(' ')

    linhas_direito = xml_direito[0]
    texto_normlaizado_direito = linhas_direito.replace('\n', ' ')
    linhas_direito = texto_normlaizado_direito.split(' ')
    print(linhas_esquerdo)
    
    # Criar widgets para as linhas do texto
    for item in linhas_esquerdo:
        if item == comparacao_e:
            linhas_esquerda = ft.Text(item, bgcolor=ft.colors.RED_300, padding=5)
            print(f"Teste na linha {linhas_esquerda}")
        else:
            linhas_esquerda = ft.Text(item, bgcolor=ft.colors.PINK_300)

    for item in linhas_direito:
        if item ==comparacao_d:
            linhas_direita = ft.Text(item, bgcolor=ft.colors.RED_300, padding=5)
        else:
            linhas_direita = ft.Text(item, bgcolor=ft.colors.PINK_300)


    
    # Criar containers para cada texto
    conteudo_esquerdo = ft.Column(linhas_esquerda, expand=True, scroll=ft.ScrollMode.AUTO)
    conteudo_direito = ft.Column(linhas_direita, expand=True, scroll=ft.ScrollMode.AUTO)
    
    corpo = ft.ListView(        
        [
        ft.Container(
        content = ft.Row([conteudo_esquerdo, conteudo_direito], expand=True),
        border_radius=20,
        padding=5,
        expand=True,
        bgcolor=ft.colors.WHITE,                        
        )
    ],    
    )

    modal_completo = ft.AlertDialog(
        modal=True,
        title=header,
        content=corpo,
        bgcolor=ft.colors.BLUE_GREY_900,
        content_padding=10,        
    )
    
    return modal_completo
