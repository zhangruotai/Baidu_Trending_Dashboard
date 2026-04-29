from flask import Flask, jsonify
from flask_cors import CORS

from db_config import DB_CONFIG
from MySQL_Helper import MySQLHelper


app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "Flask成功运行"


@app.route("/api/trending", methods=["GET"])
def get_trending():
    try:
        db = MySQLHelper(**DB_CONFIG)

        sql = """
            SELECT 
                ranking,
                title,
                hot_index,
                DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at
            FROM baidu_trending
            ORDER BY ranking ASC
            LIMIT 50
        """

        data = db.query_all(sql)

        return jsonify({
            "success": True,
            "count": len(data),
            "data": data
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })



if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)