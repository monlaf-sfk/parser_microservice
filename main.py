# main.py
from fastapi import FastAPI
from broker import broker_obj
from taskiq import TaskiqDepends
from tasks import parse_website_task
from taskiq_redis.exceptions import ResultIsMissingError
app = FastAPI()


@app.on_event("startup")
async def startup():
    await broker_obj.startup()


@app.on_event("shutdown")
async def shutdown():
    await broker_obj.shutdown()


@app.post("/parse")
async def start_parsing(url: str):
    task = await parse_website_task.kiq(url)

    return {"task_id": task.task_id, "message": "Parsing started"}


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    try:
        task_result = await broker_obj.result_backend.get_result(task_id)

        if not task_result:
            return {"status": "processing"}

        return {"status": "ready", "data": task_result.return_value}
    except ResultIsMissingError:
        return {"status": "not found"}