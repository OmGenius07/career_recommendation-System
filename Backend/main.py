from fastapi import FastAPI
from pydantic import BaseModel
from .prompt_logic import build_prompt
from .gpt_client import get_career_recommendations
app = FastAPI()

class UserProfile(BaseModel):
    skills: str
    interests: str
    personality: str
    location: str
    education: str
    experience: str = ""
    salary_expectation: str = ""

@app.post("/recommend")
async def recommend_career(profile: UserProfile):
    try:
        prompt = build_prompt(
            skills=profile.skills,
            interests=profile.interests,
            personality=profile.personality,
            location=profile.location,
            education=profile.education,
            experience=profile.experience,
            salary_expectation=profile.salary_expectation
        )
        recommendations = await get_career_recommendations(prompt)
        return {"ok": True, "recommendations": recommendations}
    except Exception as exc:
        # Always return JSON so the frontend can parse it
        return {"ok": False, "error": str(exc)}

if __name__ == "__main__":
    import uvicorn
    # Run using module path so reload works; run from project root
    uvicorn.run("Backend.main:app", host="0.0.0.0", port=8000, reload=True)
