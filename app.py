from flask import Flask, render_template, request, jsonify
from main import graph

app = Flask(__name__)


def build_initial_state(user_input: str) -> dict:
    return {
        "messages": [{"role": "user", "content": user_input}],
        "user_question": user_input,
        "google_results": None,
        "bing_results": None,
        "reddit_results": None,
        "selected_reddit_urls": None,
        "reddit_post_data": None,
        "google_analysis": None,
        "bing_analysis": None,
        "reddit_analysis": None,
        "final_answer": None,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/research", methods=["POST"])
def research():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    question = (data.get("question") or "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        state = build_initial_state(question)
        final_state = graph.invoke(state)
        answer = final_state.get("final_answer") or "No answer could be generated."
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Research error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)