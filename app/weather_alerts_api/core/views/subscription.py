"""
"""
from re import I
from typing import Optional, List

from fastapi import HTTPException, Depends

from starlette.status import HTTP_404_NOT_FOUND
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.api_model import APIMessage
from starlette.responses import Response
from sqlalchemy.exc import IntegrityError
from app.weather_alerts_api.core.models.database import SessionLocal
from app.weather_alerts_api.core.models.subscription import Subscription as ModelSubscription
from app.weather_alerts_api.core.schemas.subscription import SubscriptionNew, SubscriptionExisting

subscription_router = InferringRouter()


def get_subscription(subscription_id, session: SessionLocal) -> SubscriptionExisting:
    subscription_new: Optional[ModelSubscription] = session.query(ModelSubscription).get(subscription_id)
    if subscription_new is None:
        raise HTTPException(detail=f'subscription_id: {subscription_id} does not exist', status_code=HTTP_404_NOT_FOUND)
    
    return subscription_new

def get_session():
    return SessionLocal()


@cbv(subscription_router)
class Subscriptions:

    session: SessionLocal = Depends(get_session)

    @subscription_router.post("/subscription")
    def create(self, subscription: SubscriptionNew) -> SubscriptionExisting:
        subscription_new = ModelSubscription(
            email=subscription.email, 
            city_id=subscription.city_id,
            state_id=subscription.state_id,
            country_id=subscription.country_id,
            conditions=subscription.conditions,
            is_active=subscription.is_active
        )

        self.session.add(subscription_new)
        try:
            self.session.commit()
        except IntegrityError as e:
            return Response(f"{str(e.orig)}", status_code=500)
        return SubscriptionExisting.from_orm(subscription_new)

    @subscription_router.get("/subscription/{subscription_id}")
    def read(self, subscription_id: str) -> SubscriptionExisting:
        subscription_new = get_subscription(subscription_id=subscription_id, session=self.session)
        return SubscriptionExisting.from_orm(subscription_new)
    
    @subscription_router.get("/subscriptions")
    def list(self) -> List[SubscriptionExisting]:
        subscriptions: Optional[ModelSubscription] = self.session.query(ModelSubscription).all()
        subscriptions = [SubscriptionExisting.from_orm(s) for s in subscriptions]
        return subscriptions

    @subscription_router.delete("/subscription/{subscription_id}")
    def delete(self, subscription_id: str) -> APIMessage:
        subscription_new = get_subscription(subscription_id=subscription_id, session=self.session)
        self.session.delete(subscription_new)
        try:
            self.session.commit()
        except IntegrityError as e:
            return Response(f"{str(e.orig)}", status_code=500)
        return APIMessage(detail=f"Deleted subscription {subscription_new}")

    @subscription_router.put("/subscription/{subscription_id}")
    def update(self, subscription_id, subscription: SubscriptionNew) -> SubscriptionExisting:
        subscription_new = get_subscription(subscription_id=subscription_id, session=self.session)
        subscription_new.email=subscription.email
        subscription_new.city_id=subscription.city_id
        subscription_new.state_id=subscription.state_id
        subscription_new.country_id=subscription.country_id
        subscription_new.conditions=subscription.conditions
        subscription_new.is_active=subscription.is_active
        self.session.add(subscription_new)
        try:
            self.session.commit()
        except IntegrityError as e:
            return Response(f"{str(e.orig)}", status_code=500)
        return SubscriptionExisting.from_orm(subscription_new)
