import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = "Agenda Pessoal"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 600

    #Função para salvar os dados no banco de dados
    def cadastrar_veiculo(e):
        if not txt_modelo.value or not txt_marca.value:
            txt_modelo.error_text = "Campo obrigatório"
            page.update()
            return
        
        conn = sqlite3.connect('data/agenda.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO veiculos (modelo, marca, ano, cor, placa)
            VALUES (?, ?, ?, ?, ?)
        ''', (txt_modelo.value, txt_marca.value, txt_ano.value, txt_cor.value, txt_placa.value))
        conn.commit()
        conn.close()
        
        # Limpar todos os campos para dar a sensação de "próximo"
        txt_modelo.value = ""
        txt_marca.value = ""
        txt_ano.value = ""
        txt_cor.value = ""
        txt_placa.value = ""
        
        # Mostrar aviso de sucesso
        page.snack_bar = ft.SnackBar(ft.Text("Veículo cadastrado com sucesso!"), bgcolor="green")
        page.snack_bar.open = True
        
        # Focar de volta no primeiro campo
        txt_modelo.focus()
        page.update()

    # Lista para exibir os veículos
    lista_veiculos = ft.Column()

    def carregar_veiculos():
        lista_veiculos.controls.clear()
        conn = sqlite3.connect('data/agenda.db')
        cursor = conn.cursor()
        cursor.execute('SELECT modelo, marca, placa FROM veiculos')

        for row in cursor.fetchall():
            lista_veiculos.controls.append(
                ft.ListTile(
                    leading=ft.Icon("directions_car"),
                    title=ft.Text(f"{row[0]} - {row[1]}"),
                    subtitle=ft.Text(f"Placa: {row[2]}"),
                )
            )
        conn.close()
        page.update()

    # Chamar a função ao iniciar
    carregar_veiculos()

    # Campos de entrada
    txt_modelo = ft.TextField(label="Modelo (ex: Fiesta)")
    txt_marca = ft.TextField(label="Marca (ex: Ford)")
    txt_ano = ft.TextField(label="Ano", keyboard_type=ft.KeyboardType.NUMBER)
    txt_cor = ft.TextField(label="Cor")
    txt_placa = ft.TextField(label="Placa")
    btn_salvar = ft.ElevatedButton("Cadastrar Veículo", on_click=cadastrar_veiculo)

    # Adicionar na tela
    page.add(
        ft.Text("Cadastro de Veículo", size=30, weight=ft.FontWeight.BOLD),
        txt_modelo,
        txt_marca,
        txt_ano,
        txt_cor,
        txt_placa,
        btn_salvar,
        ft.Divider(),
        ft.Text("Veículos Cadastrados", size=20, weight="bold"),
        lista_veiculos
    )

ft.app(target=main)