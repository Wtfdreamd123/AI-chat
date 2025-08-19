from fastapi import FastAPI, APIRouter
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import routes
from chat_routes import chat_router

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="AI Coder Backend", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Database dependency
async def get_database():
    return db

# Health check endpoint
@api_router.get("/")
async def root():
    return {"message": "AI Coder Backend is running!", "status": "healthy"}

@api_router.get("/health")
async def health_check():
    try:
        # Test database connection
        await db.list_collection_names()
        return {"status": "healthy", "database": "connected", "ai_service": "ready"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

# Include chat router
api_router.include_router(chat_router)

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("AI Coder Backend starting up...")
    logger.info(f"Database: {os.environ['DB_NAME']}")
    logger.info("AI Service initialized with Emergent LLM Key")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    logger.info("AI Coder Backend shut down")