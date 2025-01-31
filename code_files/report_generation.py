from openai import OpenAI
from pydantic import BaseModel, Field
import json

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def generate_report_with_ai(transcribed_text, comments):

    client = OpenAI(api_key=openai_api_key)

    class ErcpEvent(BaseModel):
        abdominal_pain: str = Field(
            alias="Abdominal Pain",
            description="The presence or absence of abdominal pain.",
        )
        juandice: str = Field(
            alias="Juandice", description="Whether the patient has jaundice."
        )
        bile_duct_stone: str = Field(
            alias="Bile Duct Stone", description="The presence of bile duct stones."
        )
        periampullary_tumor: str = Field(
            alias="Periampullary Tumor",
            description="Whether there is a periampullary tumor.",
        )
        pancreatic_billary_tumor: str = Field(
            alias="Pancreatic/Billary Tumor",
            description="Presence of pancreatic or biliary tumor.",
        )
        previous_surgery: str = Field(
            alias="Previous Surgery", description="Details of any previous surgeries."
        )
        cholecystectomy: str = Field(
            alias="Cholecystectomy",
            description="Whether the patient has had a cholecystectomy.",
        )
        a_phosphatase: int = Field(
            alias="A.Phosphatase", description="A.Phosphatase level of the patient."
        )
        bilirubin: int = Field(
            alias="Bilirubin", description="Bilirubin level of the patient."
        )
        abnormal_imaging: str = Field(
            alias="Abnormal Imaging",
            description="Details of any abnormal imaging findings.",
        )
        other: str = Field(
            alias="Other",
            description="Any other relevant information not covered by the above categories.",
        )
        access_to_papilla: str = Field(
            alias="Access To Papilla",
            description="Access to the papilla during the procedure.",
        )
        opacification: str = Field(
            alias="Opacification",
            description="Whether opacification was achieved during the procedure.",
        )
        cannulation: str = Field(
            alias="Cannulation", description="Cannulation status in the procedure."
        )
        precut: str = Field(
            alias="Precut", description="Whether precut was used during the procedure."
        )
        stenting: str = Field(
            alias="Stenting", description="Whether stenting was performed."
        )
        sphincterotomy: str = Field(
            alias="Sphincterotomy", description="Whether sphincterotomy was performed."
        )
        spy_glass: str = Field(
            alias="Spy Glass", description="Whether SpyGlass procedure was used."
        )
        stone_removal: str = Field(
            alias="Stone Removal", description="Whether stone removal was performed."
        )
        size_and_type: str = Field(
            alias="Size & Type", description="Mention the size of the stent"
        )
        sphincteroplasty: str = Field(
            alias="Sphincteroplasty",
            description="Whether sphincteroplasty was performed.",
        )
        ehl: str = Field(
            alias="EHL",
            description="Whether EHL (Electrohydraulic Lithotripsy) was performed.",
        )
        conclusion: str = Field(
            alias="Conclusion",
            description="Give a brief summary of the entire procedure carried out",
        )

    # Prompt for GPT model
    prompt = (
        "Extract the relevant medical details and structure them based on the "
        "provided schema for ERCP reports:\n\n"
        f"Transcription: {transcribed_text}\n\nComments: {comments}\n"
    )

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert doctor for Endoscopy"},
            {"role": "user", "content": prompt},
        ],
        response_format=ErcpEvent,
    )

    event = completion.choices[0].message.parsed
    return event

