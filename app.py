import flet as ft
from controls import comparar
from controls import modal

# -----------------------------------------------------------------------------------------------------função principal da página 

def main(page: ft.Page):
    page.title = "Comparador de XML"
    page.bgcolor = ft.colors.BLUE_GREY_900
    xml_esquerdo = []
    xml_direito = []

    header = ft.Text("Comparador de XML", size=50, text_align="Center", color=ft.colors.ORANGE_700, font_family="Georgia", weight=ft.FontWeight.BOLD)

# -----------------------------------------------------------------------------------------------------funções para a label dos dois principais campos
    def blur_esquerdo(e):
        if not esquerdo.value:
            esquerdo.label_style = ft.TextStyle(color=ft.colors.TRANSPARENT, size=20)       
        else:
            esquerdo.label_style = ft.TextStyle(color=ft.colors.LIGHT_BLUE_200, size=20)        
        page.update()

    def blur_direito(e):
        if not direito.value:
            direito.label_style = ft.TextStyle(color=ft.colors.TRANSPARENT, size=20)       
        else:
            direito.label_style = ft.TextStyle(color=ft.colors.LIGHT_BLUE_200, size=20)        
        page.update()    

    def focus_esquerdo(e):       
        esquerdo.label_style = ft.TextStyle(color=ft.colors.LIGHT_BLUE_200, size=20)        
        page.update()
    
    def focus_direito(e):
        direito.label_style = ft.TextStyle(color=ft.colors.LIGHT_BLUE_200, size=20)
        page.update()
        
 # -----------------------------------------------------------------------------------------------------const com os dois campos onde vai ser colado o XML
    esquerdo = ft.TextField(                
        filled=True,
        expand=True,
        min_lines=30,
        max_lines=30,
        content_padding=30,       
        shift_enter=True,
        bgcolor=ft.colors.WHITE,        
        border_color=ft.colors.LIGHT_BLUE_200,
        border_radius=20,
        label="XML para a comparação",
        label_style=ft.TextStyle(color=ft.colors.TRANSPARENT, size=20),       
        on_focus=focus_esquerdo,
        on_blur=blur_esquerdo,      
    )
    direito = ft.TextField(              
        filled=True,
        expand=True,
        min_lines=30,
        max_lines=30,
        content_padding=30,
        shift_enter=True,        
        bgcolor=ft.colors.WHITE,       
        border_color=ft.colors.LIGHT_BLUE_200,
        border_radius=20,
        label="XML para a comparação",
        label_style=ft.TextStyle(color=ft.colors.TRANSPARENT, size=20),        
        on_focus=focus_direito,
        on_blur=blur_direito,                     
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
        border_color=ft.colors.ORANGE_400,
        border_radius=20,
        label="Divergências no XML da Esquerda", 
        label_style=ft.TextStyle(color=ft.colors.ORANGE_900),              
        )
      
    resposta_da_comparacao1 = ft.TextField(       
        filled=True,
        expand=True,
        min_lines=1,
        max_lines=20,
        shift_enter=True,        
        bgcolor=ft.colors.WHITE,
        border_color=ft.colors.ORANGE_400,
        border_radius=20,
        label="Divergências no XML da Direita", 
        label_style=ft.TextStyle(color=ft.colors.ORANGE_900), 
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
        resposta_da_comparacao.value = comparado[0]
        resposta_da_comparacao1.value = comparado[1]

        atualizar(xml_esquerdo, xml_direito, comparado[0], comparado[1])      

        page.update()

        botao_abrir_modal.disabled = False        
        page.update()
                  

    #local onde vai ficar o modal----------------------------------------------------------------------------
       

    
    print(xml_direito)
    dialog = modal.modal(xml_esquerdo, xml_direito)
    dialog.actions = ft.ElevatedButton("fechar", on_click=lambda e: page.close(dialog), bgcolor=ft.colors.ORANGE_500, color="White"),

    def atualizar(xml_esquerdo, xml_direito, comparado_e, comparado_d):
        dialog = modal.modal_separado_por_linhas(xml_esquerdo, xml_direito, comparado_e, comparado_d)
        page.update()

    def funcoes_do_modal(e):        
        page.open(dialog)
        page.update()
        
           

    #botões de controle----------------------------------------------------------------------------  
                
    botao_comparar_xml = ft.ElevatedButton("COMPAR OS XML", 
                              icon='FOLDER_COPY_OUTLINED', 
                              icon_color=ft.colors.ORANGE_700, 
                              bgcolor=ft.colors.GREY_700,
                              color=ft.colors.ORANGE_700, 
                              on_click=comparar_os_xml)
    
    botao_abrir_modal = ft.ElevatedButton("MOSTAR INFORMAÇÃO NO XML", 
                              icon='MANAGE_SEARCH', 
                              icon_color=ft.colors.GREY_200, 
                              bgcolor=ft.colors.ORANGE_700,
                              color=ft.colors.GREY_200,
                              disabled=True, 
                              on_click=funcoes_do_modal                              
                              )

    #Conteiner com a parte onde cola os textos e fica o botão de comparar --------------------------------------------------------------------------
    page.add(
    ft.ListView(
    [
        header,
        ft.Container(
            content=corpo,      
            padding=10,
            expand=True,
            bgcolor="White",
            border_radius=20,
        ),        
        botao_comparar_xml,
        conteiner_da_resposta,   
        botao_abrir_modal,
    ],
    expand=True, spacing=10,    
    ),
    dialog
    )
    page.update()

ft.app(target=main)
#ft.app(target=main, view=ft.WEB_BROWSER)