import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from models.message import Message, Messages
from models.report import Report
from models.usage import UsageItem, UsageResponse
from utils.credits import calculate_credits

app = FastAPI()

# Configure CORS with multiple origins
origins = ["http://localhost:3000", "https://pilgrim.isv.ee"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create FastAPI instance with custom docs and openapi url
app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

# Sample queries remain the same
SAMPLE_QUERIES = [
    ("Who were the main directors of the French New Wave movement?", None),
    ("Generate a comprehensive report on World War II Pacific Theatre battles", 5392),
    ("What were the innovative techniques used in Citizen Kane?", None),
    ("Create a detailed report on Ancient Egyptian dynasties", 1124),
    ("How did the Industrial Revolution impact European society?", None),
    ("What were the major technological advances in early cinema?", None),
    ("Generate a report on the Rise and Fall of the Roman Empire", 8806),
    ("Which films won both Best Picture and Best Director Oscars in the 1970s?", None),
    ("What were the key events leading to the American Revolution?", None),
    ("How did Studio System in Hollywood work during its Golden Age?", None),
    ("Explain the significance of the Byzantine Empire", None),
    ("What made Alfred Hitchcock's filming techniques revolutionary?", None),
    ("How did the Renaissance change European art and culture?", None),
    ("What was the impact of sound on early cinema?", 3345),
    ("Who were the key figures in the Civil Rights Movement?", None),
]


@app.get("/api/v1/users/{user_id}/messages", response_model=dict)
async def get_user_messages(user_id: int):
    if user_id not in [1, 2, 3]:
        raise HTTPException(status_code=404, detail="User not found")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    messages = []
    message_id = 1000
    num_messages = random.randint(20, 30)

    for _ in range(num_messages):
        random_timestamp = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        query, report_id = random.choice(SAMPLE_QUERIES)
        message = {
            "id": message_id,
            "text": query,
            "timestamp": random_timestamp.isoformat() + "Z",
        }
        if report_id:
            message["report_id"] = report_id
        messages.append(message)
        message_id += 1

    messages.sort(key=lambda x: x["timestamp"])
    return {"messages": messages}


@app.get("/api/v1/messages/{user_id}/current", response_model=Messages)
async def get_current_period_messages(user_id: int):
    response = await get_user_messages(user_id)
    messages = [Message(**msg) for msg in response["messages"]]
    return Messages(messages=messages)


@app.get("/api/v1/reports/{report_id}", response_model=Report)
async def get_report(report_id: int):
    report_data = {
        3345: {"id": 3345, "name": "Discounted Demo Report", "credit_cost": 1.0},
        5392: {"id": 5392, "name": "Customised Usage Report", "credit_cost": 5.0},
        8806: {
            "id": 8806,
            "name": "Fully Constructed Report",
            "credit_cost": 4.0,
        },
        1124: {"id": 1124, "name": "Short Report", "credit_cost": 3.0},
    }

    if report_id not in report_data:
        raise HTTPException(status_code=404, detail="Report not found")

    return Report(**report_data[report_id])


@app.get("/api/v1/users/{user_id}/usage", response_model=UsageResponse)
async def get_usage(user_id: int):
    if user_id not in [1, 2, 3]:
        raise HTTPException(status_code=404, detail="User not found")

    messages = (await get_current_period_messages(user_id)).messages
    usage = []

    for message in messages:
        usage_item = UsageItem(
            message_id=message.id,
            timestamp=message.timestamp.isoformat(),
            credits_used=0,
        )

        if message.report_id:
            try:
                report = await get_report(message.report_id)
                usage_item.report_name = report.name
                usage_item.credits_used = report.credit_cost
            except HTTPException:
                usage_item.credits_used = calculate_credits(message.text)[
                    "credits_used"
                ]
        else:
            usage_item.credits_used = calculate_credits(message.text)["credits_used"]

        usage.append(usage_item)

    return UsageResponse(usage=usage)
