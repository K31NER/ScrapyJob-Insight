import pandas as pd
from typing import List
from pathlib import Path
from databases.models.jobs import Jobs

def local_backup(jobs: List[Jobs], path: str = "data/jobs.csv") -> None:
    """Realiza un backup local incremental de los datos en un CSV"""

    if not jobs:
        return

    try:
        df = pd.DataFrame(
            [job.model_dump(mode="json") for job in jobs]
        )

        # Aseguramos que la carpeta contenedora exista
        csv_path = Path(path)
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        file_exists = csv_path.exists()

        df.to_csv(
            path,
            mode="a",                # append
            header=not file_exists,  # escribe header solo la primera vez
            index=False,
            encoding="utf-8"
        )
        
        print("[SUCCESS] Backup local completado con éxito")
        
    except Exception as e:
        print(f"[ERROR] Fallo al realizar el backup local: {e}")