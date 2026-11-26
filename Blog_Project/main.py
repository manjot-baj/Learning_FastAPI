from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from schemas import PostCreate, PostResponse

"""
APP CONFIG SECTION
"""

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

"""
Dummy Data
"""

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

"""
WEB APP SECTION
"""


@app.get("/", include_in_schema=False, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        request, "home.html", {"posts": posts, "title": "Home"}
    )


@app.get("/posts/{post_id}/", include_in_schema=False)
def get_post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(
                request,
                "post.html",
                {"post": post, "title": f"{post.get("title")[:50]}"},
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


"""
API SECTION
"""


@app.get("/api/posts/", response_model=list[PostResponse])
def get_all_posts():
    return posts


@app.post(
    "/api/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_post(post: PostCreate):
    new_id = max(p["id"] for p in posts) + 1 if posts else 1
    new_post = {
        "id": new_id,
        "author": post.author,
        "title": post.title,
        "content": post.content,
        "date_posted": "April 23, 2025",
    }
    posts.append(new_post)
    return new_post


@app.get("/api/posts/{post_id}/", response_model=PostResponse)
def get_post(post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


"""
APP Exception Handling
"""


@app.exception_handler(StarletteHTTPException)
def general_http_exception_handler(request: Request, exception: StarletteHTTPException):
    message = (
        exception.detail
        if exception.detail
        else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
