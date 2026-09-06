from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    HttpUrl,
    SecretStr,
    field_validator,
    model_validator,
    computed_field,
)
from uuid import UUID, uuid4
from datetime import datetime, UTC
from functools import partial
from typing import Literal, Annotated

# BaseModel is the foundation of Pydantic models.
#
# Pydantic uses Python type annotations and validators to:
# - Validate incoming data
# - Convert compatible input types when possible
# - Enforce field constraints
# - Run custom validation logic
# - Provide detailed validation errors
# - Serialize model instances to dictionaries or JSON


class User(BaseModel):

    # ==================================================================
    # UID
    # ==================================================================

    # UUID represents a universally unique identifier.
    #
    # `default_factory=uuid4` tells Pydantic to call uuid4()
    # automatically when a uid is not provided.
    #
    # A NEW UUID is generated for every User instance.
    #
    # Therefore, uid does not need to be supplied by the caller.
    uid: UUID = Field(default_factory=uuid4)

    # ==================================================================
    # USERNAME
    # ==================================================================

    # Required field.
    #
    # The username must contain:
    # - At least 3 characters
    # - At most 20 characters
    #
    # Additional validation is performed by the custom
    # `validate_username` field validator below.
    username: Annotated[str, Field(min_length=3, max_length=20)]

    # ==================================================================
    # EMAIL
    # ==================================================================

    # EmailStr is a Pydantic type specifically designed to
    # validate email addresses.
    #
    # Unlike a plain `str`, EmailStr checks whether the value
    # has a valid email format.
    email: EmailStr

    # ==================================================================
    # WEBSITE
    # ==================================================================

    # HttpUrl validates that the value is a valid HTTP/HTTPS URL.
    #
    # The field is optional because its default value is None.
    #
    # The `add_https` validator below runs BEFORE HttpUrl validation.
    #
    # This allows us to provide:
    #
    #     "example.com"
    #
    # which is converted to:
    #
    #     "https://example.com"
    #
    # before Pydantic validates it as an HttpUrl.
    website: HttpUrl | None = None

    # ==================================================================
    # PASSWORD
    # ==================================================================

    # SecretStr is designed for sensitive values such as passwords.
    #
    # Pydantic masks the secret when the model is printed or serialized.
    #
    # To access the actual password value, use:
    #
    #     password.get_secret_value()
    password: SecretStr

    # ==================================================================
    # AGE
    # ==================================================================

    # The age must be between 13 and 130, inclusive.
    #
    # `ge=13` means:
    #     greater than or equal to 13
    #
    # `le=130` means:
    #     less than or equal to 130
    age: Annotated[int, Field(ge=13, le=130)]

    # ==================================================================
    # OPTIONAL FIELDS
    # ==================================================================

    # Optional datetime field.
    #
    # If no value is supplied, verified_at is None.
    verified_at: datetime | None = None

    # Defaults to an empty string when no value is supplied.
    bio: str = ""

    # Users are active by default.
    is_active: bool = True

    # Required fields because they do not have default values.
    first_name: str
    last_name: str

    # `int | str` is a union type.
    #
    # follower_count can contain either:
    #
    #     int
    #
    # or:
    #
    #     str
    #
    # If no value is provided, it defaults to 0.
    follower_count: int | str = 0

    # ==================================================================
    # FIELD VALIDATOR: USERNAME
    # ==================================================================

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        """
        Validate and normalize the username.

        `@field_validator("username")` tells Pydantic to run
        this method whenever the username field is validated.

        The validator allows:
        - Letters
        - Numbers
        - Underscores

        Valid examples:
            "manjot123"
            "Manjot_Bajwa"
            "user_123"

        Invalid examples:
            "manjot-bajwa"   # Hyphen is not allowed
            "manjot bajwa"   # Space is not allowed
            "manjot@123"     # @ is not allowed

        `.lower()` converts the username to lowercase.

        Example:

            "Manjot_Bajwa"

        becomes:

            "manjot_bajwa"
        """

        # Remove underscores before checking whether the remaining
        # characters are alphanumeric.
        #
        # This allows underscores while rejecting:
        # - Spaces
        # - Hyphens
        # - Special characters
        # - Other non-alphanumeric characters
        if not value.replace("_", "").isalnum():
            raise ValueError(
                "Username must contain only letters, numbers, " "and underscores"
            )

        # Normalize the username to lowercase.
        return value.lower()

    # ==================================================================
    # FIELD VALIDATOR: WEBSITE
    # ==================================================================

    @field_validator("website", mode="before")
    @classmethod
    def add_https(cls, value: str | None) -> str | None:
        """
        Add HTTPS when the website does not contain a URL scheme.

        `mode="before"` means this validator runs BEFORE Pydantic
        performs the normal HttpUrl validation.

        Example:

            "example.com"

        becomes:

            "https://example.com"

        If the value already starts with:

            "http://"

        or:

            "https://"

        it is returned unchanged.
        """

        if value and not value.startswith(("http://", "https://")):
            return f"https://{value}"

        return value

    # ==================================================================
    # COMPUTED FIELD: DISPLAY NAME
    # ==================================================================

    @computed_field
    @property
    def display_name(self) -> str:
        """
        Create a value dynamically from other model fields.

        `@computed_field` tells Pydantic that this property should
        be included when the model is serialized.

        `@property` allows us to access the method like an attribute:

            user.display_name

        instead of:

            user.display_name()

        If both first_name and last_name are available:

            "Manjot" + "Bajwa"

        becomes:

            "Manjot Bajwa"

        Otherwise, the username is used as the display name.
        """

        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"

        return self.username

    # ==================================================================
    # COMPUTED FIELD: INFLUENCER
    # ==================================================================

    @computed_field
    @property
    def is_influencer(self) -> bool:
        """
        Determine whether the user is considered an influencer.

        This is a computed field because its value is calculated
        from another field instead of being stored directly.

        A user is considered an influencer when their follower count
        is at least 10,000.

        Examples:

            follower_count = 5000
            is_influencer = False

            follower_count = 10000
            is_influencer = True

            follower_count = 50000
            is_influencer = True
        """

        return self.follower_count >= 10000


