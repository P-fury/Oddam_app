from django.core.management import BaseCommand
from oddam_app.models import Category, Institution
from user.models import CustomUser


class Command(BaseCommand):
    help = "Seeding seed data"

    def handle(self, *args, **options):
        for i in range(5):
            user = CustomUser.objects.create_user(
                username=f"user{i}",
                email=f"user{i}@test.com",
                first_name=f"user{i}",
                password="test123user",
            )

        category_names = ['ubrania', 'zabawki', 'figurki', 'buty', 'książki', 'elektronika', 'meble']
        for name in category_names:
            Category.objects.create(name=name)

        first_inst = Institution.objects.create(name='Przed siebie', description='idziemy do przodu', type='fundacja')
        first_inst.categories.add(*Category.objects.filter(name__in=['zabawki', 'figurki', 'buty']))
        print("Institution created:", first_inst)

        second_inst = Institution.objects.create(name='wszystko i nic', description='dlaciebie nic dla nas wszystko',
                                                 type='organizacja_pozarządowa')
        second_inst.categories.add(*Category.objects.filter(name__in=['zabawki', 'elektronika', 'ubrania', 'meble']))

        third_inst = Institution.objects.create(name='local heroes', description='mali bohaterowie z podworka',
                                                type='zbiórka_lokalna')
        third_inst.categories.add(*Category.objects.filter(name__in=['ubrania', 'meble', 'figurki', 'ksiazki']))

        self.stdout.write(self.style.SUCCESS('Successfully seeded database.'))
