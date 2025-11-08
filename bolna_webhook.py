from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.post("/bolna-webhook")
def bolna_webhook():
    # Get the JSON payload sent by Bolna
    data = request.get_json()

    # Log the entire payload for debugging
    print("Received webhook:")
    print(json.dumps(data, indent=2))

    # Extract key fields
    call_id = data.get("id")
    status = data.get("status")
    extracted_data = data.get("extracted_data", {})
    transcript = data.get("transcript", "")
    telephony_data = data.get("telephony_data", {})

    # Example: print specific values
    print(f"\nCall ID: {call_id}")
    print(f"Status: {status}")
    print(f"Extracted Data: {json.dumps(extracted_data, indent=2)}")

    # TODO: Save to database if needed
    # Example pseudo-code:
    # save_to_db(call_id, status, extracted_data, transcript, telephony_data)

    # Send 200 OK so Bolna knows it was received
    return jsonify({"message": "Webhook received successfully"}), 200


if __name__ == "__main__":
    # Run the server on port 3000
    app.run(host="0.0.0.0", port=3000)