class UserRegistration(BaseModel):

    # ==================================================================
    # REGISTRATION FIELDS
    # ==================================================================

    # All three fields are required.
    #
    # SecretStr is used for the password fields so that sensitive
    # password values are masked when the model is printed or serialized.
    email: EmailStr
    password: SecretStr
    confirm_password: SecretStr

    # ==================================================================
    # MODEL VALIDATOR
    # ==================================================================

    @model_validator(mode="after")
    def password_match(self) -> "UserRegistration":
        """
        Verify that password and confirm_password are identical.

        A model validator is useful when validation depends on
        multiple fields.

        `mode="after"` means this validator runs AFTER Pydantic
        has validated the individual fields.

        Both password fields are SecretStr objects, so
        `.get_secret_value()` is used to access their actual
        values for comparison.

        The return type:

            "UserRegistration"

        is a forward reference.

        The quotes tell Python that UserRegistration should be
        treated as a type name that will be resolved later.

        The method returns `self`, which is the current
        UserRegistration instance.
        """

        if self.password.get_secret_value() != self.confirm_password.get_secret_value():
            raise ValueError("Passwords do not match")

        return self


class BlogPost(BaseModel):
    """
    Pydantic model representing a blog post.

    This model demonstrates:
    - Required fields
    - Optional fields
    - Field constraints
    - Union types
    - Mutable defaults with default_factory
    - Dynamic defaults
    - Regular-expression validation
    - Literal types
    """

    # ==================================================================
    # REQUIRED FIELDS
    # ==================================================================

    # `str | int` is a union type.
    #
    # author_id can therefore be either a string or an integer.
    #
    # Valid:
    #     author_id=12345
    #     author_id="12345"
    author_id: str | int

    # Title must contain between 1 and 200 characters.
    title: Annotated[str, Field(min_length=1, max_length=200)]

    # Content must contain at least 10 characters.
    content: Annotated[str, Field(min_length=10)]

    # ==================================================================
    # SLUG
    # ==================================================================

    # The slug must contain only:
    # - Lowercase letters: a-z
    # - Numbers: 0-9
    #
    # Regular expression:
    #
    #     ^[a-z0-9]+$
    #
    # Meaning:
    #
    #     ^          Start of string
    #     [a-z0-9]   Lowercase letter or digit
    #     +          One or more characters
    #     $          End of string
    #
    # Valid:
    #     "pydantic"
    #     "pydantic123"
    #     "gettingstarted"
    #
    # Invalid:
    #     "Pydantic"          # Uppercase letter
    #     "pydantic-post"     # Hyphen
    #     "pydantic_post"     # Underscore
    slug: Annotated[str, Field(pattern=r"^[a-z0-9]+$")]

    # ==================================================================
    # FIELDS WITH DEFAULT VALUES
    # ==================================================================

    # Defaults to 0 when no value is supplied.
    view_count: int = 0

    # Blog posts are unpublished by default.
    is_published: bool = False

    # ==================================================================
    # TAGS
    # ==================================================================

    # Lists are mutable objects.
    #
    # `default_factory=list` tells Pydantic to create a NEW list
    # for every BlogPost instance.
    #
    # This prevents different BlogPost instances from sharing
    # the same list object.
    tags: list[str] = Field(default_factory=list)

    # ==================================================================
    # CREATION TIMESTAMP
    # ==================================================================

    # Automatically creates the current UTC timestamp when a
    # BlogPost instance is created.
    #
    # `default_factory` expects a callable.
    #
    # `partial()` creates a callable based on datetime.now()
    # while providing the timezone argument in advance.
    #
    # This:
    #
    #     partial(datetime.now, tz=UTC)
    #
    # is equivalent to:
    #
    #     lambda: datetime.now(tz=UTC)
    #
    # Therefore, every BlogPost receives its own creation timestamp.
    create_at: datetime = Field(default_factory=partial(datetime.now, tz=UTC))

    # ==================================================================
    # STATUS
    # ==================================================================

    # Literal restricts the field to a fixed set of values.
    #
    # Valid:
    #     "draft"
    #     "published"
    #     "archived"
    #
    # Invalid:
    #     "deleted"
    #     "pending"
    #     "active"
    #
    # If no status is provided, "draft" is used.
    status: Literal["draft", "published", "archived"] = "draft"


