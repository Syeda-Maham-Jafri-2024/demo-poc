from openai import OpenAI
from pydantic import BaseModel, Field
import json

# from fpdf import FPDF


def generate_report_with_ai(transcribed_text, comments):

    client = OpenAI(api_key="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")

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
    # event_dict = event.dict(by_alias=True)

    # formatted_event = json.dumps(event_dict, indent=4)
    # print("Report Generation Complete")
    return event


# generate_report_with_ai(
#     """You should keep your personal information. I will, I will take care of it. Don't worry. Right now, what I'm trying to do is go inside the stomach. Okay. And this is not a main part of the procedure, but usually if there's cancer, then I might find some area blocked. Right. Some procedures are easier than others. Now, this is me going inside. So, there's the esophagus, the stomach, or small intestine. Right. We're in the small intestine, where bile comes out. Now, I think you guys know what bile is, right? Yeah. If it doesn't come out, it will be very painful. That's all I know. It's yellow. That's all. So, this patient, she has had elevated bilirubin, and there's evidence of stones on her stomach. Right. On that basis, we're doing ERT. Now, I'm going to look for her ampulla. Now, this is it. This is the opening we're looking for. This is what you call the ampulla. This whole structure is called the ampulla. It's the opening of the bile duct. Right. What cannulation means is, with this device, you know how IV cannula is? Yeah. This is called the cannulotope. Okay. We're going to cannulate that little hole, and pass a wire inside the duct. And we'll only be able to visualize what's behind this fluoroscopy. Okay. I'm going to load this in my scope. Another feature that we can start adding if we do voices is mention the morphology of the ampulla. Yeah. So, it's a small, normal-sized ampulla. Okay? I can't even see it. You say small, but I can't even see it. You can see the opening, right? Yes. And right now, you'll see the bile. Okay. So, you want the scope? It's made? Yes. Wow. Which scope did you give me? That one. Isn't it fun? Isn't it an elevator? It's big. Okay. So, I'm going to touch into it, create an axis. I'm trying to align it so that I can go in. Okay. You should be able to feel it now. Do you want me to guide you? No? In? Okay. I'm taking it back a little. Because I have a good axis. I really have a good axis. So, Now, I'm going to Now, go for it. Yes. Now, unboot. Keep it. Now, it's battery is still there, but it's elevator is not good. Now, go for it. Yes. Go. Okay. Now, you have to go forward a lot because the axis is not good. Why? Floro? Floro is better. No. This is for you. It's elevator is not good. It's 180. Okay. Yes. Okay. Better. One second. Go. Take it back a little. Take it back a little. Yes. Okay. Okay.
# So what we had is a double pleated ambulance and that's basically the morphology. You saw it then, it looked very small. So sometimes the scope technicalities are that if your elevator isn't good, then you can't actually see the whole thing properly unless you can leave it. It's actually a little bit of a double pleated ambulance. And we got the access, so that was me trying to align the cannula dome. And now I know I'm in the tunnel because usually this configuration of the wire means this is the center. We're going to confirm it by placing dye. Please inject dye. Okay, so this is a common bile duct because the dye is passing into a tubular structure. He's going to keep putting the dye in until I get the whole duct highlighted. So the normal configuration is like a wire. You can see one duct coming from the right, one duct coming from the left. And the wire is inside the left duct. And you can see one main common channel in the bottom. And can you see there's a whiteness shadow right above my scope? This black structure, this tubular structure is my scope. But you can see something white right above it, right? That's a stone. That's how I know that I'm in the right place. That's how I know that this isn't a pathology. Now I have enough dye inside. Now I'm going to ask him to take... Now I'm going to cut it. The process of cutting this ampulla is so that I can pull out the stone by sweeping the duct. When I do a cut, it's called a sphincterotomy. Now this is my cutting wire. So far, the only thing that I would like to report, maybe more comprehensively, again, describing what the ampulla looked like. You can see some pus coming out. Now if I see pus coming out, which is the whitish, cloudy fluid, that means I'm probably going to have to place a stent. Because there's infection inside. Pus is everywhere. So... Okay. So I'm going to try to create an axis which is straight. Don't pull back, Jinu. I'm not pulling back. Okay, like this? This is sphincterotomy. And it has to be a very careful process. You can't read it at all. Both. You can see the mucosa is cooking. So I'm basically burning the tissue with very specific electric current setting. Both. Slightly. Okay, unbroken. Let me assess. I think we're good, Mavya. So that's infection. Now there's no point getting her stone out right now. I can. I can take out the stone and place the stent. But first I need to do this cutting properly. Unbroken? Unbroken. Full broken? Full broken. Hard? Yes. How much should I cut? But the axis isn't coming out well. I don't want to go here. This isn't coming out well either. But I don't want to move the stone to the side. I don't want to cut this way. I want to cut that way. So I don't want my vision to be foggy. I'm supposed to keep it safe. Yeah, my direction is... So the problem is that young patients...
# who are female, especially, have a tendency of developing the main complications of the artery, and that's pancreatitis. So, we want to stay clear of that. I would still like to cut it, but I can't get an angle. Can I get the hobby? Reverse walk? Yes. This is also good. It's a very good car. I'm going. The access is very good. Change it. This whole process of cutting is a sphincterotomy. This process needs to be recorded because without a sphincterotomy, you shouldn't do anything else. The opening is so small. But now you can see some yellow fluid coming out, right? That's blood. And now you can see whitish powder fluid. That's pus. What I'm going to do now is take a balloon. And bleed that stone out. At this point, I'm recording what the ampulla looks like. I want to record that I did a cannulation in first attempt. And then I'm going to record that initial cholangiogram. That's what you call a cholangiogram. The cholangiogram shows a dilated duct with a filling defect in the mid-CBD. That area where the stone is, is mid-CBD. And the area where you can see the multiple smaller branches, that's above the hilum. So that's what we have. So now we're putting in a balloon. Everything that I do, I can see it going in endoscopically. But I'm going to follow it fluoroscopically. Anything I see through the x-ray is fluoroscopy. We've done enough cases. Now I'm going to try to get the stone out. Now I'm going to move it down. I feel that the stone might be very big. Okay, it's late. I don't know if it came out. I'm not sure it came out because it seems to be quite big. I think it did. It doesn't seem so. There is something there. You can see that little nugget. Is this allowed? She thinks she did so. I didn't record you. I didn't record you. Do it right.
# You can do it. Do it. Do it. You will see. It will happen. Take it out. You are going to the right. Can you put it here? Put it here. Right. Right. Right. Right. Right. You will have to pass it. You will have to exchange it later. You will have to exchange it later. You will have to exchange it later. Is it? Yes. So we tried to sweep it out physically. It wouldn't come out. So that basically means balloon trawl done twice. Because I tried to sweep it out twice. Stone could not be retrieved. In view of pus and retained stone at 10 centimeters sand will be placed. That's my plan. Once the infection settles down, I give her antibiotics, the inflammation settles down, then I'll bring her back in maybe a month. And I'll actually open this place up a little more and then remove the stone. Regardless, she needs a tent anyway. Okay. Straighten it. I'll straighten it. Okay. Come on, pump it up. Leave it, it's not coming out. Come on, pump it up. Come on, come on. Come back. Come back. Come back. Come back, come back. Come back. Now, pull back, hold. Back, hold. Come back. Four minutes to time. Hold. Pull back. Pull back. This is a mechanism of releasing the stress. You don't have to get this... Come back. Come back. Come back, hold. Five minutes to time. Hold. Pull back, hold. Pull back, hold. Hold. Pull back, hold. Is this the right place? Pull back, hold. Come back. Hold. Come back. Let's check thoracic. And here also? Pull back, hold. Pull back, hold. Pull back, hold. Pull back, hold. That's it. Now you tell me, what do we do in bleeding? There is no bleeding yet. Blood is coming. Blood is coming. Thank you. For more information visit www.osho.com www.osho.com OSHO is a registered Trademark of OSHO International Foundation
# So, it's always good to take a collaborative opinion, if I feel like it's leaving, somebody else might say it's not that significant, but I feel like we can probably inject this for her own safety. It takes a while, these people know, my hands would not cooperate. It's important. Like, for now, I would physically want him to come and see this. Do you want a balloon or something? It's free. Do you have a balloon in your pants? Balloon? Do you want me to get one for you? I'll get one for you. I'll get one for you. No. I'm short-sighted. Do you want me to get one for you? Yeah. Okay. Okay, now wash your hands. Thank you. One round, I'm going to give it. Is it connecting? No, it's not. Hello? Give me the wire, Tahira. Give me the wire. You're going to clean up the blood right now, yes? I would like to make sure that it's not actively bleeding. I see a little bit of blood coming out. I want to make sure I take great precautions because that can easily bleed again. Okay. Okay. Are you going to wear it? I would like to make sure that the wire doesn't fall. I'll have it inspected.
# So this is what I'm just doing, I'm smashing the balloon against the ampulla to create a clot. So this is what you call tamponade, basically like covering a wound with something, with pressure. This is the same balloon I used to sweep the stone out, but it's quite a crusty stone, and since the angulation for the cut wasn't very good, I decided to place a stand for now because she already has too much infection. We'll take it out next time. So when you place this balloon, isn't it going to block the passage? No, the stent is still down there, that's open. I'm just placing it to create pressure for two minutes. Okay, I'll continue to move it then. And the stent stays there? It doesn't slip away? The stent stays there. It has a flange, like basically an anchor, and it stays inside, hooks inside. But at some point in life it has to dissolve away, right? Within three months we're going to take it out. Oh, you're going to take it out yourself? Okay. In this case, within one month. Okay. So what does that mean for the patient? Is it painful? No, the stent is going to cause, it's going to open up the duct. The pain she's having because of the jaundice, because of the stone blockage, that's going to go away. Okay. Because the stent has opened the passage that the stone was blocking. Right. Because it shifts the stone to the side, and it opened the passage that it was blocking. Okay. One minute only. The reason it's always good to be extra cautious with our patients is because we get that demographic of patient that isn't from Karachi, that's too socially, economically struggling to come back or get admitted if they get sick. We want to give them as much safety as possible. Make sense. Now I'm going to check if there's any blood. I am very happy. This is all quartered blood. It's not actually blood. Okay. Good. Let me double check. Okay. Okay. Okay. Okay. Okay. Okay. Okay. Okay. Now you can see the splines sticking out of the stent. That's basically what's holding the stent in place. And there's another one inside. Okay. So it kind of sticks to that. It's on to it basically. Thank you. So we're done. I'm going to suction out some air. I'm happy that there's no active bleeding. Okay. Okay. So this wasn't actually that wide. Can we air dilute it? See what I said was that wide? Oh yeah. It's a completely collapsed system otherwise. Should I end the recording? Yeah. Or is there something I should... You can end the recording. Okay. Okay. Okay. Okay. Okay. Okay. Okay. Okay. Okay. Okay.""",
#     "",
# )


