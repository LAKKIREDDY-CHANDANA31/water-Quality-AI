def answer_water_question(
    question,
    prediction=None,
    confidence=None,
    risk=None,
    recommendation=None,
    explanation=None
):
    """
    AI Water Assistant.

    Answers questions about the current water-quality
    prediction and general water-quality information.
    """

    if not question or not question.strip():
        return "Please enter a question."

    question = question.lower().strip()

    # =========================================================
    # HELP
    # =========================================================

    if (
        "help" in question
        or "what can i ask" in question
        or "what can you do" in question
    ):
        return (
            "I am your AI Water Assistant. You can ask me questions such as:\n\n"
            "• Is the water safe to drink?\n"
            "• Why is the water potable?\n"
            "• Why is the water not potable?\n"
            "• What is the confidence?\n"
            "• What is the risk level?\n"
            "• What should I do?\n"
            "• Explain the prediction.\n"
            "• What model is being used?\n"
            "• What parameters are analyzed?\n"
            "• What does pH mean?\n"
            "• What does turbidity mean?"
        )

    # =========================================================
    # GENERAL PARAMETER QUESTIONS
    # These work even before prediction.
    # =========================================================

    if "ph" in question:
        return (
            "pH measures how acidic or alkaline the water is. "
            "The pH scale normally ranges from 0 to 14, with 7 being neutral. "
            "The DNN model uses pH as one of the nine input parameters."
        )

    if "hardness" in question:
        return (
            "Water hardness mainly relates to dissolved minerals such as "
            "calcium and magnesium. Hardness is one of the nine parameters "
            "used by the DNN model."
        )

    if "solids" in question or "tds" in question:
        return (
            "Solids represent dissolved substances present in the water. "
            "A high concentration can affect water quality and taste. "
            "Solids are one of the parameters analyzed by the model."
        )

    if "chloramine" in question:
        return (
            "Chloramines are disinfectant compounds used in some water "
            "treatment systems. Their concentration is included as one "
            "of the model's water-quality parameters."
        )

    if "sulfate" in question:
        return (
            "Sulfate is a naturally occurring ion that can be present in "
            "water. Its concentration is included in the water-quality "
            "analysis."
        )

    if "conductivity" in question:
        return (
            "Electrical conductivity indicates how well water conducts "
            "electricity, which is related to dissolved ions in the water. "
            "It is one of the nine parameters used by the model."
        )

    if "organic carbon" in question:
        return (
            "Organic carbon represents carbon from organic compounds "
            "present in the water. It is one of the parameters analyzed "
            "by the DNN model."
        )

    if "trihalomethane" in question or "thm" in question:
        return (
            "Trihalomethanes are chemical compounds that can form during "
            "water disinfection. Their concentration is included in the "
            "model's water-quality analysis."
        )

    if "turbidity" in question:
        return (
            "Turbidity describes how cloudy or hazy water is because of "
            "suspended particles. It is one of the nine parameters used "
            "by the DNN model."
        )

    if (
        "parameter" in question
        or "parameters" in question
        or "features" in question
    ):
        return (
            "The DNN model analyzes nine water-quality parameters:\n\n"
            "1. pH\n"
            "2. Hardness\n"
            "3. Solids\n"
            "4. Chloramines\n"
            "5. Sulfate\n"
            "6. Conductivity\n"
            "7. Organic Carbon\n"
            "8. Trihalomethanes\n"
            "9. Turbidity"
        )

    # =========================================================
    # NO PREDICTION YET
    # =========================================================

    if prediction is None:
        return (
            "Please analyze a water sample first. "
            "After the prediction is available, I can answer questions "
            "about its potability, confidence, risk, recommendation, "
            "and explanation."
        )

    # =========================================================
    # POTABILITY
    # =========================================================

    if (
        "potable" in question
        or "drink" in question
        or "safe" in question
    ):

        if prediction == "POTABLE":
            return (
                f"The DNN model predicts that the water is POTABLE. "
                f"The reported confidence is {confidence}. "
                f"However, model predictions should not replace "
                f"laboratory testing before drinking."
            )

        return (
            f"The DNN model predicts that the water is NOT POTABLE. "
            f"The reported confidence is {confidence}. "
            f"The assessed risk is {risk}. "
            f"Treatment and laboratory verification are recommended "
            f"before consumption."
        )

    # =========================================================
    # CONFIDENCE
    # =========================================================

    if (
        "confidence" in question
        or "certain" in question
        or "sure" in question
    ):
        return (
            f"The model's reported confidence is {confidence}. "
            "This represents how strongly the model supports its "
            "prediction. It should not be interpreted as laboratory certainty."
        )

    # =========================================================
    # RISK
    # =========================================================

    if (
        "risk" in question
        or "danger" in question
        or "dangerous" in question
    ):
        return (
            f"The current assessed risk level is {risk}. "
            "The risk assessment is based on the DNN prediction "
            "and its probability."
        )

    # =========================================================
    # RECOMMENDATION
    # =========================================================

    if (
        "recommend" in question
        or "recommendation" in question
        or "what should" in question
        or "what do i do" in question
        or "next step" in question
    ):
        return f"Recommendation:\n{recommendation}"

    # =========================================================
    # EXPLANATION
    # =========================================================

    if (
        "why" in question
        or "explain" in question
        or "explanation" in question
        or "reason" in question
    ):
        return f"Here is the model explanation:\n\n{explanation}"

    # =========================================================
    # MODEL
    # =========================================================

    if (
        "model" in question
        or "dnn" in question
        or "deep neural" in question
    ):
        return (
            "This project uses a Deep Neural Network (DNN) model "
            "for water-potability prediction. The model receives "
            "nine water-quality parameters and produces a prediction "
            "and probability."
        )

    # =========================================================
    # GENERAL RESULT
    # =========================================================

    if (
        "result" in question
        or "sample" in question
        or "water quality" in question
    ):
        return (
            f"Current prediction: {prediction}\n"
            f"Confidence: {confidence}\n"
            f"Risk level: {risk}\n\n"
            f"Recommendation: {recommendation}"
        )

    # =========================================================
    # DEFAULT
    # =========================================================

    return (
        "I can help you understand your water-quality analysis. "
        "Try asking:\n\n"
        "• Is the water safe to drink?\n"
        "• Why is the water not potable?\n"
        "• What is the confidence?\n"
        "• What is the risk level?\n"
        "• What should I do?\n"
        "• Explain the prediction.\n"
        "• What model is being used?\n"
        "• What does pH mean?\n"
        "• What does turbidity mean?"
    )