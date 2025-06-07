import os
from flask import Flask, send_file, jsonify, request
import logging
from logging.handlers import RotatingFileHandler
from src.translate import Word
from src.auto_complete import auto_complete
from src.database import init_db, log_query, get_today_query_count

app = Flask(__name__, static_folder="static")


def load_words():
    try:
        with open(app.root_path + "/static/words", "r") as file:
            words = [line.strip().lower() for line in file if line.strip()]
            app.logger.info(f"成功加载 {len(words)} 个单词")
            return words  # 添加返回值
    except Exception as e:
        app.logger.error(f"单词文件加载失败: {str(e)}")
        return []


app.config["all_eng_words"] = load_words()  # 在app.run前加载
app.config["enable_autocomplete"] = True
app.config["database_file"] = app.root_path + "/db/query_history.db"
init_db(app.config["database_file"])


@app.route("/")
def index():
    return send_file("static/index.html")


@app.route("/test")
def test():
    return "Hello World"


@app.route("/translate")
def translate():
    word = request.args.get("text", "")
    log_query(app.config["database_file"],word, request.remote_addr, request.user_agent.string)
    word_instance = Word(word)
    return jsonify(word_instance.result())


@app.route("/autocomplete")
def autocomplete():
    prefix = request.args.get("prefix", "").lower()
    suggestions = auto_complete(prefix, app.config["all_eng_words"])
    return jsonify(suggestions)


@app.route("/ducksay")
def ducksay():
    count = get_today_query_count(app.config["database_file"])
    message = f"今天小鸭学习了 {count} 个单词" if count > 0 else "嘎嘎，小鸭今天什么都没学"
    return jsonify(
        {
            "message": message,
        }
    )


def init_logging():
    handler = RotatingFileHandler(
        filename="app.log",
        maxBytes=1024 * 1024 * 5,  # 5MB
        backupCount=3,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)


def main():
    init_logging()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


if __name__ == "__main__":
    main()
