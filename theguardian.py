import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from datetime import datetime

async def baixar_pagina(session, url):
    """baixar uma pagina de forma assícrona"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        async with session.get(url, headers=headers) as response:
            return await response.text()
    except Exception as e:
        print(f"erro ao baixar {url}:{e}")
        return None

def extrair_noticias(html, categoria):
    """extrair dados"""
    if not html:
        return []
    
    soup = BeautifulSoup(html, "html.parser")
    noticias = []
    
    selectores = [
        'a[data-link-name="article"]',
        '.fc-item__title a',
        '.js-headline-text', 
        'a.u-faux-block-link__overlay',
    ]
    
    for seletor in selectores:
        links = soup.select(seletor)
        if links:
            print(f"encontrados {len(links)} links com seletor: {seletor}")
            for link in links[:15]:
                try:
                    titulo = link.get_text(strip=True)
                    if not titulo or len(titulo) < 15:
                        continue
                    
                    href = link.get('href', '')
                    if not href.startswith('http'):
                        href = "https://www.theguardian.com" + href
                    
                    data = datetime.now().strftime("%Y-%m-%d")
                    
                    noticias.append({
                        "titulo": titulo,
                        "categoria": categoria,
                        "data": data,
                        "link": href
                    })
                    
                except Exception as e:
                    continue
            break
    
    return noticias

async def main():
    """função principal"""
    secoes = {
        "world": "https://www.theguardian.com/world",
        "business": "https://www.theguardian.com/business",  # corrigi typo
        "technology": "https://www.theguardian.com/technology", 
        "sport": "https://www.theguardian.com/sport",
        "environment": "https://www.theguardian.com/environment"  # adicionei www
    }
    
    print("iniciando a coleta de notícias do the Guardian...")
    print("seções: world, business, technology, sport, environment")
    
    todas_noticias = []
    
    async with aiohttp.ClientSession() as session:
        for categoria, url in secoes.items():
            print(f"baixando {categoria}")
            html = await baixar_pagina(session, url)
            
            if html:
                noticias = extrair_noticias(html, categoria)
                todas_noticias.extend(noticias)
                print(f"{categoria}: {len(noticias)} notícias coletadas")
            else:
                print(f"{categoria}: falha ao coletar")
    
    # Remover duplicatas
    noticias_unicas = []
    links_vistos = set()
    
    for noticia in todas_noticias:
        if noticia['link'] and noticia['link'] not in links_vistos:
            noticias_unicas.append(noticia)
            links_vistos.add(noticia['link'])
    
    # Salvar em JSON
    with open('noticias_guardian.json', 'w', encoding='utf-8') as f:
        json.dump(noticias_unicas, f, ensure_ascii=False, indent=2)
    
    print("Concluído!")
    print(f"total de {len(noticias_unicas)} notícias únicas coletadas")
    print("notícias salvas em: noticias_guardian.json")

if __name__ == "__main__":
    asyncio.run(main())
