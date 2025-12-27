import stripe, os
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def stripe_link(discord_id, product, price):
    session = stripe.checkout.Session.create(
        payment_method_types=["card","klarna","sofort"],
        mode="payment",
        line_items=[{
            "price_data":{
                "currency":"eur",
                "product_data":{"name":product},
                "unit_amount":price
            },
            "quantity":1
        }],
        metadata={"discord_id":discord_id},
        success_url="https://wonderlife-network.eu/success",
        cancel_url="https://wonderlife-network.eu/cancel"
    )
    return session.url
