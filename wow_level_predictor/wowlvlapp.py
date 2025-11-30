import pandas as pd
from flask import Flask, request, jsonify, render_template
import joblib
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
zones_file_path = os.path.join(current_dir, 'data', 'zones.csv')

zones_df = pd.read_csv(zones_file_path)
model = joblib.load(os.path.join(current_dir, 'models', 'wow_max_level_model.pkl'))
feature_columns = joblib.load(os.path.join(current_dir, 'models', 'model_features.pkl'))

app = Flask(__name__)

@app.route('/')
def index():
    races = ['Orc', 'Tauren', 'Troll', 'Undead', 'Blood Elf']
    classes = ['Warrior', 'Hunter', 'Rogue', 'Shaman', 'Warlock', 'Paladin', 'Priest', 'Druid', 'Mage']
    zones = sorted(zones_df['Zone_Name'].dropna().unique())
    
    return render_template('index.html', races=races, classes=classes, zones=zones)

def prepare_input(data):
    df_input = pd.DataFrame([data])

    df_input['has_guild'] = (df_input['guild'] != -1).astype(int)
    df_input = df_input.drop(columns=['guild'])

    df_input = df_input.merge(
        zones_df[['Zone_Name', 'Type', 'Controlled', 'Min_rec_level']],
        left_on='zone',
        right_on='Zone_Name',
        how='left'
    ).drop(columns=['Zone_Name'])

    df_input['Type'] = df_input['Type'].fillna('Unknown')
    df_input['Controlled'] = df_input['Controlled'].fillna('Unknown')
    df_input['Min_rec_level'] = df_input['Min_rec_level'].fillna(0)

    input_features = df_input[['race', 'charclass', 'Type', 'Controlled', 'Min_rec_level', 'has_guild']]

    input_encoded = pd.get_dummies(input_features, columns=['race', 'charclass', 'Type', 'Controlled'], drop_first=True)

    for col in feature_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    input_encoded = input_encoded[feature_columns]

    return input_encoded

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)

        X = prepare_input(data)

        proba = model.predict_proba(X)[0]
        prediction = int(model.predict(X)[0])

        result = {
            'is_max_level': prediction,
            'probability': float(proba[1]),
            'message': 'Этот персонаж, скорее всего, достиг максимального уровня.' if prediction == 1
                       else 'Этот персонаж, вероятно, ещё не достиг максимального уровня.'
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)