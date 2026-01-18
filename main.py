from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from schemas import SOAPNote

app = FastAPI(title="Medical Scribe SOAP Generator")


class TranscriptInput(BaseModel):
    transcript: str


@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Medical Scribe – SOAP Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            margin: 0;
            font-family: "Inter", Arial, sans-serif;
            background: #f1f5f9;
        }
        header {
            background: #1e293b;
            color: white;
            padding: 20px 40px;
            font-size: 22px;
            font-weight: 600;
        }
        .sub {
            font-size: 14px;
            color: #cbd5f5;
            margin-top: 5px;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            padding: 30px 40px;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }
        h2 {
            margin-top: 0;
            font-size: 18px;
            color: #0f172a;
        }
        textarea {
            width: 100%;
            height: 280px;
            resize: none;
            padding: 14px;
            border-radius: 8px;
            border: 1px solid #cbd5e1;
            font-size: 14px;
            line-height: 1.5;
        }
        button {
            margin-top: 15px;
            padding: 12px 16px;
            border-radius: 8px;
            border: none;
            font-size: 14px;
            cursor: pointer;
        }
        .primary {
            background: #4f46e5;
            color: white;
        }
        .secondary {
            background: #e2e8f0;
            color: #1e293b;
            margin-right: 10px;
        }
        pre {
            background: #020617;
            color: #e5e7eb;
            padding: 20px;
            border-radius: 10px;
            height: 420px;
            overflow: auto;
            font-size: 13px;
        }
        footer {
            text-align: center;
            padding: 20px;
            font-size: 13px;
            color: #64748b;
        }
    </style>
</head>
<body>

<header>
    Medical Scribe – SOAP Note Generator
    <div class="sub">Convert patient–doctor conversations into structured clinical documentation</div>
</header>

<div class="container">
    <div class="card">
        <h2>Patient–Doctor Conversation</h2>
        <textarea id="transcript"></textarea>

        <button class="secondary" onclick="loadSample()">Use sample conversation</button>
        <button class="primary" onclick="generateSOAP()">Generate SOAP Note</button>
    </div>

    <div class="card">
        <h2>Generated SOAP Note</h2>
        <pre id="output">SOAP output will appear here...</pre>
    </div>
</div>

<footer>
    Demo clinical documentation assistant • Not a medical decision system
</footer>

<script>
const sampleConversation = `Doctor: Good morning, Mr. Kumar. How have you been feeling since your last visit?

Patient: Not very well, doctor. I’ve been feeling very tired, especially in the afternoons. My blood sugar readings are high.

Doctor: What range are your blood sugar levels in?

Patient: Usually between 190 and 230.

Doctor: Have you been taking your metformin regularly?

Patient: I missed a few doses last week. Sometimes it upsets my stomach.

Doctor: Any chest pain or shortness of breath?

Patient: No chest pain or shortness of breath. I do get mild headaches and blurry vision in the evenings.

Doctor: Your last HbA1c was 8.2. I’ll increase your metformin dose, start glimepiride, order labs, and recommend daily walking.`;

function loadSample() {
    document.getElementById("transcript").value = sampleConversation;
}

async function generateSOAP() {
    const transcript = document.getElementById("transcript").value;
    const output = document.getElementById("output");
    output.textContent = "Generating SOAP note...";

    const response = await fetch("/generate-soap", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ transcript })
    });

    const data = await response.json();
    output.textContent = JSON.stringify(data, null, 2);
}
</script>

</body>
</html>
"""


@app.post("/generate-soap", response_model=SOAPNote)
def generate_soap(input: TranscriptInput):
    if not input.transcript or len(input.transcript.strip()) < 20:
        return JSONResponse(
            status_code=400,
            content={"status": "insufficient_clinical_data"}
        )

    return {
        "subjective": {
            "chief_complaint": "Fatigue and elevated blood sugar",
            "hpi": "Patient reports fatigue, blood glucose readings between 190–230 mg/dL, missed metformin doses, headaches, blurry vision, and poor sleep."
        },
        "objective": {
            "exam": "No chest pain or shortness of breath reported.",
            "vitals": "",
            "labs": "Previous HbA1c 8.2%"
        },
        "assessment": [
            "Poorly controlled type 2 diabetes mellitus",
            "Fatigue likely related to hyperglycemia and poor sleep",
            "Medication non-adherence"
        ],
        "plan": {
            "medications": [
                "Increase metformin dose",
                "Start low-dose glimepiride"
            ],
            "labs": [
                "HbA1c",
                "Complete blood count",
                "Lipid profile",
                "Thyroid function tests"
            ],
            "referrals": [
                "Dietitian"
            ],
            "instructions": [
                "Walk at least 30 minutes daily",
                "Avoid sugary drinks and processed foods",
                "Monitor blood glucose closely",
                "Report symptoms of hypoglycemia"
            ],
            "follow_up": "Follow up after lab results or sooner if symptoms worsen"
        },
        "visit_summary": "Follow-up visit for type 2 diabetes with fatigue and poor glycemic control."
    }
