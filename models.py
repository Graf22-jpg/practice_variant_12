"""Класи предметної області: Client, Service, Order, OrderItem.

Структура відповідає docs/class-diagram.png та docs/data-model.md.
Атрибути, конструктори й методи класів реалізуються на день 6.
"""

from decimal import Decimal
from enum import Enum


class OrderStatus(Enum):
    """Статус замовлення (BR-08)."""

    ACCEPTED = "Прийнято"
    IN_PROGRESS = "В роботі"
    READY = "Готово"
    ISSUED = "Видано"
    CANCELLED = "Скасовано"


class Material(Enum):
    """Матеріал речі та коефіцієнт вартості (BR-03)."""

    NORMAL = ("Звичайна тканина", Decimal("1.0"))
    DELICATE = ("Делікатна тканина", Decimal("1.3"))
    LEATHER_FUR = ("Шкіра, замша, хутро", Decimal("1.5"))

    def __init__(self, label: str, coefficient: Decimal) -> None:
        self.label = label
        self.coefficient = coefficient


class Client:
    """Клієнт хімчистки."""


class Service:
    """Послуга з прайс-листа."""


class OrderItem:
    """Річ у замовленні з вибраними послугами."""


class Order:
    """Замовлення (квитанція)."""
