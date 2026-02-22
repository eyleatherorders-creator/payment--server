@app.route("/create-payment", methods=["POST"])
def create_payment():

    try:
        data = request.json or {}

        customer = data.get("customer", {})
        items = data.get("items", [])

        icredit_payload = {
            "GroupPrivateToken": ICREDIT_TOKEN,
            "CustomerFirstName": customer.get("firstName", "Customer"),
            "CustomerLastName": customer.get("lastName", "Guest"),
            "EmailAddress": customer.get("email", ""),
            "PhoneNumber": customer.get("phone", ""),
            "Currency": 1,
            "Items": [
                {
                    "Description": item.get("name", "Item"),
                    "Quantity": item.get("qty", 1),
                    "UnitPrice": item.get("price", 0)
                }
                for item in items
            ],
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

        return jsonify(response.json())

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "error": "Payment creation failed",
            "message": str(e)
        }), 500
