/* ============================================================
   AI WATER ASSISTANT
============================================================ */

const assistantInput =
    document.getElementById("assistantInput");

const assistantSend =
    document.getElementById("assistantSend");

const chatArea =
    document.getElementById("chatArea");


/* ============================================================
   STORE CURRENT PREDICTION
============================================================ */

let latestPrediction = null;


/* ============================================================
   SAVE PREDICTION RESULT
============================================================ */

function displayPrediction(result) {

    /* Save result for AI Assistant */
    latestPrediction = result;


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

    resultEmpty.style.display = "none";
    resultContent.style.display = "block";


    /* -----------------------------------------------
       POTABILITY
    ------------------------------------------------ */

    if (isPotable) {

        predictionStatus.classList.remove(
            "not-potable"
        );

        predictionIcon.textContent = "✓";

        predictionLabel.textContent = "POTABLE";

    } else {

        predictionStatus.classList.add(
            "not-potable"
        );

        predictionIcon.textContent = "⚠";

        predictionLabel.textContent = "NOT POTABLE";
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

        let value = parseFloat(confidenceValue);

        if (value <= 1) {
            value *= 100;
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
        result.risk ??
        result.risk_level ??
        calculateRisk(
            confidenceValue,
            isPotable
        );


    /* -----------------------------------------------
       ASSESSMENT
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
   ASK AI WATER ASSISTANT
============================================================ */

async function askWaterAssistant() {

    const question =
        assistantInput.value.trim();


    if (!question) {
        return;
    }


    /* -----------------------------------------------
       ADD USER MESSAGE
    ------------------------------------------------ */

    addUserMessage(question);

    assistantInput.value = "";


    /* -----------------------------------------------
       THINKING MESSAGE
    ------------------------------------------------ */

    const thinking =
        document.createElement("div");

    thinking.className = "ai-message";

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
       CHECK WHETHER PREDICTION EXISTS
    ------------------------------------------------ */

    if (!latestPrediction) {

        thinking.remove();

        addAIMessage(
            "Please analyze a water sample first. Then I can answer questions about the prediction, confidence, risk, recommendation, and explanation."
        );

        return;
    }


    /* -----------------------------------------------
       SEND QUESTION TO FLASK /ask
    ------------------------------------------------ */

    try {

        const response =
            await fetch("/ask", {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    question: question,

                    prediction:
                        latestPrediction.prediction,

                    confidence:
                        latestPrediction.confidence ??
                        latestPrediction.probability,

                    risk:
                        latestPrediction.risk ??
                        latestPrediction.risk_level,

                    recommendation:
                        latestPrediction.recommendation,

                    explanation:
                        latestPrediction.explanation

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


        /* -----------------------------------------------
           SHOW AI RESPONSE
        ------------------------------------------------ */

        if (data.success === false) {

            addAIMessage(
                data.error ??
                "The AI Assistant could not answer your question."
            );

            return;
        }


        const answer =
            data.answer ??
            data.response ??
            data.message ??
            "I could not generate a response.";


        addAIMessage(answer);


    } catch (error) {

        console.error(
            "AI Assistant Error:",
            error
        );

        thinking.remove();

        addAIMessage(
            "I am unable to connect to the AI Assistant right now."
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
   SEND BUTTON
============================================================ */

if (assistantSend) {

    assistantSend.addEventListener(
        "click",
        askWaterAssistant
    );
}


/* ============================================================
   ENTER KEY
============================================================ */

if (assistantInput) {

    assistantInput.addEventListener(
        "keydown",
        function(event) {

            if (event.key === "Enter") {

                event.preventDefault();

                askWaterAssistant();
            }

        }
    );
}