from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from typing import Optional
import json

app = FastAPI()

@app.get("/pay", response_class=HTMLResponse)
async def payment_page(
    amount: float = Query(..., description="Payment amount"),
    currency: str = Query("RUB", description="Currency"),
    description: str = Query("Ödeme işlemi", description="Payment description"),
    accountId: str = Query("user@example.com", description="User account ID"),
    invoiceId: Optional[str] = Query(None, description="Invoice ID"),
    skin: Optional[str] = Query("mini", description="Widget skin"),
    data: Optional[str] = Query("{}", description="Extra data as JSON string")
):
    try:
        data_dict = json.loads(data)
    except json.JSONDecodeError:
        data_dict = {}

    html_content = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>Ödeme Sayfası</title>
        <script src="https://widget.cloudpayments.ru/bundles/cloudpayments.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #f9f9f9;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            button {{
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 15px 30px;
                font-size: 18px;
                border-radius: 8px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Ödeme İşlemi</h2>
            <p>{description}</p>
            <p>Tutar: {amount} {currency}</p>
            <button onclick="pay()">Öde</button>
        </div>

        <script>
        function pay() {{
            var widget = new cp.CloudPayments();
            widget.charge({{
                publicId: 'test_api_00000000000000000000001',
                description: '{description}',
                amount: {amount},
                currency: '{currency}',
                accountId: '{accountId}',
                invoiceId: '{invoiceId or ""}',
                skin: '{skin}',
                data: {json.dumps(data_dict)}
            }},
            {{
                onSuccess: function (options) {{
                    alert('Ödeme başarılı');
                }},
                onFail: function (reason, options) {{
                    alert('Ödeme başarısız');
                }}
            }});
        }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
