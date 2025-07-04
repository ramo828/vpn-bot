from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from settings.lang import lang as lng
from settings.setting import setting
from time import sleep
from database import Database
from html_data.pay_data import get_html
from html_data.contract import generate_privacy_policy
from bot import send_message_to_admin, send_message_to_user, clear_pay_message
from vpn_api import VPN

import json
vpn = VPN()
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
    accountId: str = Query("ece64bcf1a4611c4c7ef03f308981f33", description="Payment account ID"),
    tg_id: int = Query(..., description="User Telegram ID"),
    invoiceId: Optional[str] = Query(None, description="Invoice ID"),
    skin: Optional[str] = Query("mini", description="Widget skin"),
    data: Optional[str] = Query("{}", description="Extra data as JSON string"),
    language: Optional[str] = Query("en", description="Language code (az, tr, en, ru)")
):
    global telegram_id
    global default_language
    global plan_name
    global plan_month
    plan_name = "one_month" if plan == 1 else "three_months" if plan == 2 else "six_months" if plan == 6 else "one_year"
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
        description=description,
        accountId=accountId,
        invoiceId=invoiceId,
        skin=skin,
        data_dict=data_dict,
        language=language
    ))


@app.get("/contract", response_class=HTMLResponse)
async def contract_page(
        email: str = Query("example@example.com", description="User email"),
        site: str = Query("https://example.com", description="Site URL"),
        bot_url: str = Query("https://t.me/example_bot", description="Bot URL"),

):

    return HTMLResponse(generate_privacy_policy(
        email=email,
        site_url=site,
        bot_url=bot_url
    ))

@app.get("/payment_status")
async def payment_status(status: bool = Query(..., description="Payment status")):
    payment_lang = db.get_user_language(telegram_id)
    if status:
        print("Get month: , ",plan_month)
        print("Payment was successful")
        db.update_vpn_access(1, telegram_id)
        db.set_user_plan(plan=plan_month, telegram_id=telegram_id)
        vpn.json_data = {"name": str(telegram_id)}
        vpn_data = vpn.create_key()
        db.update_vpn_status(
                        telegram_id=telegram_id,
                        vpn_server=vpn_data.get("accessUrl"),
                        vpn_id=vpn_data.get("id")
                    )
        send_message_to_user(int(telegram_id), lng[payment_lang]["payment"]["pay_success_message"]+ " " +plan_name)
        sleep(1/3)
        send_message_to_user(int(telegram_id), vpn_data["accessUrl"])
        sleep(5)
        send_message_to_admin(f"Payment was successful for user: {telegram_id}")
        # success_callback(telegram_id=telegram_id, month=plan_month)
        return JSONResponse({"message": lng[payment_lang]["payment"]["pay_success_message"]+" "+plan_name, "success": True})
    else:
        db.update_vpn_access(0, telegram_id)
        clear_pay_message()
        print("Payment failed")
        send_message_to_user(int(telegram_id), lng[payment_lang]["payment"]["pay_error_message"])
        sleep(5)
        send_message_to_admin(f"Payment failed for user: {telegram_id}")
        return JSONResponse({"message": lng[payment_lang]["payment"]["pay_error_message"], "success": False})
