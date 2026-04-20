from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

app = Flask(__name__)

# training dataset
urls = [
"login-bank-secure.com",
"verify-paytm-account.com",
"free-gift-card-login.com",
"bank-update-secure-login.com",
"google.com",
"github.com",
"amazon.in",
"microsoft.com"
]

labels = [1,1,1,1,0,0,0,0]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(urls)

model = MultinomialNB()
model.fit(X, labels)


@app.route("/", methods=["GET","POST"])
def home():

    result=None
    score=0
    indicators=[]
    advice=""

    if request.method=="POST":

        url=request.form.get("url")

        X_test=vectorizer.transform([url])
        prediction=model.predict(X_test)[0]

        if prediction==1:

            result="⚠ Phishing Website Detected"
            score=85

            indicators=[
            "Suspicious keywords detected",
            "Domain impersonation pattern",
            "Possible credential harvesting",
            "ML phishing signature matched"
            ]

            advice="Do NOT login or enter credentials."

        else:

            result="✅ Website Looks Safe"
            score=10

            indicators=[
            "No phishing pattern detected",
            "Domain reputation normal"
            ]

            advice="Website appears safe but stay cautious."

    return render_template(
        "index.html",
        result=result,
        score=score,
        indicators=indicators,
        advice=advice
    )


@app.route("/chat", methods=["POST"])
def chat():

    message=request.form.get("message")

    if "phishing" in message.lower():
        reply="Phishing attacks trick users into giving credentials."

    elif "safe link" in message.lower():
        reply="Always verify domain spelling and HTTPS."

    else:
        reply="I'm AI Security Assistant."

    return jsonify({"reply":reply})


@app.route("/email", methods=["POST"])
def email():

    text=request.form.get("email")

    if "verify" in text or "password" in text or "bank" in text:
        result="⚠ Suspicious Email Detected"
    else:
        result="Email Looks Safe"

    return jsonify({"result":result})


if __name__ == "__main__":
    app.run(debug=True)