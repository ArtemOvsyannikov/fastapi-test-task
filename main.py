from fastapi import FastAPI
from pydantic import BaseModel
from time import monotonic
import asyncio
import uvicorn

class TestResponse(BaseModel):
    elapsed: float  

app = FastAPI()

semaphore = asyncio.Semaphore(1)

async def work() -> None:
    async with semaphore: 
        await asyncio.sleep(3)

@app.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    ts1 = monotonic() 
    await work()  
    ts2 = monotonic()
    return TestResponse(elapsed=ts2 - ts1) 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)