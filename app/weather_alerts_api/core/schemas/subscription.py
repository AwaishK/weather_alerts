from typing import Optional, Any
from fastapi_utils.api_model import APIModel


class SubscriptionNew(APIModel):
    email: str
    city_id: str
    state_id: Optional[str]
    country_id: Optional[str]
    conditions: Any
    is_active: Optional[bool]


class SubscriptionExisting(SubscriptionNew):
    id: Optional[int]
