from openai import OpenAI
import json

client = OpenAI()

def analyze_pdf(template_path: str, knowledge_path: str):
   # 1. Subir ambos PDFs
   template_file = client.files.create(
       file=open(template_path, "rb"),
       purpose="assistants"
   )
   
   knowledge_file = client.files.create(
       file=open(knowledge_path, "rb"),
       purpose="assistants"
   )
   
   # 2. Crear el thread y adjuntar los archivos
   thread = client.beta.threads.create(
       messages=[
           {
               "role": "user",
               "content": """Analiza el PDF de template y proporciona dos elementos:
               1. Una estructura JSON vacía que represente el formato del documento
               2. Una plantilla Markdown que replique el estilo

               IMPORTANTE: Tu respuesta debe contener ÚNICAMENTE:
               - Primero el JSON
               - Luego el texto exacto "---MARKDOWN TEMPLATE---" en una línea nueva
               - Finalmente la plantilla Markdown con su CSS correspondiente""",
               "attachments": [
                   {
                       "file_id": template_file.id,
                       "tools": [{"type": "file_search"}]
                   }
               ]
           }
       ]
   )
   
   # 3. Crear y ejecutar el run
   run = client.beta.threads.runs.create(
       thread_id=thread.id,
       assistant_id="asst_ZKDNl1dbP3OaAZMntLVuxzmd"
   )
   
   # 4. Esperar el resultado
   while run.status != 'completed':
       run = client.beta.threads.runs.retrieve(
           thread_id=thread.id,
           run_id=run.id
       )
   
   # 5. Obtener la respuesta
   messages = client.beta.threads.messages.list(thread_id=thread.id)
   response = messages.data[0].content[0].text.value
   
   try:
       # Separar JSON y Markdown
       json_str, markdown_template = response.split("---MARKDOWN TEMPLATE---")
       
       # Limpiar delimitadores markdown del JSON
       json_str = json_str.replace("```json", "").replace("```", "").strip()
       
       # Limpiar delimitadores markdown del template
       markdown_template = markdown_template.replace("```markdown", "").replace("```", "").strip()
       
       # Parsear el JSON
       json_structure = json.loads(json_str)
       
       return json_structure, markdown_template
   except Exception as e:
       print(f"Error procesando respuesta: {e}")
       print("Respuesta completa:", response)
       raise

if __name__ == "__main__":
   json_structure, markdown_template = analyze_pdf("./inspeccion.pdf")
   
   # Guardar JSON
   with open("estructura.json", "w", encoding="utf-8") as f:
       json.dump(json_structure, f, indent=2, ensure_ascii=False)
   
   # Guardar Markdown
   with open("plantilla.md", "w", encoding="utf-8") as f:
       f.write(markdown_template)