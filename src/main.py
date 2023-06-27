import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.modules.collection_points import collection_points_router
from src.modules.rewards import rewards_router
from src.modules.auth import auth_router, user_router
from src.modules.trash_collected import trash_collected_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(rewards_router, prefix="/rewards")
app.include_router(collection_points_router, prefix="/collection_points")
app.include_router(trash_collected_router, prefix="/trash_collected")
app.include_router(auth_router, prefix="/auth")
app.include_router(user_router, prefix="/user")

@app.get("/")
async def health_check():
    return {
        "Status":"OK",
        "Message":"Access /docs to more information"    
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
