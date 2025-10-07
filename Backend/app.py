from flask import Flask, request, jsonify, send_from_directory
from database import init_db, get_goals, add_goal, delete_goal
import os

app = Flask(__name__)

# ----------- Serve Frontend -----------
@app.route("/")
def home():
    return send_from_directory("../Frontend", "index.html")

@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory("../Frontend", filename)

# ----------- API Endpoints -----------
@app.route("/api/goals", methods=["GET"])
def api_get_goals():
    """Fetch all goals from PostgreSQL"""
    try:
        goals = get_goals()
        return jsonify(goals)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/goals", methods=["POST"])
def api_add_goal():
    """Add a new goal"""
    try:
        data = request.json
        goal_text = data.get("goal")
        if goal_text:
            add_goal(goal_text)
            return jsonify({"message": "Goal added!"}), 201
        return jsonify({"error": "Goal text required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/goals/<int:goal_id>", methods=["DELETE"])
def api_delete_goal(goal_id):
    """Delete a goal by ID"""
    try:
        delete_goal(goal_id)
        return jsonify({"message": f"Goal {goal_id} deleted!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------- Run -----------
if __name__ == "__main__":
    try:
        init_db()  # Ensure DB and table are initialized
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        print(f"❌ Failed to initialize app: {e}")