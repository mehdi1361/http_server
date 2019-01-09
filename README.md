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

> use  BASE_URL before all api

|    | url                            |method|description                                             |
|----|--------------------------------|------|--------------------------------------------------------|
| 1  |/api/user                       |POST  |create player                                           |
| 2  |/api/login                      |POST  |login player                                            |
| 3  |/api/user/select_hero/          |POST  |select hero for player                                  |
| 4  |/api/user/player_info/          |POST  |fetch user data                                         |
| 5  |/api/user/open_chest/           |POST  |open chest                                              |
| 6  |/api/user/use_skip_gem/         |POST  |skip remaining time for open chest                      |
| 7  |/api/user/chest_ready/          |POST  |open chest and use items in chest                       |
| 8  |/api/user/set_player_name/      |POST  |set player name for first time                          |
| 9  |/api/user/change_player_name/   |POST  |change player name for for second                       |
| 10 |/api/user/set_tutorial_done/    |POST  |set tutorial done                                       |
| 11 |/api/user/leader_board/         |POST  |show leaderboard if user join to league                 |
| 12 |/api/user/has_league/           |POST  |return true if user join to league else false           |
| 13 |/api/user/claim/                |POST  |if user league improved claim add to user currency      |
| 14 |/api/user/active_playoff/       |POST  |active playoff                                          |
| 15 |/api/user/skip_gem_cool_down/   |POST  |if troop cooldown skip cooldown with gem                |
| 16 |/api/user/match_count/          |POST  |user games count                                        |
| 17 |/api/user/video_ads/            |POST  |decrease user troop cooldown                            |
| 18 |/api/user/register_account/     |POST  |register google account if ok add benefit to user       |
| 19 |/api/shop/store/                |POST  |return store data                                       |
| 20 |/api/shop/buy_gem/              |POST  |if ok from store add gem to user gem                    |
| 21 |/api/shop/buy_coin/             |POST  |if ok decrease gem and increase coin                    |
| 22 |/api/shop/buy_chest/            |POST  |if ok decrease gem and buy chest                        |
| 23 |/api/troop/level_up/            |POST  |if card is enough update user troop card level          |
| 24 |/api/troop/spell_level_up/      |POST  |if card is enough update user troop spell card level    |
| 25 |/api/hero/level_up/             |POST  |if card is enough update user hero card level           |
| 26 |/api/hero/spell_level_up/       |POST  |if card is enough update user hero spell card level     |
| 27 |/api/hero/chakra_spell_level_up/|POST  |if card is enough update user chakra spell card level   |
| 28 |/api/hero/selected_items/       |POST  |if ok hero selected item updated                        |
| 29 |/api/item/level_up/             |POST  |if card is enough update item card level                |
| 30 |/api/message/read/              |POST  |if ok return 200 and change message status to ready     |



#### database class model


