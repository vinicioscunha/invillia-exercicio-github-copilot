"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from pydantic import BaseModel

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Join the school basketball team and compete in tournaments",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Swimming Club": {
        "description": "Learn swimming techniques and participate in swim meets",
        "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": []
    },
    "Drama Club": {
        "description": "Explore acting, stage production, and perform in school plays",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Art Workshop": {
        "description": "Learn painting, drawing, and other artistic techniques",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Math Olympiad Training": {
        "description": "Prepare for math competitions with advanced problem-solving techniques",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    }
}


class SignupRequest(BaseModel):
    email: str


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, signup_request: SignupRequest):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if the student is already signed up -
    if signup_request.email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")

    # Validar se o aluno já está inscrito
    signed_up_activities = 0
    for activity in activities.values():
        if signup_request.email in activity["participants"]:
            signed_up_activities += 1
    if signed_up_activities >= 3:
        raise HTTPException(status_code=400, detail="Student already signed up for 3 activities")
    activity["participants"].append(signup_request.email)
    return {"message": f"Signed up {signup_request.email} for {activity_name}"}
