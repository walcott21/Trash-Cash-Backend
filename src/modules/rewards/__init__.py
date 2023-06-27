from fastapi import APIRouter
from src.modules.rewards.repository import create_reward, read_rewards, update_reward, delete_reward
from src.common.models.rewards import Reward

rewards_router = APIRouter(tags=["Rewards"])

@rewards_router.post("/create")
async def create_reward_controller(reward: Reward):
    result = await create_reward(reward)
    if result:
        return 201
    return 400

@rewards_router.get("/read", response_model=list[Reward])
async def read_rewards_controller(name:str|None = None,id:str|None = None):
    result =  await read_rewards(name,id)
    return result

@rewards_router.patch("/update")
async def update_reward_controller(updated_reward: Reward):
    result = await update_reward(updated_reward)
    if result:
        return 201
    return 400

@rewards_router.delete("/delete/{id}")
async def delete_reward_controller(id:str):
    await delete_reward(id)
    return 202