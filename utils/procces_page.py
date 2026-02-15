import httpx
from enum import Enum
from bs4 import BeautifulSoup

class Page(str, Enum):
    LINKEDIN = "LINKEDIN"
    COMPUTRABAJO = "COMPUTRABAJO"
    MAGNETO = "MAGNETO"
    GETONBOARD = "GETONBOARD"
    ELEMPLEO = "ELEMPLEO"
    
HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
def procces_site(url: str, page: Page, silent: bool = False) -> BeautifulSoup:
    """ Realiza la peticon y parseo de la pagina web """
    
    try:
        # Realizamos la peticion
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        
        # Parsemos el html
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if not silent:
            print(f"[SUCCESS] Scraping realizado con exito [{page.value}]")
            
        return soup
    
    except Exception as e:
        print(f"[Error] Fallo al procesar scraping")
        raise httpx.ReadError(f"[Error] al procesar pagina [{page}]: {e}")
    