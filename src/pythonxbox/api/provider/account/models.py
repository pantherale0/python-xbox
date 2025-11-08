from enum import Enum

from pythonxbox.common.models import CamelCaseModel


class ClaimGamertagResult(Enum):
    NotAvailable = 409
    Available = 200


class ChangeGamertagResult(Enum):
    ChangeSuccessful = 200
    NoFreeChangesAvailable = 1020

class GamertagInfo(CamelCaseModel):
    """
    Detailed breakdown of a modern Xbox Gamertag.
    """
    gamertag: str
    gamertag_suffix: str
    classic_gamertag: str
    composed_gamertag: str

class ContentException(CamelCaseModel):
    """
    Represents a parental control exception (Allow/Block) for a specific title or application.
    """
    action: str  # e.g., "Allow" or "Block"
    app_id: str
    id: str
    content_id: str
    content_type: str  # e.g., "Game" or "Application"
    country_code: str | None = None
    display_name: str
    icon: str | None = None # Field is null in the example
    ratings: list[str] # A list of strings, each being "RATING_BOARD:RATING"

class FamilyMemberSettings(CamelCaseModel):
    """
    The root model for the user's Family Safety Settings and Profile.

    GET /family/memberXuid({xuid})/users/{user_id}

    This model represents the full payload from the family member settings endpoint, 
    detailing personal info, content restrictions, and parental control configurations
    for a child user in the family group.
    """
    user_id: str
    email: str
    first_name: str
    last_name: str
    image_url: str
    gamertag: GamertagInfo
    xuid: str
    role: str  # e.g., "Child"
    can_view_restricted_content: bool
    can_view_tv_adult_content: bool
    activity_reporting: bool
    content_exceptions: list[ContentException]
    maturity_level: int
    web_filtering_level: str  # e.g., "OnlineCommunication"
    web_filtering_exceptions: list[str] # Empty list in example, assumed to be List[str]
    allow_purchase_and_downloads: str  # e.g., "FreeAndPaid"
    restrict_promotional_content: bool
    date_of_birth: str
    cid: str
    age_group: str  # "Child" or "Adult"
    msa_locale: str
    msa_country_code: str

class FamilyGroupResponse(CamelCaseModel):
    """
    The root model for the user's Xbox Family Group.

    GET /family/memberXuid({xuid})

    This model represents the full payload from the family group endpoint, 
    detailing the unique family ID, a list of all current family members 
    (FamilyMemberSettings) with their complete profile and safety settings, and 
    any pending member invitations.
    """
    family_id: str
    family_users: list[FamilyMemberSettings]
    # 'pendingMembers' is an empty list in the sample,
    # so we model it as a list of un-typed dictionaries.
    pending_members: list[dict]
