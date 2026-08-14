from agent.predictor import predict_water_quality
from agent.risk_assessment import assess_risk
from agent.explanation import generate_explanation


def answer_water_question(question, prediction=None, confidence=None,
                          risk=None, recommendation=None, explanation=None):
    """
    AI Water Agent.

    Answers questions using the current water-quality prediction,
    confidence, risk, recommendation and explanation.
    """

    if not question:
        return "Please enter a question about the water-quality result."

    question = question.lower().strip()

    # ---------------------------------------------------------
    # No prediction available yet
    # ---------------------------------------------------------

    if prediction is None:

        if "what can you ask" in question or "help" in question:
            return (
                "You can ask me questions about water potability, "
                "confidence, risk level, recommendations, the DNN model, "
                "or water-quality parameters."
            )

        return (
            "Please analyze a water sample first. "
            "After the prediction is available, you can ask me questions "
            "about the result."
        )

    # ---------------------------------------------------------
    # POTABILITY QUESTIONS
    # ---------------------------------------------------------

    if (
        "potable" in question
        or "drink" in question
        or "safe" in question
        or "safe to drink" in question
    ):

        if prediction == "POTABLE":
            return (
                f"The DNN model predicts that the water is POTABLE. "
                f"The reported confidence is {confidence}. "
                f"However, laboratory verification is recommended "
                f"before drinking or large-scale consumption."
            )

        return (
            f"The DNN model predicts that the water is NOT POTABLE. "
            f"The reported confidence is {confidence}. "
            f"The assessed risk is {risk}. "
            f"Treatment and laboratory verification are recommended "
            f"before consumption."
        )

    # ---------------------------------------------------------
    # CONFIDENCE QUESTIONS
    # ---------------------------------------------------------

    if (
        "confidence" in question
        or "certain" in question
        or "accuracy" in question
        or "sure" in question
    ):

        return (
            f"The model's reported confidence for this prediction is "
            f"{confidence}. "
            f"Confidence indicates how strongly the model supports "
            f"its prediction; it is not the same as laboratory certainty."
        )

    # ---------------------------------------------------------
    # RISK QUESTIONS
    # ---------------------------------------------------------

    if (
        "risk" in question
        or "danger" in question
        or "dangerous" in question
    ):

        return (
            f"The current assessed risk level is {risk}. "
            f"This risk assessment is based on the model prediction "
            f"and its probability."
        )

    # ---------------------------------------------------------
    # RECOMMENDATION QUESTIONS
    # ---------------------------------------------------------

    if (
        "recommend" in question
        or "recommendation" in question
        or "what should" in question
        or "what do i do" in question
        or "next step" in question
    ):

        return (
            f"Recommendation: {recommendation}"
        )

    # ---------------------------------------------------------
    # EXPLANATION QUESTIONS
    # ---------------------------------------------------------

    if (
        "why" in question
        or "explain" in question
        or "explanation" in question
        or "reason" in question
    ):

        return (
            f"Here is the model explanation:\n\n"
            f"{explanation}"
        )

    # ---------------------------------------------------------
    # MODEL QUESTIONS
    # ---------------------------------------------------------

    if (
        "model" in question
        or "dnn" in question
        or "deep neural" in question
        or "ai" in question
    ):

        return (
            "The water-quality prediction is generated using the "
            "Deep Neural Network (DNN) model. The DNN analyzes the "
            "nine water-quality parameters and produces a potability "
            "prediction and probability."
        )

    # ---------------------------------------------------------
    # PARAMETERS QUESTIONS
    # ---------------------------------------------------------

    if (
        "parameter" in question
        or "parameters" in question
        or "water quality" in question
    ):

        return (
            "This project analyzes nine water-quality parameters: "
            "pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, "
            "Organic Carbon, Trihalomethanes, and Turbidity."
        )

    # ---------------------------------------------------------
    # GENERAL WATER QUESTION
    # ---------------------------------------------------------

    if (
        "water" in question
        or "sample" in question
        or "result" in question
    ):

        return (
            f"Current prediction: {prediction}\n"
            f"Confidence: {confidence}\n"
            f"Risk level: {risk}\n\n"
            f"Recommendation: {recommendation}"
        )

    # ---------------------------------------------------------
    # DEFAULT RESPONSE
    # ---------------------------------------------------------

    return (
        "I can help you understand this water-quality prediction. "
        "Try asking questions such as:\n\n"
        "• Is the water safe to drink?\n"
        "• Why is the water potable?\n"
        "• Why is the water not potable?\n"
        "• What is the confidence?\n"
        "• What is the risk level?\n"
        "• What do you recommend?\n"
        "• What model is being used?\n"
        "• What parameters are analyzed?"
    )


# -------------------------------------------------------------
# ORIGINAL TERMINAL AGENT
# -------------------------------------------------------------

def main():

    print("=" * 60)
    print("        WATER QUALITY AI AGENT")
    print("=" * 60)

    print("\nEnter the following water quality parameters:\n")

    ph = float(input("pH: "))
    hardness = float(input("Hardness: "))
    solids = float(input("Solids: "))
    chloramines = float(input("Chloramines: "))
    sulfate = float(input("Sulfate: "))
    conductivity = float(input("Conductivity: "))
    organic_carbon = float(input("Organic Carbon: "))
    trihalomethanes = float(input("Trihalomethanes: "))
    turbidity = float(input("Turbidity: "))

    sample = [
        ph,
        hardness,
        solids,
        chloramines,
        sulfate,
        conductivity,
        organic_carbon,
        trihalomethanes,
        turbidity,
    ]

    prediction, probability = predict_water_quality(sample)

    risk, recommendation = assess_risk(
        prediction,
        probability
    )

    explanation = generate_explanation(
        prediction,
        probability
    )

    print("\n" + "=" * 60)
    print("                AI AGENT RESULT")
    print("=" * 60)

    if prediction == 1:
        prediction_text = "POTABLE"
        print("\nPrediction        : POTABLE")
    else:
        prediction_text = "NOT POTABLE"
        print("\nPrediction        : NOT POTABLE")

    print(f"Confidence        : {probability:.2%}")
    print(f"Risk Level        : {risk}")
    print(f"\nRecommendation    :\n{recommendation}")

    print("\nExplanation")
    print("-" * 60)
    print(explanation)

    print("=" * 60)


if __name__ == "__main__":
    main()