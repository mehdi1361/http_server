from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User
from objects.models import UserChest


class FreeChestCreatorJob(CronJobBase):
    RUN_EVERY_MINS = 1  # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'chest.free'    # a unique code

    @staticmethod
    def do():
        print('test cron')
        for user in User.objects.all():
            if UserChest.deck_is_open(user, 'free'):
                pass
