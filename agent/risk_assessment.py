def assess_risk(prediction, probability):
    """
    Assess environmental risk based on prediction and confidence.

    Parameters
    ----------
    prediction : int
        0 = Not Potable
        1 = Potable

    probability : float
        Model confidence

    Returns
    -------
    risk_level : str
    recommendation : str
    """

    if prediction == 1:

        if probability >= 0.80:
            risk = "LOW RISK"

            recommendation = (
                "Water is likely safe for drinking based on the model prediction."
            )

        else:

            risk = "MODERATE RISK"

            recommendation = (
                "Water appears potable, but laboratory verification is recommended."
            )

    else:

        if probability <= 0.30:

            risk = "HIGH RISK"

            recommendation = (
                "Water is predicted to be unsafe for drinking. Treatment is recommended before use."
            )

        else:

            risk = "MODERATE RISK"

            recommendation = (
                "Water quality is uncertain. Further laboratory testing is recommended."
            )

    return risk, recommendation


# ------------------------------
# Testing
# ------------------------------

if __name__ == "__main__":

    risk, recommendation = assess_risk(0, 0.24)

    print("\n========== Risk Assessment ==========\n")

    print("Risk Level :", risk)
    print("Recommendation :", recommendation)