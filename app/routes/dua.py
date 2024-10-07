from fastapi import Request, APIRouter
from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from app.utils.prompt import stream_dua


router = APIRouter()

@router.get("/dua")
async def get_dua(request: Request):
    query = request.query_params.get('query')
    if not query:
        return {"error": "Query parameter is required. Example: /dua?query=anger"}
    
    return StreamingResponse(stream_dua(query), media_type="text/event-stream")