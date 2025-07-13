# main.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))



from dotenv import load_dotenv
from utils.model_loader import ModelLoader
from concurrent.futures import ThreadPoolExecutor, as_completed
from agents.medical_agents import (
    Cardiologist, Psychologist, Pulmonologist,
    Endocrinologist, Immunologist, Neurologist,
    MultidisciplinaryTeam
)
from config.config_loader import load_config


# ✅ Load environment variables from .env (e.g., OPENAI_API_KEY)
load_dotenv(dotenv_path=".env")

# ✅ Read the medical report
report_path = "Medical Reports/report_1.txt"
with open(report_path, "r") as file:
    medical_report = file.read()

# ✅ Initialize all individual agents
agents = {
    "Cardiologist": Cardiologist(medical_report),
    "Psychologist": Psychologist(medical_report),
    "Pulmonologist": Pulmonologist(medical_report),
    "Endocrinologist": Endocrinologist(medical_report),
    "Immunologist": Immunologist(medical_report),
    "Neurologist": Neurologist(medical_report)
}

# ✅ Run agents concurrently and collect results
def get_response(agent_name, agent):
    response = agent.run()
    return agent_name, response

responses = {}
with ThreadPoolExecutor() as executor:
    futures = {
        executor.submit(get_response, name, agent): name
        for name, agent in agents.items()
    }
    for future in as_completed(futures):
        agent_name, response = future.result()
        responses[agent_name] = response

# ✅ Initialize Multidisciplinary Team Agent
team_agent = MultidisciplinaryTeam(
    cardiologist_report=responses["Cardiologist"],
    psychologist_report=responses["Psychologist"],
    pulmonologist_report=responses["Pulmonologist"],
    endocrinologist_report=responses["Endocrinologist"],
    immunologist_report=responses["Immunologist"],
    neurologist_report=responses["Neurologist"]
)

# ✅ Run final diagnosis
final_diagnosis = team_agent.run()
final_diagnosis_text = "### Final Diagnosis:\n\n" + final_diagnosis

# ✅ Save output to file
output_path = "results/final_diagnosis.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    f.write(final_diagnosis_text)

print(f"\n✅ Final diagnosis saved to: {output_path}")


