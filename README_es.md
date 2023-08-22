Django E-commerce

Este es un sitio web de comercio electrónico muy simple construido con Django.

---

Resumen del proyecto

El sitio web muestra productos. Los usuarios pueden agregar y quitar productos de su carrito, al mismo tiempo que especifican la cantidad de cada artículo. Luego pueden ingresar su dirección y elegir Stripe para manejar el procesamiento de pagos.

---

Ejecutar el Proyecto

Para poner en marcha este proyecto, sigue estos pasos:

1. Instala Python 3 y pip:

   sudo apt install python3-pip

2. Crea un entorno virtual para el proyecto:

   pip install virtualenv

3. Clona o descarga este repositorio y ábrelo en tu editor.

4. En una terminal, ejecuta el siguiente comando en el directorio base del proyecto para crear el entorno virtual:

   virtualenv nombredelentorno

5. Activa el entorno virtual (en Mac/Linux):

   source nombredelentorno/bin/activate

6. Instala las dependencias del proyecto:

   pip install -r requirements.txt
   pip install psycopg2-binary
   pip install Pillow

7. Ejecuta el proyecto:

   python manage.py runserver

8. Para crear un superusuario:

   python manage.py createsuperuser

9. Para realizar migraciones:

   python manage.py makemigrations nombredelaaplicacion
   python manage.py migrate

10. En caso de necesitar restablecer migraciones:

    Eliminar la carpeta de migración y la tabla en la base de datos
    python3 manage.py makemigrations core(Aplicación)
    python3 manage.py migrate core(Aplicación)
    python3 manage.py migrate

Nota: Si deseas que los pagos funcionen, deberás ingresar tus propias claves de API de Stripe en el archivo .env en los archivos de configuración.
