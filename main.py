import requests
from lxml import html
from rich.progress import track
from rich.console import Console

console = Console()
base_url = "https://www.inscricao.marinha.mil.br/ordi/index_concursos.jsp?id_concurso="
engnav_links = []

def verificar_concurso(i):
    url = f"{base_url}{i:02d}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            titulo = tree.xpath('/html/body/table[1]/tbody/tr[2]/td[4]/span/b/text()')
            if titulo:
                titulo = titulo[0].strip()
                if 'EngNav' in titulo:
                    return titulo, url
    except Exception as e:
        console.print(f"[yellow]⚠️ Erro ao acessar {url}: {e}[/yellow]")
    return None

# Teste com o id_concurso 98
console.print("[bold magenta]🔎 Testando o concurso 98 antes de varrer todos...[/bold magenta]")
resultado_teste = verificar_concurso(98)
if resultado_teste:
    console.print(f"[green]🎯 Encontrado: [bold]{resultado_teste[0]}[/bold][/green]")
else:
    console.print("[red]❌ Nada encontrado no concurso 98. Verifique o XPath ou o carregamento da página.[/red]")
    exit()

# Varrer do 01 ao 200
console.print("\n[bold cyan]🔍 Buscando concursos com EngNav de id_concurso=01 até 200...[/bold cyan]\n")

for i in track(range(1, 201), description="📡 Verificando concursos..."):
    resultado = verificar_concurso(i)
    if resultado:
        engnav_links.append(resultado)

# Salvar os resultados em um .txt
with open("resultados_engnav.txt", "w", encoding="utf-8") as f:
    for titulo, link in engnav_links:
        f.write(f"{titulo}\n{link}\n\n")

# Resultado final
console.print("\n[bold green]✅ Resultados salvos em 'resultados_engnav.txt'[/bold green]")
if engnav_links:
    for titulo, link in engnav_links:
        console.print(f"[bold white]{titulo}[/bold white]\n[blue]{link}[/blue]\n")
else:
    console.print("[yellow]⚠️ Nenhum concurso com 'EngNav' encontrado.[/yellow]")
