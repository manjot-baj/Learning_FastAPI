from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    HttpUrl,
    SecretStr,
    field_validator,
    model_validator,
    computed_field,
    ConfigDict,
)
from uuid import UUID, uuid4
from datetime import datetime, UTC
from functools import partial
from typing import Literal, Annotated
import json


class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        strict=True,
        # extra="allow",
        extra="forbid",
        validate_assignment=True,
        # frozen=True,
    )
    uid: UUID = Field(alias="id", default_factory=uuid4)
    username: Annotated[str, Field(min_length=3, max_length=20)]
    email: EmailStr
    website: HttpUrl | None = None
    password: SecretStr
    age: Annotated[int, Field(ge=13, le=130)]
    verified_at: datetime | None = None
    bio: str = ""
    is_active: bool = True
    first_name: str = None
    last_name: str = None
    follower_count: int | str = 0

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.replace("_", "").isalnum():
            raise ValueError(
                "Username must contain only letters, numbers, " "and underscores"
            )
        return value.lower()

    @field_validator("website", mode="before")
    @classmethod
    def add_https(cls, value: str | None) -> str | None:
        if value and not value.startswith(("http://", "https://")):
            return f"https://{value}"
        return value

    @computed_field
    @property
    def display_name(self) -> str:
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.username

    @computed_field
    @property
    def is_influencer(self) -> bool:
        return self.follower_count >= 10000


class UserRegistration(BaseModel):
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr

    @model_validator(mode="after")
    def password_match(self) -> "UserRegistration":
        if self.password.get_secret_value() != self.confirm_password.get_secret_value():
            raise ValueError("Passwords do not match")
        return self


class Comment(BaseModel):
    content: str
    author_email: EmailStr
    likes: int = 0


class BlogPost(BaseModel):
    author: User
    title: Annotated[str, Field(min_length=1, max_length=200)]
    content: Annotated[str, Field(min_length=10)]
    # slug: Annotated[str, Field(pattern=r"^[a-z0-9]+$")]
    view_count: int = 0
    is_published: bool = False
    tags: list[str] = Field(default_factory=list)
    create_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))
    status: Literal["draft", "published", "archived"] = "draft"
    comments: list[Comment] = Field(default_factory=list)


if __name__ == "__main__":

    # post = BlogPost(
    #     author_id=12345,
    #     title="Getting Started With Pydantic",
    #     content="This article explains the basics of Pydantic models.",
    #     slug="gettingstartedwithpydantic",
    #     view_count=100,
    #     is_published=True,
    #     tags=["python", "pydantic"],
    #     status="published",
    # )
    # print(post.model_dump_json(indent=2))

    # ==================================================================
    # INVALID BLOG POST
    # ==================================================================

    # post = BlogPost(
    #     author_id=12345,
    #     title="",
    #     content="Short",
    #     slug="Getting-Started",
    #     view_count="many",
    #     is_published="yes",
    #     tags=["python", 123],
    #     status="pending",
    # )

    # print(post.model_dump_json(indent=2))

    # ==================================================================
    # VALID USER
    # ==================================================================

    # user = User(
    #     username="Manjot_Bajwa_123",
    #     email="manjot@example.com",
    #     password="MySecurePassword123",
    #     age=25,
    #     website="example.com",
    #     first_name="Manjot",
    #     last_name="Bajwa",
    #     follower_count=15000,
    #     bio="Pydantic learner",
    # )

    # print(user.model_dump_json(indent=2))

    # ==================================================================
    # INVALID USER
    # ==================================================================

    # user = User(
    #     username="ab",
    #     email="not-an-email",
    #     password="MySecurePassword123",
    #     age=10,
    #     website="not-a-url",
    #     first_name="Manjot",
    #     last_name="Bajwa",
    # )

    # print(user.model_dump_json(indent=2))

    # ==================================================================
    # VALID USER REGISTRATION
    # ==================================================================

    # user_reg = UserRegistration(
    #     email="bajwa@gmail.com",
    #     password="Qwerty@1",
    #     confirm_password="Qwerty@1",
    # )
    # print(user_reg.model_dump_json(indent=2))

    # ==================================================================
    # INVALID USER REGISTRATION
    # ==================================================================

    # user_reg = UserRegistration(
    #     email="bajwa@gmail.com",
    #     password="Qwerty@1",
    #     confirm_password="Qwerty1",
    # )

    # print(user_reg.model_dump_json(indent=2))

    # Nested

    # post_data = {
    #     "title": "Understanding Pydantic Models",
    #     "content": "Pydantic makes data validation easy and intuitive...",
    #     "slug": "understanding-pydantic",
    #     "author": {
    #         "username": "coreyms",
    #         "email": "CoreyMSchafer@gmail.com",
    #         "age": 39,
    #         "password": "secret123",
    #     },
    #     "comments": [
    #         {
    #             "content": "I think I understand nested models now!",
    #             "author_email": "student@example.com",
    #             "likes": 25,
    #         },
    #         {
    #             "content": "Can you cover FastAPI next?",
    #             "author_email": "viewer@example.com",
    #             "likes": 15,
    #         },
    #     ],
    # }

    # post = BlogPost(**post_data)
    # print(post.model_dump_json(indent=2))

    # configDict
    user_data = {
        "id": "3bc4bf25-1b73-44da-9078-f2bb310c7374",
        "username": "Corey_Schafer",
        "email": "CoreyMSchafer@gmail.com",
        "age": "39",
        "password": "secret123",
    }
    user = User.model_validate(user_data)
    # user = User.model_validate_json(json.dumps(user_data))
    print(user.model_dump_json(indent=2, by_alias=True, include={"username", "email"}))
