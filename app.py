
import streamlit as st
import os
from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents import get_agents
from utils import save_as_pdf

# Load API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it in environment variables.")
    st.stop()

config = {
    "config_list": [{"model": "gpt-4", "api_key": OPENAI_API_KEY}],
    "temperature": 0.7,
}

st.set_page_config(page_title="Startup Builder AI", layout="wide")
st.title("🚀 AI Startup Builder (AutoGen Multi-Agent)")

startup_idea = st.text_area("Describe your startup idea:", height=150)

if st.button("Build My Startup") and startup_idea.strip():
    with st.spinner("🤖 Agents are working..."):

        # Create agents
        agents = get_agents(config)
        user = UserProxyAgent(name="User", code_execution_config=False)
        groupchat = GroupChat(agents=[user] + agents, messages=[], max_round=12)
        manager = GroupChatManager(groupchat=groupchat, llm_config=config)

        # Start the conversation
        user.initiate_chat(manager, message=startup_idea)

        # Collect agent messages
        agent_outputs = {}
        for msg in groupchat.messages:
            role = msg['sender'].replace("Agent", "").replace("Checker", " Checker").strip()
            if role not in agent_outputs:
                agent_outputs[role] = msg['content']
            else:
                agent_outputs[role] += "\n\n" + msg['content']

    st.success("🎉 Your AI startup is ready!")

    for section, content in agent_outputs.items():
        st.subheader(f"🧠 {section}")
        st.markdown(content)

    if st.button("📄 Download PDF Summary"):
        save_as_pdf(agent_outputs)
        with open("output.pdf", "rb") as f:
            st.download_button("Download output.pdf", f, file_name="startup_summary.pdf", mime="application/pdf")
