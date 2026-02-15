import yaml
from pathlib import Path

def load_prompt():
    # Definimos la ruta al archivo yml
    prompt_path = Path(__file__).parent / "prompts/system.yml"
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    instructions = []
    if config:
        # Estructuramos por secciones para mejorar la comprensión del modelo
        if "Rol" in config:
            instructions.append(f"ROL ACTUAL: {config['Rol']}")
        
        if "Objetivo" in config:
            instructions.append("TUS OBJETIVOS:")
            instructions.extend(config["Objetivo"] if isinstance(config["Objetivo"], list) else [config["Objetivo"]])
            
        if "Instrucciones" in config:
            instructions.append("PASOS TÉCNICOS:")
            instructions.extend(config["Instrucciones"])
            
        if "Restricciones" in config:
            instructions.append("RESTRICCIONES CRÍTICAS:")
            instructions.extend(config["Restricciones"])
            
        if "Tipo_Respuesta" in config:
            instructions.append(f"FORMATO DE SALIDA: {config['Tipo_Respuesta']}")
            
    return instructions

SYSTEM_PROMPT = load_prompt()

if __name__ == "__main__":
    pass