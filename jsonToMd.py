from openai import OpenAI
import json

# Initialize OpenAI client
client = OpenAI()

# Your assistant ID here
ASSISTANT_ID = "asst_mloihn8bR4uNgqPW8FLz5tBJ"

def convert_json_to_md(json_data: dict, template_content: str) -> str:
    """
    Convert JSON data to Markdown using a template and GPT assistance.
    
    Args:
        json_data (dict): The JSON structure to convert
        template_path (str): Path to the Markdown template file
    
    Returns:
        str: Generated Markdown content
    """
    
    # Create thread with the conversion request
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": f"""Por favor, genera un documento Markdown basado en esta plantilla y estos datos.

Template Markdown:
{template_content}

JSON Data:
{json.dumps(json_data, ensure_ascii=False, indent=2)}

IMPORTANTE: 
- Mantén el estilo y formato exacto de la plantilla
- Reemplaza los marcadores de posición con los datos del JSON
- Incluye todas las rutas de imágenes del JSON tal como están
- Conserva cualquier CSS o estilo especial de la plantilla
"""
            }
        ]
    )
    
    # Create and execute the run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )
    
    # Wait for completion
    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    # Get the response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    markdown_content = messages.data[0].content[0].text.value
    
    return markdown_content

if __name__ == "__main__":
    # Example usage
    json_data = """
{
"document": {
    "title": "INSPECCION RAMIREZ",
    "date": "2025-01-05",
    "prepared_by": "Cesar Perales",
    "company": "SRL SAC PYR",
    "general_data": {
    "inspection_date": "2025-01-01",
    "contractor_name": "cesar perales"
    },
    "summary": [
    {
        "technician_name": "Tecnico Ramirez",
        "observations": "Ninguna, todo bien ",
        "image": "./imagen1.png"
    },
    {
        "technician_name": "Rocky Balboa",
        "observations": "Alguna que ver. Tal vez 2",
        "image": "./imagen2.png"
    }
    ],
    "history_of_risks_and_problems": {
    "inspection_date": "2025-01-09",
    "risks": [
        {
        "description": "Ninguno",
        "image": null
        }
    ]
    },
    "conclusions_recommendations": [
    {
        "recommendation": "",
        "image": null,
        "description": ""
    }
    ],
    "supervisor_signature": {
    "name": "Cesar Andre",
    "signature": null
    }
}
}
                """
    
    template_content = """
# Informe de Inspección

## Datos Generales
**Fecha de Inspección:** [inspection_date]  
**Nombre del Contratista:** [contractor_name]  

---

## Resumen
### Técnico Responsable: [technician_name]

#### Observaciones:
- observacion 1
- observacion 2


### Técnico Responsable 2: ...

...

---

## Historial de Riesgos y Problemas
**Fecha de Inspección:** [inspection_date]  

#### Riesgos Identificados:
- [Riesgo 1]
- [Riesgo 2]
- [Riesgo 3]

---

## Conclusiones y Recomendaciones
- **Recomendación:** [recommendation]

---

## Firma del Supervisor
**Nombre:** [name]  
**Firma:**  

---

> _**Nota:** Este informe es confidencial y debe ser utilizado únicamente para fines relacionados con el proyecto especificado._

    """
    
    result = convert_json_to_md(json_data, template_content)
    
    # Save the result
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(result)