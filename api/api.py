from flask import Flask, jsonify, request
from scraper import scrape_betr
from calculation import calculate_percentage

app = Flask(__name__)

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
    
    data = calculate_percentage(LAST_FILE)
    return jsonify({"status": "success", "data": data, "message": f"File {file.filename} uploaded successfully."})

@app.route("/get_calculations", methods=["GET"])
def refresh():
    if not LAST_FILE:
        return jsonify({"status": "error", "message": "No file uploaded yet."}), 400
    data = calculate_percentage(LAST_FILE)
    return jsonify({"status": "success", "data": data, "message": "Data refreshed successfully."})
    

if __name__ == '__main__':
    app.run(debug=True)