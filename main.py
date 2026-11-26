"""Точка входу: запуск програми та консольне меню.

Система управління послугами хімчистки (варіант 12).
"""

from typing import Callable

APP_NAME = "Система управління послугами хімчистки"
VARIANT = 12

NOT_IMPLEMENTED_MESSAGE = "Функція буде реалізована пізніше."

# Пункт меню: (клавіша, назва, обробник)
MenuItem = tuple[str, str, Callable[[], None]]


def not_implemented() -> None:
    """Тимчасовий обробник для ще не реалізованих функцій."""
    print(NOT_IMPLEMENTED_MESSAGE)
    pause()


def pause() -> None:
    input("\nНатисніть Enter, щоб продовжити...")


def run_menu(title: str, items: list[MenuItem], exit_label: str) -> None:
    """Показує меню, поки користувач не обере пункт «0».

    Неправильний вибір не завершує програму: виводиться повідомлення,
    і меню показується знову.
    """
    handlers = {key: handler for key, _, handler in items}

    while True:
        print()
        print("=" * 50)
        print(f" {title}")
        print("=" * 50)
        for key, label, _ in items:
            print(f" {key}. {label}")
        print(f" 0. {exit_label}")
        print("-" * 50)

        choice = input("Оберіть пункт меню: ").strip()

        if choice == "0":
            return
        if choice not in handlers:
            print("Невірний вибір, спробуйте ще раз.")
            continue

        print()
        handlers[choice]()


# ---------- Підменю ----------

def clients_menu() -> None:
    run_menu(
        "Клієнти",
        [
            ("1", "Зареєструвати клієнта", not_implemented),
            ("2", "Переглянути всіх клієнтів", not_implemented),
            ("3", "Знайти клієнта (телефон / ПІБ)", not_implemented),
            ("4", "Редагувати клієнта", not_implemented),
            ("5", "Видалити клієнта", not_implemented),
        ],
        exit_label="Назад",
    )


def price_list_menu() -> None:
    run_menu(
        "Прайс-лист послуг",
        [
            ("1", "Переглянути прайс-лист", not_implemented),
            ("2", "Додати послугу", not_implemented),
            ("3", "Редагувати послугу", not_implemented),
            ("4", "Деактивувати / активувати послугу", not_implemented),
        ],
        exit_label="Назад",
    )


def orders_view_menu() -> None:
    run_menu(
        "Перегляд і пошук замовлень",
        [
            ("1", "Усі замовлення", not_implemented),
            ("2", "Знайти замовлення за номером", not_implemented),
            ("3", "Фільтр за статусом", not_implemented),
            ("4", "Фільтр за клієнтом", not_implemented),
            ("5", "Сортування списку замовлень", not_implemented),
        ],
        exit_label="Назад",
    )


# ---------- Головне меню ----------

MAIN_MENU: list[MenuItem] = [
    ("1", "Клієнти", clients_menu),
    ("2", "Прайс-лист послуг", price_list_menu),
    ("3", "Оформити замовлення", not_implemented),
    ("4", "Перегляд і пошук замовлень", orders_view_menu),
    ("5", "Змінити статус замовлення", not_implemented),
    ("6", "Скасувати замовлення", not_implemented),
    ("7", "Видати замовлення клієнту", not_implemented),
    ("8", "Прострочені замовлення", not_implemented),
]


def print_header() -> None:
    print("=" * 50)
    print(f" {APP_NAME}")
    print(f" Варіант № {VARIANT}")
    print("=" * 50)
    print("Програму успішно запущено.")


def main() -> None:
    print_header()
    try:
        run_menu("Головне меню", MAIN_MENU, exit_label="Вихід")
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C / Ctrl+Z: завершуємо без трасування помилки (E-20)
        print()
    print("Роботу програми завершено. До побачення!")


if __name__ == "__main__":
    main()
