from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

RAKUTEN_API_KEY = "1079908094230273280"  # ←ご自身の楽天APIキーを入力
AFFILIATE_ID = "05de2d98.53ab4c56.05de2d99.e6237a71"

@app.route("/api/get_hotel_details", methods=["GET"])
def get_hotel_details():
    hotel_nos = request.args.getlist("hotelNo")
    if not hotel_nos:
        return jsonify({"error": "No hotelNo provided"}), 400

    results = []
    for hotel_no in hotel_nos[:5]:
        url = "https://app.rakuten.co.jp/services/api/Travel/HotelDetailSearch/20170426"
        params = {
            "applicationId": RAKUTEN_API_KEY,
            "affiliateId": AFFILIATE_ID,
            "hotelNo": hotel_no,
            "format": "json"
        }
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            if data.get("hotel"):
                results.append(data["hotel"][0]["hotelBasicInfo"])

    return jsonify({"hotels": results})

handler = app  # ←Vercelで必要な設定
