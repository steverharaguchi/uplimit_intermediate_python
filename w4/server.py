from w4.logger_config import server_logger
from fastapi import FastAPI, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
from threading import Thread
import asyncio
from starlette.websockets import WebSocket
from w4.utils.websocket import ConnectionManager
from w2.utils.response_model import ProcessStatus
from w2.utils.database import DB

app = FastAPI()
manager = ConnectionManager()

# start an asynchronous task that will keep broadcasting the process status to all the connected clients
broadcast_continuous = Thread(target=asyncio.run, args=(manager.broadcast_all(),))
broadcast_continuous.start()


# The below endpoint is used to create websocket connection
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # create a websocket connection for a client and assign it to a room
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            # Broadcast message to all the connections/clients in a chatroom
            await websocket.send_text(f"Websocket connection established Connected")

    except WebSocketDisconnect:
        server_logger.warning("Client disconnected")


# health check API
@app.get("/health")
async def get():
    server_logger.info("`/health` API called")
    return {"status": "ok"}


# Below endpoint renders an HTML page
@app.get("/home")
async def get():
    server_logger.info("`/home` API called")

    with open('index.html', 'r') as f:
        html = f.read()

    # render a HTML page
    return HTMLResponse(html)


# Below endpoint to get the initial data
@app.get("/processes")
async def get() -> List[ProcessStatus]:
    server_logger.info("`/processes` API called")

    db = DB()
    processes = db.read_all()

    return [
        ProcessStatus(process_id=process['process_id'], file_name=process['file_name'],
                      file_path=process['file_path'], description=process['description'],
                      start_time=process['start_time'], end_time=process['end_time'], percentage=process['percentage'])
        for process in processes]
