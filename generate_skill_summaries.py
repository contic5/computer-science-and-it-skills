import pandas as pd
from openai import OpenAI
import json
import textwrap
from skill_model import SkillAnalysisModel
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


force_overwrite=True

def prepare_prompt(row:pd.Series):
    skill=row["Skill"]
    field=row["Category"]

    prompt=f'''
    Explain the following skill is used in the {field} field: {skill}. Make the language clear to understand for non-specialist readers.
    '''

    prompt=textwrap.dedent(prompt)
    return prompt

def save_data(analysis_list:list):
    analysis_df=pd.DataFrame.from_dict(analysis_list)
    print("SAVING DATA")
    print(f"Skills Analyzed: {len(analysis_list)}")

    analysis_df.to_excel("src/results/Analyzed Skills.xlsx",sheet_name="Results",index=False)

def generate_response(row:pd.Series,skill_df)->dict:
    client = OpenAI()

    print(f"{row['ID']}/{len(skill_df)}")
    prompt=prepare_prompt(row)
    print(prompt)

    response = client.responses.parse(
        model="gpt-6.1-terra",
        input=prompt,
        text_format=SkillAnalysisModel,
    )

    
    print(response.output_text)

    #Load response text into a json dictionary
    response_dict=json.loads(response.output_text)

    #Convert job list into string with comma separated elements.
    response_dict["Jobs"]=",".join(response_dict["Jobs"])
    usage=response.usage
    response_dict["Input_Tokens"]=usage.input_tokens
    response_dict["Output_Tokens"]=usage.output_tokens
    response_dict["Cost"]=(0.10*usage.input_tokens)/1000000+(0.50*usage.output_tokens)/1000000

    #Turn row into a dictionary
    row_dict=row.to_dict()

    #Merge row dictionary and response dictionary
    analysis_dict=row_dict | response_dict
    return analysis_dict

def main():
    skill_df=pd.read_excel("src/data/Skills.xlsx",sheet_name="Skills")
    analysis_list=[]

    previous_analysis_df=pd.read_excel("src/results/Analyzed Skills.xlsx",sheet_name="Results")
    previous_analysis_skills_list=[]
    if len(previous_analysis_df)>0:
        previous_analysis_skills_list=previous_analysis_df["Skill"].to_list()

    for index,row in skill_df.iterrows():
        #Generate new results if we want to forcibly rewrite all data
        if force_overwrite:
            new_response=generate_response(row,skill_df)
            analysis_list.append(new_response)
        else:
            #Fetch matching row if there is a match
            try:
                previous_match_index=previous_analysis_skills_list.index(row["Skill"])
                print("Using previously calculated results")
                analysis_list.append(previous_analysis_df.iloc[previous_match_index].to_dict())
            #Otherwise, generate new response.
            except ValueError:
                new_response=generate_response(row,skill_df)
                analysis_list.append(new_response)
            
        
        #Save after every few rows to prevent data loss
        if(index%3==0):
            save_data(analysis_list)
    save_data(analysis_list)

if __name__=="__main__":
    main()