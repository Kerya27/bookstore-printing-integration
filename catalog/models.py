from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    """Категорія книг (наприклад: Художня, Наукова, Дитяча)"""
    name = models.CharField(max_length=200, verbose_name='Назва')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, verbose_name='Опис')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name


class Book(models.Model):
    """Книга в каталозі"""
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='books',
        verbose_name='Категорія'
    )
    title = models.CharField(max_length=300, verbose_name='Назва')
    author = models.CharField(max_length=200, verbose_name='Автор')
    description = models.TextField(blank=True, verbose_name='Опис')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна')
    stock = models.PositiveIntegerField(default=0, verbose_name='Кількість на складі')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Обкладинка')
    is_available = models.BooleanField(default=True, verbose_name='Доступна')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'{self.title} — {self.author}'


class Order(models.Model):
    """Замовлення покупця"""
    STATUS_CHOICES = [
        ('new', 'Нове'),
        ('confirmed', 'Підтверджено'),
        ('printing', 'В друці'),
        ('ready', 'Готово'),
        ('shipped', 'Відправлено'),
        ('delivered', 'Доставлено'),
    ]

    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Користувач'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='new', verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата оновлення')
    comment = models.TextField(blank=True, verbose_name='Коментар')

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']

    def __str__(self):
        return f'Замовлення #{self.pk} — {self.user.username}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    """Позиція в замовленні"""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Замовлення'
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE,
        verbose_name='Книга'
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна на момент замовлення')

    class Meta:
        verbose_name = 'Позиція замовлення'
        verbose_name_plural = 'Позиції замовлення'

    def __str__(self):
        return f'{self.book.title} x{self.quantity}'

    def get_total_price(self):
        return self.price * self.quantity


class PrintJob(models.Model):
    """Виробниче завдання на друк"""

    STATUS_CHOICES = [
        ('pending',   'Очікує'),
        ('prepress',  'Додрукарська підготовка'),
        ('printing',  'Друк'),
        ('postpress', 'Післядрукарська обробка'),
        ('done',      'Виконано'),
    ]

    PRINT_METHOD_CHOICES = [
        ('offset',  'Офсетний друк'),
        ('digital', 'Цифровий друк'),
        ('risograph', 'Ризографія'),
    ]

    BINDING_CHOICES = [
        ('perfect', 'Клейове скріплення (КБС)'),
        ('thread',  'Ниткове зшивання'),
        ('staple',  'Скобка (брошурування)'),
        ('hardcover', 'Тверда палітурка'),
    ]

    PAPER_CHOICES = [
        ('offset_80',  'Офсетний 80 г/м²'),
        ('offset_120', 'Офсетний 120 г/м²'),
        ('coated_130', 'Крейдований 130 г/м²'),
        ('coated_170', 'Крейдований 170 г/м²'),
    ]

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE,
        related_name='print_job',
        verbose_name='Замовлення'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name='Статус виробництва'
    )

    # Технологічні параметри
    format = models.CharField(
        max_length=20, blank=True, verbose_name='Формат видання',
        help_text='Наприклад: 60×84/16, 70×100/16'
    )
    circulation = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Тираж (прим.)'
    )
    print_method = models.CharField(
        max_length=20, choices=PRINT_METHOD_CHOICES,
        blank=True, verbose_name='Спосіб друку'
    )
    paper_type = models.CharField(
        max_length=20, choices=PAPER_CHOICES,
        blank=True, verbose_name='Тип паперу'
    )
    binding_type = models.CharField(
        max_length=20, choices=BINDING_CHOICES,
        blank=True, verbose_name='Тип скріплення'
    )

    notes = models.TextField(blank=True, verbose_name='Виробничі примітки')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='Початок виробництва')
    finished_at = models.DateTimeField(null=True, blank=True, verbose_name='Завершення виробництва')

    class Meta:
        verbose_name = 'Виробниче завдання'
        verbose_name_plural = 'Виробничі завдання'

    def __str__(self):
        return f'Виробниче завдання для замовлення #{self.order.pk}'

    def get_duration(self):
        """Повертає тривалість виробництва або None"""
        if self.started_at and self.finished_at:
            return self.finished_at - self.started_at
        return None

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, verbose_name='Адреса доставки')

    class Meta:
        verbose_name = 'Профіль'
        verbose_name_plural = 'Профілі'

    def __str__(self):
        return f'Профіль {self.user.username}'

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)