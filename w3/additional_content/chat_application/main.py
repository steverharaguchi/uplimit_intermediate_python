import time

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from typing import List, Dict
from threading import Thread
import asyncio


class ConnectionManager:
    def __init__(self):
        # self.connections contains the chat room to connection mapping
        # Every chat room can contain multiple clients
        self.connections: Dict[int:List[WebSocket]] = dict()

    async def connect(self, websocket: WebSocket, room: int):
        """
        Create a connection for a client and assign it to the specified room
        """
        await websocket.accept()

        # create a chatroom if it does not exist
        if room not in self.connections:
            self.connections[room] = list()

        # Adding the client connection to a chatroom
        self.connections[room].append(websocket)

    async def broadcast(self, data: str, room: int):
        """
        Broadcast data to all the clients in the chatroom
        """
        for connection in self.connections[room]:
            await connection.send_text(data)

    async def broadcast_all(self):
        """
        Broadcast data to every connection
        """
        while True:
            for room, connections in self.connections.items():
                for connection in connections:
                    await connection.send_text('Hi. Mike testing. Mike testing')

            time.sleep(1)


app = FastAPI()
manager = ConnectionManager()

broadcast_continuous = Thread(target=asyncio.run, args=(manager.broadcast_all(),))
broadcast_continuous.start()


# The below endpoint is used to create websocket connection
@app.websocket("/ws/{room}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, room: int):
    # create a websocket connection for a client and assign it to a room
    await manager.connect(websocket, room=room)

    while True:
        data = await websocket.receive_text()
        # Broadcast message to all the connections/clients in a chatroom
        await manager.broadcast(f"Client {client_id}: {data}", room=room)


# Below endpoint renders a HTML page
@app.get("/")
async def get():
    with open('index.html', 'r') as f:
        html = f.read()

    # render a HTML page
    return HTMLResponse(html)