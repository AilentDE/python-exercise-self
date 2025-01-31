# pip install Faker, loguru
from loguru import logger
from faker import Faker
from random import randint, choice
from collections import deque
from itertools import groupby
from operator import itemgetter
from typing import Callable

fake = Faker()

cities: deque[str] = deque()
for _ in range(5):
    while tar := fake.city():
        if tar not in cities:
            cities.append(tar)
            break
logger.info(f"cities: {list(cities)}")

peoples: deque[dict[str, str | int]] = deque()
for _ in range(10):
    peoples.append(
        {
            "name": fake.name(),
            "age": randint(18, 60),
            "city": choice(cities),
        }
    )
logger.info(f"peoples: {list(map(lambda x: x['name'], peoples))}")

get_city: Callable[[dict[str, str | int]], str] = itemgetter("city")
sorted_peoples: list[dict[str, str | int]] = sorted(peoples, key=get_city)

logger.success("sorted_peoples:")
for person in sorted_peoples:
    logger.info(f"{person['city']}: {person['name']}")

logger.success("groupby:")
for city, people in groupby(sorted_peoples, get_city):
    logger.info(f"{city}: {list(people)}")
