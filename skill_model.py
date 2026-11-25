from typing import Literal
from pydantic import BaseModel, Field

class SkillAnalysisModel(BaseModel):
    Long_Explanation:str= Field(description="A 3 to 5 sentence explanation of the skill")
    Short_Explanation:str=Field(description="A 1 sentence explanation of the skill")
    Jobs:list[str]=Field(description="The names of 3 jobs where the skill is most often used.")