from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json

app = Flask(__name__)

# 获取 OpenAI API Key
print(os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/analyze_trip", methods=["POST"])
def analyze_trip():
    try:
        # 接收纯文本输入
        text = request.data.decode("utf-8").strip()
        if not text:
            return jsonify({"error": "No text provided"}), 400

        prompt = f"""
你将从一段高德地图足迹 OCR 文本中提取以下字段：

1. 起始地（start_location）：文本中**倒数第四行**
2. 目的地（end_location）：文本中**倒数第三行**
3. 行驶距离（distance）：单位为 km，例如 "16.7 km"
4. 行驶时长（duration）：例如 "00:26:48"
5. 驾驶时间（start_time）：通常在文本顶部，格式为 yyyy.MM.dd HH:mm，例如 "2025.03.08 13:08"

输入示例：
{text}

请直接返回以下 JSON 格式（不要包含任何解释说明，不要使用 Markdown 标记）：

{{
  "start_location": "",
  "end_location": "",
  "distance": "",
  "duration": "",
  "start_time": ""
}}
"""



        # 使用新版本 openai SDK 的调用方式
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
 

        result = response.choices[0].message.content

        # 解析 JSON 格式
        try:
            structured_data = json.loads(result)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse OpenAI response", "raw": result}), 500

        return jsonify(structured_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 启动 Flask 服务，绑定 0.0.0.0 以支持外部访问
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



