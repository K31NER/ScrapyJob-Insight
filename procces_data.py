from utils.procces_data import local_backup
from databases.functions.jobs import insert_jobs
from scrapyn.site.linkedin import linkeding_scraper
from Agent.agent import redact_agent
from Agent.schema import JobEntry

def main(job_title: str, backup: bool = True):
    # 1. Scraping
    linkeding_jobs = linkeding_scraper(job_title)
    
    # Lista para almacenar solo los trabajos procesados con éxito por la IA
    processed_jobs = []
    
    # 2. Procesamiento con IA
    total_jobs = len(linkeding_jobs)
    print(f"[INFO] Procesando {total_jobs} empleos con la IA...")
    for i, job in enumerate(linkeding_jobs):
        try:
            entry = JobEntry(
                title=job.title,
                location=job.location if job.location != "Error" else None,
                description=job.description
            )
            print(f"[PROCESSING - {i+1}] Analizando {job.title}...")
            response = redact_agent.run(entry)
            
            if response and response.content:
                # Actualizamos el objeto original
                job.skills = response.content.skills
                job.location = response.content.location
                job.seniority = response.content.seniority.value if hasattr(response.content.seniority, 'value') else response.content.seniority
                
                # Agregamos a la lista de procesados
                processed_jobs.append(job)
            
            print(f"[SUCCESS] {job.title} analizado con éxito")
            print(f"[INFO] Quedan: {total_jobs - (i + 1)}")
            
        except Exception as e:
            print(f"[ERROR] Error al procesar '{job.title}': {e}")

    # 3. Guardado final (Usando la lista de trabajos ya actualizados)
    if processed_jobs:
        if backup:
            print(f"[INFO] Realizando backup local de {len(processed_jobs)} empleos")
            local_backup(processed_jobs,path="data/jobs_proccess.csv")
        
        #print("[INFO] Subiendo a la nube")
        #insert_jobs(processed_jobs)
        #print("[SUCCESS] Scrapeo y limpieza completados con éxito.")
    else:
        print("[WARNING] No hay empleos procesados para guardar.")
        
if __name__ == "__main__":
    job = "Desarrollador de software"
    main(job,backup=True)