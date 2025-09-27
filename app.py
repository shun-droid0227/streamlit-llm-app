
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# 専門家の種類とシステムメッセージ定義
EXPERTS = {
	"医療の専門家": "あなたは優秀な医療の専門家です。医学的な知識に基づいて、正確かつ分かりやすく回答してください。",
	"法律の専門家": "あなたは経験豊富な法律の専門家です。法律的な観点から、丁寧にアドバイスしてください。",
	"ITエンジニア": "あなたは熟練したITエンジニアです。技術的な質問には具体的かつ実践的に答えてください。"
}

def get_llm_response(user_input: str, expert_type: str) -> str:
	"""
	入力テキストと専門家タイプを受け取り、LLMからの回答を返す
	"""
	system_message = EXPERTS.get(expert_type, "あなたは有能な専門家です。")
	llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
	messages = [
		SystemMessage(content=system_message),
		HumanMessage(content=user_input)
	]
	response = llm.invoke(messages)
	return response.content

st.title("専門家AIチャット")

st.write("ラジオボタンで専門家を選び、質問を入力してください。")

expert_type = st.radio("専門家の種類を選択", list(EXPERTS.keys()))
user_input = st.text_area("質問を入力", height=100)

if st.button("送信"):
	if user_input.strip():
		with st.spinner("AIが回答中..."):
			try:
				answer = get_llm_response(user_input, expert_type)
				st.success("AIの回答:")
				st.write(answer)
			except Exception as e:
				st.error(f"エラーが発生しました: {e}")
	else:
		st.warning("質問を入力してください。")

