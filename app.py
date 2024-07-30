import flet as ft
from time import sleep
from controls import comparar


def main(page: ft.Page):
    page.title = "Comparador de XML"
    page.bgcolor = ft.colors.BLUE_GREY_900
    xml_esquerdo = []
    xml_direito = [] 

    header = ft.Text("Comparador de XML", size=50, text_align="Center", color=ft.colors.ORANGE_800)
    esquerdo = ft.TextField(        
        filled=True,
        expand=True,
        min_lines=30,
        max_lines=30,       
        shift_enter=True,
        bgcolor=ft.colors.WHITE,
        border_radius=20,
        
    )
    direito = ft.TextField(        
        filled=True,
        expand=True,
        min_lines=30,
        max_lines=30,
        shift_enter=True,        
        bgcolor=ft.colors.WHITE,
        border_radius=20,        
    )
    corpo = ft.Row([esquerdo, direito], expand=False)

    #Conteiner onde vai ficar a resposta da comparação----------------------------------------------------------------------------------------

    
    resposta_da_comparacao = ft.TextField(
        filled=True,
        expand=True,
        min_lines=1,
        max_lines=20,
        shift_enter=True,        
        bgcolor=ft.colors.WHITE,
        border_color="Transparent",
        )  
    resposta_da_comparacao1 = ft.TextField(
        filled=True,
        expand=True,
        min_lines=1,
        max_lines=20,
        shift_enter=True,        
        bgcolor=ft.colors.WHITE,
        border_color="Transparent",
        )  

    conteiner_da_resposta = ft.ListView(
            [
                ft.Container(
                content=ft.Row([resposta_da_comparacao, resposta_da_comparacao1]),
                border_radius=20,
                padding=10,
                expand=True,
                bgcolor=ft.colors.WHITE
                ),
            ]
            )
        

    #Função para adicionar o conteiner com a resposta da comparação----------------------------------------------------------------------------  
    def comparar_os_xml(e):
        if xml_esquerdo == []:        
            xml_esquerdo.append(esquerdo.value)
        else:
            xml_esquerdo.clear()
            xml_esquerdo.append(esquerdo.value)

        if xml_direito == []:
            xml_direito.append(direito.value)
        else:
            xml_direito.clear()
            xml_direito.append(direito.value)
                          
        comparado = comparar.comparador(xml_esquerdo, xml_direito)                     
        resposta_da_comparacao.value = f'{comparado[0]}'        
        resposta_da_comparacao1.value = f'{comparado[1]}'        
        page.update()


    botao = ft.ElevatedButton("COMPAR OS XML", 
                              icon='FOLDER_COPY_OUTLINED', 
                              icon_color=ft.colors.ORANGE_700, 
                              bgcolor=ft.colors.GREY_700,
                              color=ft.colors.ORANGE_700, 
                              on_click=comparar_os_xml)

    #Conteiner com a parte onde cola os textos e fica o botão de comparar --------------------------------------------------------------------------
    page.add(
    ft.ListView(
    [
        header,
        ft.Container(
            content=corpo,      
            padding=10,
            expand=True,
        ),        
        botao,
        conteiner_da_resposta   
    ],
    expand=True, spacing=10,    
    )
    )
    page.update
    
    




ft.app(target=main)
#ft.app(target=main, view=ft.WEB_BROWSER)