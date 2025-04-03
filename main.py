from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from rich.progress import track
from rich.console import Console
import shutil
import time

console = Console()
base_url = "https://www.inscricao.marinha.mil.br/ordi/index_concursos.jsp?id_concurso="
engnav_links = []

# Configuração do navegador headless para Microsoft Edge
options = EdgeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

def verificar_concurso(id_concurso):
    url = f"{base_url}{id_concurso:02d}"
    try:
        driver.get(url)
        time.sleep(1)  # pequeno delay para garantir carregamento
        elemento = driver.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[2]/td[4]/span/b')
        texto = elemento.text.strip()
        if "EngNav" in texto:
            return texto, url
    except Exception as e:
        console.print(f"[yellow]⚠️ {url} — {e}[/yellow]")
    return None

# Teste inicial com o 98
console.print("[bold magenta]🔎 Testando concurso 98...[/bold magenta]")
teste = verificar_concurso(98)
if teste:
    console.print(f"[green]🎯 Encontrado: {teste[0]}[/green]")
else:
    console.print("[red]❌ Nada encontrado no concurso 98. Verifique se há proteção adicional ou bloqueios.[/red]")
    driver.quit()
    exit()

# Escaneando todos de 01 a 200
console.print("\n[bold cyan]🔍 Varredura de concursos de 01 a 200...[/bold cyan]\n")
for i in track(range(1, 201), description="📡 Escaneando..."):
    resultado = verificar_concurso(i)
    if resultado:
        engnav_links.append(resultado)

driver.quit()

# Salvando os resultados
with open("resultados_engnav.txt", "w", encoding="utf-8") as f:
    for titulo, link in engnav_links:
        f.write(f"{titulo}\n{link}\n\n")

# Mostrando os achados no terminal
console.print("\n[bold green]✅ Resultados salvos em 'resultados_engnav.txt'[/bold green]")
for titulo, link in engnav_links:
    console.print(f"[bold white]{titulo}[/bold white]\n[blue]{link}[/blue]\n")
