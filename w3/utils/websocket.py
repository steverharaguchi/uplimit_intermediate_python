from typing import List
from starlette.websockets import WebSocket, WebSocketState
import time
from w2.utils.database import DB


class ConnectionManager:
    def __init__(self):
        # self.connections contains the chat room to connection mapping
        # Every chat room can contain multiple clients
        self.connections: List[WebSocket] = []
        self.db = DB()

    async def connect(self, websocket: WebSocket):
        """
        Create a connection and add it to the connections list
        """
        await websocket.accept()

        # Adding the client connection
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        """
        Broadcast data to all the clients
        """
        for connection in self.connections:
            await connection.send_text(data)

    async def broadcast_all(self):
        """
        Broadcast data to every connection
        """
        while True:
            try:
                for connection in self.connections:
                    if (connection.application_state == WebSocketState.CONNECTED and
                            connection.client_state == WebSocketState.CONNECTED):
                        processes = self.db.read_all()
                        await connection.send_json(processes)

                time.sleep(1)

            except Exception as e:
                print(e)
