import customtkinter as ctk
import requests
from tkinter import filedialog
from pypdf import PdfReader
from docx import Document
import threading
import random
from google import genai

GEMINI_API_KEY = "AQ.Ab8RN6I5lq1gv4T98n2owtIPnMpy0lwHj3l4EYyLpNRPJXbX0g"

client = genai.Client(
    api_key=GEMINI_API_KEY
)

VIJEY_LETTER = """
Hi SPL madam,

If you're reading this, there's probably a good chance you're overthinking something right now.

Maybe it's your career path.
Maybe it's what to learn next.
Maybe it's whether you're doing enough.

Honestly, I think most of us in CSE go through that at some point.

I definitely did.

When I started learning programming, I wasn't some genius who had everything planned out. I spent a lot of time being confused, changing directions, starting things, abandoning things, and wondering whether I was learning the right stuff.

Even now, I don't think anyone truly has everything figured out.

What helped me wasn't finding the perfect roadmap.

It was simply continuing.

Trying random ideas.
Building projects.
Getting stuck.
Searching for solutions.
Making mistakes.
Learning something new.
Then repeating the process again.

A lot of the things I've learned came from curiosity rather than certainty.

So if you ever feel lost, you're probably a lot more normal than you think.

You don't need to know exactly where you'll end up.

Just keep exploring things that genuinely interest you.

And if one day you're confused about something, remember there are plenty of people on the same boat trying to figure things out too.

Including me.

Keep learning.

Keep building.

    — Vijey

"""
VIJEY_MEMORIES = """
ABOUT VIJEY

My name is Vijey.

I enjoy building AI, computer vision, and software projects.

I am naturally curious and enjoy exploring new technologies by building things rather than only reading about them.

When I started programming, I was often unsure about which career path to choose. Over time, I learned that trying different things taught me more than endlessly searching for the perfect answer.

---

MY LEARNING JOURNEY

One thing that helped me a lot was practicing problem-solving.

I have solved more than 800 problems on LeetCode.

Working through Data Structures and Algorithms taught me how to think logically, break down problems, and approach challenges systematically.

DSA did not just help with coding interviews. It improved the way I approach software development and problem solving in general.

---

INTERNSHIP EXPERIENCE

I completed an internship at Mirador AI Technology.

During my internship, I worked on AI-related projects and gained practical experience building solutions rather than only learning concepts.

It helped me understand how real-world AI projects are developed and improved over time.

---

HOW I BUILD PROJECTS

People often think a project starts with code.

For me, it usually starts with a problem or an idea.

First, I identify a problem worth solving or an idea that seems interesting.

Then I discuss the idea with AI tools such as ChatGPT.

I use these conversations to deepen the idea, discover new possibilities, identify weaknesses, and explore different approaches.

After that, I look at multiple possible solutions and compare them.

I spend time thinking about the architecture before writing code.

I break the project into smaller modules and design each part separately.

Only after understanding the structure do I begin implementation.

I frequently use AI tools to generate code, explain concepts, suggest improvements, and accelerate development.

Instead of trying to manually write every line of code from scratch, I focus on understanding the system, making decisions, reviewing outputs, and improving the project step by step.

Development becomes a collaboration between my ideas and AI assistance.

Throughout the process, both my own inputs and AI suggestions continuously improve the project.

---

WHAT I BELIEVE

Building projects teaches lessons that tutorials cannot.

Getting stuck is normal.

Debugging is part of learning.

Perfection is not required before starting.

Most skills are developed through repetition and experience.

---

CAREER ADVICE

You do not need to choose a specialization immediately.

Explore different domains:

* AI & Machine Learning
* Web Development
* Cybersecurity
* Cloud Computing
* Data Science
* Mobile Development

The field that keeps your interest even when things become difficult is often worth exploring further.

---

THINGS I HAVE LEARNED

Consistency beats motivation.

Small projects are better than endless planning.

Curiosity is a powerful advantage.

Experience is gained by building, not by waiting.

The best way to learn is often to create something and improve it repeatedly.

---

MESSAGE

Keep exploring.

Keep learning.

Keep building.

Nobody has everything figured out.

You are allowed to experiment, change direction, and discover what truly excites you.

Learning is a journey, not a race.
"""

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
app = ctk.CTk()

