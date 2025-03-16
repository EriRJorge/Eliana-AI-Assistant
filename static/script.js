document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatHistory = document.getElementById('chatHistory');
    const sendButton = document.getElementById('sendButton');
    const suggestionButtons = document.querySelectorAll('.suggestion-btn');
    const clearChatButton = document.getElementById('clearChat');
    
    // Initialize timestamp for the welcome message
    updateInitialTimestamp();
    
    // Add event listeners
    chatForm.addEventListener('submit', handleSubmit);
    userInput.addEventListener('keypress', handleTyping);
    clearChatButton.addEventListener('click', clearChat);
    
    // Add event listeners to suggestion buttons
    suggestionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const text = this.getAttribute('data-text');
            userInput.value = text;
            chatForm.dispatchEvent(new Event('submit'));
        });
    });
    
    // Focus on input field when page loads
    userInput.focus();
    
    // Functions
    function handleSubmit(e) {
        e.preventDefault();
        const message = userInput.value.trim();
        
        if (message === '') return;
        
        // Add user message to chat
        addMessageToChat('user-message', '<img class="fas fa-user">', message);
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send message to server
        sendMessageToServer(message);
    }
    
    function handleTyping(e) {
        // Enable send button animation when user types
        if (userInput.value.trim() !== '') {
            sendButton.classList.add('active');
        } else {
            sendButton.classList.remove('active');
        }
    }
    
    function addMessageToChat(className, avatarContent, messageText) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        
        const timestamp = getFormattedTime();
        
        messageDiv.innerHTML = `
            <div class="avatar">
                ${avatarContent}
            </div>
            <div class="message-content">
                <p>${messageText}</p>
                <span class="timestamp">${timestamp}</span>
            </div>
        `;
        
        chatHistory.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        
        chatHistory.appendChild(typingDiv);
        scrollToBottom();
    }
    
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    function sendMessageToServer(message) {
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add AI response to chat
            addMessageToChat('ai-message', '<img alt="logo" src="/static/asian-anime-girl-wearing-a-green-bow (3).png">', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessageToChat('ai-message', '<img alt="logo" src="/static/asian-anime-girl-wearing-a-green-bow (3).png">', 'Sorry, I encountered an error. Please try again later.');
        });
    }
    
    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    function getFormattedTime() {
        const now = new Date();
        let hours = now.getHours();
        const minutes = now.getMinutes().toString().padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        
        hours = hours % 12;
        hours = hours ? hours : 12; // Convert 0 to 12
        
        return `${hours}:${minutes} ${ampm}`;
    }
    
    function updateInitialTimestamp() {
        const initialTimestamp = document.querySelector('.ai-message .timestamp');
        if (initialTimestamp) {
            initialTimestamp.textContent = getFormattedTime();
        }
    }
    
    function clearChat(e) {
        e.preventDefault();
        
        // Keep only the first welcome message
        const welcomeMessage = chatHistory.querySelector('.message');
        chatHistory.innerHTML = '';
        if (welcomeMessage) {
            chatHistory.appendChild(welcomeMessage);
            updateInitialTimestamp();
        }
    }
});
