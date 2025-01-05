from openai import OpenAI
import json

client = OpenAI()

def analyze_image(image_path, image_name, context_info):
    # 1. Subir la imagen
    file = client.files.create(
        file=open(image_path, "rb"),
        purpose="vision"
    )
    
    # 2. Crear el thread con el mensaje y la imagen
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Context information: {context_info}
                        Image name: {image_name}
                        Please analyze this image and provide a JSON with:
                        - description
                        - observations
                        - image_name"""
                    },
                    {
                        "type": "image_file",
                        "image_file": {"file_id": file.id}
                    }
                ]
            }
        ]
    )
    
    # 3. Crear y ejecutar el run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_9JcjVs8igGS2iIHPMtQZhkQC" # Aquí va el ID de tu asistente
    )
    
    # 4. Esperar el resultado
    while run.status != 'completed':
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    
    # 5. Obtener la respuesta
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    json_string = messages.data[0].content[0].text.value  # Obtenemos el string JSON
    return json.loads(json_string)  # Convertimos el string JSON a un diccionario de Python


# Uso
if __name__ == "__main__":
    #test code
    result = analyze_image(
        "./images.jpeg",
        "image_name.png",
        "No debe existir agujeros grandes en el suelo. No deben haber personas cerca de cualquier agujero pequeño o grande que haya."
    )
    print(result)