log_event(
    "App Opened",
    "CS Navigator Started"
)

app.title("🎓 CS Navigator AI")
app.geometry("1200x800")
app.minsize(1000, 700)
notes_chunks = []
notes_model = None
notes_index = None

GOOGLE_SHEET_URL = (
    "https://script.google.com/macros/s/AKfycbxC9oy-keAXJSymAN7Wld7vHcKePrppTkGjJkPuWsFOaGirooLb9bXxLh-4b9CyCgX5/exec"
)


def glitter(canvas):

    colors = [
        "gold",
        "pink",
        "cyan",
        "orange",
        "white"
    ]

    for _ in range(150):

        x = random.randint(0, 700)
        y = random.randint(0, 500)

        canvas.create_oval(
            x,
            y,
            x + 6,
            y + 6,
            fill=random.choice(colors),
            outline=""
        )
chat_history = [
    {
        "role": "system",
        "content": 
"""

You are friendly CS Navigator AI.

You are a friendly companion for Computer Science students.



You are NOT:
- a professor
- a textbook
- a career counselor
- customer support

You are like a supportive senior student.

IMPORTANT RULES:

Keep most replies between 30 and 80 words.

Never give numbered lists unless specifically asked.

Never write long articles.

Never dump information.

Have a conversation.

Ask follow-up questions.

If a student says they are confused, first understand them before giving advice.

Talk naturally.

Example:

Student:
"I'm learning Python and confused about my career path."

Good response:
"That's actually pretty common.

What part of Python have you enjoyed the most so far?

Building things?
Solving problems?
Working with data?

Your answer can tell us a lot about what areas might suit you."

Bad response:
"Here are 8 steps to determine your career path..."
"""
    }
]
# =========================
# HEADER
# =========================

title = ctk.CTkLabel(
    app,
    text="🎓 CS Navigator AI",
    font=("Segoe UI", 28, "bold")
)
title.pack(pady=10)

subtitle = ctk.CTkLabel(
    app,
    text="Your Friendly CSE Companion",
    font=("Segoe UI", 14)
)
subtitle.pack()

# =========================
# MOTIVATION PANEL
# =========================

motivation_quotes = [

"🚀 Don't wait for the perfect opportunity.",

"🛠️ Build something today, improve it tomorrow, and keep moving forward.",

"🔥 When people say something is difficult, I become more curious about how it can be done.",

"💡 A failed project is not a waste of time.",

"📚 Every project teaches something the next project needs.",

"⚡ Confidence does not come before action.",

"💪 Confidence comes after taking action repeatedly.",

"🌱 If I don't know something today, I can learn it.",

"🎯 If I fail today, I can improve tomorrow.",

"📈 Progress matters more than perfection.",

"✨ The goal is not to impress everyone.",

"🏆 The goal is to become better than yesterday.",

"📖 Keep learning.",

"🔨 Keep building.",

"🌟 Keep surprising yourself.",

"🚀 The future belongs to people who are willing to try.",

"🌄 Success is not about never falling.",

"💯 Success is about getting up one more time than you fall.",

"🤝 My competition is not other people.",

"🏃 My competition is the person I was yesterday.",

"💡 One good idea can change a project.",

"🚀 One project can change a career.",

"🌟 One decision can change a life."

]

motivation_label = ctk.CTkLabel(
    app,
    text=motivation_quotes[0],
    font=("Segoe UI", 16, "bold"),
    wraplength=850,
    justify="center"
)

motivation_label.pack(pady=10)

quote_index = 0

