from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "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"

# General context about the project
general_context = (
    "You are an intelligent assistant for a food-based app called Culinary Compass. "
    "This app helps users explore dishes by providing descriptions, ingredients, and nutritional information. "
    "It also alerts diabetic users about dishes that may not be suitable for their condition. "
    "You may receive context about a specific dish or a user query. Respond appropriately and help the user.Give in just text format."
)

# In-memory storage for session contexts
session_contexts = {}

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        # Parse the incoming JSON request
        data = request.json

        # Extract session ID, user query, and dish context from the request
        session_id = data.get("session_id", "default_session")
        user_query = data.get("query", "").strip()
        dish_context = data.get("context", None)

        # Initialize the session context if it doesn't exist
        if session_id not in session_contexts:
            session_contexts[session_id] = [{"role": "system", "content": general_context}]

        # Add dish context (if provided) to the session context
        if dish_context:
            session_contexts[session_id].append(
                {"role": "system", "content": f"Dish Context: {dish_context}"}
            )

        # Append the user's query to the session context
        session_contexts[session_id].append({"role": "user", "content": user_query})

        # Call the GPT model
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use the model available to you
            messages=session_contexts[session_id],
            max_tokens=200,
            temperature=0.7
        )

        # Extract the bot's response
        bot_response = response["choices"][0]["message"]["content"].strip()

        # Append the bot's response to the session context
        session_contexts[session_id].append({"role": "assistant", "content": bot_response})

        # Return the bot's response to the client
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
