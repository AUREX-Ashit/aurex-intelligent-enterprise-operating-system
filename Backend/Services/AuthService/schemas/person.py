from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class PersonReferenceRequest(BaseModel):
    """
    Request to recognize an incoming reference to a person. Only exact
    matching is supported; no fuzzy, probabilistic, or AI-assisted
    matching is performed.
    """
    email: EmailStr = Field(
        ...,
        description="Incoming Person reference to recognize, supplied as an email address."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "person@corpstage.com"
            }
        }
    }


class EstablishPersonRequest(BaseModel):
    """
    Request to establish a new Person, following a prior recognition
    attempt (against the same email) that found no existing match.
    """
    email: EmailStr = Field(
        ...,
        description="The same Incoming Person reference already checked via recognition, for which no match was found."
    )
    first_name: str = Field(..., min_length=1, description="Person's first name.")
    last_name: str = Field(..., min_length=1, description="Person's last name.")
    display_name: str = Field(..., min_length=1, description="Person's display name.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "person@corpstage.com",
                "first_name": "Ashit",
                "last_name": "Padhi",
                "display_name": "Ashit Padhi"
            }
        }
    }


class AuthoritativePersonContext(BaseModel):
    """The confirmed person record returned on a match."""
    person_id: UUID = Field(..., description="Identifier of the existing, already-established person.")
    first_name: str = Field(..., description="Person's first name, as already recorded.")
    last_name: str = Field(..., description="Person's last name, as already recorded.")
    display_name: str = Field(..., description="Person's display name, as already recorded.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "person_id": "550e8400-e29b-41d4-a716-446655440000",
                "first_name": "Ashit",
                "last_name": "Padhi",
                "display_name": "Ashit Padhi"
            }
        }
    }


class PersonRecognitionOutcome(str, Enum):
    """Result of a recognition attempt."""
    # Only two outcomes are implemented. A third, candidate-matching outcome
    # (probabilistic matches requiring human confirmation, per EX-C006-04)
    # is not represented here because probabilistic matching is not
    # implemented — it is not silently folded into NO_CANDIDATE.
    MATCHED = "MATCHED"
    NO_CANDIDATE = "NO_CANDIDATE"


class PersonRecognitionResponse(BaseModel):
    """Result of a person-recognition request."""
    outcome: PersonRecognitionOutcome = Field(..., description="Recognition outcome.")
    person: AuthoritativePersonContext | None = Field(
        None,
        description="Populated only when outcome is MATCHED; null when NO_CANDIDATE."
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "outcome": "MATCHED",
                "person": {
                    "person_id": "550e8400-e29b-41d4-a716-446655440000",
                    "first_name": "Ashit",
                    "last_name": "Padhi",
                    "display_name": "Ashit Padhi"
                }
            }
        }
    }
