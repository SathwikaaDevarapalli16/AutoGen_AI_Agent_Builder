
import streamlit as st
import os
import pandas as pd
from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents import get_agents
from utils import save_as_pdf

# Set page config
st.set_page_config(page_title="Startup Builder AI", layout="wide")
st.title("🚀 AI Startup Builder (AutoGen Multi-Agent)")

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("❌ OpenAI API key not found. Please set it in environment variables.")
    st.stop()

# Agent config
config = {
    "config_list": [{"model": "gpt-3.5-turbo", "api_key": OPENAI_API_KEY}],
    "temperature": 0.7,
}

# Input box
startup_idea = st.text_area(
    "Describe your startup idea:",
    height=150,
    placeholder="Example: I want to build a startup for Ayurvedic protein powder for gamers..."
)

# On click
if st.button("Build My Startup") and startup_idea.strip():
    with st.spinner("🤖 Agents are building your startup..."):

        # Setup agents
        agents = get_agents(config)
        user = UserProxyAgent(name="User", code_execution_config=False)
        groupchat = GroupChat(agents=[user] + agents, messages=[], max_round=8)
        manager = GroupChatManager(groupchat=groupchat, llm_config=config)

        # Run multi-agent convo
        user.initiate_chat(manager, message=startup_idea)

        # Collect outputs
        agent_outputs = {}
        for msg in groupchat.messages:
            if 'sender' not in msg or 'content' not in msg:
                continue
            role = msg['sender'].replace("Agent", "").replace("Checker", " Checker").strip()
            agent_outputs.setdefault(role, "")
            agent_outputs[role] += msg['content'] + "

"

    # Show results
    st.success("🎉 Your AI startup is ready!")

    for section, content in agent_outputs.items():
        st.subheader(f"🧠 {section}")
        if "|---" in content and "|" in content:
            try:
                from io import StringIO
                table_lines = [line.strip() for line in content.splitlines() if "|" in line]
                table_text = "
".join(table_lines)
                df = pd.read_csv(StringIO(table_text), sep="|", engine="python")
                df.columns = [col.strip() for col in df.columns]
                df = df.dropna(axis=1, how="all")
                st.dataframe(df)
            except Exception as e:
                st.markdown(content)
        else:
            st.markdown(content)

    # Download button
    pdf_buffer = save_as_pdf(agent_outputs)
    st.download_button(
        label="📥 Download PDF Summary",
        data=pdf_buffer,
        file_name="startup_summary.pdf",
        mime="application/pdf"
    )

