# Notino UI Tests — Лабораторна робота №2

Автоматизовані UI-тести для веб-застосунку [notino.ua](https://www.notino.ua/) на основі Selenium WebDriver + pytest.

## Технології

- Python 3.14
- Selenium WebDriver
- pytest
- ChromeDriver (undetected)

## Структура проєкту
```
NotinoTests/
├── test_notino.py   # Тест-кейси
├── conftest.py      # Конфігурація драйвера
├── utils.py         # Допоміжні функції
└── README.md
```

## Тести

| Тест | Тест-кейс | Опис |
|------|-----------|------|
| test_valid_search | TC_1 | Пошук «Calvin Klein» |
| test_invalid_search | TC_3 | Невалідний пошук |
| test_add_product_to_cart | TC_10 | Додавання товару в кошик |
| test_login_page_ui | TC_5 | Перевірка UI сторінки входу |
| test_filter_by_brand | TC_8 | Фільтрація за брендом Hugo Boss |

## Запуск

Встанови залежності:
```
pip install selenium pytest
```

Запусти тести:
```
pytest -v test_notino.py 
```
