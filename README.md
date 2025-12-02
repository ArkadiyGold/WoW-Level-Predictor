# ⚔️ WoW Battleground Predictor
Предсказание шанса победы персонажа в следующем поле боя на основе его фракции, класса, роли и активности в бонусных событиях.

Проект использует реальные боевые логи PvP из World of Warcraft (The Burning Crusade).

## Задача:
Классификация:

**Класс 1:** команда персонажа победила в бою
**Класс 0:** команда персонажа проиграла

## Модель учитывает:

- Фракцию (Horde / Alliance)
- Класс (Warrior, Mage, Druid и др.)
- Роль (DPS / Heal)
- Участие в бонусном ивенте (BE = 1/0)
- Историческую среднюю эффективность класса в выбранной фракции

## Структура проекта:

wow-battleground-predictor/
- ├── data/                   # Данные боёв
- ├── model/                 # Обученная модель и статистика
- │   ├── battlegrounds_model.pkl
- │   ├── model_features.pkl
- │   ├── win_rate_by_faction_role.pkl
- │   ├── heal_ratio_stats.pkl
- │   ├── efficiency_map.pkl
- │   └── class_efficiency.pkl
- ├── templates/
- │   └── index.html          # Веб-интерфейс с рекомендациями
- └── wowbattleground.py                  # Flask API

## Запуск
```
git clone https://github.com/ArkadiyGold/wow-battleground-predictor.git
cd wow-battleground-predictor
pip install -r requirements.txt
python app.py
```

## Сайт:
http://127.0.0.1:5000

## Данные:
- Основной датасет: боевые логи полей боя (Battlegrounds)
- Файлы: wowbgs.csv, wowgil.csv, wowsm.csv, wowbgs2.csv и др.
- Источник: самостоятельно собранные/обработанные PvP-логи (аналог Kaggle Battlegrounds)
- Колонки: Faction, Class, Rol, KB, D, HK, DD, HD, Honor, Win, BE
## Модель:
- Алгоритм: RandomForestClassifier (сравнивался с XGBoost, выбрана лучшая)
- Точность: 0.6395904436860068
## Признаки:
- Faction (фракция)
- Class (класс)
- Rol (роль: DPS/Heal)
- BE (бонусный ивент)
- avg_efficiency (средняя эффективность по группе)
## Особенности:
- Динамические рекомендации на основе боёв:
«Шаманы Орды побеждают в 71% случаев»
«Идеальный отряд — 2 хилера + 5 DPS»

**Адаптивный интерфейс:** выбор роли зависит от класса (только хил-классы могут быть heal)

**Визуальное оформление:** тематический фон, анимация, игровые шрифты
