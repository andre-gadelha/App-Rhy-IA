const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const loadingIndicator = document.getElementById('loading-indicator');

async function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;

    appendMessage(message, 'user-message');
    userInput.value = '';
    loadingIndicator.style.display = 'block';
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        appendMessage(data.response, 'gemini-message');
    } catch (error) {
        console.error('Erro ao enviar mensagem:', error);
        appendMessage("Desculpe, houve um erro ao conectar com a IA.", 'gemini-message');
    } finally {
        loadingIndicator.style.display = 'none';
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

function appendMessage(text, className) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', className);
    messageDiv.textContent = text;
    chatBox.appendChild(messageDiv);
}

userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});
