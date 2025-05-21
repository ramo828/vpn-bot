class PartnerModel:
    def __init__(self, name:str, url:str, description:str):
        self.name = name
        self.url = url
        self.description = description
partners = [
    PartnerModel(name = "BotFather", url="https://t.me/BotFather", description= "Bot Maker bot"),
    PartnerModel(name = "ID Finder", url="https://t.me/Information_id_bot", description= "Telegram İD Finder"),
    PartnerModel(name = "New Number Bot", url="https://t.me/new_number_v5_bot", description= "Number Diller extension bot")
]

partner_lang = {
    "az": {
        "contact_message": "Partnerlik üçün əlaqə saxlayın!",
        "question":"Bizimlə partner olmaq istəyərsən?",
        "contact": "@ramo828"
    },
    "tr": {
        "contact_message":"Ortaklık için iletişime geçin!",
        "question":"Bizimle ortak olmak ister misiniz?",
        "contact": "@ramo828"
    },
    "ru": {
        "contact_message":"Свяжитесь для партнерства!",
        "question":"Хотите стать нашим партнером?",
        "contact": "@ramo828"
    },
     "en": {
        "contact_message":"Contact us for partnership!",
        "question":"Would you like to become our partner?",
        "contact": "@ramo828"
    }
}