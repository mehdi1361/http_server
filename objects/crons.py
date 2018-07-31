import os
import random
from django.core import management
from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User
from objects.models import UserChest, League, LeagueUser, CreatedLeague, LeagueTime
from datetime import datetime
from django.db  import transaction


class FreeChestCreatorJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'chest.free'    # a unique code

    @staticmethod
    def do():
        # print('test cron')
        for user in User.objects.all():
            if UserChest.deck_is_open(user, 'free'):
                pass


class Backup(CronJobBase):
    RUN_AT_TIMES = ['03:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'objects.Backup'

    def do(self):
        file_name = '{}{}{}.gz'.format(
            datetime.now().year,
            datetime.now().month
            if datetime.now().month > 10 else '0{}'.format(datetime.now().month),
            datetime.now().day
        )
        management.call_command('dbbackup', '-z', '-o {}'.format(file_name))


class LeagueReset(CronJobBase):
    RUN_AT_TIMES = ['1:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'objects.Reset'

    def do(self):
        if LeagueTime.remain_time() == 0:
            result = []

            for created_league in CreatedLeague.enable_leagues.all():
                result += created_league.promoted_list() + created_league.normal_list() \
                          + created_league.demoted_list()
                created_league.close()

            for item in result:
                CreatedLeague.create_or_join(
                    player=item['player'],
                    league=item['league'],
                    prize=item['claim'],
                    league_player=item['claim_league'],
                    type=item['type']
                )

            LeagueTime.reset()

        else:
            print "not yet reset leagues"


class FakeUserGame(CronJobBase):
    RUN_EVERY_MINS = 10
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'objects.fak_game'

    def do(self):
        for created_league in CreatedLeague.enable_leagues.all():
            for fake_user in created_league.params['fake_user']:
                fake_user_chance = random.randint(0, 100)

                if fake_user['win_rate'] > fake_user_chance:
                    fake_user['score'] += random.randint(10, 18)
                    if fake_user['score'] > 1000:
                        fake_user['score'] = random.randint(900, 1000)

                    fake_user['win_rate'] -= 1

                    if fake_user['win_rate'] < fake_user['min_rate']:
                        fake_user['win_rate'] = fake_user['min_rate']

                else:
                    fake_user['score'] -= random.randint(10, 18)
                    if fake_user['score'] < 0:
                        fake_user['score'] = 0

                    fake_user['win_rate'] += 1

                    if fake_user['win_rate'] > fake_user['max_rate']:
                        fake_user['win_rate'] = fake_user['max_rate']

            created_league.save()
