from flask import Flask, render_template, request
import pickle
import numpy as np
import datetime

app = Flask(__name__)

with open('predictor.pickle', 'rb') as model_file:
    model = pickle.load(model_file)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve form data
        is_holiday = int(request.form['is_holiday'])
        temperature = float(request.form['temperature'])
        date = request.form['date']
        hour = int(request.form['hour'])
        weather_type = int(request.form['weather_type'])
        weather_description = int(request.form['weather_description'])

        # Convert date input to necessary components
        date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
        weekday = date_obj.weekday()
        month_day = date_obj.day
        year = date_obj.year
        month = date_obj.month

        # Prepare input data
        input_data = np.array([[is_holiday, temperature, weekday, hour, month_day, year, month, weather_type, weather_description]])


        # Predict traffic volume
        prediction = model.predict(input_data)
        traffic_volume  = round(prediction[0], 2)


        # Classify traffic volume and set CSS class
        if traffic_volume <= 1000:
            traffic_status = "No Traffic"
            traffic_class = "no-traffic"
        elif traffic_volume > 1000 and traffic_volume <= 3000:
            traffic_status = "Busy or Normal Traffic"
            traffic_class = "busy-traffic"
        elif traffic_volume > 3000 and traffic_volume <= 5500:
            traffic_status = "Heavy Traffic"
            traffic_class = "heavy-traffic"
        else:
            traffic_status = "Worst Case"
            traffic_class = "worst-traffic"

        return render_template('index.html', prediction_text=f'Traffic Volume: {traffic_volume}', traffic_status=traffic_status, traffic_class=traffic_class)
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)