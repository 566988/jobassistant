import streamlit as st
from parser import parse_resume
from llm_chain import analyze_resume, rewrite_experience
import os

st.set_page_config(page_title="AI求职助手", page_icon="📝", layout="wide")
st.title("📝 AI 求职助手 - 简历优化 & 职位匹配（通义千问）")

# 初始化 session state
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

# 侧边栏：DashScope API Key 配置
with st.sidebar:
    st.header("🔑 配置")
    # 从环境变量或 Streamlit secrets 读取 API Key
    dashscope_key = os.environ.get("DASHSCOPE_API_KEY", st.secrets.get("DASHSCOPE_API_KEY", ""))
    user_api_key = st.text_input("输入你的 DashScope API Key", value=dashscope_key, type="password")
    if user_api_key:
        os.environ["DASHSCOPE_API_KEY"] = user_api_key
        st.success("API Key 已设置 ✅")
    else:
        st.warning("请输入 DashScope API Key 才能使用 AI 功能")

    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("""
    1. 上传你的简历（PDF/Word/TXT）
    2. 粘贴目标职位的描述
    3. 点击“开始分析”获取匹配度和优化建议
    4. 可选：对某段经历进行 AI 重写优化
    """)

# 主界面布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 上传简历")
    uploaded_file = st.file_uploader("支持 PDF, DOCX, TXT", type=["pdf", "docx", "txt"])
    if uploaded_file is not None:
        try:
            st.session_state.resume_text = parse_resume(uploaded_file)
            st.success("简历解析成功！")
            with st.expander("查看解析后的文本"):
                st.text(st.session_state.resume_text[:2000])
        except Exception as e:
            st.error(f"解析失败: {e}")

with col2:
    st.subheader("🎯 目标职位描述")
    jd_input = st.text_area("粘贴职位描述（Job Description）", height=250, value=st.session_state.jd_text)
    if jd_input:
        st.session_state.jd_text = jd_input

# 分析按钮
if st.button("🔍 开始分析", type="primary", disabled=not (user_api_key and st.session_state.resume_text and st.session_state.jd_text)):
    with st.spinner("AI 正在深度分析中，请稍候..."):
        try:
            analysis = analyze_resume(st.session_state.resume_text, st.session_state.jd_text)
            st.session_state.analysis_result = analysis
        except Exception as e:
            st.error(f"分析出错: {e}")

# 显示分析结果
if st.session_state.analysis_result:
    st.markdown("---")
    st.header("📊 分析结果")
    st.markdown(st.session_state.analysis_result)

# 单段经历优化
st.markdown("---")
st.subheader("✏️ 单段经历优化")
experience_input = st.text_area("粘贴你想优化的一段经历（如一个工作职责描述）")
if st.button("✨ 基于 JD 优化这段经历", disabled=not (user_api_key and experience_input and st.session_state.jd_text)):
    with st.spinner("重写中..."):
        try:
            rewritten = rewrite_experience(experience_input, st.session_state.jd_text)
            st.markdown("**优化后：**")
            st.text(rewritten)
        except Exception as e:
            st.error(f"重写出错: {e}")