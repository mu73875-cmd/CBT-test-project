from flask import Flask, render_template, request, redirect, session
from models import Question
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "secret123"


questions = [

Question(
"The Internet is best defined as:",
["single computer network","collection of isolated computers","A global network of interconnected computers","A local area network"],
"A global network of interconnected computers"
),

Question(
"What does IP stand for in Internet terminology?",
["Internet Path","Internet Provider","Internet Protocol","Internal Process"],
"Internet Protocol"
),

Question("What does WWW stand for?",
["World Wide Web","World Web Wide","Wide World Web","Web World Wide"],
"World Wide Web"),

Question("Which is a programming language?",
["HTML","CSS","Python","HTTP"],
"Python"),

Question("Which part of computer stores data permanently?",
["RAM","ROM","CPU","Cache"],
"ROM"),

Question("What does LAN stand for?",
["Local Area Network","Large Area Network","Long Area Network","Light Area Network"],
"Local Area Network"),

Question("Which is an input device?",
["Printer","Speaker","Keyboard","Monitor"],
"Keyboard"),

Question("What does GPU stand for?",
["Graphics Processing Unit","General Processing Unit","Graphical Program Unit","Global Processing Unit"],
"Graphics Processing Unit"),

Question("Which software is used to browse the internet?",
["Excel","Chrome","Word","Paint"],
"Chrome"),

Question("What is the full meaning of PDF?",
["Portable Document Format","Print Document File","Public Data File","Personal Document Format"],
"Portable Document Format"),
Question("What does USB stand for?",
["Universal Serial Bus","United System Board","Universal System Bus","User Serial Base"],
"Universal Serial Bus"),

Question("Which of these is an operating system?",
["Windows","Google","Intel","Facebook"],
"Windows"),

Question("What is the brain of the computer?",
["Monitor","Keyboard","CPU","Mouse"],
"CPU"),

Question("Which key is used to delete text?",
["Shift","Ctrl","Delete","Tab"],
"Delete"),

Question("Which device displays output?",
["Keyboard","Monitor","Mouse","Scanner"],
"Monitor"),

Question(
"Python is a?",
["Snake","Programming Language","Car","Game"],
"Programming Language"
),

Question(
"What does CPU stand for?",
["Central Process Unit","Central Processing Unit","Computer Personal Unit","Central Power Unit"],
"Central Processing Unit"
),

Question(
"Which device is used to input text into a computer?",
["Monitor","Keyboard","Printer","Speaker"],
"Keyboard"
),

Question(
"HTML is used for?",
["Designing web pages","Programming robots","Creating databases","Making games"],
"Designing web pages"
),

Question(
"What does RAM stand for?",
["Random Access Memory","Read Access Memory","Run Access Memory","Real Access Memory"],
"Random Access Memory"
),

Question(
"Which company created Windows?",
["Apple","Microsoft","Google","IBM"],
"Microsoft"
),

Question(
"What does URL stand for?",
["Uniform Resource Locator","Universal Resource Link","Unique Reference Link","Uniform Reference Locator"],
"Uniform Resource Locator"
),

Question(
"Which language is mainly used for web page styling?",
["Python","Java","CSS","C++"],
"CSS"
),

Question(
"Which of the following is a web browser?",
["Chrome","Excel","PowerPoint","Photoshop"],
"Chrome"
),

Question(
"What does HTTP stand for?",
["HyperText Transfer Protocol","High Transfer Text Protocol","Hyper Tool Transfer Protocol","HyperText Transmission Process"],
"HyperText Transfer Protocol"
),

Question(
"Which device prints documents on paper?",
["Scanner","Printer","Monitor","Router"],
"Printer"
)

]


@app.route("/", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        matric = request.form["matric"]
        dob = request.form["dob"]

        session["user"] = username
        session["matric"] = matric
        session["dob"] = dob

        return redirect("/home")

    return render_template("login.html")


@app.route("/home")
def home():

    if "user" not in session:
        return redirect("/")

    return render_template("index.html", user=session["user"])


@app.route("/start")
def start_quiz():

    if "user" not in session:
        return redirect("/")

    session["answers"] = {}
    return redirect("/quiz/0")


@app.route("/quiz/<int:qnum>", methods=["GET","POST"])
def quiz(qnum):

    if "user" not in session:
        return redirect("/")

    if qnum >= len(questions):
        return redirect("/result")

    if request.method == "POST":

        answer = request.form.get("answer")

        answers = session.get("answers", {})
        answers[str(qnum)] = answer
        session["answers"] = answers

        if qnum + 1 < len(questions):
            return redirect(f"/quiz/{qnum+1}")
        else:
            return redirect("/result")

    question = questions[qnum]

    return render_template(
        "quiz.html",
        question=question,
        qnum=qnum,
        total=len(questions)
    )


@app.route("/result")
def result():

    if "user" not in session:
        return redirect("/")

    answers = session.get("answers", {})
    score = 0

    for i, q in enumerate(questions):

        if answers.get(str(i)) == q.answer:
            score += 1

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    result_data = {
        "name": session["user"],
        "matric": session["matric"],
        "dob": session["dob"],
        "score": score,
        "total": len(questions),
        "time": time
    }

    try:
        with open("results.json","r") as file:
            data = json.load(file)
    except:
        data = []

    data.append(result_data)

    with open("results.json","w") as file:
        json.dump(data,file,indent=4)

    return render_template(
        "result.html",
        score=score,
        total=len(questions),
        time=time,
        user=session["user"],
        matric=session["matric"],
        dob=session["dob"]
    )


@app.route("/all_results")
def all_results():

    if "user" not in session:
        return redirect("/")

    try:
        with open("results.json","r") as file:
            data = json.load(file)
    except:
        data = []

    return render_template("all_results.html", results=data)


@app.route("/logout")
def logout():

    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)