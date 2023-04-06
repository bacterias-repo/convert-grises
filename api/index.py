import cv2
import requests
from io import BytesIO
from github import Github

def grayscale_image(url):
    # Descarga la imagen desde la URL
    response = requests.get(url)
    img = cv2.imdecode(np.frombuffer(response.content, np.uint8), 1)

    # Convierte la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Crea un objeto BytesIO para guardar la imagen en memoria
    buffer = BytesIO()
    cv2.imwrite(buffer, gray)
    buffer.seek(0)

    return buffer

def upload_to_github(buffer):
    # Autenticación con la API key de GitHub
    g = Github("tu_api_key")

    # Accede al repositorio y a la carpeta de imágenes
    repo = g.get_repo("tu_usuario/tu_repositorio")
    contents = repo.get_contents("images")

    # Guarda la imagen en la carpeta de imágenes
    filename = "grayscale_image.jpg"
    repo.create_file(f"images/{filename}", f"Convirtiendo imagen a escala de grises", buffer.getvalue(), branch="main")

    # Retorna la URL de la imagen en el repositorio de GitHub
    return f"https://raw.githubusercontent.com/tu_usuario/tu_repositorio/main/images/{filename}"

def main(request):
    # Obtiene la URL de la imagen a convertir
    url = request.args.get('url')

    # Convierte la imagen a escala de grises y la guarda en GitHub
    buffer = grayscale_image(url)
    url_github = upload_to_github(buffer)

    # Retorna la URL de la imagen en escala de grises en GitHub
    return {'url': url_github}
