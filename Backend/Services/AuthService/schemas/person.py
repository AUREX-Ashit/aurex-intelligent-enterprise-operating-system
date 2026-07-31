from datetime import datetime
from enum import Enum
from typing import Literal
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


# ---------------------------------------------------------------------------
# BA-03 — Understand Authoritative Person Context (EX-C006-03)
# ---------------------------------------------------------------------------

class PersonUnderstandingContext(BaseModel):
    """
    Privacy-respecting, provenance-aware view of a Person's authoritative
    context (EX-C006-03). Surfaces only boolean cross-capability existence
    signals — never Identity's or Membership's own data, per PE-001-C006's
    own Out-of-Scope boundary (§1.4).
    """
    person_id: UUID
    first_name: str
    last_name: str
    display_name: str
    is_active: bool
    has_identity: bool = Field(..., description="Whether at least one Identity (C-001) exists for this Person — existence signal only, never Identity's own data.")
    has_active_membership: bool = Field(..., description="Whether at least one active Membership (C-007) exists for this Person — existence signal only, never Membership's own data.")

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BA-04 — Distinguish Candidate Person Matches (EX-C006-04)
# ---------------------------------------------------------------------------

class PersonDistinctionDecisionType(str, Enum):
    SELECTED_EXISTING = "SELECTED_EXISTING"
    NEW_PERSON = "NEW_PERSON"


class DistinguishPersonRequest(BaseModel):
    """
    Governed human confirmation resolving a Candidate Person Context to
    exactly one Authoritative Person Context, or an explicit new-Person
    decision (EX-C006-04). Applies identically whether candidate_person_ids
    contains one entry or several, per the Recognition Authority Rule
    (PE-001-C006 §1.7) — no confidence-based auto-selection exists.
    """
    candidate_person_ids: list[UUID] = Field(..., min_length=1, description="The candidate set under consideration — one or more Person IDs.")
    decision_type: PersonDistinctionDecisionType = Field(..., description="SELECTED_EXISTING confirms one candidate; NEW_PERSON declares none of the candidates match.")
    selected_person_id: UUID | None = Field(None, description="Required when decision_type is SELECTED_EXISTING; SHALL be one of candidate_person_ids.")
    rationale: str = Field(..., min_length=1, description="Why this candidate was selected, or why none were (BR-C006-003).")

    model_config = {
        "json_schema_extra": {
            "example": {
                "candidate_person_ids": ["550e8400-e29b-41d4-a716-446655440000"],
                "decision_type": "SELECTED_EXISTING",
                "selected_person_id": "550e8400-e29b-41d4-a716-446655440000",
                "rationale": "Matching email domain and full legal name confirmed by Person Steward.",
            }
        }
    }


class PersonDistinctionDecisionResponse(BaseModel):
    """EX-C006-04's outcome: a resolved Authoritative Person Context, or an explicit new-Person decision — never a merely probable one."""
    id: UUID
    candidate_person_ids: list[UUID]
    decision_type: PersonDistinctionDecisionType
    selected_person_id: UUID | None
    rationale: str
    decided_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BA-05 — Resolve Conflicting Person Context (EX-C006-05)
# ---------------------------------------------------------------------------

class PersonConflictClassification(str, Enum):
    AMBIGUITY = "AMBIGUITY"
    CORRECTION_NEEDED = "CORRECTION_NEEDED"


class ResolvePersonConflictRequest(BaseModel):
    """
    Classifies a conflict between incoming and authoritative Person
    context as an ambiguity (wrong person identified) or a correction
    need (right person, wrong fact) — BR-C006-004. Classification is
    always an explicit human decision (AI SHALL NOT resolve the conflict
    itself, PE-001-C006 §5.7); this endpoint records and routes an
    already-made classification, it does not compute one.
    """
    conflicting_reference: str = Field(..., min_length=1, description="The incoming information that conflicts with the current Authoritative Person Context.")
    classification: PersonConflictClassification = Field(..., description="Human-made classification of the conflict.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "conflicting_reference": "Incoming reference states a different last name for the same email.",
                "classification": "CORRECTION_NEEDED",
            }
        }
    }


class PersonConflictClassificationResponse(BaseModel):
    """EX-C006-05's outcome: a routed ambiguity or a routed correction need — never resolved through the same path."""
    person_id: UUID
    classification: PersonConflictClassification
    routed_to: str = Field(..., description="EX-C006-04 (Distinguish) for AMBIGUITY, or EX-C006-07 (Correct) for CORRECTION_NEEDED.")

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BA-06 — Review Potential Duplicate Person Indication (EX-C006-06)
# ---------------------------------------------------------------------------