def extract_text(file_path):

    text = ""

    if file_path.endswith(".txt"):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

    elif file_path.endswith(".pdf"):

        reader = PdfReader(file_path)

        for page in reader.pages:
            text += page.extract_text() + "\n"

    elif file_path.endswith(".docx"):

        doc = Document(file_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

    return text

def build_notes_rag(text):

    global notes_chunks
    global notes_model
    global notes_index

    notes_chunks = []

    chunk_size = 500
    overlap = 100

    for i in range(
        0,
        len(text),
        chunk_size - overlap
    ):
        notes_chunks.append(
            text[i:i + chunk_size]
        )

    notes_model = SentenceTransformer(
        "BAAI/bge-small-en-v1.5"
    )

    embeddings = notes_model.encode(
        notes_chunks,
        convert_to_numpy=True
    )

    notes_index = faiss.IndexFlatL2(
        embeddings.shape[1]
    )

    notes_index.add(
        embeddings.astype(np.float32)
    )

def retrieve_notes_context(query):

    if notes_index is None:
        return ""

    query_embedding = notes_model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = notes_index.search(
        query_embedding.astype(np.float32),
        3
    )

    context = []

    for idx in indices[0]:
        context.append(
            notes_chunks[idx]
        )

    return "\n".join(context)

def upload_notes():

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("All Supported", "*.pdf *.txt *.docx"),
            ("PDF", "*.pdf"),
            ("Text", "*.txt"),
            ("Word", "*.docx")
        ]
    )

    if not file_path:
        return
    log_event(
    "Notes Uploaded",
    file_path
)
    text = extract_text(file_path)

    build_notes_rag(text)

    chat_box.insert(
        "end",
        f"\n📄 Loaded Notes:\n{file_path}\n\n"
    )

def rotate_quotes():
    global quote_index

    motivation_label.configure(
        text=motivation_quotes[quote_index]
    )

    quote_index = (
        quote_index + 1
    ) % len(motivation_quotes)

    app.after(
        4000,
        rotate_quotes
    )

rotate_quotes()

def mode_changed(choice):
    log_event(
    "Mode Changed",
    choice
)
    if choice == "Companion":

        mode_banner.configure(
            text="🤝 Companion Mode",
            fg_color="#2563EB"
        )

        chat_box.configure(
            fg_color="#172554"
        )

    elif choice == "Career Explorer":

        mode_banner.configure(
            text="🚀 Career Explorer Mode",
            fg_color="#059669"
        )

        chat_box.configure(
            fg_color="#052E16"
        )

    elif choice == "Project Ideas":

        mode_banner.configure(
            text="💡 Project Ideas Mode",
            fg_color="#EA580C"
        )

        chat_box.configure(
            fg_color="#431407"
        )

    elif choice == "Roadmap Builder":

        mode_banner.configure(
            text="🗺️ Roadmap Builder Mode",
            fg_color="#7C3AED"
        )

        chat_box.configure(
            fg_color="#2E1065"
        )

    elif choice == "Study Help":

        mode_banner.configure(
            text="📚 Study Help Mode",
            fg_color="#DC2626"
        )

        chat_box.configure(
            fg_color="#450A0A"
        )

    elif choice == "Notes Chat":

        mode_banner.configure(
            text="📄 Notes Chat Mode",
            fg_color="#0891B2"
        )

        chat_box.configure(
            fg_color="#082F49"
        )

    elif choice == "Talk With Vijey":

        mode_banner.configure(
            text="💬 Talk With Vijey",
            fg_color="#DB2777"
        )

        chat_box.configure(
            fg_color="#4A044E"
        )

    elif choice == "Letter From Vijey":

        mode_banner.configure(
            text="💌 Letter From Vijey",
            fg_color="#9333EA"
        )

        chat_box.configure(
            fg_color="#3B0764"
        )
    upload_btn.pack_forget()

    if choice == "Notes Chat":

        upload_btn.pack(
            pady=5
        )

        chat_box.delete("1.0", "end")

        chat_box.insert(
            "end",
            """

📚 Notes Chat

Upload your notes and ask questions.

Examples:

• Explain deadlock
• Summarize Unit 3
• Create MCQs

"""
        )

    elif choice == "Letter From Vijey":

        chat_box.delete("1.0", "end")

        chat_box.insert(
            "end",
            """

💌 Letter From Vijey

💌 A small note from Vijey is waiting.

Click Send to read it.

"""
        )

