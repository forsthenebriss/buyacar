# buyacar

BuyACar is a django project developed for Web App Development. This app allows to create an account and browse cars currently in the database, contact the seller by email, or to add own car for sale and become a seller. 

## Authors
Yiwei Liu 2431251L 
Romana Canigova 2481149C
Zelong Huang  2430984H
Harry Borthwick 2465129B

## Set up

1) clone the git repository
```bash
$ git clone https://github.com/forsthenebriss/buyacar.git
```
2) ented the repository and activate rango
```bash
$ cd buyacar
$ conda activate rango
```
3) make migrations and populate script
```python
(rango) $ pyhton manage.py makemigrations rango
(rango) $ python manage.py migrate
(rango) $ python population_script.py
```
4) create a superuser to access the database
```pyhton
(rango) $ python manage.py createsuperuser
```
5)install the requirements
```bash
(rango) $ pip install -r requirements.txt
```
6) run server, you are all set up
```python
(rango) $ python manage.py runserver
```

## PythonAnywhere url
http://forsthenebriss.pythonanywhere.com/

## External sources used


Tango With Django (old project as template, book source)
https://getbootstrap.com/docs/ (official documentation)
https://www.w3schools.com/  (HTML/CSS/Javascript)
https://stackoverflow.com (for looking up coding errors)
