def generate_explanation(prediction, probability):
    """
    Generate a human-readable explanation for the prediction.

    Parameters
    ----------
    prediction : int
        0 = Not Potable
        1 = Potable

    probability : float
        Model confidence

    Returns
    -------
    explanation : str
    """

    confidence = probability * 100

    if prediction == 1:

        explanation = f"""
The AI model predicts that the water is POTABLE.

Confidence: {confidence:.2f}%

This indicates that the measured water quality parameters
are within the range commonly associated with safe drinking water.

Recommendation:
Although the prediction is positive, laboratory testing is
recommended before large-scale consumption.
"""

    else:

        explanation = f"""
The AI model predicts that the water is NOT POTABLE.

Confidence: {(100-confidence):.2f}%

The measured water quality parameters suggest that the water
may not be safe for drinking.

Recommendation:
Water treatment and laboratory verification are recommended
before human consumption.
"""

    return explanation


# -------------------------
# Testing
# -------------------------

if __name__ == "__main__":

    print(generate_explanation(0, 0.24))