import uvicorn
from fastapi import FastAPI
from app.weather_alerts_api.core.views.subscription import subscription_router

app = FastAPI()
app.include_router(subscription_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app",host='0.0.0.0', port=8080, reload=True, debug=True, workers=3)

