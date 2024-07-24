import flet as ft
from simulacion import simulacion
from support import get_table, validar_i_j, validar_n

def main(page: ft.Page):
    page.title = "Simulación VPN"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = ft.colors.GREY_100
    page.scroll = ft.ScrollMode.ADAPTIVE


    def close_ventana_error(e):
            ventana_error.open = False
            page.update()


    ventana_error = ft.AlertDialog(
        title = ft.Text("Error"),
        content = ft.Text("Por favor, ingrese valores válidos para los parámetros."),
        actions=[
            ft.TextButton("Ok", on_click=close_ventana_error),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )


    def mostrar_resultados(res1, res2):
        res.value = f"\n Proyecto A - ${res1[0]}\n Proyecto B - ${res1[1]}\n Proyecto C - ${res1[2]}\n VPN: {res2} M"
        page.update()

    
    def simular(e):
        
        # Validar parámetros
        n_validado = validar_n(n_input.value)
        i_j_validados = validar_i_j(i_input.value, j_input.value, n_input.value)

        if not (n_validado and i_j_validados):
            page.dialog = ventana_error
            ventana_error.open = True
            page.update()
            return

        i, j = i_j_validados

        # Simular
        tablas, mejor_combinacion, mejor_combinacion_vpn = simulacion(n_validado, i, j)

        # Mostrar resultados
        page.add(resultados)

        mostrar_resultados(mejor_combinacion, round(mejor_combinacion_vpn, 4))

        try:
            get_table(tablas, auto_open=True)
        except PermissionError:
            page.dialog = ventana_error
            ventana_error.content = ft.Text("Debe cerrar la ventana de excel para realizar nuevamente la simulación.")
            ventana_error.open = True
            page.update()

    
    # Resultados
    res = ft.Text("-", color="#4581e5", size=25, weight=ft.FontWeight.BOLD)
    resultados = ft.Row(controls=[ft.Text("Mejor combinación de inversión posible:", color=ft.colors.BLACK, size=25, weight=ft.FontWeight.BOLD),
                                  res], alignment=ft.MainAxisAlignment.CENTER)

    # Parámetros de la simulación
    n_input = ft.TextField(label="Cantidad de filas a simular (n):", label_style=ft.TextStyle(color=ft.colors.GREY_500), width=300, color=ft.colors.BLACK)

    i_label = ft.Text("Mostrar", color=ft.colors.BLACK)
    i_input = ft.TextField(label="i =", label_style=ft.TextStyle(color=ft.colors.GREY_500), width=300, color=ft.colors.BLACK)
    
    j_label = ft.Text("filas a partir de la fila", color=ft.colors.BLACK)
    j_input = ft.TextField(label="j =", label_style=ft.TextStyle(color=ft.colors.GREY_500), width=300, color=ft.colors.BLACK)

    # Botón de simulación
    simulate_button = ft.ElevatedButton(text="Simular", on_click=simular)  # Aquí iría la lógica de simulación

    
    # Disposición de componentes
    page.add(
        n_input,
        ft.Row(controls=[i_label, i_input, j_label, j_input], alignment=ft.MainAxisAlignment.CENTER),
        simulate_button,
    )

# Ejecutar la aplicación
ft.app(target=main)
