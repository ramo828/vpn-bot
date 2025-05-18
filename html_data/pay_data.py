from settings.setting import setting
from settings.lang import lang as lng
import json
from utility.util import start_telebit,LANG_MAPPING

cloud_api = setting['cloud_api']

# HTML yaradan Python funksiyası
# Daha oxunaqlı və modern dizayn üçün dəyişənlər ayrıca təyin edildi və şərhlər Azərbaycan türkcəsindədir

def get_html(amount, currency, description, accountId, invoiceId, skin, data_dict, language):
    # Telebit vasitəsilə əldə olunan ictimai (public) URL
    public_url = start_telebit()

    # Lokalizasiya üçün dinamiki mətni dəyişənlərə yazırıq
    title = lng[language]['payment']['title']
    pay_button = lng[language]['payment']['button']
    amount_label = lng[language]['payment']['amount']
    success_msg = lng[language]['payment']['pay_success_message']
    error_msg = lng[language]['payment']['pay_error_message']
    widget_lang = LANG_MAPPING.get(language, 'en-US')
    data_json   = json.dumps(data_dict)    # JSON formatında əlavə məlumat

    # HTML şablonu
    html_template = f"""
<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <script src="https://widget.cloudpayments.ru/bundles/cloudpayments.js"></script>
    <style>
        /* Əsas qüsursuz font və rəng palitrası */
        :root {{
            --primary: #4CAF50;
            --primary-dark: #45a049;
            --bg: #fafafa;
            --card-bg: #ffffff;
            --text-color: #333333;
            --radius: 12px;
            --shadow: 0 8px 20px rgba(0,0,0,0.1);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: var(--bg);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .card {{
            background: var(--card-bg);
            padding: 2rem;
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            max-width: 400px;
            width: 90%;
            text-align: center;
        }}
        .card h2 {{
            color: var(--text-color);
            font-size: 1.75rem;
            margin-bottom: 1rem;
        }}
        .card p {{
            color: var(--text-color);
            margin: 0.5rem 0;
            font-size: 1rem;
        }}
        #payBtn {{
            margin-top: 1.5rem;
            background: var(--primary);
            color: #fff;
            border: none;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            border-radius: var(--radius);
            cursor: pointer;
            transition: background 0.3s ease;
        }}
        #payBtn:hover {{
            background: var(--primary-dark);
        }}
    </style>
</head>
<body>
    <script>Telegram.WebApp.ready();</script>
    <div class="card">
        <h2>{title}</h2>
        <p>{description}</p>
        <p><strong>{amount_label}:</strong> {amount} {currency}</p>
        <button id="payBtn">{pay_button}</button>
    </div>

    <script>
        /* Ödəniş düyməsinə klik edildikdə CloudPayments widget-ını çağırır */
        (function() {{
            const payBtn = document.getElementById('payBtn');
            payBtn.addEventListener('click', () => {{
                const widget = new cp.CloudPayments({{ language: "{widget_lang}", cultureName: "{widget_lang}"}});
                widget.pay('charge', {{
                    publicId: '{cloud_api}',  // Public API açarı
                    description: `{description}`,  // Ödəniş təsviri
                    amount: {amount},               // Məbləğ
                    currency: '{currency}',        // Valyuta
                    accountId: '{accountId}',      // Hesab ID
                    invoiceId: '{invoiceId}',      // Faktura ID
                    skin: '{skin}',                // Widget görünüşü
                    data: {data_json}              // Əlavə JSON məlumat
                }}, {{
                    onSuccess: () => alert('{success_msg}'),  // Uğurlu ödəniş mesajı
                    onFail: () => alert('{error_msg}'),       // Uğursuz ödəniş mesajı
                    onComplete: (paymentResult) => {{
                        const status = paymentResult.success;
                        // Serverə status-u göndərir
                        fetch(`{public_url}/payment_status?status=${{status}}`)
                            .then(res => res.json())
                            .then(data => console.log('Server cavabı:', data))
                            .catch(err => console.error('Xəta:', err));

                        // Telegram WebApp-ə məlumat göndərib pəncərəni bağlayır
                        Telegram.WebApp.sendData(
                            JSON.stringify({{ status, invoiceId: '{invoiceId}' }}),
                            () => Telegram.WebApp.close()
                        );
                       setTimeout(() => Telegram.WebApp.close(), 2000);
                    }}
                }});
            }});
        }})();
    </script>
</body>
</html>
"""

    return html_template