# ======================================================================
# EXAMPLES
# ======================================================================

if __name__ == "__main__":

    # ==================================================================
    # VALID BLOG POST
    # ==================================================================

    # All supplied values satisfy the validation rules.
    #
    # author_id:
    #     Integer is allowed.
    #
    # title:
    #     Between 1 and 200 characters.
    #
    # content:
    #     Contains at least 10 characters.
    #
    # slug:
    #     Contains only lowercase letters and numbers.
    #
    # view_count:
    #     Integer.
    #
    # is_published:
    #     Boolean.
    #
    # tags:
    #     List containing strings.
    #
    # status:
    #     One of the allowed Literal values.

    post = BlogPost(
        author_id=12345,
        title="Getting Started With Pydantic",
        content="This article explains the basics of Pydantic models.",
        slug="gettingstartedwithpydantic",
        view_count=100,
        is_published=True,
        tags=["python", "pydantic"],
        status="published",
    )

    print("========== VALID BLOG POST ==========")
    print(post.model_dump_json(indent=2))

    # ==================================================================
    # INVALID BLOG POST
    # ==================================================================

    # Uncomment this example to see Pydantic's ValidationError.
    #
    # This is invalid because:
    #
    # - title="" -> minimum length is 1
    # - content="Short" -> minimum length is 10
    # - slug="Getting-Started" -> uppercase letters and hyphen
    # - view_count="many" -> must be an integer
    # - is_published="yes" -> invalid boolean value
    # - tags contains 123 -> tags must contain strings
    # - status="pending" -> not an allowed Literal value

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

    # ==================================================================
    # VALID USER
    # ==================================================================

    # username:
    #     "Manjot_Bajwa_123"
    #
    # The username validator:
    # - Allows letters
    # - Allows numbers
    # - Allows underscores
    # - Converts the value to lowercase
    #
    # Stored value:
    #
    #     "manjot_bajwa_123"
    #
    # website:
    #     "example.com"
    #
    # The `mode="before"` validator converts it to:
    #
    #     "https://example.com"
    #
    # uid:
    #     Automatically generated by uuid4().
    #
    # is_influencer:
    #     Computed automatically from follower_count.
    #
    # display_name:
    #     Computed automatically from first_name and last_name.

    user = User(
        username="Manjot_Bajwa_123",
        email="manjot@example.com",
        password="MySecurePassword123",
        age=25,
        website="example.com",
        first_name="Manjot",
        last_name="Bajwa",
        follower_count=15000,
        bio="Pydantic learner",
    )

    print("\n========== VALID USER ==========")
    print(user.model_dump_json(indent=2))

    # ==================================================================
    # INVALID USER
    # ==================================================================

    # Uncomment this example to see Pydantic's ValidationError.
    #
    # This is invalid because:
    #
    # - username="ab" -> fewer than 3 characters
    # - email="not-an-email" -> invalid email format
    # - age=10 -> age must be at least 13
    # - website="not-a-url" -> not a valid HttpUrl
    #
    # The website validator adds "https://" first, but the resulting
    # value is still not a valid URL.

    # user = User(
    #     username="ab",
    #     email="not-an-email",
    #     password="MySecurePassword123",
    #     age=10,
    #     website="not-a-url",
    #     first_name="Manjot",
    #     last_name="Bajwa",
    # )

    # ==================================================================
    # VALID USER REGISTRATION
    # ==================================================================

    # Both password fields contain the same value.
    #
    # The model validator runs after field validation and confirms
    # that password and confirm_password match.

    user_reg = UserRegistration(
        email="bajwa@gmail.com",
        password="Qwerty@1",
        confirm_password="Qwerty@1",
    )

    print("\n========== VALID USER REGISTRATION ==========")
    print(user_reg.model_dump_json(indent=2))

    # ==================================================================
    # INVALID USER REGISTRATION
    # ==================================================================

    # Uncomment this example to trigger the model validator.
    #
    # The individual fields are valid, but the two passwords
    # do not match.
    #
    # The model validator raises:
    #
    #     ValueError: Passwords do not match

    # user_reg = UserRegistration(
    #     email="bajwa@gmail.com",
    #     password="Qwerty@1",
    #     confirm_password="Qwerty1",
    # )
