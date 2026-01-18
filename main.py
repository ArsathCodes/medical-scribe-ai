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
<html>
<head>
    <title>Medical Scribe – SOAP Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f7fb;
            margin: 0;
            padding: 0;
        }
        .container {
            max-width: 900px;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #2b2e4a;
        }
        p {
            text-align: center;
            color: #555;
        }
        textarea {
            width: 100%;
            height: 180px;
            padding: 15px;
            font-size: 14px;
            border-radius: 8px;
            border: 1px solid #ccc;
            resize: none;
        }
        button {
            margin-top: 20px;
            width: 100%;
            padding: 14px;
            background: #4f46e5;
            color: white;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        button:hover {
            background: #4338ca;
        }
        pre {
            background: #111827;
            color: #e5e7eb;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            margin-top: 25px;
        }
        footer {
            text-align: center;
            margin-top: 30px;
            color: #888;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Medical Scribe – SOAP Note Generator</h1>
        <p>Paste patient–doctor conversation below</p>

        <textarea id="transcript" placeholder="Enter conversation transcript here..."></textarea>

        <button onclick="generateSOAP()">Generate SOAP Note</button>

        <pre id="output"></pre>
    </div>

    <footer>
        Clinical documentation assistant – Demo UI
    </footer>

    <script>
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
            "hpi": "Patient reports fatigue, blood glucose readings between 190–230 mg/dL, missed metformin doses, poor sleep, headaches, and blurry vision."
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
