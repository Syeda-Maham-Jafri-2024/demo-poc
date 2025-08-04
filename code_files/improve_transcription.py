from dotenv import load_dotenv
import os

from openai import OpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def correct_ercp_transcription(transcription_text):
    system_prompt = (
        "You are a highly experienced ERCP surgeon specializing in Endoscopic Retrograde Cholangiopancreatography. "
        "Your task is to carefully review a medical transcription of an ERCP procedure and correct ONLY the incorrectly transcribed ERCP-specific terms. "
        "DO NOT change general sentences, formatting, punctuation, or non-medical words—only correct any medical terms that have been inaccurately captured. "
        "Ensure the terminology is precise, using the most accurate medical nomenclature related to ERCP surgeries. "
        "If a term is ambiguous but seems related to ERCP, infer the most likely correct term based on context. "
        "If no correction is needed, return the transcription as is."
    )

    user_prompt = f"""
    **Original Transcription of ERCP Procedure:**
    {transcription_text}
    
    **Task:**
    - Identify incorrect or misspelled ERCP-related medical terms.
    - Replace them with the correct medical terminology without altering anything else in the transcription.
    - Ensure that the final output maintains the exact same structure but with medically accurate terminology.
    - Donot add any heading to the output transcription.
    """

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content


# response = correct_ercp_transcription(
#     transcription_text="""
# The patient was prepped for the endoscopic retrograde cholongriopancreatogrphy procedure.
# A duodenoscope was inserted, but we encountered a structure in the bile duck.
# We then performed a spintrectomy to allow better access.
# A pankreatic stent was placed to address the blockage.
# """
# )
# print(response)
