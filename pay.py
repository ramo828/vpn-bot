from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from settings.lang import lang as lng
from settings.setting import setting
from time import sleep
from database import Database
from html_data.pay_data import get_html
from bot import send_message_to_admin, send_message_to_user, clear_pay_message
import json

app = FastAPI()
db = Database(setting['db_filename'])
plan_name = ""
plan_month = 0

cloud_api = setting['cloud_api']
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)
telegram_id = ""
default_language = "en"

@app.get("/pay", response_class=HTMLResponse)
async def payment_page(
    amount: float = Query(..., description="Payment amount"),
    currency: str = Query("RUB", description="Currency"),
    plan: int = Query(..., description="Payment plan"),
    description: str = Query("Ödeme işlemi", description="Payment description"),
    accountId: str = Query("user@example.com", description="User account ID"),
    tg_id: int = Query(..., description="User Telegram ID"),
    invoiceId: Optional[str] = Query(None, description="Invoice ID"),
    skin: Optional[str] = Query("mini", description="Widget skin"),
    data: Optional[str] = Query("{}", description="Extra data as JSON string"),
    language: Optional[str] = Query("tr", description="Language code (az, tr, en, ru)")
):
    global telegram_id
    global default_language
    global plan_name
    global plan_month

    plan_name = "one_month" if plan == 1 else "three_months" if plan == 2 else "six_months"
    plan_month = plan
    telegram_id = str(tg_id)
    default_language = language
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError:
        data_dict = {}

    return HTMLResponse(get_html(
        amount=amount,
        currency=currency,
        plan=plan,
        description=lng[default_language]["payment"]["description"],
        accountId=accountId,
        invoiceId=invoiceId,
        skin=skin,
        data_dict=data_dict,
        language=language
    ))

@app.get("/payment_status")
async def payment_status(status: bool = Query(..., description="Payment status")):
    if status:
        print("Payment was successful")
        db.update_vpn_access(1, telegram_id)
        db.set_user_plan(plan_month, telegram_id)
        send_message_to_user(int(telegram_id), lng[default_language]["payment"]["pay_success_message"]+ " " +plan_name)
        sleep(5)
        send_message_to_admin(f"Payment was successful for user: {telegram_id}")
        clear_pay_message()
        return JSONResponse({"message": lng[default_language]["payment"]["pay_success_message"]+" "+plan_name, "success": True})
    else:
        db.update_vpn_access(0, telegram_id)
        print("Payment failed")
        send_message_to_user(int(telegram_id), lng[default_language]["payment"]["pay_error_message"])
        sleep(5)
        send_message_to_admin(f"Payment failed for user: {telegram_id}")
        return JSONResponse({"message": lng[default_language]["payment"]["pay_error_message"], "success": False})