class PersonReconciliationOutcome(str, Enum):
    CONFIRMED_DUPLICATE = "CONFIRMED_DUPLICATE"
    CONFIRMED_DISTINCT = "CONFIRMED_DISTINCT"
    ESCALATED = "ESCALATED"


class ReconcilePersonRequest(BaseModel):
    """
    Records a governed Reconciliation Decision for two Person contexts
    suspected of representing the same human (EX-C006-06). Never a
    silent merge — technical consolidation following a confirmed
    duplicate is a downstream data-governance action outside this
    Enterprise Experience's own scope (PE-001-C006 §5.3).
    """
    person_id_a: UUID
    person_id_b: UUID
    decision: PersonReconciliationOutcome
    rationale: str = Field(..., min_length=1)

    model_config = {
        "json_schema_extra": {
            "example": {
                "person_id_a": "550e8400-e29b-41d4-a716-446655440000",
                "person_id_b": "660e8400-e29b-41d4-a716-446655440001",
                "decision": "CONFIRMED_DISTINCT",
                "rationale": "Different dates of birth confirmed via authoritative source.",
            }
        }
    }


class PersonReconciliationDecisionResponse(BaseModel):
    id: UUID
    person_id_a: UUID
    person_id_b: UUID
    decision: PersonReconciliationOutcome
    rationale: str
    reviewed_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BA-07 — Correct Person Context (EX-C006-07)
# ---------------------------------------------------------------------------

class CorrectPersonRequest(BaseModel):
    """Corrects an inaccurate authoritative Person fact while preserving the prior value (BR-C006-006)."""
    field_name: Literal["first_name", "last_name", "display_name"]
    corrected_value: str = Field(..., min_length=1)
    reason: str = Field(..., min_length=1)
    approval_reference: str | None = Field(None, max_length=255)

    model_config = {
        "json_schema_extra": {
            "example": {
                "field_name": "last_name",
                "corrected_value": "Padhi-Rao",
                "reason": "Legal name change confirmed via updated identification document.",
            }
        }
    }


class PersonCorrectionResponse(BaseModel):
    """EX-C006-07's outcome: the corrected fact is authoritative; the prior value remains visible as superseded, not deleted."""
    correction_id: UUID
    person: AuthoritativePersonContext
    field_name: str
    prior_value: str
    corrected_value: str
    corrected_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BA-08 — Enrich Person Context (EX-C006-08)
# ---------------------------------------------------------------------------

class PersonEnrichmentSensitivity(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class EnrichPersonRequest(BaseModel):
    """Adds legitimate new detail to a Person's authoritative context, additive only (BR-C006-007)."""
    attribute_name: str = Field(..., min_length=1, max_length=255)
    attribute_value: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1, max_length=255, description="Attributable provenance — required.")
    sensitivity_classification: PersonEnrichmentSensitivity

    model_config = {
        "json_schema_extra": {
            "example": {
                "attribute_name": "preferred_pronoun",
                "attribute_value": "they/them",
                "source": "Self-reported during onboarding collaboration.",
                "sensitivity_classification": "INTERNAL",
            }
        }
    }


class PersonEnrichmentResponse(BaseModel):
    id: UUID
    person_id: UUID
    attribute_name: str
    attribute_value: str
    source: str
    sensitivity_classification: PersonEnrichmentSensitivity
    accepted_at: datetime

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# BA-09 / BA-10 — Hand Off Person Context to Identity / Membership
# (EX-C006-10 / EX-C006-11)
# ---------------------------------------------------------------------------

class PersonHandoffOutcomeType(str, Enum):
    ACCEPTED = "ACCEPTED"
    RETURNED = "RETURNED"


class PersonHandoffRequest(BaseModel):
    """
    Records the caller-reported outcome of a Person-context hand-off to a
    dependent capability (EX-C006-10/11). C-006 never calls into the
    dependent capability's own API (Contract 5.8) — the caller (acting on
    behalf of Identity Management or Membership Management) reports
    whether the hand-off was accepted or returned, mirroring WP-02
    BA-10's own already-accepted hand-off precedent.
    """
    outcome: PersonHandoffOutcomeType
    reason: str | None = Field(None, description="Required context when outcome is RETURNED — e.g. insufficient Person context to proceed.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "outcome": "ACCEPTED",
            }
        }
    }


class PersonHandoffOutcome(BaseModel):
    """EX-C006-10/11's outcome: an explicit accepted-or-returned Hand-off Outcome; the underlying Person context is always preserved unchanged."""
    person_id: UUID
    target_capability: Literal["C-001", "C-007"]
    outcome: PersonHandoffOutcomeType
    reason: str | None

    model_config = {"from_attributes": True}
