import streamlit as st
import random

# === 🎨 页面配置 ===
st.set_page_config(
    page_title="🦖 爸爸牌·算术大闯关",
    page_icon="💯",
    layout="centered"
)

# === 🧠 核心逻辑：初始化状态 (Session State) ===
# Streamlit 每次点击按钮都会刷新整个代码，所以必须把
# “当前的题目”和“分数”存在 session_state 里，否则一刷新题目就变了
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_count' not in st.session_state:
    st.session_state.total_count = 0
if 'current_num1' not in st.session_state:
    st.session_state.current_num1 = 0
if 'current_num2' not in st.session_state:
    st.session_state.current_num2 = 0
if 'operator' not in st.session_state:
    st.session_state.operator = '+'
if 'answered' not in st.session_state:
    st.session_state.answered = False # 标记当前题是否已答

# === ⚙️ 爸爸的控制台 (侧边栏) ===
with st.sidebar:
    st.header("⚙️ 爸爸的控制台")
    st.write("悄悄调整难度，不要让小朋友看到哦！")
    max_num = st.slider("最大数字范围", 5, 20, 10) # 默认10以内
    allow_sub = st.checkbox("启用减法", value=False) # 默认只做加法
    
    if st.button("重置所有分数"):
        st.session_state.score = 0
        st.session_state.total_count = 0
        st.rerun()

# === 🎲 出题函数 ===
def generate_question():
    # 随机决定是加法还是减法
    if allow_sub and random.choice([True, False]):
        op = '-'
    else:
        op = '+'
    
    if op == '+':
        n1 = random.randint(0, max_num)
        n2 = random.randint(0, max_num - n1) # 保证结果不超过 max_num
    else:
        n1 = random.randint(0, max_num)
        n2 = random.randint(0, n1) # 保证结果不为负数
        
    st.session_state.current_num1 = n1
    st.session_state.current_num2 = n2
    st.session_state.operator = op
    st.session_state.answered = False

# 如果是第一次运行（数字都是0），先出个题
if st.session_state.current_num1 == 0 and st.session_state.current_num2 == 0 and st.session_state.total_count == 0:
    generate_question()

# === 🖥️ 主界面展示 ===
st.title("🦖 算术大闯关")
st.caption("加油！答对有奖励哦！")

# 进度条
col_score1, col_score2 = st.columns(2)
col_score1.metric("🌟 小星星 (得分)", st.session_state.score)
col_score2.metric("📝 已做题目", st.session_state.total_count)

st.divider()

# 显示巨大的题目
# 使用 Markdown 和 HTML 语法把字体弄得超级大
question_str = f"{st.session_state.current_num1} {st.session_state.operator} {st.session_state.current_num2} = ?"
st.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #4CAF50;'>{question_str}</h1>", unsafe_allow_html=True)

st.divider()

# 答题区域
if not st.session_state.answered:
    # 使用 form 表单，这样按回车键也能提交
    with st.form(key='answer_form'):
        user_ans = st.number_input("请输入答案：", min_value=0, max_value=100, step=1, label_visibility="collapsed")
        submit_btn = st.form_submit_button(label='🚀 发射答案！', use_container_width=True)
    
    if submit_btn:
        # 计算正确答案
        if st.session_state.operator == '+':
            correct_ans = st.session_state.current_num1 + st.session_state.current_num2
        else:
            correct_ans = st.session_state.current_num1 - st.session_state.current_num2
        
        # 判断对错
        if user_ans == correct_ans:
            st.session_state.score += 1
            st.balloons() # 🎉 放气球特效！
            st.success(f"🎉 太棒了！答案就是 {correct_ans}！")
        else:
            st.error(f"😅 哎呀，差点点！正确答案是 {correct_ans} 哦。")
        
        st.session_state.total_count += 1
        st.session_state.answered = True
        st.rerun() # 刷新页面显示结果

else:
    # 如果已经答完了，显示“下一题”按钮
    if st.button("👉 下一题 (Next)", type="primary", use_container_width=True):
        generate_question()
        st.rerun()

# 底部装饰
st.markdown("---")
st.markdown("<center>❤️ 爸爸用 Python 为你制作 ❤️</center>", unsafe_allow_html=True)
