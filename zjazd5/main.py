from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory database for users
users = [
    {"id": 1, "name": "Jan Kowalski", "email": "jan@kowalski.pl"},
    {"id": 2, "name": "Anna Nowak", "email": "anna@nowak.pl"}
]

# GET /users
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# GET /users/{id}
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

# POST /users
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

# PUT /users/{id}
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user.update({"name": data["name"], "email": data["email"]})
    return jsonify(user), 200

# DELETE /users/{id}
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
