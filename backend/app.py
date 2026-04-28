from flask import Flask, jsonify # 导入Flask框架，jsonify把Python数据转换成JSON返回给前端
from flask_cors import CORS      # 允许前端React跨域访问Flask后端
import pymysql                   # 导入MySQL连接库
from db_config import DB_CONFIG  # 导入MySQL数据库连接配置

app = Flask(__name__) # 创建Flask后端应用
CORS(app) #开启跨域访问，使React前端可以请求Flask接口
app.json.ensure_ascii = False   # 让JSON返回中文，不显示中文对应的Unicode编码
app.json.sort_keys = False      # 保持返回字段顺序，不自动排序

# 定义数据库连接函数
def get_connection():
    return pymysql.connect(**DB_CONFIG)

# 定义首页接口，测试Flask是否正常启动
@app.route("/")
def home():
    return "Flask成功运行"

# 定义后端API接口
@app.route("/api/trending", methods=["GET"]) # 前端会请求 http://localhost:5001/api/trending 网址获得数据
def get_trending():
    connection = get_connection() # 连接MySQL数据库

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT ranking,
                title,
                hot_index,
                DATE_FORMAT(created_at, '%Y-%m-%d %H:%i:%s') AS created_at # 时间格式化成字符串
                FROM baidu_trending
                ORDER BY ranking ASC
                LIMIT 50
            """
            cursor.execute(sql)
            data = cursor.fetchall()
        
        # 把查询结果返回给前端
        return jsonify({
            "success": True,
            "count": len(data),
            "data": data
        })

    # 数据库连接或查询出错，返回错误信息
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

    # 关闭数据库连接
    finally:
        connection.close()


@app.route("/api/refresh", methods=["POST"])
def refresh_trending():
    try:
        # 这里导入你的爬虫类
        from Baidu_Trending_Spider import ensure_database, BaiduTrendingSpider
        from MySQL_Helper import MySQLHelper

        ensure_database()

        db = MySQLHelper(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="zzm123456",
            database="spider_db"
        )

        spider = BaiduTrendingSpider(db)
        spider.run()

        return get_trending()

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)