from typing import List
from databases.models.jobs import Jobs
from scrapyn.site.sites import LINKEDIN
from utils.procces_page import procces_site, Page


def linkeding_scraper(job_title: str) -> List[Jobs]:
    results: List[Jobs] = []
    
    # Definimos la url
    URL = f"{LINKEDIN}?keywords={job_title}&f_TPR=r86400"
    
    soup = procces_site(URL, Page.LINKEDIN)
    
    # El contenedor de los trabajos en la versión pública es 'jobs-search__results-list'
    jobs_list = soup.select_one("ul.jobs-search__results-list")
    
    if not jobs_list:
        # Probamos con un selector genérico si el específico falla
        print("Probando con un selector generico")
        jobs_list = soup.select_one("ul")
    
    if not jobs_list:
        raise ValueError("Contenedor principal no encontrado")
    
    for job_item in jobs_list.select("li"):
        
        title_tag = job_item.select_one(".base-search-card__title")
        link_tag = job_item.select_one("a.base-card__full-link")

        # Fallback para la versión con artdeco
        if not title_tag:
            title_tag = job_item.select_one(".artdeco-entity-lockup__title")
            if title_tag:
                link_tag = title_tag.select_one("a")

        if not title_tag or not link_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = link_tag.get("href")

        # Ahora obtenemos los detalles de cada trabajo
        try:
            print(f"[LINKEDIN] Obteniendo detalles de: {title}")
            detail_soup = procces_site(link, Page.LINKEDIN,silent=True)
            
            # Título (h1 en SSR, h2 en web interactiva según usuario)
            detail_title = detail_soup.select_one("h1.top-card-layout__title, h2.text-heading-large")
            detail_title = detail_title.get_text(strip=True) if detail_title else title
            
            # Salario
            salary = detail_soup.select_one(".salary, .compensation__salary")
            salary_text = salary.get_text(strip=True) if salary else "No especificado"
            
            # País / Ubicación
            location = detail_soup.select_one(".topcard__flavor--bullet, .topcard__flavor:nth-of-type(2)")
            location_text = location.get_text(strip=True) if location else "No especificada"
            
            # Descripción completa
            description = detail_soup.select_one(".description__text, .show-more-less-html__markup")
            description_text = description.get_text(separator="\n", strip=True) if description else "Sin descripción"

            results.append(Jobs(
                title=detail_title,
                page=Page.LINKEDIN,
                link=link,
                salary=salary_text,
                location=location_text,
                description=description_text
            ))
            
        except Exception as e:
            print(f"Error al obtener detalles de {link}: {e}")
            # Agregamos la info básica si fallan los detalles
            results.append(Jobs(
                title=title,
                page=Page.LINKEDIN,
                link=link,
                salary="Error",
                location="Error",
                description="Error al cargar detalles"
            ))
    
    f"[RESULT] {len(results)} Ofertas encontradas en Linkeding\n"
    return results


