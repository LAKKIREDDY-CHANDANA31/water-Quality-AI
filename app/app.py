from flask import Flask, render_template, request, jsonify
import os
import csv
from datetime import datetime
import sys

# ============================================================
# ADD PROJECT ROOT TO PYTHON PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# IMPORT AI COMPONENTS
# ============================================================

from agent.predictor import predict_water_quality
from agent.risk_assessment import assess_risk
from agent.explanation import generate_explanation


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        prediction=None,
        confidence=None,
        risk=None,
        recommendation=None,
        explanation=None,
        error=None
    )


# ============================================================
# WATER QUALITY PREDICTION API
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # ----------------------------------------------------
        # SUPPORT JSON FROM JAVASCRIPT
        # ----------------------------------------------------

        if request.is_json:

            data = request.get_json()

            ph = float(data["ph"])
            hardness = float(data["hardness"])
            solids = float(data["solids"])
            chloramines = float(data["chloramines"])
            sulfate = float(data["sulfate"])
            conductivity = float(data["conductivity"])
            organic_carbon = float(data["organic_carbon"])
            trihalomethanes = float(data["trihalomethanes"])
            turbidity = float(data["turbidity"])

        # ----------------------------------------------------
        # ALSO SUPPORT NORMAL HTML FORM
        # ----------------------------------------------------

        else:

            ph = float(request.form["ph"])
            hardness = float(request.form["hardness"])
            solids = float(request.form["solids"])
            chloramines = float(request.form["chloramines"])
            sulfate = float(request.form["sulfate"])
            conductivity = float(request.form["conductivity"])
            organic_carbon = float(request.form["organic_carbon"])
            trihalomethanes = float(request.form["trihalomethanes"])
            turbidity = float(request.form["turbidity"])


        # ----------------------------------------------------
        # CREATE SAMPLE
        # ----------------------------------------------------

        sample = [
            ph,
            hardness,
            solids,
            chloramines,
            sulfate,
            conductivity,
            organic_carbon,
            trihalomethanes,
            turbidity
        ]


        # ----------------------------------------------------
        # DNN PREDICTION
        # ----------------------------------------------------

        prediction, probability = predict_water_quality(sample)


        # ----------------------------------------------------
        # RISK ASSESSMENT
        # ----------------------------------------------------

        risk, recommendation = assess_risk(
            prediction,
            probability
        )


        # ----------------------------------------------------
        # AI EXPLANATION
        # ----------------------------------------------------

        explanation = generate_explanation(
            prediction,
            probability
        )


        # ----------------------------------------------------
        # PREDICTION TEXT
        # ----------------------------------------------------

        prediction_text = (
            "POTABLE"
            if prediction == 1
            else "NOT POTABLE"
        )


        # ----------------------------------------------------
        # SAVE HISTORY
        # ----------------------------------------------------

        history_directory = os.path.join(
            BASE_DIR,
            "history"
        )

        os.makedirs(
            history_directory,
            exist_ok=True
        )

        history_file = os.path.join(
            history_directory,
            "prediction_history.csv"
        )


        with open(
            history_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                ph,
                hardness,
                solids,
                chloramines,
                sulfate,
                conductivity,
                organic_carbon,
                trihalomethanes,
                turbidity,
                prediction_text,
                f"{probability:.2%}"
            ])


        # ----------------------------------------------------
        # RETURN JSON FOR JAVASCRIPT
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "prediction": prediction_text,

            "confidence": f"{probability:.2%}",

            "probability": probability,

            "risk": risk,

            "recommendation": recommendation,

            "explanation": explanation,

            "model": "Deep Neural Network (DNN)"

        })


    except Exception as e:

        print("\nPREDICTION ERROR:")
        print(str(e))

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# ============================================================
# RUN FLASK
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("WATER QUALITY AI")
    print("=" * 60)
    print("Model : Deep Neural Network (DNN)")
    print("Server: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )