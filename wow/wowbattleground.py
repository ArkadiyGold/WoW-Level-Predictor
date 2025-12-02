import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# Загрузка модели и данных
model = joblib.load(os.path.join(current_dir, 'model', 'battlegrounds_model.pkl'))
feature_columns = joblib.load(os.path.join(current_dir, 'model', 'model_features.pkl'))
win_rate = joblib.load(os.path.join(current_dir, 'model', 'win_rate_by_faction_role.pkl'))
class_efficiency = joblib.load(os.path.join(current_dir, 'model', 'class_efficiency.pkl'))

app = Flask(__name__)

@app.route('/')
def index():
    factions = ['Horde', 'Alliance']
    classes = ['Warrior', 'Hunter', 'Rogue', 'Shaman', 'Warlock', 'Paladin', 'Priest', 'Druid', 'Mage', 'Death Knight', 'Monk', 'Demon Hunter']
    return render_template('index.html', factions=factions, classes=classes)

def get_recommendations(faction, char_class, role):
    recs = []

    # 1. Шанс победы по фракции и роли
    key_fr = (faction, role)
    if key_fr in win_rate:
        win_prob = win_rate[key_fr]
        recs.append(f"Исторически, такие персонажи побеждают в {win_prob*100:.1f}% боёв.")

    # 2. Эффективность класса
    key_class = (faction, char_class)
    if key_class in class_efficiency:
        eff = class_efficiency[key_class]
        level = 'высокая' if eff > 60 else 'низкая'
        recs.append(f"Средняя эффективность {char_class} ({faction}): {eff:.2f} — {level}.")

    # 3. Совет по хилерам
    if role == 'dps':
        recs.append("💡 Совет: убедитесь, что в отряде есть хотя бы 1 хилер.")
    elif role == 'heal':
        recs.append("💡 Совет: вы — ключевой игрок! Идеальный отряд — 2-3 хилера.")

    return recs

def prepare_input(data):
    faction = data['Faction']
    char_class = data['Class']
    role = data['Rol']
    be = 1 if data['BE'] == 'Yes' else 0

    # Создаём среднюю эффективность
    key = (faction, char_class)
    avg_eff = class_efficiency.get(key, 0.0)

    be = 1 if data['BE'] == 'Yes' else 0

    input_dict = {
        'Faction': [faction],
        'Class': [char_class],
        'Rol': [role],
        'BE': [be],
        'avg_efficiency': [avg_eff]
    }
    df_input = pd.DataFrame(input_dict)
    input_encoded = pd.get_dummies(df_input, columns=['Faction', 'Class', 'Rol'], drop_first=True)

    # Приводим к нужному набору признаков
    for col in feature_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    return input_encoded[feature_columns]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        X = prepare_input(data)
        proba = model.predict_proba(X)[0]
        prediction = int(model.predict(X)[0])
        recommendations = get_recommendations(data['Faction'], data['Class'], data['Rol'])

        result = {
            'win': prediction,
            'probability': float(proba[1]),
            'message': '✅ Высокий шанс победы в следующем бою!' if prediction == 1
                       else '⚠️ Шанс победы низкий. Подумайте о тактике или составе группы.',
            'recommendations': recommendations
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)