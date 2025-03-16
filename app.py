# app.py - Enhanced Flask backend for Eliana AI

from flask import Flask, render_template, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import random
import re
import time
import json
import datetime
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from flask import send_from_directory

# Download necessary NLTK resources
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

app = Flask(__name__)

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load knowledge base
def load_knowledge_base():
    try:
        if os.path.exists('knowledge_base.json'):
            with open('knowledge_base.json', 'r') as f:
                return json.load(f)
        else:
            knowledge_base = {
                "facts": {
                    "ai": "Artificial Intelligence is the simulation of human intelligence in machines.",
                    "python": "Python is a high-level programming language known for its readability and versatility.",
                    "web": "The World Wide Web is an information system where documents are accessible via URLs.",
                    "eliana": "I am Eliana, a web-based AI assistant designed to help answer questions and have conversations."
                },
                "user_questions": {}
            }
            save_knowledge_base(knowledge_base)
            return knowledge_base
    except Exception as e:
        print(f"Error loading knowledge base: {e}")
        return {"facts": {}, "user_questions": {}}

def save_knowledge_base(knowledge_base):
    try:
        with open('knowledge_base.json', 'w') as f:
            json.dump(knowledge_base, f, indent=2)
    except Exception as e:
        print(f"Error saving knowledge base: {e}")

knowledge_base = load_knowledge_base()

# Enhanced response patterns
responses = {
    "greeting": [
        "Hello! I'm Eliana. How can I help you today?",
        "Hi there! Eliana here. What can I do for you?",
        "Greetings! I'm Eliana, your virtual assistant. What brings you here today?"
    ],
    "farewell": [
        "Goodbye! Have a great day!",
        "See you later! Feel free to chat again anytime.",
        "Farewell! I'll be here if you need any help later."
    ],
    "thanks": [
        "You're welcome! Anything else you'd like to know?",
        "Happy to help! Let me know if you need anything else.",
        "My pleasure! Feel free to ask more questions."
    ],
    "identity": [
        "I'm Eliana, a web-based AI assistant designed to help with information and conversations. I can answer questions, provide information, and learn from our interactions.",
        "My name is Eliana. I'm a virtual assistant created to chat and provide information. I'm constantly learning to better assist you.",
        "I'm Eliana! I'm here to assist with your questions and provide helpful responses. I use NLP to understand your requests and can learn from our conversations."
    ],
    "capabilities": [
        "I can answer questions, provide information on various topics, tell you the current time and date, check the weather (if you provide a location), perform simple calculations, and learn from our conversations.",
        "My capabilities include answering questions, providing facts on topics I know about, telling time, basic math, and remembering information from our conversation.",
        "I'm designed to have informative conversations, answer questions, provide time and date information, perform basic calculations, and learn new information you share with me."
    ],
    "weather_missing_location": [
        "I'd be happy to check the weather for you. Could you please specify a city or location?",
        "To provide weather information, I need to know which location you're interested in.",
        "Which city would you like the weather forecast for?"
    ],
    "default": [
        "I'm still learning. Could you rephrase that, or ask me something else?",
        "I'm not sure I understand completely. Could you try asking in a different way?",
        "I don't have that information yet, but I'm learning. Can you try another question?"
    ],
"search_no_query": [
    "What would you like me to search for?",
    "I'd be happy to look that up. What specifically are you interested in?",
    "Sure, I can search for information. What topic should I look up?"
],
"Feelings": [
    "Im  Good, How are you?",
    "I am doing well, how about you?",
],
"Good": [
    "Thats Great to hear!",
    "Nice to hear that!",
],
"Bad": [
    "I am extremely sorry for that!",
],
"Sad": [
    "I am extremely sorry for that!",
],
"Happy": [
    "I am happy to hear that!",
],
"Angry": [
    "I am extremely sorry for that!",
],
"Love": [
    "I do too!",
],
"Conversation": [
    "Sure, I am here to help you!",
    "I am here to help you!",
    "Sure, I am here to help you!",
],
"Compliment": [
    "Thank you so much"
    "I am happy to help you!",
],
"Jokes": [
    "Why did the tomato turn red? Because it saw the salad dressing!",
    "What do you call cheese that isn't yours? Nacho cheese!",
    "Why couldn't the bicycle stand up by itself? It was two tired!",
    "What do you get when you cross a snowman and a vampire? Frostbite!",
    "Why don't scientists trust atoms? Because they make up everything!",
    "How does a penguin build its house? Igloos it together!",
    "What do you call an alligator in a vest? An investigator!",
    "Why did the math book look sad? Because it had too many problems!",
    "How do you organize a space party? You planet!",
    "Why did the golfer bring two pairs of pants? In case he got a hole in one!"
],
"Music": [
    "I love music! What's your favorite genre or artist?",
    "Music is so powerful. What songs or artists do you like?",
    "I enjoy music. Do you have a favorite song or band?"
],

}

