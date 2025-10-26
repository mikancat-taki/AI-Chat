import os
from flask import Flask, render_template, request, jsonify
import requests
import random
from dotenv import load_dotenv # 環境変数をロードするために再度追加

# .envファイルから環境変数を読み込む（ローカル開発用）
load_dotenv()

app = Flask(__name__)

# 環境変数からBing Search API Keyとエンドポイントを設定
BING_API_KEY = os.environ.get("BING_API_KEY")
BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search" # 例: Bing Web Search API

# APIキーがない場合は警告を出す
if not BING_API_KEY:
    print("Warning: BING_API_KEY is not set. Bing AI functionality will be limited or fail.")

# ローカルフォールバック応答を定義
def get_local_fallback_response(question):
    """
    APIが失敗した場合やキーがない場合のローカル応答
    """
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["こんにちは", "やあ"]):
        return "Bing AIに接続中…！こんにちは、星の海から応答します。"
    if any(word in question_lower for word in ["ありがとう", "感謝"]):
        return "どういたしまして！情報探索を続けます。"
    
    return random.choice([
        "Bing AIに接続できませんでした。申し訳ありませんが、もう一度質問を繰り返してください。",
        "現在、外部ネットワークとの接続が不安定です。ローカルAIの応答です。",
    ])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get('question')
    if not user_question:
        return jsonify({'error': '質問がありません'}), 400

    if not BING_API_KEY:
        # APIキーがない場合のフォールバック
        return jsonify({'answer': get_local_fallback_response(user_question)})

    # --- Bing Search APIによる応答生成 ---
    
    headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
    params = {"q": user_question, "count": 3} # 質問をクエリとして送信し、結果を3件取得
    
    try:
        response = requests.get(BING_ENDPOINT, headers=headers, params=params, timeout=5)
        response.raise_for_status() # HTTPエラーが発生した場合に例外を発生させる
        search_results = response.json()
        
        ai_answer = "検索結果に基づいた応答です：\n\n"
        
        if 'webPages' in search_results and search_results['webPages']['value']:
            # 検索結果から最も関連性の高い3つの情報を抽出
            for i, result in enumerate(search_results['webPages']['value']):
                ai_answer += f"[{i+1}] **{result.get('name', 'タイトルなし')}**:\n"
                ai_answer += f" - {result.get('snippet', '概要なし')}\n"
                # Bing AIのような流暢な応答をシミュレート
            
            ai_answer += "\nこれはBing AIによる検索結果です。詳細情報は提供されたリンクから確認してください。"
        else:
            ai_answer = get_local_fallback_response(user_question) # 検索結果がない場合はフォールバック
            
        return jsonify({'answer': ai_answer})

    except requests.exceptions.RequestException as e:
        print(f"Bing API Error: {e}")
        # API呼び出し失敗時のフォールバック
        return jsonify({'answer': get_local_fallback_response(user_question)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # 環境変数を設定していない場合は警告が出るため、デバッグモードを無効にして実行を推奨
    app.run(host='0.0.0.0', port=port, debug=False)
