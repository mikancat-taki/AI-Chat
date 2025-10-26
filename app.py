import os
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# APIを使わないローカルAIの応答ロジック
def get_local_ai_response(question):
    """
    簡単なルールベースで応答を生成する関数
    """
    # 質問を小文字にして、キーワードが含まれているかチェック
    question = question.lower()
    
    # ルールベースの応答辞書
    qa_pairs = {
        "こんにちは": ["こんにちは！何かお探しですか？", "どうも！ご用件はなんでしょう？"],
        "ありがとう": ["どういたしまして！", "お役に立ててうれしいです。"],
        "名前は": ["私はこのアプリに内蔵されたAIです。", "私の名前はまだありません。"],
        "天気": ["ごめんなさい、外部の天気情報は取得できないんです。", "今日の天気は...分かりません！"],
        "おはよう": ["おはようございます！良い一日を！", "おはようございます。"],
    }
    
    # 完全に一致する質問があれば、その答えをランダムに返す
    for key, value in qa_pairs.items():
        if key in question:
            return random.choice(value)
    
    # 一致するものがなければ、デフォルトの応答を返す
    default_responses = [
        "なるほど、もう少し詳しく教えていただけますか？",
        "すみません、よく分かりませんでした。",
        f"「{question}」についてですね。興味深いです。",
        "面白い質問ですね！",
    ]
    return random.choice(default_responses)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'error': '質問がありません'}), 400

    try:
        # ローカルのAI関数を呼び出す
        ai_answer = get_local_ai_response(user_question)
        return jsonify({'answer': ai_answer})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': '応答生成中にエラーが発生しました。'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
