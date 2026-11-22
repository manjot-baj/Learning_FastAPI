from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts: list[dict] = [
    {
        "id": 1,
        "author": "John Smith",
        "title": "Getting Started with FastAPI",
        "content": "FastAPI is a modern Python framework for building APIs quickly and efficiently.",
        "date_posted": "May 10, 2025",
    },
    {
        "id": 2,
        "author": "Sarah Johnson",
        "title": "Why Python is Popular",
        "content": "Python is one of the most popular programming languages because of its simplicity and versatility.",
        "date_posted": "May 11, 2025",
    },
    {
        "id": 3,
        "author": "Michael Brown",
        "title": "Introduction to REST APIs",
        "content": "REST APIs allow different applications to communicate with each other using HTTP methods.",
        "date_posted": "May 12, 2025",
    },
    {
        "id": 4,
        "author": "Emily Davis",
        "title": "Learning Python Dictionaries",
        "content": "Python dictionaries store data in key-value pairs and make it easy to organize and retrieve information.",
        "date_posted": "May 13, 2025",
    },
    {
        "id": 5,
        "author": "David Wilson",
        "title": "Building Your First Web Application",
        "content": "Building a web application with Python is a great way to learn backend development and database integration.",
        "date_posted": "May 14, 2025",
    },
]


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@app.get("/api/posts/")
def get_posts():
    return posts
