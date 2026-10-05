from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip().lower()
    language = data.get("language", "english")

    # Basic computational functionality
    try:
        expression = message.replace("calculate", "").replace("what is", "").strip()
        allowed_characters = "0123456789+-*/(). "
        if expression and all(char in allowed_characters for char in expression):
            result = eval(expression, {"__builtins__": {}}, {})
            if language == "sanskrit":
                response = f"परिणामः: {result}"
            else:
                response = f"Result: {result}"
            return jsonify({"response": response})
    except Exception:
        pass

    # Sanskrit responses
    if language == "sanskrit":
        if "namaste" in message or "नमस्ते" in message:
            response = "नमस्ते! भवतः स्वागतं अस्ति।"
        elif "hello" in message or "hi" in message or "hey" in message:
            response = "नमस्ते! अहं भवतः साहाय्यं कर्तुं शक्नोमि।"
        elif "who are you" in message:
            response = "अहं एकः सरलः बहुभाषिकः संगणकीयः चैटबॉट् अस्मि।"
        elif "help" in message:
            response = "अहं अभिवादनं, सामान्यप्रश्नान्, सरलगणनां च कर्तुं शक्नोमि।"
        else:
            response = "क्षम्यताम्, अहं एतत् न अवगच्छामि।"

    # English responses
    else:
        if "hey" in message:
            response = "Hey there! How can I help you?"
        elif "hello" in message or "hi" in message:
            response = "Hello! How can I help you?"
        elif "who are you" in message:
            response = "I am a simple multilingual computational chatbot."
        elif "help" in message:
            response = "You can greet me, ask who I am, or give me a calculation."
        else:
            response = "Sorry, I don't understand that yet."

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
