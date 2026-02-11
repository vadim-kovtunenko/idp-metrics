# IDP Dashboard

Дашборд с менеджерскими и аналитическими метриками. Расчёты выполняются в Python, визуализация — Plotly + Dash.

## Структура репозитория

```
idp-dashboard/
├── app.py                 # Точка входа, создание Dash-приложения
├── config/
│   └── theme.py           # Цвета и общие настройки графиков
├── data/
│   └── sample_data.py     # Загрузка и расчёт данных (заменить на реальные источники)
├── components/
│   └── charts.py          # Переиспользуемые графики (Plotly)
├── layout/
│   └── dashboard.py       # Разметка дашборда, сетка графиков
├── assets/
│   └── custom.css         # Адаптивная вёрстка и стили
└── requirements.txt
```

## Запуск

```bash
cd idp-dashboard
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Откройте в браузере: http://localhost:8050

## Текущие графики

1. **RAG Common & SBOL** — линейный график вызовов сервисов по месяцам (ось Y: 20–45 млн).
2. **RAG Common** — линейный график вызовов по месяцам (ось Y: 500 тыс.–3 млн).

Оба графика расположены рядом, с адаптивной сеткой (на узких экранах — друг под другом).

## Добавление новых метрик

- Данные: добавить функцию в `data/` (или новый модуль), возвращающую `pd.DataFrame`.
- График: добавить функцию в `components/charts.py` с использованием `config/theme.py`.
- Разметка: добавить блок в `layout/dashboard.py` в `charts-row` или новую строку сетки.

Цвета и общие настройки осей вынесены в `config/theme.py` для единообразия.
