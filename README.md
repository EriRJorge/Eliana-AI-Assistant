# Eliana AI Assistant
 Virtual Assistant Web Framework Headed by Type_Software

# Eliana AI - Flask Backend

Eliana AI is a web-based AI assistant designed to engage in conversations, answer questions, and learn from user interactions. This project leverages Flask for the backend and uses Natural Language Processing (NLP) to enhance understanding and responses.

## Features
- **Conversational AI**: Responds to greetings, farewells, compliments, and various emotional cues.
- **Knowledge Base**: Stores and retrieves facts, with the ability to learn from interactions.
- **NLP Integration**: Utilizes NLTK for tokenization, lemmatization, and stopword filtering.
- **Web Scraping**: Supports dynamic data fetching using Selenium and BeautifulSoup.
- **Custom Responses**: Offers predefined response patterns for diverse conversational scenarios.
- **Weather Information**: Can provide weather updates based on user-provided locations.
- **Basic Calculations**: Responds to simple arithmetic queries.

## Installation
1. **Clone the Repository**:
```bash
git clone <repository-url>
cd eliana-ai-backend
```

2. **Set Up Virtual Environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

4. **Download NLTK Data** (if not already downloaded):
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

## Running the Application
Start the Flask development server:
```bash
python app.py
```
By default, the application will be accessible at `http://127.0.0.1:5000/`.

## API Endpoints
- **`/`**: Home page rendering.
- **`/ask`** (POST): Accepts user questions and returns AI-generated responses.
- **`/weather`** (POST): Provides weather information for a specified location.

## File Structure
```
├── app.py                  # Main Flask application file
├── knowledge_base.json     # Stores facts and learned information
├── templates/              # Contains HTML templates
├── static/                 # Contains static files like CSS and JS
└── requirements.txt        # Python dependencies
```

## Customization
- **Knowledge Base**: Edit `knowledge_base.json` to add or modify known facts.
- **Response Patterns**: Update the `responses` and `patterns` dictionaries in `app.py` for custom behavior.
- **Web Scraping**: Modify the Selenium logic to handle different scraping requirements.

# Eliana JS

## Overview
This JavaScript powers the interactive chat interface. It allows users to send messages, receive automated responses, and interact with suggestion buttons. The application also handles chat history, typing indicators, and timestamping for messages.

## Features
- **Message Submission:** Users can type messages and submit them via a form.
- **Suggestion Buttons:** Predefined suggestion buttons allow for quick message inputs.
- **Typing Indicator:** Displays a visual indicator while the AI is generating a response.
- **Timestamping:** Each message includes a formatted timestamp.
- **Chat Clearing:** Users can clear the chat history, preserving the initial welcome message.
- **Send Button Activation:** The send button activates visually when the user starts typing.

## Usage
1. Type a message into the input field and press the send button or submit the form to send the message.
2. Click on a suggestion button to auto-fill the input with predefined text.
3. Observe the AI-generated response, which will appear with a typing indicator.
4. Use the clear chat button to reset the chat while keeping the welcome message.

## Key Functions
- **handleSubmit(e):** Handles form submissions and initiates message sending.
- **handleTyping(e):** Toggles the send button animation based on user input.
- **addMessageToChat(className, avatarContent, messageText):** Appends messages to the chat history.
- **showTypingIndicator():** Displays a typing animation while awaiting a response.
- **removeTypingIndicator():** Removes the typing animation once a response is received.
- **sendMessageToServer(message):** Sends the user's message to the server and handles the response.
- **scrollToBottom():** Ensures the chat view scrolls to the latest message.
- **getFormattedTime():** Returns the current time in a 12-hour AM/PM format.
- **updateInitialTimestamp():** Updates the timestamp of the initial message on page load.
- **clearChat(e):** Clears the chat history, retaining the initial welcome message.

## API Endpoint
- **POST /chat:** Accepts a JSON object with a "message" key and returns a JSON response containing the AI's reply.

## Error Handling
- If the server request fails, an error message is displayed to the user.

## Customization
- **Avatars:** Customize avatars by changing the `avatarContent` in the `addMessageToChat` function.
- **Suggestion Texts:** Modify the `data-text` attributes of suggestion buttons.
- **Styling:** Customize styles by editing the associated CSS file.

# Eliana AI FrontEnd

Eliana AI Assistant is an intelligent, conversational web assistant designed to interact with users in a friendly and intuitive manner.

## Features
- **Interactive Chat Interface:** Users can type messages and receive AI responses in real-time.
- **Predefined Suggestions:** Quick-access buttons for common queries like "Who are you?" or "What's the weather in NYC?"
- **Responsive Design:** Optimized for different screen sizes and devices.
- **Chat History Display:** Conversations are displayed in a scrollable container.
- **Custom Avatar:** Eliana is represented with an anime-inspired avatar.
- **Chat Clearing Option:** Users can clear the chat history with a dedicated link.

## Usage
- **Start a Conversation:** Type a message in the input box and press the send button or hit enter.
- **Use Suggestions:** Click any suggestion button for instant queries.
- **Clear Chat:** Click the "Clear Chat" link in the footer to reset the chat history.

## Dependencies
- [Font Awesome](https://fontawesome.com/) - For icons used in buttons.

## Customization
- **Styling:** Modify `static/styles.css` to adjust the design and layout.
- **Behavior:** Update `static/script.js` to customize chat logic or message handling.
- **Avatar:** Replace the avatar image in the `static/` directory.

## Customization
Modify the CSS variables in `style.css` to tailor the look and feel:

# CSS Colors for Eliana AI Assistant

```css
:root {
    --primary-color: #6c5ce7;
    --secondary-color: #E1FFBB;
    --accent-color: #7158e2;
    --text-color: #2d3436;
    --light-bg: #f9f9f9;
    --chat-user: #e4f4ff;
    --chat-ai: #f0e6ff;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --border-radius: 12px;
    --transition: all 0.3s ease;
}
```

## Author of Frontend
[Eri R Jorge] - [erirjorge.online]


## Requirements
- Python 3.8+
- Flask
- NLTK
- Selenium
- BeautifulSoup4
- Requests
- Chrome WebDriver (for Selenium)

## Contributing
Contributions are welcome! Feel free to submit pull requests or open issues to enhance the project.

## Acknowledgments
- [Flask](https://flask.palletsprojects.com/)
- [NLTK](https://www.nltk.org/)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)

## Contact
For questions or collaborations, please contact Eri R Jorge at [erirjorge@gmail.com].