# """
# Summarize, clean, and structure the text into a professional report using GPT.
# """
# # Enhanced prompt for detailed instructions
# prompt = f"""
# You are an expert in the field of Endoscopy and a medical writer. this is a transcription of a discussion between a doctor and a medical team: {transcribed_text}
# These were the additionl comments added by the doctor: {comments}
# Based on the transcription and additional comments, please generate a professional, technical and detailed endoscopy report by following these instructions:

# 1. **Procedure Identification**: First, identify the type of procedure performed
# 2. **Procedure Summary**: Explain the indication for the procedure, including any patient history if available in the transcription
# 3. **Step-by-Step Procedure Details**: Provide a structured breakdown of the procedure, including the following if applicable:
#     - Equipment used in otder(e.g., balloon catheter, basket).
#     - Any difficulties encountered (e.g., inability to retrieve stones, complications).
#     - Medications administered during the procedure (e.g., anesthesia, antibiotics).
# 4. **Post-Procedure Findings**: Describe the immediate post-procedure findings such as:
#     - Whether the procedure was successful or not
#     - Any abnormalities or complications observed.
# 5. **Suggestions for Follow-up**: Provide specific follow-up instructions including:
#     - Medication (e.g., antibiotics, pain management).
#     - Follow-up imaging or tests (e.g., LFTs, imaging studies).
#     - Future procedures or surgeries (e.g., laparoscopic cholecystectomy).