# Enhanced pattern matching
patterns = {
    "greeting": r"(?i)^(hi|hello|hey|greetings|good (morning|afternoon|evening)).*",
    "farewell": r"(?i)^(bye|goodbye|see you|farewell|exit|quit).*",
    "thanks": r"(?i)(^|.*\s+)(thanks|thank you|thx|appreciate it).*",
    "identity": r"(?i).*(who are you|what are you|your name|about yourself|tell me about you).*",
    "capabilities": r"(?i).*(what can you do|your capabilities|what are you capable of|help me with|how can you help).*",
    "time": r"(?i).*(what time is it|what is the time|current time|time now).*",
    "date": r"(?i).*(what (is the|'s the) date|what day is it|current date|today's date).*",
    "weather": r"(?i).*(weather|temperature|forecast).*",
    "calculation": r"(?i).*calculate\s+(\d+[\+\-\*\/]\d+).*",
    "Feelings": r"(?i).*(how are you|how are you doing|how do you do|how do you feel)(.*)",
    "direct_math": r"(?i)^(\d+[\+\-\*\/]\d+)$",
    "learn_fact": r"(?i).*(remember|learn|know) that (.*)",
    "search": r"(?i).*(search for|look up|find information about|google) (.*)",
    "what_fact": r"(?i).*(what|who|where|when|why|how) (is|are|was|were) (.*)",
    "Good": r"(?i).*(good|fine|great|well)(.*)",
    "Bad": r"(?i).*(bad|terrible|sad|unhappy|not good).*",
    "Sad": r"(?i).*(sad|unhappy|depressed|down).*",
    "Happy": r"(?i).*(happy|joyful|excited|pleased).*",
    "Angry": r"(?i).*(angry|mad|upset|frustrated).*",
    "Love": r"(?i).*(love|adore|care).*",
    "Conversation": r"(?i).*(talk|chat|speak|converse).*",
    "Compliment": r"(?i).*(good job|well done|nice work|great job|amazing work).*",
    "Jokes": r"(?i).*(joke|jokes|funny|humor).*",
    "Music": r"(?i).*(music|songs|artists|bands).*",
}

def preprocess_text(text):
    """Preprocess text by tokenizing, removing stopwords and lemmatizing"""
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and token.isalnum()]
    return tokens

def extract_keywords(text):
    """Extract meaningful keywords from text"""
    tokens = preprocess_text(text)
    return set(tokens)

def get_current_time():
    """Return current time in a friendly format"""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}."

def get_current_date():
    """Return current date in a friendly format"""
    current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {current_date}."

def get_weather(location):
    """Simulate getting weather information"""
    # In a real application, you would use a weather API
    # This is a placeholder response
    weathers = ["sunny", "partly cloudy", "cloudy", "rainy", "stormy", "snowy", "windy", "clear"]
    temps = list(range(5, 38))
    
    weather = random.choice(weathers)
    temp = random.choice(temps)
    
    return f"In {location}, it's currently {weather} with a temperature of {temp}°C."

def evaluate_math_expression(expression):
    """Safely evaluate a simple math expression"""
    try:
        # Remove all spaces and validate it only contains allowed characters
        expression = expression.replace(" ", "")
        if not re.match(r'^[\d\+\-\*\/\(\)\.]+$', expression):
            return "I can only perform basic arithmetic operations."
        
        # Evaluate expression safely
        result = eval(expression)
        return f"The result of {expression} is {result}."
    except:
        return "I couldn't calculate that. Please check the expression."

def learn_new_fact(text):
    """Extract and store a new fact from user input"""
    # Extract what comes after "remember that" or similar phrases
    match = re.search(r"(?i)(remember|learn|know) that (.*)", text)
    if match:
        fact = match.group(2).strip().lower()
        # Extract the subject of the fact (before "is" or similar)
        subject_match = re.search(r"(?i)(.*?) (is|are|was|were) (.*)", fact)
        if subject_match:
            subject = subject_match.group(1).strip()
            predicate = subject_match.group(3).strip()
            
            # Store in knowledge base
            knowledge_base["facts"][subject] = fact.capitalize()
            save_knowledge_base(knowledge_base)
            
            return f"I've learned that {fact.capitalize()}. Thank you for teaching me!"
        else:
            # If we can't parse it nicely, just store the whole thing
            key = fact.split()[0] if fact.split() else "fact"
            knowledge_base["facts"][key] = fact.capitalize()
            save_knowledge_base(knowledge_base)
            return f"I've noted that {fact.capitalize()}. Thanks for the information!"
    
    return "I'm not sure what fact you want me to learn."

