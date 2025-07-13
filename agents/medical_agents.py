from langchain.prompts import PromptTemplate
from utils.model_loader import ModelLoader

from config.config_loader import load_config




class Agent:
    def __init__(self,medical_report = None,role = None,other_info = None,patient_metadata = None):
        """Initialize the agent with medical reports, role, other info, and patient metadata."""
        self.medical_report = medical_report
        self.role = role
        self.other_info = other_info
        self.patient_metadata = patient_metadata
        self.prompt_template = self.create_prompt_template()
        self.model = ModelLoader().load_model()




    def create_prompt_template(self):
        if self.role == "MultidisciplinaryTeam":
          templates = f"""
             You are a Multidisciplinary Medical Team of healthcare professionals.
             You will receive a medical report of a patient visited by a cardiologist, psychologist, pulmonologist, endocrinologist, immunologist, and neurologist.
             Task : Review the patient's medical report from the cardiologist, psychologist, pulmonologist, endocrinologist, immunologist, and neurologist,analyze them and come up with a list of 3 possible health issues of the patient.
             Just return a list of bullet points of 3 possible health issues of the patient and for each issue provide the reason.

             Cardiologist Report: {self.other_info.get('cardiologist_report', '')}
             Psychologist Report: {self.other_info.get('psychologist_report', '')}
             Pulmonologist Report: {self.other_info.get('pulmonologist_report', '')}
             Endocrinologist Report: {self.other_info.get('endocrinologist_report', '')}
             Immunologist Report: {self.other_info.get('immunologist_report', '')}
             Neurologist Report: {self.other_info.get('neurologist_report', '')}
        """
          return PromptTemplate.from_template(templates)

        else:
          templates = {
             "Cardiologist":"""
                   You are a board certified Cardiologist specialising in the prevention,act lika a Cardiologist.You will receive a medical report of a patient.
                   Task : Review the patient's cardiac workup, including ECG, blood tests, Holter monitor results, and echocardiogram.
                   Focus: Determine if there are any subtle signs of cardiac issues that could explain the patient’s symptoms. Rule out any underlying heart conditions, such as arrhythmias or structural abnormalities, that might be missed on routine testing.
                    Recommendation: Provide guidance on any further cardiac testing or monitoring needed to ensure there are no hidden heart-related concerns. Suggest potential management strategies if a cardiac issue is identified.
                    Please only return the possible causes of the patient's symptoms and the recommended next steps.
                    Medical Report: {medical_report}
                    """,
              "Psychologist":"""  
                    You are a board certified Psychologist specializing in mental health assessment and diagnosis,act like a Psychologist. You will receive a patient's report.    
                    Task : Review the patient's psychological evaluation, including cognitive tests, behavioral assessments, and interviews and provide a psychological assessment.
                    Focus : Identify any underlying psychological conditions that may not be immediately apparent, such as anxiety disorders, mood disorders, or cognitive impairments.
                    Recommendation: Offer guidance on how to address these mental health concerns, including therapy, counseling, or other interventions.
                    Please only return the possible mental health issues and the recommended next steps.
                    Patient's Report: {medical_report}
                    """,

               "Pulmonologist":""" 
                       You are a board certified Pulmonologist specializing in respiratory health,act like a Pulmonologist. You will receive a patient's report.
                       Task : Review the patient's pulmonary function tests, imaging studies, and clinical history and provide a pulmonary assessment.
                       Focus : Identify any subtle signs of respiratory issues that may not be evident in routine evaluations, such as early-stage COPD, asthma, or interstitial lung disease.  
                       Recommendation: Offer guidance on how to address these respiratory concerns, including pulmonary function tests, imaging studies, or other interventions.
                       Please only return the possible respiratory issues and the recommended next steps.
                       Patient's Report: {medical_report}
                    """,
                "Endocrinologist":"""
                    You are a board certified Endocrinologist specializing in hormonal health,act like a Endocrinologist. You will receive a patient's report.
                    Task : Review the patient's hormonal evaluations, including thyroid function tests, glucose metabolism assessments, and adrenal function tests.
                    Focus : Identify any subtle signs of hormonal imbalances that may not be evident in routine evaluations, such as early-stage diabetes, thyroid disorders, or adrenal insufficiency.
                    Recommendation: Offer guidance on how to address these hormonal concerns, including further testing or management strategies.
                    Please only return the possible hormonal issues and the recommended next steps.
                    Patient's Report: {medical_report}
                """,
                "Immunologist":"""
                    You are a board certified Immunologist specializing in immune system disorders,act like a Immunologist. You will receive a patient's report.
                    Task : Review the patient's immunological evaluations, including allergy tests, autoimmune markers, and immune function assessments.
                    Focus : Identify any subtle signs of immune system dysfunction that may not be evident in routine evaluations, such as early-stage autoimmune diseases or immunodeficiencies.
                    Recommendation: Offer guidance on how to address these immune concerns, including further testing or management strategies.
                    Please only return the possible immune issues and the recommended next steps.
                    Patient's Report: {medical_report}
                """,
                "Neurologist":"""
                    You are a board certified Neurologist specializing in neurological disorders,act like a Neurologist. You will receive a patient's report.
                    Task : Review the patient's neurological evaluations, including imaging studies, nerve conduction tests, and clinical history.
                    Focus : Identify any subtle signs of neurological issues that may not be evident in routine evaluations, such as early-stage neurodegenerative diseases or peripheral neuropathies.
                    Recommendation: Offer guidance on how to address these neurological concerns, including further testing or management strategies.
                    Please only return the possible neurological issues and the recommended next steps.
                    Patient's Report: {medical_report}
                """
          }

        templates = templates[self.role]
        return PromptTemplate.from_template(templates)
    

    def run(self):
        print(f"{self.role} is running...")
        prompt = self.prompt_template.format(medical_report=self.medical_report)
        try:
            response = self.model.invoke(prompt)
            return response.content
        except Exception as e:
            print("Error occurred:", e)
            return None

#Define specialized agents for medical tasks

class Cardiologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Cardiologist")

class Psychologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Psychologist")

class Pulmonologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Pulmonologist")


class Endocrinologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Endocrinologist")


class Immunologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Immunologist")


class Neurologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Neurologist")


class MultidisciplinaryTeam(Agent): 
     def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report,
                  endocrinologist_report, immunologist_report, neurologist_report):
        other_info = {
            "cardiologist_report": cardiologist_report,
            "psychologist_report": psychologist_report,
            "pulmonologist_report": pulmonologist_report,
            "endocrinologist_report": endocrinologist_report,
            "immunologist_report": immunologist_report,
            "neurologist_report": neurologist_report
        }
        super().__init__(role="MultidisciplinaryTeam", other_info= other_info)










