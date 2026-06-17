from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

def get_llm():
    return ChatTongyi(model="qwen-plus", temperature=0.3)

# 提示模板（不变）
analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert career coach and resume writer. 
Analyze the resume against the job description provided.
Output the following in a structured format:

1. Match Score: Give a percentage (0-100%) based on overall qualification fit.
2. Key Matching Points: List what the candidate meets well.
3. Missing Requirements: List what is missing or could be strengthened.
4. Keyword Suggestions: Important keywords from the JD that should be added if applicable.
5. Resume Optimization Suggestions: Specific, actionable advice to tailor the resume, including rewritten summary, bullet point improvements, and skills to highlight.

Use plain English, be direct and helpful."""),
    ("human", "Resume:\n{resume}\n\nJob Description:\n{jd}")
])

rewrite_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert resume writer. Rewrite the given experience bullet point to better match the job description. 
Use strong action verbs, include quantifiable achievements if possible, and mirror keywords from the JD.
Return only the rewritten bullet point(s)."""),
    ("human", "Original: {experience}\nTarget Job Description: {jd}\nRewritten Version:")
])

def analyze_resume(resume_text, jd_text):
    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=analysis_prompt)
    return chain.run(resume=resume_text, jd=jd_text)

def rewrite_experience(experience_text, jd_text):
    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=rewrite_prompt)
    return chain.run(experience=experience_text, jd=jd_text)
