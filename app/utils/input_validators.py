from flask import jsonify

def validate_user_input(data: dict, required_keys):
  if not data:
    return jsonify({"error": "Request body is required"}), 400

  missing_keys = []
  for key in required_keys:
    if key not in data:
      missing_keys.append(key)

  if missing_keys:
    return jsonify({"error": f"Missing required fields: {', '.join(missing_keys)}"}), 400

  return None