from typing import Any

import redis
from redis_lru import RedisLRU

from seeds.models import Author, Quote

# Підключення до Redis
client = redis.StrictRedis(host="localhost", port=6379, password=None)
# Створення кешу з обмеженням LRU (Least Recently Used)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    """
    Пошук цитат за тегом з використанням кешування LRU.

    Args:
        tag: Тег для пошуку.

    Returns:
        Список цитат, автори яких містять повне ім'я або опис, що відповідає тегу, або повідомлення "NO MATCHES", якщо результатів немає.
    """
    print(f"Find by tag '{tag}'")
    quotes = Quote.objects(tags__iregex=tag)
    result = {}
    for q in quotes:
        result[q.author.fullname] = q.quote
    if result:
        return result
    else:
        return "NO MATCHES"


@cache
def find_by_author(author: str) -> list[list[Any]]:
    """
    Пошук цитат за ім'ям автора з використанням кешування LRU.

    Args:
        author: Повне або часткове ім'я автора.

    Returns:
        Список цитат для кожного автора, або повідомлення "NO MATCHES", якщо результатів немає.
    """
    print(f"Find by name '{author}'")
    authors = Author.objects(fullname__istartswith=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    if result:
        return result
    else:
        return "NO MATCHES"


def handler():
    """
    Основний цикл програми, що обробляє вхідні запити користувача.
    """
    while True:
        request = input(">>> ")
        request.strip()

        if request.startswith("exit"):
            print("Bye")
            break
        if request.startswith("tag:"):
            tags = request[4:].strip()
            try:
                for tag in tags.split(","):
                    print(find_by_tag(tag))
            except ValueError:
                print(find_by_tag(tags))
        if request.startswith("name:"):
            name = request[5:].strip()
            print(find_by_author(name))
        else:
            pass


if __name__ == "__main__":
    handler()
