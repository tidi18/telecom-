import logging
from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta, date
from .models import Book



new_books_logger = logging.getLogger("new_books_logger")
new_books_handler = logging.FileHandler('new_books.log', encoding='utf-8')
new_books_formatter = logging.Formatter('%(asctime)s - %(message)s')
new_books_handler.setFormatter(new_books_formatter)
new_books_logger.addHandler(new_books_handler)
new_books_logger.setLevel(logging.INFO)


anniversary_logger = logging.getLogger("anniversary_logger")
anniversary_handler = logging.FileHandler('anniversary_books.log', encoding='utf-8')
anniversary_formatter = logging.Formatter('%(asctime)s - %(message)s')
anniversary_handler.setFormatter(anniversary_formatter)
anniversary_logger.addHandler(anniversary_handler)
anniversary_logger.setLevel(logging.INFO)


@shared_task
def notify_new_books():
    """Логирует новые книги за последние 24 часа"""

    yesterday = timezone.now() - timedelta(days=1)
    new_books = Book.objects.filter(created_at__gte=yesterday)

    if not new_books.exists():
        new_books_logger.info("Нет новых книг за последние 24 часа")
        return "Нет новых книг"

    book_list = ", ".join([book.title for book in new_books])
    users = User.objects.all()

    for user in users:
        new_books_logger.info(
            f"Пользователь {user.email}: новые книги за последние 24 часа: {book_list}"
        )

    return f"Уведомления о новых книгах отправлены {users.count()} пользователям"


@shared_task
def notify_anniversary_books():
    """Логирует юбилейные книги"""
    today = timezone.localdate()
    users = User.objects.all()
    anniversary_years = [5, 10, 20, 25, 50, 75, 100]

    books = Book.objects.all()

    found = False

    for book in books:
        pub_date = book.publication_date

        if pub_date.day == today.day and pub_date.month == today.month:
            years_passed = today.year - pub_date.year

            if years_passed in anniversary_years:
                found = True

                for user in users:
                    anniversary_logger.info(
                        f"Пользователь {user.email}: юбилей книги '{book.title}' — {years_passed} лет!"
                    )

    if not found:
        return "Проверка юбилейных книг выполнена"

    return "Юбилейные книги найдены"