def answer_fact_question(text):
    """Try to answer a fact-based question using the knowledge base"""
    # Extract the subject of the question
    match = re.search(r"(?i)(what|who|where|when|why|how) (is|are|was|were) (.*)", text)
    if match:
        subject = match.group(3).strip().lower()
        subject = subject.rstrip('?')
        
        # Check keywords in knowledge base
        keywords = preprocess_text(subject)
        for keyword in keywords:
            if keyword in knowledge_base["facts"]:
                return knowledge_base["facts"][keyword]
        
        # Check direct match in knowledge base
        if subject in knowledge_base["facts"]:
            return knowledge_base["facts"][subject]
        
        # Store the question for future learning
        knowledge_base["user_questions"][subject] = text
        save_knowledge_base(knowledge_base)

        # Search the web for an answer
        # web_result = web_search(subject)
        # if web_result:
        #     return web_result
        
        return f"I don't know what {subject} is yet. If you tell me, I'll remember it for next time!"
    
    return None

def extract_location(text):
    """Extract location information from a weather query"""
    # This is a simplified approach - in a real app, you'd use NER
    words = text.split()
    location_indicators = ["in", "at", "for"]
    
    for i, word in enumerate(words):
        if word.lower() in location_indicators and i < len(words) - 1:
            # Return the word after the location indicator
            return words[i + 1].strip(',.?!')
    
    return None

def web_search(query):
    """Perform a web search using a public API instead of scraping"""
    try:
        import requests
        import json
        
        # Format the query
        search_query = query.replace(' ', '+')
        
        # Use SerpAPI, or another search API (you'll need an API key)
        # This is just an example - replace with your preferred API
        api_key = "05814960486b6522acfb54614c02e59009e9d79c9ec808f34f65bddb3cc88f59"  # Replace with your actual API key
        url = f"https://serpapi.com/search?q={search_query}&api_key={api_key}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
        
        # Alternative: Use a different free API like Wikipedia API for certain queries
        wiki_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={search_query}&format=json"
        wiki_response = requests.get(wiki_url)
        
        if wiki_response.status_code == 200:
            wiki_data = wiki_response.json()
            if 'query' in wiki_data and 'search' in wiki_data['query'] and len(wiki_data['query']['search']) > 0:
                first_result = wiki_data['query']['search'][0]
                # Extract and clean snippet (Wikipedia returns HTML)
                from bs4 import BeautifulSoup
                snippet = BeautifulSoup(first_result.get('snippet', ''), 'html.parser').get_text()
                
                if snippet:
                    # Add to knowledge base
                    key_terms = query.split()[:2]
                    key = ' '.join(key_terms).lower()
                    knowledge_base["facts"][key] = snippet
                    save_knowledge_base(knowledge_base)
                    
                    return f"Based on search results: {snippet}"
        
        return "No meaningful results found. Please check your spelling or try another question."
    except Exception as e:
        print(f"Error performing web search: {e}")
        return f"Search error: {str(e)}"
    
def generate_response(user_input):
    """Generate a response based on user input"""
    # Add typing delay to simulate thinking
    time.sleep(0.5)
    
    # Match patterns to determine response category
    for category, pattern in patterns.items():
        if re.match(pattern, user_input.strip()):
            if category == "time":
                return get_current_time()
            elif category == "date":
                return get_current_date()
            elif category == "weather":
                location = extract_location(user_input)
                if location:
                    return get_weather(location)
                else:
                    return random.choice(responses["weather_missing_location"])
            elif category == "calculation" or category == "direct_math":
                # Extract the math expression
                if category == "calculation":
                    match = re.search(r"calculate\s+([\d\+\-\*\/\(\)\.]+)", user_input)
                    if match:
                        expression = match.group(1)
                        return evaluate_math_expression(expression)
                else:
                    # Direct math expression
                    return evaluate_math_expression(user_input)
            elif category == "learn_fact":
                return learn_new_fact(user_input)
            elif category == "what_fact":
                fact_answer = answer_fact_question(user_input)
                if fact_answer:
                    return fact_answer
                # If no answer, fall through to default responses
            elif category == "search":
                match = re.search(r"(?i)(search for|look up|find information about|google) (.*)", user_input)
                if match:
                    query = match.group(2)
                    web_result = web_search(query)
                    if web_result:
                        return web_result
                    # If no answer, fall through to default responses
            elif category == "identity":
                return random.choice(responses["identity"])
            elif category == "capabilities":
                return random.choice(responses["capabilities"])
            elif category == "greeting":
                return random.choice(responses["greeting"])
            elif category == "farewell":
                return random.choice(responses["farewell"])
            elif category == "thanks":
                return random.choice(responses["thanks"])
            else:
                return random.choice(responses[category])
    
    # If no specific pattern matches, try keyword extraction
    keywords = extract_keywords(user_input)
    for keyword in keywords:
        if keyword in knowledge_base["facts"]:
            return knowledge_base["facts"][keyword]
    
    # If still no match, use default responses
    return random.choice(responses["default"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = generate_response(user_message)
    
    # Add slight delay to seem more natural
    time.sleep(0.5)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)