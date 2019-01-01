# Divine server http request

#### Server requirements
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.linux server like centos  or ubuntu

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.install DataBase postgresql **version 10**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.install **python 2.7** on server

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. install **python2.7-dev**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. install **python2.7-pip**


#### Application requirements

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.clone project in directory

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.cd to project directory

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. pip install virtualenv

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. run ```virtaulenv venv -p python2.7```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. run ```source venv/bin/activate```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6. run ```pip install -r requirements.txt```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;7. run ```psql ``` to login psql command line .run ```psql>\password``` to set password for postgres user

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;8. run ```vim(or nano) ancient_server/settings.py``` and set postgres password in database section

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;9. run ```createdb -h localhost -U postgres -E UTF8 anc_db```. enter password you set before.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;10. run ```python manage.py migrate```

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;11. run ```python manage.py loaddata objects/fixtures/*``` and ```python manage.py loaddata shopping/fixtures/*```
 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;12. run ```python manage.py run server 0.0.0.0:8000``` 

> if deploy in systemd linux server visit [config django in centos7](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-centos-7). if use
initd linux server visit [config django in ubuntu](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04)

 

#### Api's

|    | url                                   |method|description                                       |
|----|---------------------------------------|------|--------------------------------------------------|
| 1  |BASE_URL/api/user                      |POST  |create player                                     |
| 2  |BASE_URL/api/login                     |POST  |login player                                      |
| 3  |BASE_URL/api/user/select_hero/         |POST  |select hero for player                            |
| 4  |BASE_URL/api/user/player_info/         |POST  |fetch user data                                   |
| 5  |BASE_URL/api/user/open_chest/          |POST  |open chest                                        |
| 6  |BASE_URL/api/user/use_skip_gem/        |POST  |skip remaining time for open chest                |
| 7  |BASE_URL/api/user/chest_ready/         |POST  |open chest and use items in chest                 |
| 8  |BASE_URL/api/user/set_player_name/     |POST  |set player name for first time                    |
| 9  |BASE_URL/api/user/change_player_name/  |POST  |change player name for for second                 |
| 10 |BASE_URL/api/user/set_tutorial_done/   |POST  |set tutorial done                                 |
| 11 |BASE_URL/api/user/leader_board/        |POST  |show leaderboard if user join to league           |
| 12 |BASE_URL/api/user/has_league/          |POST  |return true if user join to league else false     |
| 13 |BASE_URL/api/user/claim/               |POST  |if user league improved claim add to user currency|




