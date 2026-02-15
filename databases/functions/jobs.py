from typing import List
from databases.models.jobs import Jobs
from databases.db_config import collection

def insert_jobs(jobs: List[Jobs]):
    """ Inserta trabajos en la db"""
    try:
        # Convertimos en una lista de diccionarios compatibles con JSON
        # mode="json" serializa objetos como 'date' a strings que MongoDB acepta
        jobs_dict = [job.model_dump(mode="json") for job in jobs]
        
        # Insertamos en la base de datos
        if jobs_dict:
            collection.insert_many(jobs_dict)
        
        print(f"[SUCCESS] {len(jobs_dict)} documentos subidos a la nube con éxito")
        
        return jobs
    
    except Exception as e:
        print(f"[Error] Fallo al subir datos: {e}")
        return []
    
    
