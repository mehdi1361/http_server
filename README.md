# Divine server http request

##### Server requirements
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.linux server like centos  or ubuntu

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.install DataBase postgresql **version 10**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.install **python 2.7** on server

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. install **python2.7-dev**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. install **python2.7-pip**


##### Application requirements

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.clone project in directory

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.cd to project directory

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. pip install virtualenv

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. run ```virtaulenv venv -p python2.7```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. run ```source venv/bin/activate```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. run ```source venv/bin/activate```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6. run ```pip install -r requirements.txt```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7. run ```psql ``` to login psql command line .run ```psql>\password``` to set password for postgres user

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7. run ```vim(or nano) ancient_server/settings.py``` and set postgres password in database section

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7. run ```createdb -h localhost -U postgres -E UTF8 anc_db```. enter password you set before.


&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8. run ```python manage.py migrate```
