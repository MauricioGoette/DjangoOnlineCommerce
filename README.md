
# Django E-commerce

This is a very simple e-commerce website built with Django.

## Quick demo

[![alt text](https://justdjango.s3-us-west-2.amazonaws.com/media/gifs/djecommerce.gif "Logo")](https://youtu.be/z4USlooVXG0)

---

## Project Summary

The website displays products. Users can add and remove products to/from their cart while also specifying the quantity of each item. They can then enter their address and choose Stripe to handle the payment processing.

---

## Running this project

```
sudo apt install python3-pip
```

To get this project up and running you should start by having Python installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv venvname
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active

deactivate
```

Then install the project dependencies with

```
pip install -r requirements.txt
python3 -m pip install -r requirements.txt 

pip install psycopg2-binary
pip install Pillow
```

Now you can run the project with this command

```
python manage.py runserver

python3 manage.py runserver 192.168.0.111:8000
```

```
python manage.py createsuperuser
```

```
python manage.py makemigrations appname
```

```
python manage.py migrate
```

## Migration reset
Delete migration folder and table in database
python3 manage.py makemigrations core(App)
python3 manage.py migrate core(App)
python3 manage.py migrate


**Note** if you want payments to work you will need to enter your own Stripe API keys into the `.env` file in the settings files.

---
