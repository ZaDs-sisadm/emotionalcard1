## 👤 Автор

| Поле        | Інформація                                      |
|-------------|-------------------------------------------------|
| Автор       | ZaDs-sisadm                                     |
| Гілка       | `lab1`                                          |
| Репозиторій | https://github.com/ZaDs-sisadm/emotionalcard1   |

---

## 📋 Вимоги

- Python **3.10+**
- pip

---

## ⚙️ Конфігурація

Проєкт використовує файл `config.py` (або `.env`) для налаштувань середовища:

```python
# config.py
DEBUG = True
HOST  = "localhost"
PORT  = 8501
GDPR_COOKIE_EXPIRY_DAYS = 365
APP_NAME = "EmotionalCards"
```

Також можна використовувати змінні середовища:

```bash
export DEBUG=True
export PORT=8501
```

---

## 🚀 Основні команди

### Встановлення залежностей
```bash
pip install -r requirements.txt
```

### Запуск основного застосунку
```bash
python main.py
```

### Запуск Storybook (Streamlit)
```bash
streamlit run storybook/storybook_app.py
```

### Генерація документації (pdoc)
```bash
pdoc --html --output-dir docs components/
```

### Перевірка ліцензій
```bash
pip-licenses --format=markdown > license-report.md
```

### Запуск тестів
```bash
pytest tests/
```

---

## 📁 Структура проєкту

```
emotionalcard1/
├── components/
│   ├── card.py           # Базовий компонент Card
│   └── emotional_card.py # Комплексний компонент EmotionalCard
├── cookie_popup/
│   └── gdpr_cookie.py    # Модуль GDPR Cookie Consent
├── storybook/
│   └── storybook_app.py  # Streamlit Storybook
├── docs/                 # Автоматично згенерована документація
├── config.py
├── main.py
├── requirements.txt
├── LICENSE
├── PRIVACY_POLICY.md
├── license-report.md
└── README.md
```

---

## 📜 Ліцензія

Цей проєкт ліцензований під **MIT License** — деталі у файлі [LICENSE](./LICENSE).

---

## 🔒 Конфіденційність

Проєкт відповідає вимогам GDPR. Деталі у файлі [PRIVACY_POLICY.md](./PRIVACY_POLICY.md).
