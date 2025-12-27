import stripe, os

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_stripe_subscription(
    customer_id: str,
    price_id: str,
    discord_id: int,
    product_name: str
):
    return stripe.Subscription.create(
        customer=customer_id,
        items=[{"price": price_id}],
        metadata={
            "discord_id": discord_id,
            "product": product_name
        }
    )
