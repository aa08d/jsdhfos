import yookassa

from uuid import uuid4

yookassa.Configuration.account_id = "1128275"
yookassa.Configuration.secret_key = "live_708KMTGISD5OyFut8yZrwSvB2TaRgMjG1S__UuXPgOI"


def create(amount, days) -> yookassa.Payment:
    payment_id = str(uuid4())
    payment = yookassa.Payment.create(
        {
            "amount": {
                "value": amount,
                "currency": "RUB",
            },
            "payment_method_data": {
                "type": "bank_card",
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://t.me/GadVPNBot"
            },
            "capture": True,
            "metadata": {
                "days": days
            },
            "description": "Оплата товаров и услуг"
        },
        payment_id,
    )

    return payment.confirmation.confirmation_url, payment.id
