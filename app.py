from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# templatesフォルダ内のindex.htmlをレンダリングする
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # 簡単な応答ロジックの例
    user_question = request.json.get('question')
    if user_question:
        # ここにAIの応答を生成する処理を実装します
        # 例: "「" + user_question + "」についてですね。調べてみます。"
        ai_answer = f"「{user_question}」についてですね。調べてみます。"
        return jsonify({'answer': ai_answer})
    return jsonify({'error': '質問がありません'}), 400

if __name__ == '__main__':
    # 環境変数からポート番号を取得。なければ5000を使う。
    port = int(os.environ.get('PORT', 5000))
    # デバッグモードは開発環境でのみ有効にするのが望ましい
    app.run(host='0.0.0.0', port=port, debug=True)
