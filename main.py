from utils.procces_data import local_backup
from databases.functions.jobs import insert_jobs
from scrapyn.site.linkedin import linkeding_scraper

def main(job_title: str, backup: bool = True):
        
        # Obtenemos la lista de empleos
        linkeding_jobs = linkeding_scraper(job_title)
        
        # Realizamos el backup local
        if backup:
            print("[INFO] Relizando backup local")
            local_backup(linkeding_jobs)
        
        # Subimos a la nube
        print("[INFO] Subiendo a la nube")
        insert_jobs(linkeding_jobs)
        
        print("[SUCCESS] Scrapeo completado con exito...")
        
if __name__ == "__main__":
    job = "Desarrollador de software"
    main(job,backup=True)