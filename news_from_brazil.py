import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

sites=[
   'https://g1.globo.com/' ,
   'https://brasil.uxdesign.cc/',
    'https://www.uol.com.br/',
    'https://www.cnnbrasil.com.br/' 
]
async def pegar_sites(session,url):
    try:
        async with session.get(url) as response:
            html= await response.text()
            soup=BeautifulSoup(html,"html.parser")
            
            titulo=[]
            for tag in soup.find_all(["h1","h2","h3"]):
                texto=tag.get_text().strip()
                if texto:
                    titulo.append(texto)
            return{
                'url':url,
                'títulos':titulo[:5]
            }
    except:
        return{
            'url':url,
            'título': ["erro ao acessar o site"]
            
        }
async def main():
    async with  aiohttp.ClientSession() as session:
        tarefas=[]
        for url in sites:
            tarefa=pegar_sites(session,url)
            tarefas.append(tarefa)
        resultado = await asyncio.gather(*tarefas)

        
        with open('resultado.json','w',encoding='utf-8') as f:
            json.dump(resultado,f,ensure_ascii=False,indent=2)
        print("arquivo pronto!")

if __name__ =="__main__":
    asyncio.run(main())
