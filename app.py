from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

ICREDIT_TOKEN = os.environ.get("ICREDIT_TOKEN")

@app.route("/")
def home():
    return "Server is running"

@app.route("/create-payment", methods=["POST"])
def create_payment():

    data = request.json
    customer = data.get("customer")
    items = data.get("items")

    icredit_payload = {
        "GroupPrivateToken": ICREDIT_TOKEN,
        "CustomerFirstName": customer.get("firstName"),
        "CustomerLastName": customer.get("lastName"),
        "EmailAddress": customer.get("email"),
        "PhoneNumber": customer.get("phone"),
        "Currency": 1,
        "Items": [
            {
                "Description": item["name"],
                "Quantity": item["qty"],
                "UnitPrice": item["price"]
            }
            for item in items
        ],
        "RedirectURL": "https://yourname.github.io/success.html",
        "FailRedirectURL": "https://yourname.github.io/fail.html",
        "IPNURL": "https://your-render-url.onrender.com/ipn",
        "IPNMethod": 1
    }

    response = requests.post(
        "https://testicredit.rivhit.co.il/API/PaymentPageRequest.svc/GetUrl",
        json=icredit_payload
    )

    return jsonify(response.json())

@app.route("/ipn", methods=["POST"])
def ipn():
    print("IPN DATA:", request.json)

    return "OK", 200
if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
