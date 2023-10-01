from rich.console import Console
from rich.table import Table

console = Console()

def gestionarSlices(usuario):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("N°", justify="right")
    table.add_column("Nombre",justify="center")
    table.add_column("Fecha", justify="left")
    table.add_column("Número VMs", justify="lef")
    table.add_column("Número enlaces", justify="left")
    table.add_column("Activo", justify="left")
    table.add_row("1", "Prueba", "11/07/2023", "4", "5", "Si")
    table.add_row("2","VNRT","7/04/2023","10","20","Si")
    table.add_row("3","Exogeni","2/01/2023","15","20","Si")
    table.add_row("4", "Entorno1", "19/07/2023", "8", "9", "No")
    table.add_row("5", "Simulación", "4/08/2023", "6", "10", "Si")
    console.print(table)
    return