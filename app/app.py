from flask import Flask, render_template, request, jsonify
import os
import csv
from datetime import datetime
import sys

# ============================================================
# PROJECT ROOT
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ============================================================
# AI COMPONENTS
# ============================================================

from agent.agent import answer_water_question
from agent.predictor import predict_water_quality
from agent.risk_assessment import assess_risk
from agent.explanation import generate_explanation


# ============================================================
# FLASK
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

    return render_template("index.html")


# ============================================================
# PREDICT
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 500


        # ----------------------------------------------------
        # GET WATER PARAMETERS
        # ----------------------------------------------------

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
        # SAMPLE
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

        prediction, probability = \
            predict_water_quality(sample)


        # ----------------------------------------------------
        # RISK
        # ----------------------------------------------------

        risk, recommendation = \
            assess_risk(
                prediction,
                probability
            )


        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        explanation = \
            generate_explanation(
                prediction,
                probability
            )


        # ----------------------------------------------------
        # TEXT RESULT
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
            "History"
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
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "prediction": prediction_text,

            "confidence": f"{probability:.2%}",

            "probability": probability,

            "risk": risk,

            "recommendation": recommendation,

            "explanation": explanation,

            "model":
                "Deep Neural Network (DNN)"
        })


    except Exception as e:

        print("PREDICTION ERROR:")
        print(str(e))

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# ============================================================
# AI WATER ASSISTANT
# ============================================================

@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No question data received."
            }), 400


        # ----------------------------------------------------
        # GET QUESTION
        # ----------------------------------------------------

        question = data.get(
            "question",
            ""
        ).strip()


        # ----------------------------------------------------
        # GET CURRENT RESULT
        # ----------------------------------------------------

        prediction = data.get(
            "prediction"
        )

        confidence = data.get(
            "confidence"
        )

        risk = data.get(
            "risk"
        )

        recommendation = data.get(
            "recommendation"
        )

        explanation = data.get(
            "explanation"
        )


        # ----------------------------------------------------
        # ASK AI AGENT
        # ----------------------------------------------------

        answer = answer_water_question(

            question=question,

            prediction=prediction,

            confidence=confidence,

            risk=risk,

            recommendation=recommendation,

            explanation=explanation
        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "answer": answer

        })


    except Exception as e:

        print("AI AGENT ERROR:")
        print(str(e))

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("          WATER QUALITY AI")
    print("=" * 60)
    print("Model  : Deep Neural Network (DNN)")
    print("Server : http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )