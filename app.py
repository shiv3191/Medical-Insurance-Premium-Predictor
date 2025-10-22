from flask import Flask, request, render_template
import pickle as pkl
import pandas as pd

# Load trained model
model = pkl.load(open('MIPML.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # HTML form for user input

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
    age = int(request.form['age'])
    sex = int(request.form['sex'])
    bmi = float(request.form['bmi'])
    children = int(request.form['children'])
    smoker = int(request.form['smoker'])
    region = int(request.form['region'])

    # Prepare input for prediction
    input_data = pd.DataFrame([[age, sex, bmi, children, smoker, region]],
                              columns=['age','sex','bmi','children','smoker','region'])
    
    # Predict premium
    prediction = model.predict(input_data)[0]
    prediction_text = f"${round(prediction, 2)}"
    
    # Render result page with prediction and user inputs
    return render_template('result.html', 
                         prediction_text=prediction_text,
                         age=age,
                         sex=str(sex),
                         bmi=bmi,
                         children=children,
                         smoker=str(smoker),
                         region=str(region))

if __name__ == "__main__":
    app.run(debug=True)