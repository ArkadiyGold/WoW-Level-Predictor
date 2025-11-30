# WoW-Level-Predictor

Предсказание достиг ли персонаж в World of Warcraft максимального уровня (70) на основе расы, класса, зоны и наличия гильдии.

## Задача
Бинарная классификация:
- **Класс 1**: персонаж на уровне 70
- **Класс 0**: персонаж ниже 70 уровня

## Структура проекта
- `data/` — данные
- `models/` — обученная модель
- `notebooks/` — код обучения модели (Google Colab)
- `templates/index.html` — веб-интерфейс
- `installers.txt` — установщик библиотек
- `wowlvlapp.py` — Flask API

 ## Запуск

   ```bash
   git clone https://github.com/ArkadiyGold/wow-level-predictor.git
   cd wow-level-predictor
   pip install -r installers.txt
   python wowlvlapp.py
   ```
