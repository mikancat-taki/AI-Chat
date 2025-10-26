import os
from flask import Flask, render_template, request, jsonify
import random
import re

app = Flask(__name__)

# APIを使わないローカルAIの応答ロジック
def get_local_ai_response(question):
    """
    ルールベースで応答を生成する関数を強化
    """
    question_lower = question.lower()
    
    # --- 1. 特定のキーワードに対する応答 ---
    # 挨拶
    if any(word in question_lower for word in ["こんにちは", "やあ", "どうも"]):
        return random.choice(["こんにちは！星の海へようこそ。", "どうも！何か面白い話はありますか？"])
    if any(word in question_lower for word in ["ありがとう", "感謝"]):
        return random.choice(["どういたしまして！", "お役に立てて光栄です。", "こちらこそ！"])
    # 自己紹介
    if any(word in question_lower for word in ["名前は", "あなたは誰", "自己紹介"]):
        return random.choice(["私はこのアプリの星空を旅するAIです。", "名もなき航海士、といったところでしょうか。"])
    # 天気
    if "天気" in question_lower:
        return "残念ながら、この宇宙船からは地球の天気は観測できないんです…。"
    # ユーモア
    if any(word in question_lower for word in ["面白い話", "ジョーク", "笑わせて"]):
        return random.choice([
            "宇宙人がレストランに入って一言。「この店の雰囲気、惑星一だね！」",
            "布団が吹っ飛んだ、の宇宙バージョンは「ブラックホールがホワイトホールに吸い込まれた」です。",
        ])
    # 雑学
    if any(word in question_lower for word in ["雑学", "豆知識", "教えて"]):
        return random.choice([
            "宇宙空間は完全に無音だって知ってましたか？音を伝える空気がないからです。",
            "木星の巨大な嵐「大赤斑」は、地球が丸ごと2〜3個入るほどの大きさなんですよ。",
            "光の速さは秒速約30万kmですが、それでも太陽から地球まで約8分19秒かかります。"
        ])

    # --- 2. パターンマッチングによる簡易計算 ---
    # 例: 「5たす3は？」「12 x 5 = ?」
    match = re.search(r'(\d+)\s*([\+\-\*\/]|たす|ひく|かける|わる)\s*(\d+)', question_lower)
    if match:
        num1 = int(match.group(1))
        op = match.group(2)
        num2 = int(match.group(3))
        
        try:
            if op in ['+', 'たす']:
                return f"計算しますね。答えは {num1 + num2} です。"
            if op in ['-', 'ひく']:
                return f"えーっと…たしか {num1 - num2} ですね。"
            if op in ['*', 'かける']:
                return f"暗算します… {num1 * num2} でしょうか。"
            if op in ['/', 'わる']:
                if num2 == 0:
                    return "ゼロで割ることは、宇宙の法則で禁じられているんです！"
                return f"答えは {num1 / num2} です。"
        except Exception:
            return "うーん、難しい計算はちょっと苦手かもしれません…。"

    # --- 3. デフォルトの応答 ---
    default_responses = [
        "なるほど…宇宙の神秘のようですね。",
        "もう少し詳しく教えてもらえますか？",
        f"「{question}」についてですね。興味深いです。",
        "それは、まるで未知の惑星を発見した時のような驚きです！",
        "すみません、ワームホールを通過中でよく聞き取れませんでした。",
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
        ai_answer = get_local_ai_response(user_question)
        return jsonify({'answer': ai_answer})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': '応答生成中にエラーが発生しました。'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
