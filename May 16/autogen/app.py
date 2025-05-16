import streamlit as st
import autogen

# === LLM config ===
config_list = [
    {
        'model': 'gemini-2.0-flash',
        'api_key': 'AIzaSyAtY7Pm8uXIYQez_Bt251_zYQg3OORsm2A',  # Replace with your API key
        "api_type": "google",
    }
]

llm_config = {
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

# === Initialize assistant and user_proxy ===
assistant = autogen.AssistantAgent(
    name="CTO",
    llm_config=llm_config,
    system_message="Chief technical officer of a tech company"
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web", "use_docker": False},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

st.title("AI Assistant Chat Demo")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_area("Enter your task for the assistant", height=100)

if st.button("Send Task to Assistant"):
    if user_input.strip():
        # Send task to assistant
        user_proxy.initiate_chat(assistant, message=user_input)
        
        # Try to get last assistant reply from user_proxy history
        last_message = None
        if hasattr(user_proxy, 'history') and len(user_proxy.history) > 0:
            last_message = user_proxy.history[-1]
        
        if last_message and 'content' in last_message:
            reply = last_message['content']
        else:
            # Mock reply if autogen does not return history immediately
            reply = "This is a mock assistant reply. Replace this with actual autogen reply."
        
        # Append user input and assistant reply to chat history
        st.session_state['chat_history'].append(("User", user_input))
        st.session_state['chat_history'].append(("Assistant", reply))

# Display chat history
for sender, message in st.session_state['chat_history']:
    if sender == "User":
        st.markdown(f"**User:** {message}")
    else:
        st.markdown(f"**Assistant:** {message}")
