from fastapi import FastAPI, status, Response, HTTPException
from src.treatment_entities.entities import Treatmentinput
from src.treatment_entities.treatment_center import TreatmentCenter

app = FastAPI()

@app.post('/treat/attributes', tags="Treatment")
def get_new_answer_attributes(input : Treatmentinput):
    return TreatmentCenter.run_line(line_name='attributes_pipeline', input=input)

@app.post('/treat/intent', tags="Treatment")
def get_new_answer_intent(input : Treatmentinput):
    return TreatmentCenter.run_line(line_name='intent_pipeline', input=input)

@app.post('/treat/entity', tags="Treatment")
def get_new_answer_entity(input : Treatmentinput):
    return TreatmentCenter.run_line(line_name='entity_pipeline', input=input)

@app.post('/treat/filters', tags="Treatment")
def get_new_answer_entity(input : Treatmentinput):
    return TreatmentCenter.run_line(line_name='filter_pipeline', input=input)

@app.post('/treat/mandatory/attributes', tags="Util")
def run_mandatory_treatments(input : Treatmentinput):
    input.complete_treatment = False
    return TreatmentCenter.run_line(line_name='attributes_pipeline', input=input)