# Please generate the report in a well-structured format as guided above

# Important Instructions: Use only the {transcribed_text} and {comments} to extract information to generate report, Do not make up anything from your own
# """

# # Call OpenAI GPT API
# client = OpenAI(api_key="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")
# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": prompt},
#     ],
# )

# # Extract the generated report text
# report = response.choices[0].message.content
# print("Report generation complete.")
# return report
# Reason For ERCP
# abdominal_pain: dict = Field(
#     default={"status": "No", "days": 0}, alias="Abdominal Pain"
# )
# juandice: dict = Field(default={"status": "No", "days": 0}, alias="Juandice")
# bile_duct_stone: str = Field(default="None", alias="Bile Duct Stone")
# periampullary_tumor: str = Field(default="None", alias="Periampullary Tumor")
# pancreatic_billary_tumor: str = Field(
#     default="None", alias="Pancreatic/Billary Tumor"
# )
# previous_surgery: str = Field(default="None", alias="Previous Surgery")
# cholecystectomy: str = Field(default="No", alias="Cholecystectomy")
# a_phosphatase: int = Field(default=0, alias="A.Phosphatase")
# bilirubin: int = Field(default=0, alias="Bilirubin")
# abnormal_imaging: str = Field(default="None", alias="Abnormal Imaging")
# other: str = Field(default=" ", alias="Other")

# # Examination
# access_to_papilla: str = Field(default="None", alias="Access To Papilla")
# opacification: str = Field(default="None", alias="Opacification")
# cannulation: str = Field(default="None", alias="Cannulation")

# # Therapy
# precut: str = Field(default="No", alias="Precut")
# stenting: str = Field(default="No", alias="Stenting")
# sphincterotomy: str = Field(default="No", alias="Sphincterotomy")
# spy_glass: str = Field(default="No", alias="Spy Glass")
# stone_removal: str = Field(default="No", alias="Stone Removal")
# size_and_type: str = Field(default="No", alias="Size & Type")
# sphincteroplasty: dict = Field(
#     default={"status": "No", "value": "No"}, alias="Sphincteroplasty"
# )
# ehl: str = Field(default="No", alias="EHL")
