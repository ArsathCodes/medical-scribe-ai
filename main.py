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
<title>Medical Scribe</title>
<style>
body{font-family:Arial;background:#f1f5f9;margin:0}
header{background:#1e293b;color:white;padding:20px;font-size:22px}
.container{display:grid;grid-template-columns:1fr 1fr;gap:20px;padding:25px}
.card{background:white;padding:20px;border-radius:10px;box-shadow:0 4px 10px rgba(0,0,0,0.1)}
textarea{width:100%;height:260px;padding:10px}
button{padding:10px 15px;margin-top:10px;border:none;border-radius:5px;cursor:pointer}
.primary{background:#4f46e5;color:white}
.secondary{background:#e2e8f0}
pre{background:#020617;color:#e5e7eb;padding:15px;height:380px;overflow:auto}
</style>
</head>

<body>

<header>Medical Scribe – SOAP Generator</header>

<div class="container">

<div class="card">
<h3>Conversation</h3>

<textarea id="transcript"></textarea>

<button class="secondary" onclick="loadSample()">Use Sample</button>
<button class="primary" onclick="generate()">Generate</button>
</div>

<div class="card">
<h3>SOAP Output</h3>
<pre id="output">Waiting...</pre>
</div>

</div>

<script>

const sample = `Doctor: Good morning. How are you?

Patient: I feel tired and my sugar is high.

Doctor: Are you taking medicines?

Patient: I missed some doses.

Doctor: Your HbA1c is high. Increase metformin and walk daily.`;

function loadSample(){
 document.getElementById("transcript").value = sample;
}

async function generate(){

 const text = document.getElementById("transcript").value;

 const res = await fetch("/generate-soap",{
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body:JSON.stringify({transcript:text})
 });

 const data = await res.json();

 document.getElementById("output").textContent =
 JSON.stringify(data,null,2);
}

</script>

</body>
</html>
"""


@app.post("/generate-soap", response_model=SOAPNote)
def generate_soap(input: TranscriptInput):

    text = input.transcript.lower()

    chief = "General consultation"
    hpi = "Patient reports health concerns."
    exam = "No abnormal findings."
    labs = ""

    assessment = []
    meds = []
    lab_tests = []
    referrals = []
    instructions = []

    follow = "Follow up as advised"


    # Fatigue
    if "tired" in text or "fatigue" in text:
        chief = "Fatigue"
        hpi = "Patient reports persistent tiredness."


    # Headache
    if "headache" in text:
        hpi += " Complains of headache."


    # Blurry vision
    if "blurry" in text:
        hpi += " Reports blurry vision."


    # Diabetes
    if "sugar" in text or "diabetes" in text:
        chief = "High blood sugar"
        assessment.append("Poorly controlled diabetes")
        labs = "HbA1c elevated"
        lab_tests.append("HbA1c")
        meds.append("Adjust diabetes medication")


    # Fever
    if "fever" in text:
        chief = "Fever"
        assessment.append("Possible infection")
        lab_tests.append("CBC")
        meds.append("Paracetamol")


    # BP
    if "bp" in text or "pressure" in text:
        chief = "High blood pressure"
        assessment.append("Hypertension")
        meds.append("BP medication adjustment")


    # Doctor advice
    if "walk" in text or "exercise" in text:
        instructions.append("Daily exercise")


    if "diet" in text:
        instructions.append("Healthy diet")


    if "dietitian" in text:
        referrals.append("Dietitian")


    if "no chest pain" in text:
        exam = "No chest pain or breathlessness."


    # Defaults
    if not assessment:
        assessment.append("General medical condition")

    if not meds:
        meds.append("Symptomatic treatment")

    if not instructions:
        instructions.append("Follow doctor instructions")


    return {

        "subjective":{
            "chief_complaint":chief,
            "hpi":hpi
        },

        "objective":{
            "exam":exam,
            "vitals":"",
            "labs":labs
        },

        "assessment":assessment,

        "plan":{
            "medications":meds,
            "labs":lab_tests,
            "referrals":referrals,
            "instructions":instructions,
            "follow_up":follow
        },

        "visit_summary":
        f"Visit for {chief.lower()} with appropriate treatment."

    }
