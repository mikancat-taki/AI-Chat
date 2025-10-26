document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatLog = document.getElementById('chat-log');
    const sendButton = form.querySelector('button');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const question = userInput.value.trim();
        if (!question) return;

        appendMessage('user', question);
        userInput.value = '';
        sendButton.disabled = true;

        // ローディング表示を追加
        const loadingElement = appendMessage('ai', '考え中...', true);

        try {
            const response = await fetch('/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'ネットワークエラー');
            }

            const data = await response.json();
            // ローディング表示をAIの回答に更新
            loadingElement.textContent = data.answer;

        } catch (error) {
            console.error('エラー:', error);
            loadingElement.textContent = `申し訳ありません、エラーが発生しました: ${error.message}`;
            loadingElement.style.color = 'red';
        } finally {
            sendButton.disabled = false;
            chatLog.scrollTop = chatLog.scrollHeight;
        }
    });

    function appendMessage(sender, message, isLoading = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        messageElement.textContent = message;

        if (isLoading) {
            messageElement.classList.add('loading-indicator');
        }

        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
        return messageElement; // 要素を返す
    }
});
