# Medical Scribe – SOAP Note Generator

## Overview
This project converts patient–doctor conversation transcripts into structured SOAP clinical notes.

## API Endpoint
POST /generate-soap

### Input
{
  "transcript": "Patient–doctor conversation text"
}

### Output
Structured SOAP note in strict JSON format.

## Tech Stack
- Python
- FastAPI
- Pydantic

## Design Notes
The system focuses on clinical correctness and strict schema enforcement.
Automation using an open-source LLM can be added later without changing the API.

## Limitations
This system performs medical documentation only and does not provide diagnosis or treatment decisions.
