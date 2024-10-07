from fastapi import APIRouter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.utils.prompt import get_dua_for_prayer
from app.utils.notifications import send_notification_to_all_users

router = APIRouter()

scheduler = AsyncIOScheduler()

prayer_times = {
    "Fajr": "05:00",
    "Dhuhr": "12:30",
    "Asr": "15:45",
    "Maghrib": "18:00",
    "Isha": "20:00",
}

async def recommend_dua(prayer_name: str):
    # Get the Dua for the specified prayer from LLM
    dua = await get_dua_for_prayer(prayer_name)
    
    # Log the Dua for debugging
    print(f"Sending notification for {prayer_name}: {dua}")

    # Send notification to all subscribed users
    await send_notification_to_all_users(prayer_name, dua)

def schedule_prayer_jobs():
    # Schedule jobs for each prayer time
    for prayer, time_str in prayer_times.items():
        hour, minute = map(int, time_str.split(":"))
        scheduler.add_job(recommend_dua, "cron", hour=hour, minute=minute, args=[prayer])

# Start the scheduler when FastAPI app starts
@router.on_event("startup")
async def startup_event():
    schedule_prayer_jobs()
    scheduler.start()
