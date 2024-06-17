import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quiz_data import premier_league_easy, world_cup_medium, champions_league_hard

user_database = [{"username": "admin", "password": "password", "points": 0}]

current_question = 0
score = 0
user_points = 0
username = None
current_quiz_data = None  

def show_home_page():
    register_frame.pack_forget()
    login_frame.pack_forget()
    profile_frame.pack_forget()
    quiz_frame.pack_forget()
    quiz_selection_frame.pack_forget()
    home_frame.pack()

def show_register_page():
    home_frame.pack_forget()
    login_frame.pack_forget()
    profile_frame.pack_forget()
    quiz_frame.pack_forget()
    quiz_selection_frame.pack_forget()
    register_frame.pack()

def show_login_page():
    home_frame.pack_forget()
    register_frame.pack_forget()
    profile_frame.pack_forget()
    quiz_frame.pack_forget()
    quiz_selection_frame.pack_forget()
    login_frame.pack()

def show_profile_page():
    global username, user_points
    home_frame.pack_forget()
    register_frame.pack_forget()
    login_frame.pack_forget()
    quiz_frame.pack_forget()
    quiz_selection_frame.pack_forget()
    if username:
        profile_label.config(text=f"Welcome, {username}! Points: {user_points}")
    else:
        profile_label.config(text="Hello Guest")
    profile_frame.pack()

def start_quiz(quiz_data):
    global current_quiz_data
    current_quiz_data = quiz_data 
    show_quiz_page()
    reset_quiz()
    show_question()

def show_quiz_selection_page():
    home_frame.pack_forget()
    register_frame.pack_forget()
    login_frame.pack_forget()
    profile_frame.pack_forget()
    quiz_frame.pack_forget()
    quiz_selection_frame.pack()
    
    for widget in quiz_selection_frame.winfo_children():
        widget.destroy()

    ttk.Button(quiz_selection_frame, text="Premier League Easy Quiz",
               command=lambda: show_quiz_page_with_data(premier_league_easy)).pack(pady=10)
    ttk.Button(quiz_selection_frame, text="World Cup Medium Quiz",
               command=lambda: show_quiz_page_with_data(world_cup_medium)).pack(pady=10)
    ttk.Button(quiz_selection_frame, text="Champions League Hard Quiz",
               command=lambda: show_quiz_page_with_data(champions_league_hard)).pack(pady=10)

def show_quiz_page_with_data(quiz_data):
    quiz_selection_frame.pack_forget() 
    show_quiz_page()
    start_quiz(quiz_data)

def show_quiz_page():
    home_frame.pack_forget()
    register_frame.pack_forget()
    login_frame.pack_forget()
    profile_frame.pack_forget()
    quiz_frame.pack()

def reset_quiz():
    global current_question, score
    current_question = 0
    score = 0
    score_label.config(text="Score: 0/{}".format(len(current_quiz_data)))

def show_question():
    global current_question
    if current_question < len(current_quiz_data):
        question = current_quiz_data[current_question]
        qs_label.config(text=question["question"])

        choices = question["choices"]
        for i in range(4):
            choice_btns[i].config(text=choices[i], state="normal")

        feedback_label.config(text="")
        next_btn.config(state="disabled")
    else:
        finish_quiz()

def check_answer(choice):
    global current_question, score

    question = current_quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")

    if selected_choice == question["answer"]:
        score += 1
        update_score()
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")

    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")

def update_score():
    global score
    score_label.config(text="Score: {}/{}".format(score, len(current_quiz_data)))

    global user_points
    user_points = score * 5

    if username:
        profile_label.config(text=f"Welcome, {username}! Points: {user_points}")

def next_question():
    global current_question
    current_question += 1

    if current_question < len(current_quiz_data):
        show_question()
    else:
        finish_quiz()

def finish_quiz():
    messagebox.showinfo("Quiz Completed",
                        "Quiz Completed! Final score: {}/{}".format(score, len(current_quiz_data)))
    update_score()
    show_home_page()

root = tk.Tk()
root.title("Football Quiz")
root.geometry("600x500")
style = Style(theme="flatly")

style.configure("TLabel", font=("Helvetica", 20))
style.configure("TButton", font=("Helvetica", 16))

home_frame = ttk.Frame(root, padding=20)
register_frame = ttk.Frame(root, padding=20)
login_frame = ttk.Frame(root, padding=20)
profile_frame = ttk.Frame(root, padding=20)
quiz_selection_frame = ttk.Frame(root, padding=20)
quiz_frame = ttk.Frame(root, padding=20)

ttk.Label(home_frame, text="Football Quiz", font=("Helvetica", 24)).pack(pady=20)
ttk.Button(home_frame, text="Profile", command=show_profile_page).pack(pady=10)
ttk.Button(home_frame, text="Register", command=show_register_page).pack(pady=10)
ttk.Button(home_frame, text="Log In", command=show_login_page).pack(pady=10)
ttk.Button(home_frame, text="PLAY", command=show_quiz_selection_page).pack(pady=10)

ttk.Label(register_frame, text="Register", font=("Helvetica", 24)).pack(pady=20)
ttk.Label(register_frame, text="Username:").pack()
username_entry = ttk.Entry(register_frame)
username_entry.pack(pady=5)
ttk.Label(register_frame, text="Password:").pack()
password_entry = ttk.Entry(register_frame, show="*")
password_entry.pack(pady=5)
ttk.Button(register_frame, text="Register", command=lambda: register_user(username_entry.get(), password_entry.get())).pack(pady=10)
ttk.Button(register_frame, text="Back to Home", command=show_home_page).pack(pady=10)

def register_user(username, password):
    user_database.append({"username": username, "password": password})
    messagebox.showinfo("Registration", "Registration successful!")
    show_login_page()

ttk.Label(login_frame, text="Log In", font=("Helvetica", 24)).pack(pady=20)
ttk.Label(login_frame, text="Username:").pack()
login_username_entry = ttk.Entry(login_frame)
login_username_entry.pack(pady=5)
ttk.Label(login_frame, text="Password:").pack()
login_password_entry = ttk.Entry(login_frame, show="*")
login_password_entry.pack(pady=5)
ttk.Button(login_frame, text="Log In", command=lambda: login_user(login_username_entry.get(), login_password_entry.get())).pack(pady=10)
ttk.Button(login_frame, text="Back to Home", command=show_home_page).pack(pady=10)

def login_user(username_input, password_input):
    global username

    for user in user_database:
        if user["username"] == username_input and user["password"] == password_input:
            username = username_input
            messagebox.showinfo("Login", "Login successful!")
            show_profile_page()
            return
    messagebox.showerror("Login Failed", "Invalid username or password.")

ttk.Label(profile_frame, text="Profile", font=("Helvetica", 24)).pack(pady=20)
profile_label = ttk.Label(profile_frame, text="", font=("Helvetica", 16))
profile_label.pack(pady=10)
ttk.Button(profile_frame, text="Back to Home", command=show_home_page).pack(pady=10)

qs_label = ttk.Label(
    quiz_frame,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)

choice_btns = []
for i in range(4):
    button = ttk.Button(
        quiz_frame,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

feedback_label = ttk.Label(
    quiz_frame,
    anchor="center",
    padding=10
)
feedback_label.pack(pady=10)

score_label = ttk.Label(
    quiz_frame,
    text="Score: 0/{}".format(len(current_quiz_data) if current_quiz_data else 0),
    anchor="center",
    padding=10
)
score_label.pack(pady=10)

next_btn = ttk.Button(
    quiz_frame,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

show_home_page()    

root.mainloop()
