"""XApprove API Models."""

from pydantic import Field

from pythonxbox.common.models import CamelCaseModel

class TimeDuration(CamelCaseModel):
    """
    Represents a duration or a specific time point, often used for allowance or interval times.
    """
    days: int
    hour: int
    minute: int


class AllowedInterval(CamelCaseModel):
    """
    Defines a time range (begin and end) within a day.
    """
    begin: TimeDuration
    end: TimeDuration

class DailyRestriction(CamelCaseModel):
    """
    Defines the restrictions and allowances for a single day of the week.
    """
    day_of_week: int
    allowance: TimeDuration
    allowed_intervals: list[AllowedInterval]

class TimeRestrictions(CamelCaseModel):
    """
    Defines the Screen Time Configuration for a user's Xbox account.

    This model represents the full payload from the /settings/screentime endpoint, 
    encompassing the overall enablement status, global rule flag, and a list of 
    detailed Daily Restriction rules, including total play time allowance and 
    specific permitted time intervals for each day of the week.
    """
    is_enabled: bool
    is_global: bool
    daily_restrictions: list[DailyRestriction]
    exception_expired_time: str | None = None

class OrderItem(CamelCaseModel):
    """
    Represents a single historical transaction or purchase record.
    """
    total_amount: float
    total_amount_formatted: str
    timestamp: str
    display_order_id: str
    payment_method: str
    item_title: str
    publisher_name: str
    logo_image_url: str
    item_type: str
    order_item_state: str
    quantity: int
    product_id: str
    item_id: str

class SpendingHistoryResponse(CamelCaseModel):
    """
    The root model for the user's spending history.

    This model represents the complete order and transaction history for a 
    user's account from the /spending/history endpoint, including a list of 
    individual purchases (OrderHistory) and an overall status flag for 
    activity reporting (isActivityReportingEnabled).
    """
    order_history: list[OrderItem]
    is_activity_reporting_enabled: bool

class AccountBalanceItem(CamelCaseModel):
    """
    Represents a single currency balance in a user's account.
    """
    balance: float
    localized_balance: str
    country_code: str
    # currencyCode is often null/missing if the balance is zero or not configured
    currency_code: str | None = None

class AccountBalancesResponse(CamelCaseModel):
    """
    The root model for the user's account balances.

    This model represents the full payload from the /spending/account-balances 
    endpoint, detailing the current monetary balances available to the user, 
    the target user's XUID, and their configured market.
    """
    balances: list[AccountBalanceItem]
    target_xuid: int
    target_currently_set_msa_market: str

class DeviceModel(CamelCaseModel):
    """
    Represents a specific device associated with the user's account and screen time data.
    """
    device_id: str
    device_name: str
    device_class: str
    device_form_factor: str
    os_name: str
    os_version: str

class ScreenTimeEvent(CamelCaseModel):
    """
    Represents an individual screen time usage event, aggregated by date and device.
    """
    device_id: str
    date: str  # Represents the start date/time of the usage period
    time_used: str # Time duration string (e.g., "05:58:00")

class DailyScreenTimeEvent(CamelCaseModel):
    """
    Represents the total screen time usage for a single day, regardless of the device.
    """
    date: str  # Represents the start date of the day
    # timeUsed is Optional because it is omitted for days with 0 usage
    time_used: str | None = Field(default=None, alias="timeUsed")

class ScreenTimeUsageReport(CamelCaseModel):
    """
    The root model for the user's Screen Time Usage Activity Report.

    This model represents the full payload from the /activityreport/screenTimeUsage 
    endpoint, detailing device information, specific screen time events by device, 
    daily aggregated usage, and the status of activity reporting.
    """
    devices: list[DeviceModel]
    screen_time_events: list[ScreenTimeEvent]
    daily_screen_time_events: list[DailyScreenTimeEvent]
    is_activity_reporting_enabled: bool

class IconUri(CamelCaseModel):
    """
    Represents a URI for an application's icon and its specified dimensions.
    """
    uri: str
    width: int

class ApplicationMetadata(CamelCaseModel):
    """
    Metadata for a specific application/game, used to map app IDs to names and icons.
    """
    app_id: str
    icon_uris: list[IconUri]
    display_name: str

class DailyUsageEntry(CamelCaseModel):
    """
    Represents the usage time of a specific application/game on a single day.
    """
    date: str
    day_of_week: str
    usage: str # Time duration string (e.g., "00:11:00")

class AppUsage(CamelCaseModel):
    """
    Aggregates the daily usage entries for one specific application/game.
    """
    app_id: str
    daily_application_usage: list[DailyUsageEntry]

class DeviceSummary(CamelCaseModel):
    """
    Provides a summary of a device used in the report.
    """
    device_id: str
    device_class: str

class DailyAppUsageReport(CamelCaseModel):
    """
    The root model for the user's Daily Application Usage Activity Report.
    """
    app_usage: list[AppUsage]
    devices: list[DeviceSummary]
    applications: list[ApplicationMetadata]
    is_activity_reporting_enabled: bool

class SocialPerson(CamelCaseModel):
    """
    Represents a single user in a social list (friend, follower, or following).
    """
    xuid: int
    added_date: str # Timestamp of when the relationship was established

class PeopleListResponse(CamelCaseModel):
    """
    The root model for the user's social network lists.

    This model represents the full payload from the /people/following endpoint, 
    containing separate lists for users the target user is following, users who are 
    friends, and users who are followers.
    """
    following_list: list[SocialPerson]
    friends_list: list[SocialPerson]
    followers_list: list[SocialPerson]

class OverrideItem(CamelCaseModel):
    """
    Represents an active screen time override rule.
    Maps to an element in the "overrides" array.
    """
    override_type: int
    target: int | None = None # Assuming 'target' is an int if present, but null in the example
    applies_to: list[int]
    valid_until: str # ISO 8601 timestamp for when the override expires
    last_modified: str # ISO 8601 timestamp for when the override was created/modified

class ScreenTimeOverridesResponse(CamelCaseModel):
    """
    The root model for the user's Screen Time Overrides configuration and list.

    This model represents the full payload from the /settings/screentime/overrides 
    endpoint, detailing the supported actions for creating/canceling overrides, 
    and a list of all currently active or pending screen time override rules.
    """
    actions: dict # untyped dict as we're not sure what these actually represent yet.
    overrides: list[OverrideItem]
