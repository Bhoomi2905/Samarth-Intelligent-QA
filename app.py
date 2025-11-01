from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

rainfall = pd.read_csv("RainFall.csv")
crops = pd.read_csv("crops.csv")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form['question'].lower()
    answer = "Sorry, I couldn’t understand. Try asking about rainfall or crop production."

    if "rainfall" in question:
        if "andaman" in question:
            avg_rain = rainfall[rainfall['SUBDIVISION'].str.contains("Andaman", case=False)]
            avg = avg_rain['ANNUAL'].mean()
            answer = f"Average annual rainfall in Andaman & Nicobar Islands is {avg:.2f} mm (based on given data)."
        else:
            answer = "Rainfall data for that state is not available."

    elif "crop" in question or "production" in question:
        if "andaman" in question:
            crop_data = crops[crops['State Name'].str.contains("Andaman", case=False)]
            top_crop = crop_data.groupby('Crop')['Production'].sum().sort_values(ascending=False).head(1)
            crop_name = top_crop.index[0]
            crop_value = top_crop.iloc[0]
            answer = f"Highest produced crop in Andaman & Nicobar Islands is {crop_name} with total production of {crop_value} units."
        else:
            answer = "Crop data for that state is not available."

    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(debug=True)
