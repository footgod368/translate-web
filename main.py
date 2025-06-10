import os
from flask import Flask, send_file, jsonify, request
import logging
from logging.handlers import RotatingFileHandler
from src.translate import Word
from src.auto_complete import auto_complete
from src.database import init_db, log_query, get_today_query_count
from src.gpt import get_chat_response

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


@app.route('/synonyms')
def synonyms():
    word = request.args.get('word', '')
    system_prompt = (
        "你是一个专业的英语老师，你需要帮用户分析单词的同近义词。"
    )
    user_prompt = (
        f"请用中文详细分析单词{word}的同近义词，每个同近义词包含：\n"
        "1. 核心含义（不超过15字）\n"
        "2. 典型例句（中英对照）\n"
        "3. 与原词的主要差异\n"
        "格式要求：使用Markdown无序列表和代码块排版\n"
        "注意排除原词本身\n"
    )
    gpt_response = get_chat_response(system_prompt, user_prompt)
    app.logger.debug(f"GPT响应: {gpt_response}")
    return jsonify({'synonyms': gpt_response})


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
