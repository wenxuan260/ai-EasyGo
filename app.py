from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 设置你的 OpenAI API Key
openai.api_key = os.getenv("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")  # 可改为 openai.api_key = "你的key"

@app.route("/analyze_trip", methods=["POST"])
def analyze_trip():
    try:
        data = request.get_json()
        text = data.get("text")

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

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        result = response['choices'][0]['message']['content']

        # 尝试把返回字符串转为 JSON 对象
        import json
        try:
            structured_data = json.loads(result)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse OpenAI response", "raw": result}), 500

        return jsonify(structured_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
