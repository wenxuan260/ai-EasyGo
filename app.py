from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json

app = Flask(__name__)

# 获取 OpenAI API Key
client = OpenAI(api_key=os.getenv("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"))

@app.route("/analyze_trip", methods=["POST"])
def analyze_trip():
    try:
        # 接收纯文本输入
        text = request.data.decode("utf-8").strip()
        if not text:
            return jsonify({"error": "No text provided"}), 400

        prompt = f"""
从下面的出差描述中提取以下字段，并用 JSON 返回：
- 起始地
- 目的地
- 行驶距离
- 行驶时长
- 驾驶时间（日期时间）

示例描述：
{text}

请返回格式如下：
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
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
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



