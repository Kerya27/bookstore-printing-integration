# catalog/management/commands/generate_orders.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from catalog.models import Book, Order, OrderItem, PrintJob, Profile

class Command(BaseCommand):
    help = 'Генерує тестові замовлення за 3 місяці'

    def handle(self, *args, **kwargs):
        books = list(Book.objects.filter(is_available=True))
        if not books:
            self.stdout.write(self.style.ERROR('Немає книг в каталозі!'))
            return

        names = [
            ('Олена', 'Коваль', 'olena.koval@gmail.com'),
            ('Михайло', 'Бондар', 'mykhailo.bondar@ukr.net'),
            ('Аліна', 'Шевченко', 'alina.shevchenko@gmail.com'),
            ('Дмитро', 'Мельник', 'dmytro.melnyk@gmail.com'),
            ('Наталія', 'Лисенко', 'natalia.lysenko@ukr.net'),
            ('Андрій', 'Кравченко', 'andriy.kravchenko@gmail.com'),
            ('Юлія', 'Савченко', 'yulia.savchenko@gmail.com'),
            ('Ігор', 'Ткаченко', 'ihor.tkachenko@ukr.net'),
            # Нові 30 користувачів
            ('Богдан', 'Романенко', 'bohdan.romanenko@gmail.com'),
            ('Оксана', 'Гриценко', 'oksana.hrytsenko@ukr.net'),
            ('Василь', 'Петренко', 'vasyl.petrenko@gmail.com'),
            ('Тетяна', 'Карпенко', 'tetiana.karpenko@ukr.net'),
            ('Сергій', 'Демиденко', 'serhii.demydenko@gmail.com'),
            ('Марія', 'Захаренко', 'mariia.zakharenko@gmail.com'),
            ('Олексій', 'Науменко', 'oleksii.naumenko@ukr.net'),
            ('Вікторія', 'Білоус', 'viktoriia.bilous@gmail.com'),
            ('Павло', 'Тимошенко', 'pavlo.tymoshenko@gmail.com'),
            ('Інна', 'Волошин', 'inna.voloshyn@ukr.net'),
            ('Руслан', 'Бойко', 'ruslan.boiko@gmail.com'),
            ('Людмила', 'Яременко', 'liudmyla.yaremenko@ukr.net'),
            ('Максим', 'Голуб', 'maksym.holub@gmail.com'),
            ('Катерина', 'Дорошенко', 'kateryna.doroshenko@gmail.com'),
            ('Олег', 'Семененко', 'oleh.semenenko@ukr.net'),
            ('Ганна', 'Марченко', 'hanna.marchenko@gmail.com'),
            ('Микола', 'Левченко', 'mykola.levchenko@ukr.net'),
            ('Лариса', 'Пономаренко', 'larysa.ponomarenko@gmail.com'),
            ('Артем', 'Власенко', 'artem.vlasenko@gmail.com'),
            ('Світлана', 'Остапенко', 'svitlana.ostapenko@ukr.net'),
            ('Денис', 'Федоренко', 'denys.fedorenko@gmail.com'),
            ('Тамара', 'Іваненко', 'tamara.ivanenko@ukr.net'),
            ('Євген', 'Корниєнко', 'yevhen.kornienko@gmail.com'),
            ('Ірина', 'Панченко', 'iryna.panchenko@ukr.net'),
            ('Степан', 'Гончаренко', 'stepan.honcharenko@gmail.com'),
            ('Надія', 'Коломієць', 'nadiia.kolomiets@gmail.com'),
            ('Роман', 'Поліщук', 'roman.polishchuk@ukr.net'),
            ('Валентина', 'Кириченко', 'valentyna.kyrychenko@gmail.com'),
            ('Антон', 'Даниленко', 'anton.danylenko@ukr.net'),
            ('Жанна', 'Супруненко', 'zhanna.suprunenko@gmail.com'),
        ]

        phones = [
            '+380661234567', '+380971234567', '+380991234567',
            '+380501234567', '+380631234567', '+380731234567',
            '+380671234567', '+380931234567', '+380951234567',
            '+380661112233', '+380972223344', '+380993334455',
            '+380504445566', '+380635556677', '+380736667788',
            '+380677778899', '+380938889900', '+380959990011',
            '+380661010101', '+380972020202', '+380993030303',
            '+380504040404', '+380635050505', '+380736060606',
            '+380677070707', '+380938080808', '+380959090909',
            '+380661111222', '+380972222333', '+380993333444',
            '+380504444555', '+380635555666', '+380736666777',
            '+380677777888', '+380938888999', '+380959999000',
            '+380660001111', '+380971112222',
        ]

        addresses = [
            'м. Київ, вул. Хрещатик, 10, кв. 5',
            'м. Львів, вул. Шевченка, 22, кв. 3',
            'м. Харків, пр. Науки, 14, кв. 8',
            'м. Одеса, вул. Дерибасівська, 7, кв. 12',
            'м. Дніпро, вул. Робоча, 33, кв. 1',
            'м. Запоріжжя, вул. Козацька, 5, кв. 7',
            'м. Вінниця, вул. Соборна, 18, кв. 4',
            'м. Полтава, вул. Пушкіна, 9, кв. 6',
            'м. Київ, вул. Велика Васильківська, 45, кв. 2',
            'м. Львів, вул. Франка, 11, кв. 9',
            'м. Харків, вул. Сумська, 28, кв. 15',
            'м. Одеса, вул. Рішельєвська, 3, кв. 7',
            'м. Дніпро, пр. Яворницького, 55, кв. 11',
            'м. Чернігів, вул. Миру, 6, кв. 3',
            'м. Суми, вул. Соборна, 14, кв. 8',
            'м. Тернопіль, вул. Руська, 19, кв. 5',
            'м. Хмельницький, вул. Подільська, 32, кв. 10',
            'м. Черкаси, вул. Хрещатик, 8, кв. 4',
            'м. Луцьк, пр. Волі, 13, кв. 2',
            'м. Рівне, вул. Соборна, 20, кв. 6',
            'м. Івано-Франківськ, вул. Незалежності, 7, кв. 14',
            'м. Ужгород, вул. Корзо, 4, кв. 1',
            'м. Кропивницький, вул. Велика Перспективна, 25, кв. 9',
            'м. Миколаїв, пр. Леніна, 30, кв. 3',
            'м. Херсон, вул. Суворова, 17, кв. 7',
            'м. Житомир, вул. Михайлівська, 12, кв. 5',
            'м. Запоріжжя, пр. Соборний, 40, кв. 8',
            'м. Маріуполь, вул. Миру, 22, кв. 2',
            'м. Бердянськ, вул. Свободи, 9, кв. 6',
            'м. Мелітополь, вул. Центральна, 15, кв. 4',
            'м. Біла Церква, вул. Ярослава Мудрого, 3, кв. 11',
            'м. Бровари, вул. Київська, 18, кв. 7',
            'м. Ірпінь, вул. Садова, 6, кв. 3',
            'м. Буча, вул. Лісова, 11, кв. 1',
            'м. Вишневе, вул. Соборна, 24, кв. 5',
            'м. Борисполь, вул. Головатого, 8, кв. 9',
            'м. Фастів, вул. Соборна, 14, кв. 2',
            'м. Васильків, вул. Декабристів, 7, кв. 6',
        ]

        # Створюємо користувачів
        test_users = []
        for i, (first, last, email) in enumerate(names):
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first,
                    'last_name': last,
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                profile = user.profile
                profile.phone = phones[i % len(phones)]
                profile.address = addresses[i % len(addresses)]
                profile.save()
                self.stdout.write(f'  Створено: {first} {last} ({email})')
            else:
                self.stdout.write(f'  Вже існує: {email}')
            test_users.append(user)

        self.stdout.write(f'\nКористувачів готово: {len(test_users)}')

        # Логіка статусів залежно від давності
        def get_status(day_offset):
            if day_offset > 60:
                return random.choice([
                    'delivered', 'delivered', 'delivered', 'delivered', 'shipped'
                ])
            elif day_offset > 30:
                return random.choice([
                    'delivered', 'delivered', 'delivered', 'shipped', 'shipped'
                ])
            elif day_offset > 14:
                return random.choice([
                    'delivered', 'shipped', 'shipped', 'ready', 'printing'
                ])
            elif day_offset > 7:
                return random.choice([
                    'shipped', 'ready', 'printing', 'confirmed', 'confirmed'
                ])
            elif day_offset > 3:
                return random.choice([
                    'ready', 'printing', 'confirmed', 'new', 'new'
                ])
            else:
                return random.choice([
                    'printing', 'confirmed', 'new', 'new', 'new'
                ])

        print_statuses = {
            'new': 'pending',
            'confirmed': 'pending',
            'printing': 'in_progress',
            'ready': 'done',
            'shipped': 'done',
            'delivered': 'done',
        }

        comments = [
            'Будь ласка, упакуйте подарунково.',
            'Передзвоніть перед доставкою.',
            '',
            'Доставка до відділення Нової Пошти №3.',
            '',
            'Хочу отримати до п\'ятниці.',
            '',
            'Дякую за швидку обробку!',
            '',
            'Без дзвінків після 20:00.',
            '',
            'Доставте на відділення Укрпошти.',
            '',
        ]

        today = timezone.now().date()
        orders_created = 0

        # 90 днів
        for day_offset in range(90, 0, -1):
            day = today - timedelta(days=day_offset)

            # Більше замовлень у вихідні
            weekday = day.weekday()
            if weekday >= 5:  # субота/неділя
                max_orders = 5
            elif weekday == 4:  # п'ятниця
                max_orders = 4
            else:
                max_orders = 3

            orders_per_day = random.randint(0, max_orders)

            for _ in range(orders_per_day):
                user = random.choice(test_users)
                status = get_status(day_offset)

                order = Order(
                    user=user,
                    status=status,
                    comment=random.choice(comments),
                )
                order.save()

                # Встановлюємо правильну дату
                order_datetime = timezone.make_aware(
                    timezone.datetime(
                        day.year, day.month, day.day,
                        random.randint(8, 22),
                        random.randint(0, 59)
                    )
                )
                Order.objects.filter(pk=order.pk).update(created_at=order_datetime)

                # Книги в замовлення — 1-3 різні
                order_books = random.sample(books, min(random.randint(1, 3), len(books)))
                for book in order_books:
                    quantity = random.randint(1, 2)
                    OrderItem.objects.create(
                        order=order,
                        book=book,
                        quantity=quantity,
                        price=book.price,
                    )

                # PrintJob
                pj_status = print_statuses[status]
                pj = PrintJob(order=order, status=pj_status)

                if pj_status != 'pending':
                    pj.notes = random.choice([
                        'Стандартний друк.',
                        'Глянцева обкладинка.',
                        'Матова обкладинка.',
                        'Термінове виконання.',
                        '',
                    ])

                if pj_status in ('in_progress', 'done'):
                    pj.started_at = order_datetime + timedelta(hours=random.randint(2, 8))
                if pj_status == 'done':
                    pj.finished_at = pj.started_at + timedelta(hours=random.randint(4, 48))

                pj.save()
                orders_created += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nГотово! Створено {orders_created} замовлень за 90 днів '
            f'для {len(test_users)} користувачів.'
        ))