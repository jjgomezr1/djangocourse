import os
from django.conf import settings



class FileStorage:
    def save(self, file, filename: str) -> str:
        """
        Guarda un archivo en MEDIA_ROOT y devuelve la URL pública.
        """
        # Ruta completa del archivo
        path = os.path.join(settings.MEDIA_ROOT, filename)

        # Crear carpetas si no existen
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Guardar el archivo en bloques
        with open(path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Devolver la URL pública para usar en el template
        return settings.MEDIA_URL + filename

class ImageLocalStorage:
    def store(self, request):
        # Obtiene la imagen del formulario
        image_file = request.FILES['profile_image']

        # Carpeta donde se guardará
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_images')
        os.makedirs(upload_dir, exist_ok=True)

        # Ruta final
        image_path = os.path.join(upload_dir, image_file.name)

        # Guarda la imagen en el sistema de archivos
        with open(image_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # Devuelve la URL para mostrar la imagen en la vista
        return os.path.join(settings.MEDIA_URL, 'uploaded_images', image_file.name)