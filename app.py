import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Smart Student Planner", layout="centered")

st.title("📚 Smart Student Planner App")

# --- FILE STORAGE ---
DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"tasks": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# --- USER INFO ---
st.header("👤 Your Info")

name = st.text_input("Name")
age = st.number_input("Age", 10, 100)
education = st.text_input("Education")
study_hours = st.slider("Study hours/day", 0, 12)
study_days = st.slider("Study days/week", 0, 7)

# --- TASK ADD ---
st.header("📝 To-Do List")

task = st.text_input("Enter task")
deadline = st.date_input("Select deadline")

if st.button("Add Task"):
    if task:
        data["tasks"].append({
            "task": task,
            "deadline": str(deadline),
            "done": False
        })
        save_data(data)
        st.success("Task Added!")

# --- SHOW TASKS ---
st.subheader("Your Tasks")

for i, t in enumerate(data["tasks"]):
    col1, col2, col3, col4 = st.columns([4,1,1,1])

    with col1:
        status = "✅" if t["done"] else "❌"
        st.write(f"{status} {t['task']} (Due: {t['deadline']})")

    with col2:
        if st.button("Done", key=f"done{i}"):
            data["tasks"][i]["done"] = True
            save_data(data)
            st.rerun()

    with col3:
        if st.button("Delete", key=f"del{i}"):
            data["tasks"].pop(i)
            save_data(data)
            st.rerun()

    with col4:
        if st.button("Edit", key=f"edit{i}"):
            st.session_state.edit_index = i

# --- EDIT TASK ---
if "edit_index" in st.session_state:
    idx = st.session_state.edit_index
    st.subheader("✏️ Edit Task")

    new_task = st.text_input("Edit task", data["tasks"][idx]["task"])

    if st.button("Save Changes"):
        data["tasks"][idx]["task"] = new_task
        save_data(data)
        del st.session_state.edit_index
        st.rerun()

# --- REMINDER CHECK ---
st.header("⏰ Reminders")

today = datetime.today().date()

for t in data["tasks"]:
    due_date = datetime.strptime(t["deadline"], "%Y-%m-%d").date()
    if due_date == today and not t["done"]:
        st.warning(f"Reminder: {t['task']} is due today!")

# --- REPORT ---
st.header("📊 Study Report")

if st.button("Generate Report"):
    total_hours = study_hours * study_days

    st.write(f"Weekly Study Hours: {total_hours}")

    completed = sum(1 for t in data["tasks"] if t["done"])
    pending = len(data["tasks"]) - completed

    st.write(f"Completed Tasks: {completed}")
    st.write(f"Pending Tasks: {pending}")

    # Graph
    df = pd.DataFrame({
        "Type": ["Completed", "Pending"],
        "Count": [completed, pending]
    })

    st.bar_chart(df.set_index("Type"))

    if total_hours >= 4:
        st.success("Great consistency! 💪")
    else:
        st.warning("Increase study time 📈")
