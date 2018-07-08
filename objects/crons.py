import os
from django.core import management
from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User
from objects.models import UserChest, League, LeagueUser, CreatedLeague, LeagueTime
from datetime import datetime


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
            promoted_list = []
            for created_league in CreatedLeague.enable_leagues.all():
                pass

        else:
            pass
