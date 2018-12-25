from objects.models import UserCard, UserHero, \
    UserCardSpell, UserHeroSpell, UserChakraSpell, UnitSpell, HeroSpell, ChakraSpell


def create_user_card_spell():
    for instance in UserCard.objects.all():
        for spell in UnitSpell.objects.filter(unit=instance.character):
            if not UserCardSpell.objects.filter(user_card=instance, spell_id=spell.id).exists():
                UserCardSpell.objects.create(user_card=instance, spell_id=spell.id)
                print "new user card created for ", spell.id

            else:
                print "spell card exists"


def create_hero_card_spell():
    for instance in UserHero.objects.all():
        for spell in HeroSpell.objects.filter(hero=instance.hero):
            if not UserHeroSpell.objects.filter(user_hero=instance, spell_id=spell.id).exists():
                UserHeroSpell.objects.create(user_hero=instance, spell_id=spell.id)
                print "new hero spell created"

            else:
                print "hero spell card already exists"


def create_chakra_card_spell():
    for instance in UserHero.objects.all():
        for spell in ChakraSpell.objects.filter(hero=instance.hero):
            if not UserChakraSpell.objects.filter(user_hero=instance, spell_id=spell.id).exists():
                UserChakraSpell.objects.create(user_hero=instance, spell_id=spell.id)
                print "new chakra spell created"

            else:
                print "chakra spell card already exists"