/* ============================================================
   WATER QUALITY DASHBOARD
============================================================ */


/* ============================================================
   ELEMENTS
============================================================ */

const predictionForm =
    document.getElementById("predictionForm");

const predictButton =
    document.getElementById("predictButton");

const resultEmpty =
    document.getElementById("resultEmpty");

const resultContent =
    document.getElementById("resultContent");

const predictionStatus =
    document.getElementById("predictionStatus");

const predictionIcon =
    document.getElementById("predictionIcon");

const predictionLabel =
    document.getElementById("predictionLabel");

const confidence =
    document.getElementById("confidence");

const riskLevel =
    document.getElementById("riskLevel");

const assessment =
    document.getElementById("assessment");

const recommendation =
    document.getElementById("recommendation");

const explanation =
    document.getElementById("explanation");


/* ============================================================
   PREDICTION
============================================================ */

predictionForm.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        /* -----------------------------------------------
           BUTTON LOADING STATE
        ------------------------------------------------ */

        predictButton.classList.add("loading");

        predictButton.innerHTML =
            "<span>Analyzing...</span><span>⏳</span>";


        /* -----------------------------------------------
           COLLECT VALUES
        ------------------------------------------------ */

        const formData =
            new FormData(predictionForm);


        const data = {

            ph:
                parseFloat(formData.get("ph")),

            Hardness:
                parseFloat(formData.get("Hardness")),

            Solids:
                parseFloat(formData.get("Solids")),

            Chloramines:
                parseFloat(formData.get("Chloramines")),

            Sulfate:
                parseFloat(formData.get("Sulfate")),

            Conductivity:
                parseFloat(formData.get("Conductivity")),

            Organic_carbon:
                parseFloat(
                    formData.get("Organic_carbon")
                ),

            Trihalomethanes:
                parseFloat(
                    formData.get("Trihalomethanes")
                ),

            Turbidity:
                parseFloat(
                    formData.get("Turbidity")
                )

        };


        /* -----------------------------------------------
           SEND TO FLASK
        ------------------------------------------------ */

        try {

            const response =
                await fetch("/predict", {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(data)

                });


            if (!response.ok) {

                throw new Error(
                    "Prediction request failed."
                );

            }


            const result =
                await response.json();


            /* -------------------------------------------
               SHOW RESULT
            -------------------------------------------- */

            displayPrediction(result);


        } catch (error) {

            console.error(error);

            alert(
                "Unable to connect to the prediction service."
            );

        } finally {

            predictButton.classList.remove(
                "loading"
            );

            predictButton.innerHTML =
                "<span>Analyze Water Quality</span><span>→</span>";
        }

    }
);


/* ============================================================
   DISPLAY PREDICTION
============================================================ */

function displayPrediction(result) {


    /* -----------------------------------------------
       RESULT VALUE
    ------------------------------------------------ */

    const prediction =
        String(
            result.prediction ??
            result.result ??
            result.label ??
            ""
        ).toLowerCase();


    const isPotable =
        prediction.includes("potable") &&
        !prediction.includes("not");


    /* -----------------------------------------------
       SHOW RESULT CARD
    ------------------------------------------------ */

    resultEmpty.style.display =
        "none";

    resultContent.style.display =
        "block";


    /* -----------------------------------------------
       POTABILITY
    ------------------------------------------------ */

    if (isPotable) {

        predictionStatus.classList.remove(
            "not-potable"
        );

        predictionIcon.textContent =
            "✓";

        predictionLabel.textContent =
            "POTABLE";

    } else {

        predictionStatus.classList.add(
            "not-potable"
        );

        predictionIcon.textContent =
            "⚠";

        predictionLabel.textContent =
            "NOT POTABLE";
    }


    /* -----------------------------------------------
       CONFIDENCE
    ------------------------------------------------ */

    const confidenceValue =
        result.confidence ??
        result.probability ??
        result.confidence_score ??
        null;


    if (confidenceValue !== null) {

        let value =
            parseFloat(confidenceValue);


        /*
         * If backend sends 0.5943,
         * convert to 59.43.
         */

        if (value <= 1) {
            value = value * 100;
        }


        confidence.textContent =
            value.toFixed(2) + "%";

    } else {

        confidence.textContent =
            "Available from model";

    }


    /* -----------------------------------------------
       RISK
    ------------------------------------------------ */

    riskLevel.textContent =
        result.risk_level ??
        result.risk ??
        calculateRisk(
            confidenceValue,
            isPotable
        );


    /* -----------------------------------------------
       AI ASSESSMENT
    ------------------------------------------------ */

    assessment.textContent =
        result.assessment ??
        createAssessment(isPotable);


    /* -----------------------------------------------
       RECOMMENDATION
    ------------------------------------------------ */

    recommendation.textContent =
        result.recommendation ??
        createRecommendation(isPotable);


    /* -----------------------------------------------
       EXPLANATION
    ------------------------------------------------ */

    explanation.textContent =
        result.explanation ??
        createExplanation(
            isPotable,
            confidenceValue
        );
}


/* ============================================================
   DEFAULT RISK
============================================================ */

