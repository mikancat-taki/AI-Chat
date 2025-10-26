import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# 環境変数からOpenAI APIキーを設定
# render.comなどのホスティングサービスでは、環境変数設定画面でキーを設定します
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'error': '質問がありません'}), 400

    try:
        # OpenAI APIを呼び出して応答を生成
        completion = client.chat.completions.create(
            model="gpt-4o",  # 最新のモデルなどを指定
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_question}
            ]
        )
        ai_answer = completion.choices[0].message.content
        return jsonify({'answer': ai_answer})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'AIの応答生成中にエラーが発生しました。'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) # 本番を想定しDebugはFalseに
