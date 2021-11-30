from typing import Optional

import requests
from faker import Faker
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def main(request: Request):
    """Home page with invitation"""
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/requirements", response_class=HTMLResponse)
def requirements(request: Request):
    """Display the contents of the requirements.txt."""
    with open("requirements.txt", "r") as req:
        text = req.read().split()
        return templates.TemplateResponse(
            "req.html", {"request": request, "text": text}
        )


@app.get("/generate-users")
def generate_users(request: Request, user_count: Optional[int] = None):
    """
    Display randomly generated users ( first name + email)
    by default 100.
    """
    user_count = user_count if user_count else 100
    unique = Faker().unique
    user_data = [
        {"first_name": unique.first_name(), "email": unique.email()}
        for _ in range(user_count)
    ]
    return templates.TemplateResponse(
        "users.html", {"request": request, "user_data": user_data}
    )


@app.get("/space")
def generate_users(request: Request):
    astronauts = None
    try:
        req = requests.get("http://api.open-notify.org/astros.json")
        astronauts = req.json().get('people')
    except requests.exceptions.RequestException as e:
        print(e)
    return templates.TemplateResponse(
        "space.html", {"request": request, "astronauts": astronauts}
    )
