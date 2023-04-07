from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import os
import urllib.request

app = FastAPI()

@app.post("/convert")
async def convert_image(file: UploadFile = File(...)):
    # Leer la imagen subida y guardarla en una carpeta temporal
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Cargar la imagen con la librería cv2
    img = cv2.imread(file.filename)
    
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Guardar la imagen en el repositorio de GitHub
    img_name = os.path.splitext(file.filename)[0]
    cv2.imwrite(f"{img_name}_gray.jpg", gray)
    repo_url = "https://github.com/usuario/repositorio.git"
    repo_dir = "/ruta/a/repositorio/"
    os.chdir(repo_dir)
    os.system("git pull")
    os.system("git add .")
    os.system(f'git commit -m "Agregada imagen en escala de grises {img_name}"')
    os.system("git push")
    urllib.request.urlopen(f"https://api.github.com/repos/usuario/repositorio/actions/workflows/workflow.yml/dispatches",
                            data=b'{"ref":"main"}')
    return {"message": f"Imagen convertida a escala de grises y guardada en {repo_url}"}
