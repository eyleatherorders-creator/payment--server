from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

# CREATE APP FIRST
app = Flask(__name__)
CORS(app)

ICREDIT_TOKEN = os.environ.get("ICREDIT_TOKEN")


@app.route("/")
def home():
    return "Server is running"


@app.route("/create-payment", methods=["POST"])
def create_payment():
    try:
        data = request.json or {}
        print("INCOMING DATA:", data)
        print("TYPE:", type(data))

        customer = data.get("customer", {})
        items = data.get("items", [])

        # Convert your special cart structure
        formatted_items = []

        for item in items:
            if isinstance(item, list) and len(item) == 2:
                product = item[0]
                qty = item[1]

                formatted_items.append({
                    "Description": product.get("name", "Item"),
                    "Quantity": qty,
                    "UnitPrice": product.get("price", 0)
                })

        icredit_payload = {
            "GroupPrivateToken": ICREDIT_TOKEN,
            "CustomerFirstName": customer.get("firstName", "Customer"),
            "CustomerLastName": customer.get("lastName", "Guest"),
            "EmailAddress": customer.get("email", ""),
            "PhoneNumber": customer.get("phone", ""),
            "Currency": 1,
            "Items": formatted_items,
            "RedirectURL": "https://yourname.github.io/success.html",
            "FailRedirectURL": "https://yourname.github.io/fail.html",
            "IPNURL": "https://payment-server-8c4r.onrender.com/ipn",
            "IPNMethod": 1
        }

        response = requests.post(
            "https://testicredit.rivhit.co.il/API/PaymentPageRequest.svc/GetUrl",
            json=icredit_payload,
            timeout=20
        )

        print("ICREDIT RESPONSE:", response.text)

        return jsonify(response.json())

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "error": "Payment creation failed",
            "message": str(e)
        }), 500


@app.route("/ipn", methods=["POST"])
def ipn():
    print("IPN DATA:", request.json)
    return "OK", 200


