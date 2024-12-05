import os

import streamlit as st
from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY'))


def zhipu_generate_text_response(prompt):
    response = client.chat.completions.create(
        model="glm-4-flash",  # 填写需要调用的模型编码
        messages=[
            {"role": "system", "content": "你是一个短视频的文案撰写专家，能够将用户上传的文字，改写成一段适用于短视频配音的文字稿，只要文字，不要有表情符号"},
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )
    return response.choices[0].message.content.strip()


st.set_page_config(page_title="Streamlit 教程",
                   page_icon=":tada:",
                   layout="wide",
                   initial_sidebar_state="auto")



st.subheader("视频文案生成助理")




prompt = st.chat_input("Say something")
if prompt:
    st.chat_message("user").write(prompt)
    text_response = zhipu_generate_text_response(prompt)
    st.chat_message("assistant").write( text_response)