function calculateRisk(
    confidenceValue,
    isPotable
) {

    if (confidenceValue === null) {

        return isPotable
            ? "MODERATE RISK"
            : "HIGH RISK";
    }


    let value =
        parseFloat(confidenceValue);


    if (value <= 1) {
        value *= 100;
    }


    if (!isPotable) {

        if (value >= 80) {
            return "HIGH RISK";
        }

        return "MODERATE RISK";
    }


    if (value >= 80) {
        return "LOW RISK";
    }

    if (value >= 60) {
        return "MODERATE RISK";
    }

    return "MODERATE RISK";
}


/* ============================================================
   DEFAULT ASSESSMENT
============================================================ */

function createAssessment(isPotable) {

    if (isPotable) {

        return (
            "The DNN model predicts that the " +
            "provided water sample is POTABLE."
        );

    }

    return (
        "The DNN model predicts that the " +
        "provided water sample is NOT POTABLE."
    );
}


/* ============================================================
   DEFAULT RECOMMENDATION
============================================================ */

function createRecommendation(isPotable) {

    if (isPotable) {

        return (
            "Water appears potable based on the " +
            "provided parameters, but laboratory " +
            "verification is recommended before " +
            "large-scale consumption."
        );

    }

    return (
        "The water sample should not be considered " +
        "safe for direct consumption. Further " +
        "testing and appropriate treatment are recommended."
    );
}


/* ============================================================
   DEFAULT EXPLANATION
============================================================ */

function createExplanation(
    isPotable,
    confidenceValue
) {

    let confidenceText =
        "the available prediction confidence";


    if (confidenceValue !== null) {

        let value =
            parseFloat(confidenceValue);

        if (value <= 1) {
            value *= 100;
        }

        confidenceText =
            value.toFixed(2) + "% confidence";
    }


    if (isPotable) {

        return (
            "The Deep Neural Network analyzed the " +
            "nine measured water-quality parameters " +
            "and classified the sample as POTABLE " +
            "with " +
            confidenceText +
            ". Laboratory verification is still " +
            "recommended for real-world use."
        );

    }


    return (
        "The Deep Neural Network analyzed the " +
        "nine measured water-quality parameters " +
        "and classified the sample as NOT POTABLE " +
        "with " +
        confidenceText +
        ". Further investigation and treatment " +
        "are recommended."
    );
}


/* ============================================================
   AI WATER ASSISTANT
============================================================ */

const assistantInput =
    document.getElementById(
        "assistantInput"
    );

const assistantSend =
    document.getElementById(
        "assistantSend"
    );

const chatArea =
    document.getElementById(
        "chatArea"
    );


/* ============================================================
   SEND AI QUESTION
============================================================ */

async function askWaterAssistant() {

    const question =
        assistantInput.value.trim();


    if (!question) {
        return;
    }


    /* -----------------------------------------------
       USER MESSAGE
    ------------------------------------------------ */

    addUserMessage(question);

    assistantInput.value = "";


    /* -----------------------------------------------
       THINKING
    ------------------------------------------------ */

    const thinking =
        document.createElement("div");

    thinking.className =
        "ai-message";

    thinking.innerHTML = `

        <div class="chat-avatar">
            🤖
        </div>

        <div class="chat-bubble">

            <strong>
                AI Water Assistant
            </strong>

            <p>
                Thinking...
            </p>

        </div>

    `;

    chatArea.appendChild(thinking);

    scrollChat();


    /* -----------------------------------------------
       SEND TO FLASK AGENT
    ------------------------------------------------ */

    try {

        const response =
            await fetch("/agent", {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    question: question

                })

            });


        if (!response.ok) {

            throw new Error(
                "AI Agent request failed."
            );

        }


        const data =
            await response.json();


        thinking.remove();


        /* -------------------------------------------
           RESPONSE
        -------------------------------------------- */

        const answer =
            data.response ??
            data.answer ??
            data.message ??
            "I could not generate a response.";


        addAIMessage(answer);


    } catch (error) {

        console.error(error);

        thinking.remove();

        addAIMessage(
            "I am unable to connect to the AI Agent right now. Please try again."
        );

    }

}


/* ============================================================
   ADD USER MESSAGE
============================================================ */

function addUserMessage(message) {

    const element =
        document.createElement("div");

    element.className =
        "user-message";

    element.textContent =
        message;

    chatArea.appendChild(element);

    scrollChat();
}


/* ============================================================
   ADD AI MESSAGE
============================================================ */

function addAIMessage(message) {

    const element =
        document.createElement("div");

    element.className =
        "ai-message";

    element.innerHTML = `

        <div class="chat-avatar">
            🤖
        </div>

        <div class="chat-bubble">

            <strong>
                AI Water Assistant
            </strong>

            <p>
                ${escapeHTML(message)}
            </p>

        </div>

    `;

    chatArea.appendChild(element);

    scrollChat();
}


/* ============================================================
   ESCAPE HTML
============================================================ */

function escapeHTML(text) {

    const div =
        document.createElement("div");

    div.textContent =
        text;

    return div.innerHTML;
}


/* ============================================================
   SCROLL CHAT
============================================================ */

function scrollChat() {

    chatArea.scrollTop =
        chatArea.scrollHeight;
}


/* ============================================================
   BUTTON
============================================================ */

assistantSend.addEventListener(
    "click",
    askWaterAssistant
);


/* ============================================================
   ENTER KEY
============================================================ */

assistantInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            event.preventDefault();

            askWaterAssistant();
        }

    }
);