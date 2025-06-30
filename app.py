
import streamlit as st
import os
import pandas as pd
from autogen import UserProxyAgent, GroupChat, GroupChatManager
from agents import get_agents
from utils import save_as_pdf
from io import StringIO

# Load API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    st.error("OpenAI API key not found. Please set it in environment variables.")
    st.stop()

# Agent config
config = {
    "config_list": [{"model": "gpt-3.5-turbo", "api_key": OPENAI_API_KEY}],
    "temperature": 0.7,
}

st.set_page_config(page_title="Startup Builder AI", layout="wide")
st.title("🚀 AI Startup Builder (AutoGen Multi-Agent)")

# Text input
startup_idea = st.text_area(
    "Describe your startup idea:",
    height=150,
    placeholder="Ex: I want to build a startup around Ayurvedic protein powders for gamers..."
)

# Run agents on button click
if st.button("Build My Startup") and startup_idea.strip():
    with st.spinner("🤖 Agents are thinking..."):
        agents = get_agents(config)
        user = UserProxyAgent(name="User", code_execution_config=False)
        groupchat = GroupChat(agents=[user] + agents, messages=[], max_round=8)
        manager = GroupChatManager(groupchat=groupchat, llm_config=config)
        st.write("✅ Agents initialized:", [agent.name for agent in agents])


        # Initiate chat
        user.initiate_chat(manager, message=startup_idea)
        manager.run()

        st.write("✅ Chat initiated. Messages in GroupChat:", groupchat.messages)
        



        # Gather outputs
        agent_outputs = {}
        for msg in groupchat.messages:
            if 'sender' not in msg or 'content' not in msg:
                continue
            role = msg['sender'].replace("Agent", "").replace("Checker", " Checker").strip()
            if role not in agent_outputs:
                agent_outputs[role] = msg['content']
            else:
                agent_outputs[role] += "\n" + msg['content']
        st.write("Agent Outputs Collected:", agent_outputs)

    st.success("🎉 Your AI startup is ready!")

    # Display agent outputs
    for section, content in agent_outputs.items():
        st.subheader(f"🧠 {section}")
        if "|---" in content and "|" in content:
            try:
                table_lines = [line.strip() for line in content.splitlines() if "|" in line]
                table_text = "\n".join(table_lines)
                df = pd.read_csv(StringIO(table_text), sep="|", engine="python")
                df.columns = [col.strip() for col in df.columns]
                df = df.dropna(axis=1, how="all")
                st.dataframe(df)
            except Exception:
                st.markdown(content)
        else:
            st.markdown(content)

    # Generate PDF and show download button
    if agent_outputs:
        pdf_buffer = save_as_pdf(agent_outputs)
        st.download_button(
            label="📥 Download PDF Summary",
            data=pdf_buffer,
            file_name="startup_summary.pdf",
            mime="application/pdf"
        )
    else:
        st.warning( "No agent outputs to include in PDF.")


