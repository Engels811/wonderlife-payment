from flask import Flask
from webhooks.stripe_webhook import stripe_bp
from webhooks.tebex_webhook import tebex_bp

app = Flask(__name__)
app.register_blueprint(stripe_bp)
app.register_blueprint(tebex_bp)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
