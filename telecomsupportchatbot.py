import random
import re
import streamlit as st

import spacy #python -m spacy download en_core_web_sm
nlp = spacy.load('en_core_web_sm')

class TelecomSupportBot:
    def __init__(self):
        self.exit_commands = ("exit", "quit", "goodbye", "bye")
        self.intents = {
            'greeting': ['hi', 'hello', 'hey', 'morning', 'evening'],
            'goodbye': ['bye', 'goodbye', 'see', 'exit'],
            'billing_issue': ['bill', 'billing', 'overcharge', 'payment'],
            'network_issue': ['network', 'signal', 'coverage', 'drop'],
            'internet_issue': ['internet', 'data', 'speed', 'wifi', 'broadband'],
            'plan_upgrade': ['upgrade', 'plan', 'package', 'subscription'],
            'thanks': ['thank', 'thanks', 'thx']
}
        self.similarity_threshold = 0.75


    def pre_process(self, text):
        doc = nlp(text.lower())
        return [token for token in doc if not token.is_stop]

    def get_response(self, message):
        tokens = self.pre_process(message)

        best_intent = None
        best_intent_score = 0

        for intent, pattern in self.intents.items():
            for keyword in pattern:
                keyword_token = nlp(keyword)[0]
                for user_token in tokens:
                    if user_token.has_vector and keyword_token.has_vector:
                        similarity = user_token.similarity(keyword_token)
                        if similarity > best_intent_score and similarity > self.similarity_threshold:
                            best_intent = intent
                            best_intent_score = similarity

        if best_intent:
            return self.respond_to_intent(best_intent)
        
        return random.choice([
            "🤖 I didn’t quite catch that. Can you rephrase?",
            "🤖 I'm still learning. Could you say that another way?",
            "🤖 Hmm... that's interesting. Can you explain more?"
        ])

    def respond_to_intent(self, intent):
        responses = {
            'greeting': [
                "Hello! 👋 I'm here to help you with your telecom needs.",
                "Hi there! How can I assist you today?",
                "Hey! Need help with billing, internet, or something else?"
            ],
            'goodbye': [
                "Goodbye! 👋 Hope your issue is resolved.",
                "Take care! Feel free to chat again anytime.",
                "Bye! Have a wonderful day ahead."
            ],
            'billing_issue': [
                "It sounds like you’re facing billing problems. Please check your latest invoice in the app.",
                "Our system has logged a billing issue for you. A support agent will reach out soon."
            ],
            'network_issue': [
                "We’re currently working to improve network coverage in many areas.",
                "Try restarting your device. If issues persist, we can file a complaint for you."
            ],
            'internet_issue': [
                "Try resetting your router and ensure data mode is enabled.",
                "Check your plan’s data limit. Slowness could be due to exhausted quota."
            ],
            'plan_upgrade': [
                "You can upgrade your plan via the app under ‘Manage Plan’.",
                "We have great new plans available — would you like to hear more?"
            ],
            'thanks': [
                "You're welcome! 😊",
                "Glad I could help!",
                "Happy to assist!"
            ]
        }
        return random.choice(responses[intent])


# Streamlit Interface
st.set_page_config(page_title="Telecom Chatbot", page_icon="📱")
st.title("📞 Telecom Customer Support Chatbot")

if "history" not in st.session_state:
    st.session_state.history = ["🤖 Hello! I’m your telecom assistant. How can I help you today?"]

bot = TelecomSupportBot()
user_input = st.text_input("👤 You:", key="user_input")

if user_input:
    response = bot.get_response(user_input)
    st.session_state.history.append(f"👤 You: {user_input}")
    st.session_state.history.append(f"{response}")

for line in st.session_state.history:
    st.markdown(line)