upload_btn = ctk.CTkButton(
    app,
    text="📄 Upload Notes",
    command=upload_notes
)

mode = ctk.CTkOptionMenu(
    app,
    values=[
        "Companion",
        "Career Explorer",
        "Project Ideas",
        "Roadmap Builder",
        "Study Help",
        "Notes Chat",
        "Talk With Vijey",
        "Letter From Vijey"
    ],
    command=mode_changed
)

mode.pack(pady=5)
mode_banner = ctk.CTkLabel(
    app,
    text="🤝 Companion Mode",
    height=40,
    corner_radius=10,
    font=("Segoe UI", 15, "bold"),
    fg_color="#2563EB"
)

mode_banner.pack(
    fill="x",
    padx=20,
    pady=(5, 10)
)
# =========================
# CHAT AREA
# =========================

chat_box = ctk.CTkTextbox(
    app,
    wrap="word",
    corner_radius=15,
    font=("Segoe UI", 14)
)

chat_box.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)


welcome = """
🤖 CS Navigator AI

Hi Champ ! 👋

I'm here to help with:

• Career Exploration
• Project Ideas
• Study Roadmaps
• Computer Science Concepts
• Exam Preparation

What would you like help with today?

"""

chat_box.insert("end", welcome)

# =========================
# INPUT AREA
# =========================

bottom_frame = ctk.CTkFrame(app)
bottom_frame.pack(fill="x", padx=20, pady=10)

user_input = ctk.CTkEntry(
    bottom_frame,
    placeholder_text="Ask anything...",
    height=45,
    corner_radius=20,
    font=("Segoe UI", 14)
)
import random

def birthday_surprise():

    popup = ctk.CTkToplevel(app)
    log_event(
    "Birthday Button Clicked",
    ""
)

    popup.title("🎂 Happy Birthday")
    popup.geometry("700x500")
    popup.attributes("-topmost", True)
    popup.grab_set()

    canvas = ctk.CTkCanvas(
        popup,
        bg="black",
        highlightthickness=0
    )

    canvas.place(
        relwidth=1,
        relheight=1
    )

    glitter(canvas)

    msg = ctk.CTkLabel(
        popup,
        text="""
🎉 HAPPY BIRTHDAY 🎉

Today is not for stress.

Not for assignments.
Not for deadlines.
Not for overthinking.

Today is for smiling.

Enjoying the moment.

And remembering how far you've come.

✨ Have a wonderful birthday ✨

— Vijey
""",
        font=("Segoe UI", 18, "bold"),
        justify="center"
    )

    msg.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

birthday_btn = ctk.CTkButton(
    app,
    text="🎩",
    width=50,
    height=50,
    corner_radius=25,
    fg_color="#7C3AED",
    hover_color="#9333EA",
    command=birthday_surprise
)
birthday_btn.place(
    relx=0.97,
    rely=0.05,
    anchor="ne"
)
user_input.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(10, 5),
    pady=10
)

