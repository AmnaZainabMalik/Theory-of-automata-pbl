import tkinter as tk
from tkinter import ttk

# ---------------- DFA WITH TRACE ---------------- #
def validate_with_trace(username):
    q0 = "START"
    q1 = "VALID"
    q2 = "UNDERSCORE/DOT"
    qdead = "DEAD"

    state = q0
    transitions = [f"Start → {state}"]

    if len(username) < 3 or len(username) > 20:
        return False, ["Invalid length (3–20 required)"]

    for ch in username:
        prev = state

        if state == q0:
            state = q1 if ch.isalpha() else qdead

        elif state == q1:
            if ch.isalnum():
                state = q1
            elif ch in "_.":  
                state = q2
            else:
                state = qdead

        elif state == q2:
            state = q1 if ch.isalnum() else qdead

        transitions.append(f"{prev} --({ch})--> {state}")

    return state == q1, transitions


# ---------------- GUI FUNCTIONS ---------------- #
def update_live(event=None):
    username = entry.get()
    is_valid, transitions = validate_with_trace(username)

    transition_box.config(state="normal")
    transition_box.delete("1.0", tk.END)

    for t in transitions:
        transition_box.insert(tk.END, t + "\n")

    transition_box.config(state="disabled")

    if is_valid:
        result_label.config(text="✔ Accepted", fg="#2ecc71")
    else:
        result_label.config(text="✖ Rejected", fg="#e74c3c")


def clear_all():
    entry.delete(0, tk.END)
    transition_box.config(state="normal")
    transition_box.delete("1.0", tk.END)
    transition_box.config(state="disabled")
    result_label.config(text="")


# ---------------- WINDOW ---------------- #
root = tk.Tk()
root.title("DFA Username Validator (Professional GUI)")
root.geometry("850x550")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")

# ---------------- HEADER ---------------- #
header = tk.Label(root, text="DFA USERNAME VALIDATOR",
                  font=("Segoe UI", 20, "bold"),
                  bg="#1e1e2f", fg="white")
header.pack(pady=10)

# ---------------- MAIN FRAME ---------------- #
main_frame = tk.Frame(root, bg="#1e1e2f")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Split into LEFT (rules) and RIGHT (main UI)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=2)

# ---------------- RULES PANEL ---------------- #
rules_frame = tk.Frame(main_frame, bg="#2c2c3e", padx=15, pady=15)
rules_frame.grid(row=0, column=0, sticky="nsew", padx=(0,10))

tk.Label(rules_frame, text="VALIDATION RULES",
         font=("Segoe UI", 13, "bold"),
         bg="#2c2c3e", fg="#f1c40f").pack(anchor="w", pady=(0,10))

rules_text = """
1. Must start with a LETTER (A–Z, a–z)
2. Only letters, digits, _ and .
3. No consecutive _ or .
4. Must end with letter or digit
5. Length must be 3 to 20 characters
"""

tk.Label(rules_frame, text=rules_text,
         justify="left",
         font=("Segoe UI", 10),
         bg="#2c2c3e", fg="white").pack(anchor="w")

# ---------------- RIGHT FRAME ---------------- #
frame = tk.Frame(main_frame, bg="#2c2c3e", padx=20, pady=20)
frame.grid(row=0, column=1, sticky="nsew")

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=2)

# ---------------- INPUT ---------------- #
tk.Label(frame, text="Enter Username:",
         bg="#2c2c3e", fg="white",
         font=("Segoe UI", 11)).grid(row=0, column=0, sticky="w", pady=10)

entry = ttk.Entry(frame, width=35)
entry.grid(row=0, column=1, pady=10, sticky="ew")
entry.bind("<KeyRelease>", update_live)

# ---------------- RESULT ---------------- #
result_label = tk.Label(frame, text="",
                        font=("Segoe UI", 12, "bold"),
                        bg="#2c2c3e")
result_label.grid(row=1, column=0, columnspan=2, pady=10)

# ---------------- TRANSITION LABEL ---------------- #
tk.Label(frame, text="State Transitions:",
         bg="#2c2c3e", fg="white",
         font=("Segoe UI", 11)).grid(row=2, column=0, columnspan=2, sticky="w", pady=(15,5))

# ---------------- TRANSITION BOX ---------------- #
transition_box = tk.Text(frame,
                         height=12,
                         bg="#12121a",
                         fg="#00ffcc",
                         font=("Consolas", 10),
                         relief="flat")
transition_box.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)

transition_box.config(state="disabled")

frame.rowconfigure(3, weight=1)

# ---------------- BUTTONS ---------------- #
btn_frame = tk.Frame(frame, bg="#2c2c3e")
btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

ttk.Button(btn_frame, text="Clear", command=clear_all).grid(row=0, column=0, padx=15)
ttk.Button(btn_frame, text="Exit", command=root.destroy).grid(row=0, column=1, padx=15)

# ---------------- FOOTER ---------------- #
footer = tk.Label(root,
                  text="Live DFA Visualization | TOA Project",
                  bg="#1e1e2f", fg="#aaaaaa",
                  font=("Segoe UI", 9))
footer.pack(pady=5)

root.mainloop()