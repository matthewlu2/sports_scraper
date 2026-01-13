from flask import Flask, jsonify, request
from scraper import scrape_betr
from calculation import calculate_percentage

app = Flask(__name__)

TEAMS_LIST = []
LAST_FILE = ""
SECONDARY_FILE = None

@app.route('/scrape_betr', methods=['GET'])
def scrape_betr_route():
    try:
        data = scrape_betr()
        return jsonify(
            {
                "status": "success",
                "data": data
            }
        )
    except Exception as e:
        return jsonify(
            {
                "status": "error",
                "message": str(e)
            }
        ), 500
    
@app.route("/upload", methods=["POST"])
def upload_route():
    global LAST_FILE
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "No selected file"}), 400
    
    LAST_FILE = f"./uploads/{file.filename}"
    file.save(LAST_FILE)

    return jsonify({"status": "success", "message": f"File {file.filename} uploaded successfully."})

@app.route("/upload_secondary", methods=["POST"])
def upload_secondary_route():
    global SECONDARY_FILE
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"status": "error", "message": "No selected file"}), 400

    SECONDARY_FILE = f"./uploads/{file.filename}"
    file.save(SECONDARY_FILE)

    return jsonify({"status": "success", "message": f"File {file.filename} uploaded successfully."})

@app.route("/get_calculations", methods=["GET"])
def get_calculations():
    if not LAST_FILE:
        return jsonify({"status": "error", "message": "No file uploaded yet."}), 400
    data = calculate_percentage(LAST_FILE, TEAMS_LIST, SECONDARY_FILE)
    return jsonify({"status": "success", "data": data, "message": "Data refreshed successfully."})

@app.route("/update_teams", methods=["POST"])
def update_teams():
    global TEAMS_LIST
    TEAMS_LIST = request.json.get("selected_teams", [])
    return jsonify({"status": "success", "message": "Teams updated successfully."})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
