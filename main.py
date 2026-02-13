@app.post("/generate-soap", response_model=SOAPNote)
def generate_soap(input: TranscriptInput):

    text = input.transcript.lower()

    # Default values
    chief = "General consultation"
    hpi = "Patient reports health-related concerns."
    exam = "No abnormal findings reported."
    labs = ""
    assessment = []
    meds = []
    lab_tests = []
    referrals = []
    instructions = []
    follow = "Follow up as advised"

    # Subjective
    if "tired" in text or "fatigue" in text:
        chief = "Fatigue"
        hpi = "Patient reports persistent tiredness."

    if "headache" in text:
        hpi += " Complains of headache."

    if "blurry" in text:
        hpi += " Reports blurry vision."

    # Diabetes
    if "sugar" in text or "diabetes" in text:
        chief = "High blood sugar"
        assessment.append("Poorly controlled diabetes")
        labs = "Previous HbA1c elevated"
        lab_tests.append("HbA1c")
        meds.append("Adjust diabetes medication")

    # Fever / Infection
    if "fever" in text:
        chief = "Fever"
        assessment.append("Possible infection")
        lab_tests.append("Complete blood count")
        meds.append("Antipyretics")

    # BP
    if "pressure" in text or "bp" in text:
        chief = "High blood pressure"
        assessment.append("Hypertension")
        meds.append("Adjust BP medication")

    # Doctor actions
    if "metformin" in text:
        meds.append("Increase metformin dose")

    if "walk" in text or "exercise" in text:
        instructions.append("Regular physical activity")

    if "diet" in text:
        instructions.append("Follow healthy diet")

    if "dietitian" in text:
        referrals.append("Dietitian")

    # Objective
    if "no chest pain" in text:
        exam = "No chest pain or shortness of breath."

    # Defaults if empty
    if not assessment:
        assessment.append("General medical condition")

    if not instructions:
        instructions.append("Follow doctor advice")

    if not meds:
        meds.append("Symptomatic treatment")

    return {
        "subjective": {
            "chief_complaint": chief,
            "hpi": hpi
        },
        "objective": {
            "exam": exam,
            "vitals": "",
            "labs": labs
        },
        "assessment": assessment,
        "plan": {
            "medications": meds,
            "labs": lab_tests,
            "referrals": referrals,
            "instructions": instructions,
            "follow_up": follow
        },
        "visit_summary": f"Visit for {chief.lower()} with appropriate management."
    }
