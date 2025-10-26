document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatLog = document.getElementById('chat-log');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // フォームのデフォルトの送信動作をキャンセル

        const question = userInput.value.trim();
        if (!question) return;

        // ユーザーの質問をチャットログに追加
        appendMessage('user', question);
        userInput.value = ''; // 入力欄をクリア

        try {
            // バックエンドのAPIに質問を送信
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            if (!response.ok) {
                throw new Error('ネットワークの応答が正しくありませんでした。');
            }

            const data = await response.json();
            // AIの回答をチャットログに追加
            appendMessage('ai', data.answer);

        } catch (error) {
            console.error('エラー:', error);
            appendMessage('ai', '申し訳ありません、エラーが発生しました。');
        }
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight; // 自動でスクロール
    }
});
