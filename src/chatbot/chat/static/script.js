// This is script.js

document.addEventListener('DOMContentLoaded', function() {
    const inputBox = document.querySelector('.input-box input');
    const sendButton = document.querySelector('.send-button');

    function sendMessage(message) {
        console.log("sendMessage called with message:", message);
        if (message.trim() === '') {
            return; // Do nothing if the message is empty
        }

        addMessageToChat('user', message);

        const postData = new FormData();
        postData.append('message', message);

        fetch('/aichat/chatbot_response/', {
            method: 'POST',
            body: postData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Data received from server:", data);
            addMessageToChat('bot', data.message);
        })
        .catch(error => console.error('Error:', error));
    }

    function addMessageToChat(sender, message) {
        const chatArea = document.querySelector('.chat-area');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = message;
        console.log("Appending message:", message);
        chatArea.appendChild(messageDiv);

        chatArea.scrollTop = chatArea.scrollHeight;
    }

    sendButton.addEventListener('click', function() {
        sendMessage(inputBox.value);
        inputBox.value = '';
    });

    inputBox.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            sendMessage(inputBox.value);
            inputBox.value = '';
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
