from flask import Flask, request, jsonify
import base64

app = Flask(__name__)

# Sample user information
sample_user = {
    "user_id": "john_doe_17091999",
    "email": "john@xyz.com",
    "roll_number": "ABCD123"
}

# Function to validate the file
def validate_file(file_b64):
    if not file_b64:
        return {
            "file_valid": False,
            "file_mime_type": None,
            "file_size_kb": None
        }

    try:
        # Decode Base64 string
        file_data = base64.b64decode(file_b64)
        file_size_kb = len(file_data) / 1024  # Get file size in KB
        file_mime_type = "image/png"  # Assuming it's a PNG file (adjust logic if needed)

        return {
            "file_valid": True,
            "file_mime_type": file_mime_type,
            "file_size_kb": round(file_size_kb, 2)
        }
    except Exception as e:
        return {
            "file_valid": False,
            "file_mime_type": None,
            "file_size_kb": None
        }

# Function to process the input data
def process_data(data):
    numbers = []
    alphabets = []
    highest_lowercase_alphabet = None

    for item in data:
        if item.isdigit():
            numbers.append(item)
        elif item.isalpha():
            alphabets.append(item)
            # Find highest lowercase alphabet
            if item.islower() and (highest_lowercase_alphabet is None or item > highest_lowercase_alphabet):
                highest_lowercase_alphabet = item

    return {
        "numbers": numbers,
        "alphabets": alphabets,
        "highest_lowercase_alphabet": [highest_lowercase_alphabet] if highest_lowercase_alphabet else []
    }

# POST endpoint to process the data
@app.route('/bfhl', methods=['POST'])
def handle_post():
    try:
        # Get JSON data from the request
        data = request.json.get('data')
        file_b64 = request.json.get('file_b64')

        if not data or not isinstance(data, list):
            return jsonify({
                "is_success": False,
                "message": "Invalid data format"
            }), 400

        # Process the data
        processed_data = process_data(data)
        file_info = validate_file(file_b64)

        # Create response
        response = {
            "is_success": True,
            "user_id": sample_user["user_id"],
            "email": sample_user["email"],
            "roll_number": sample_user["roll_number"],
            "numbers": processed_data["numbers"],
            "alphabets": processed_data["alphabets"],
            "highest_lowercase_alphabet": processed_data["highest_lowercase_alphabet"],
            "file_valid": file_info["file_valid"],
            "file_mime_type": file_info["file_mime_type"],
            "file_size_kb": file_info["file_size_kb"]
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "is_success": False,
            "message": str(e)
        }), 500

# GET endpoint to return operation code
@app.route('/bfhl', methods=['GET'])
def handle_get():
    return jsonify({
        "operation_code": 1
    }), 200

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
