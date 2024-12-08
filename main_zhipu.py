import asyncio
import os

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.chat_models import ChatZhipuAI

import streamlit as st

st.set_page_config(page_title="Streamlit 教程",
                   page_icon=":tada:",
                   layout="wide",
                   initial_sidebar_state="auto")

st.subheader("我的聊天机器人")

# 初始化聊天历史（放在会话状态中）
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

# 初始化模型和prompt template
model = ChatZhipuAI(model="glm-4-flash",api_key=os.getenv('ZHIPU_API_KEY'))
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个友好的助手。请记住用户告诉你的信息，特别是用户的名字等个人信息。"),
    MessagesPlaceholder("msgs")
])

chain = prompt_template | model

st.sidebar.subheader("功能区")
# 添加清除按钮
if st.sidebar.button("清除对话历史"):
    st.session_state.chat_history = ChatMessageHistory()
    st.rerun()

# 显示聊天历史
for message in st.session_state.chat_history.messages:
    if isinstance(message, HumanMessage):
        st.chat_message("user").write(message.content)
    elif isinstance(message, AIMessage):
        st.chat_message("assistant").write(message.content)

# 处理用户输入
prompt = st.chat_input("Say something")

if prompt:
    st.chat_message("user").write(prompt)
    
    with st.spinner("思考中..."):  # 添加加载提示
        async def get_response():
            response = await chain.ainvoke({
                "msgs": st.session_state.chat_history.messages + [HumanMessage(content=prompt)]
            })
            return response
        
        response = asyncio.run(get_response())
    
    # 更新聊天历史
    st.session_state.chat_history.add_user_message(prompt)
    st.session_state.chat_history.add_ai_message(response.content)
    
    # 显示助手回复
    st.chat_message("assistant").write(response.content)