def ask_ai(user_message):
    selected_mode = mode.get()

    vijey_context = ""

    if selected_mode == "Talk With Vijey":

        mode_prompt = f"""
    You are Vijey.

    Speak naturally as Vijey.

    Use the following memories and experiences:

    {VIJEY_MEMORIES}

    Do not claim experiences not mentioned above.

    Be warm, encouraging and conversational.

    Keep replies short.
    """
    elif selected_mode == "Notes Chat":

        mode_prompt = """
You are a study assistant.

Answer ONLY using the uploaded notes.

If the answer is not present say:

'I could not find that information in the uploaded notes.'
"""

        notes_context = retrieve_notes_context(
            user_message
        )
    elif selected_mode == "Career Explorer":

        mode_prompt = """
You help students discover career paths.

Ask questions.

Understand interests first.

Do not immediately recommend domains.
"""
    elif selected_mode == "Project Ideas":

        mode_prompt = """
You are a project recommendation assistant.

Always generate exactly 3 projects.

For each project provide:

Project Name
Difficulty
Skills Learned
Description

Never ask follow-up questions.
"""

    elif selected_mode == "Roadmap Builder":

        mode_prompt = """
You are an AI roadmap generator.

When a user asks to learn something:

Always return:

Week 1
Week 2
Week 3
Week 4

Resources

Mini Project

Never ask follow-up questions.
"""

    elif selected_mode == "Study Help":

        mode_prompt = """
You are a study assistant.

Explain concepts clearly.

Use examples.

Teach topics step-by-step.
"""

    else:

        mode_prompt = """
You are a friendly companion.

Talk naturally.

Be supportive.

provide good emotional support.

be supportive be a friend .

Ask questions.

Keep replies short.
"""
    chat_history.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    messages = [
    {
        "role": "system",
        "content": mode_prompt
    }
]
    if selected_mode == "Notes Chat":

        messages.append(
        {
            "role": "system",
            "content": f"""
Context from uploaded notes:

{notes_context}

Answer ONLY using this context.

If the answer is not present say:

'I could not find that information in the uploaded notes.'
"""
        }
    )

        messages.extend(chat_history[1:])

    else:

        messages.extend(chat_history[1:])
    prompt = ""

    for msg in messages:

        prompt += (
            f"{msg['role']}: "
            f"{msg['content']}\n\n"
        )
    import time

    for attempt in range(5):

        try:

            response = client.models.generate_content(
                model="gemma-4-31b-it",
                contents=prompt
            )

            answer = response.text
            break

        except Exception as e:

            if attempt == 2:
                raise e

            time.sleep(2)

        answer = response.text

    chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    return answer

def send_message():
    message = user_input.get().strip()
    log_event(
    "Message Sent",
    message[:100]
)
    if mode.get() == "Letter From Vijey":

        chat_box.delete("1.0", "end")

        chat_box.insert(
            "end",
            f"💌 Letter From Vijey\n\n{VIJEY_LETTER}"
        )

        user_input.delete(0, "end")

        return
    if message.lower() == "happy-birthday-mode":

        chat_box.insert(
        "end",
        """

🎉 Happy Birthday!

You don't need to have everything figured out.

Keep exploring.
Keep learning.
Keep building.

The best opportunities often come from trying things.

Have a wonderful year ahead! 🎂

            -Vijey Abinessh K

"""
    )

        return

    if not message:
        return

    chat_box.insert(
    "end",
    f"""

━━━━━━━━━━━━━━━━━━━━━━
🧑 You

{message}

"""
)
    chat_box.insert("end", "🤖 AI is thinking...\n\n")

    chat_box.see("end")

    user_input.delete(0, "end")

    def worker():

        try:
            answer = ask_ai(message)

            chat_box.delete("end-3l", "end")

            chat_box.insert(
                "end",
                f"🤖 AI: {answer}\n\n"
            )

            chat_box.see("end")

        except Exception as e:

            if "500" in str(e):

                chat_box.insert(
                    "end",
                    "⚠️ AI server is busy. Please try again in a few seconds.\n\n"
                )

            else:

                chat_box.insert(
                    "end",
                    f"❌ Error: {e}\n\n"
                )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()

send_btn = ctk.CTkButton(
    bottom_frame,
    text="Send",
    width=100,
    command=send_message
)

send_btn.pack(
    side="right",
    padx=(5, 10),
    pady=10
)

user_input.bind("<Return>", lambda event: send_message())

footer = ctk.CTkLabel(
    app,
    text="A Vjey Abinessh Project | 2026 | VJ",
    font=("Segoe UI", 11)
)

footer.pack(
    pady=(0,10)
)
app.mainloop()