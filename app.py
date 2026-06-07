from flask import Flask, request
import hashlib
import time

app = Flask(__name__)


def proof_of_work(data, difficulty):
    nonce = 0
    target = "0" * difficulty

    start_time = time.time()

    while True:
        text = f"{data}{nonce}"

        hash_result = hashlib.sha256(
            text.encode()
        ).hexdigest()

        if hash_result.startswith(target):
            end_time = time.time()

            return {
                "nonce": nonce,
                "hash": hash_result,
                "attempts": nonce + 1,
                "time": round(end_time - start_time, 4)
            }

        nonce += 1


@app.route("/style.css")
def style():
    with open("style.css", "r", encoding="utf-8") as f:
        return f.read(), 200, {
            "Content-Type": "text/css"
        }


@app.route("/", methods=["GET", "POST"])
def home():

    result_html = ""

    if request.method == "POST":

        data = request.form.get("data")
        difficulty = int(
            request.form.get("difficulty")
        )

        result = proof_of_work(
            data,
            difficulty
        )

        result_html = f"""
        <div class="result">
            <h2>Kết quả</h2>

            <p><strong>Nonce:</strong>
            {result['nonce']}</p>

            <p><strong>Hash:</strong></p>

            <div class="hash-box">
                {result['hash']}
            </div>

            <p><strong>Số lần thử:</strong>
            {result['attempts']}</p>

            <p><strong>Thời gian:</strong>
            {result['time']} giây</p>
        </div>
        """

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    return html.replace(
        "{{RESULT}}",
        result_html
    )


if __name__ == "__main__":
    app.run(debug=True)
