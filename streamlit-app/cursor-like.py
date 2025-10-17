import streamlit as st
from openai import OpenAI
import os
import re

# --- Setup ---
client = OpenAI(api_key="")

st.set_page_config(page_title="Pseudo-Cursor", layout="wide")

# --- Title ---
st.markdown(
    """
    <h1 style="text-align:center; margin-bottom: 0;">💻 Pseudo-Cursor: GPT-Driven Code Editor</h1>
    <hr style="margin-top:0.5rem; margin-bottom:1.5rem;">
    """,
    unsafe_allow_html=True,
)

# --- Initialize session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "code" not in st.session_state:
    st.session_state.code = "print('Hello world!')"
if "code_key" not in st.session_state:
    st.session_state.code_key = 0
if "filename" not in st.session_state:
    st.session_state.filename = "main.py"

# --- Layout: 2 columns, each 50% ---
code_col, chat_col = st.columns([1, 1], gap="large")

# ===================== LEFT SIDE =====================
with code_col:
    # --- File Controls ---
    control_col1, control_col2, control_col3, control_col4 = st.columns([2, 1, 1, 1])

    with control_col1:
        uploaded_file = st.file_uploader("📂 Drag & Drop or Browse", type=["py", "txt"])
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            if file_bytes:
                file_content = file_bytes.decode("utf-8")
                st.session_state.code = file_content
                st.session_state.filename = uploaded_file.name
                st.session_state.code_key += 1
                st.toast(f"Loaded {uploaded_file.name}")

    with control_col2:
        if st.button("💾 Save", use_container_width=True):
            with open(st.session_state.filename, "w", encoding="utf-8") as f:
                f.write(st.session_state.code)
            st.toast(f"Saved to {st.session_state.filename}")

    with control_col3:
        new_name = st.text_input("Save as", st.session_state.filename, label_visibility="collapsed")
        if st.button("💾 Save As", use_container_width=True):
            with open(new_name, "w", encoding="utf-8") as f:
                f.write(st.session_state.code)
            st.session_state.filename = new_name
            st.toast(f"Saved as {new_name}")

    with control_col4:
        if st.button("🧹 Reset", use_container_width=True):
            st.session_state.code = ""
            st.session_state.code_key += 1
            st.toast("Editor cleared")

    # --- Code Editor ---
    st.markdown(f"### 🧠 Editing: `{st.session_state.filename}`")
    st.session_state.code = st.text_area(
        "Code Editor",
        value=st.session_state.code,
        key=f"code_area_{st.session_state.code_key}",
        height=550,
        label_visibility="collapsed"
    )

# ===================== RIGHT SIDE =====================
with chat_col:
    st.markdown("### 💬 Chat with GPT-4o-mini")

    # Display previous conversation
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input aligned with code editor
    prompt = st.chat_input("Ask GPT to modify or explain your code…")

# ===================== PROCESS GPT =====================
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert code editor. "
                            "When the user asks for a change, output ONLY the full updated code "
                            "inside a fenced code block like:\n```python\n# code\n```\n"
                            "If no changes are needed, explain why."
                        ),
                    },
                    *st.session_state.messages,
                    {"role": "user", "content": f"Current code:\n```python\n{st.session_state.code}\n```"},
                ],
            )

            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            # --- Extract and apply new code ---
            match = re.search(r"```(?:python)?\n([\s\S]*?)```", reply)
            if match:
                new_code = match.group(1).strip()
                st.session_state.code = new_code
                st.session_state.code_key += 1
                st.success("✅ Code updated from GPT suggestion!")
                st.rerun()

# ===================== Styling =====================
st.markdown("""
<style>
h1, h3, h4, h5 { text-align:center; }
textarea {
    font-family: monospace;
    font-size: 14px !important;
    background-color: #1e1e1e !important;
    color: #eaeaea !important;
}
div[data-testid="stFileUploaderDropzone"] {
    border: 1px dashed #888 !important;
    border-radius: 10px;
    background-color: #222 !important;
}
</style>
""", unsafe_allow_html=True)
