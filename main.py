import asyncio
import aiohttp

import streamlit as st

# your cubejs url
WS_CONN = f"ws://localhost:4000/cubejs-api/v1"

# get JWT token from security context
authorization = {
    # example token
    "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ._XEngvIuxOcA-j7y_upRUbXli4DLToNf7HxH1XNmxSc",
}

# put your query in key params
query1 = {
    "messageId": 1,  # you can set random number > 0
    "method": "subscribe",
    "params": {
        "query": {  # put your query here
            "measures": ["TicketTopicView.count"],
            "timeDimensions": [],
        },
        "queryType": "multi",
    },
}

# put your query in key params
query2 = {
    "messageId": 2,  # you can set random number > 0
    "method": "subscribe",
    "params": {
        "query": {  # put your query here
            "measures": ["TicketTopicView1s.count"],
            "timeDimensions": [],
        },
        "queryType": "multi",
    },
}


async def get_multiple_ws_url(header: st, status1: st, status2: st):
    header.write(f"url is {WS_CONN}")

    async with aiohttp.ClientSession(trust_env=True) as session:
        header.subheader(f"Connecting to websocket")
        async with session.ws_connect(WS_CONN) as websocket:
            header.subheader(f"Connected to websocket")

            # send authorization first
            header.subheader(f"Send Authorization")
            await websocket.send_json(authorization)

            # send query
            header.subheader(f"Send Query")
            await websocket.send_json(query1)
            await websocket.send_json(query2)

            # rechieve message
            header.subheader("receiving messages")
            async for message in websocket:
                data = message.json()
                if "message" in data:
                    message = data["message"]
                    if "results" in message:
                        results = message["results"]
                        if results:
                            if "data" in results[0]:
                                data = results[0]["data"]
                                if data:
                                    if "TicketTopicView1s.count" in data[0]:
                                        status1.write(data)
                                    elif "TicketTopicView.count" in data[0]:
                                        status2.write(data)


header = st.empty()
col1, col2 = st.columns(2)
asyncio.run(get_multiple_ws_url(header, col1.empty(), col2.empty()))
