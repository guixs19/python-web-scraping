import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd

urls = [
    "https://scrapingtest.com/ecommerce/load-more?brand=Samsung",
    "https://scrapingtest.com/ecommerce/load-more?brand=Apple",
    "https://scrapingtest.com/ecommerce/load-more?brand=Google",
    "https://scrapingtest.com/ecommerce/load-more?brand=Motorola"
]
nomes_dos_sites = ["Samsung", "Apple", "Google", "Motorola"]

async def parser_in_page(session, url, nome_site):
    try:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            produtos = []
            precos = []
            for tag in soup.find_all("h2", class_="product-title group-hover:text-blue-600"):
                produto = tag.get_text(strip=True)
                produtos.append(produto)
            
           
            for p in soup.find_all("div", class_="product-price"):
                preco = p.get_text(strip=True)
                precos.append(preco)
      
            df = pd.DataFrame({
                "produtos": produtos,
                "preço": precos
            })
            
            return nome_site, df
    except Exception as e:
        print(f"Error ao processar {url}: {e}")
        return nome_site, pd.DataFrame()
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [parser_in_page(session, url, nome) for url, nome in zip(urls, nomes_dos_sites)]
        resultados = await asyncio.gather(*tasks)
        
        with pd.ExcelWriter("todos_produtos.xlsx", engine="openpyxl") as writer:
            for nome_site, df in resultados:
                if not df.empty:
                    sheet_name = nome_site[:31]
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"Aba {sheet_name} salva com {len(df)} produtos")
                else:
                    print(f"Erro: DataFrame vazio para {nome_site}")
        
        print("Arquivo salvo com sucesso!")
        print("Abas criadas: Samsung, Apple, Google, Motorola")

if __name__ == "__main__":
    asyncio.run(main())
