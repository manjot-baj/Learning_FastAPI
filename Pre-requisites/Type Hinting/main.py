# from typing import Optional
from typing import NewType, TypedDict, Any, TypeVar
from dataclasses import dataclass
import random

RGB = NewType("RGB", tuple[int, int, int])

HSL = NewType("HSL", tuple[int, int, int])

# type User = dict[str, str | int | RGB | None]


# class User(TypedDict):
#     first_name: str
#     last_name: str
#     email: str
#     age: int | None
#     fav_color: RGB | None


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    age: int | None = None
    fav_color: RGB | None = None


def create_user(
    first_name: str,
    last_name: str,
    age: int | None = None,
    fav_color: RGB | None = None,
) -> User:
    email: str = f"{first_name.lower()}_{last_name.lower()}@example.com"

    return User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        age=age,
        fav_color=fav_color,
    )


# def random_choice(items: list[Any]) -> Any:
#     return random.choice(items)

# any = TypeVar("any")


# def random_choice(items: list[any]) -> any:
#     return random.choice(items)


def random_choice[any](items: list[any]) -> any:
    return random.choice(items)


user1 = create_user("Corey", "Schafer", age=38, fav_color=RGB((109, 123, 134)))
user2 = create_user("John", "Doe", fav_color=RGB((109, 123, 134)))

# print(user1)
# print(user2)

users = [user1, user2]
rando_user = random_choice(users)
print(rando_user)

emails = [user.email for user in users]
rando_email = random_choice(emails)
print(rando_email)
