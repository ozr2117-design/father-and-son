import streamlit as st
import random
import time

# === 🎨 页面配置 ===
st.set_page_config(
    page_title="🦖 爸爸的算术大冒险",
    page_icon="🚜",
    layout="centered"
)

# === 🧠 核心逻辑：初始化状态 ===
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
if 'answered_correctly' not in st.session_state:
    st.session_state.answered_correctly = False # 标记是否答对等待进入下一题
if 'show_reward' not in st.session_state:
    st.session_state.show_reward = False # 专门用来控制“动画是否播放”的标记

# === ⚙️ 爸爸的控制台 (侧边栏) ===
with st.sidebar:
    st.header("⚙️ 难度设置")
    max_num = st.slider("最大数字 (几以内加减法)", 5, 20, 10)
    allow_sub = st.checkbox("启用减法", value=False)
    
    if st.button("重置分数"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# === 🎲 出题函数 ===
def generate_question():
    if allow_sub and random.choice([True, False]):
        op = '-'
    else:
        op = '+'
    
    if op == '+':
        n1 = random.randint(0, max_num)
        n2 = random.randint(0, max_num - n1)
    else:
        n1 = random.randint(0, max_num)
        n2 = random.randint(0, n1)
        
    st.session_state.current_num1 = n1
    st.session_state.current_num2 = n2
    st.session_state.operator = op
    st.session_state.answered_correctly = False
    st.session_state.show_reward = False

# 初次加载出题
if st.session_state.total_count == 0 and st.session_state.current_num1 == 0:
    generate_question()

# === 🎉 奖励展示系统 (重点修改部分) ===
def show_random_reward():
    # 儿子喜欢的元素列表
    rewards = [
        {"icon": "🦖", "msg": "吼！霸王龙为你点赞！", "effect": "balloons"},
        {"icon": "🦕", "msg": "长颈龙说你太棒了！", "effect": "balloons"},
        {"icon": "🚜", "msg": "挖掘机挖到个大宝藏！", "effect": "snow"}, # 挖掘机配雪花更有感觉
        {"icon": "🐶", "msg": "汪汪队立大功！", "effect": "balloons"},
        {"icon": "🐱", "msg": "喵~ 送你一条小鱼干！", "effect": "snow"},
        {"icon": "🚒", "msg": "消防车来啦！冲鸭！", "effect": "balloons"},
    ]
    
    # 随机选一个
    choice = random.choice(rewards)
    
    # 1. 播放全屏特效 (气球或雪花)
    if choice["effect"] == "balloons":
        st.balloons()
    else:
        st.snow()
    
    # 2. 弹窗提示
    st.toast(choice["msg"], icon=choice["icon"])
    
    # 3. 屏幕中央显示巨大的 Emoji 动画
    st.markdown(f"""
        <div style="text-align: center; animation: bounce 1s infinite;">
            <div style="font-size: 100px;">{choice['icon']}</div>
            <h2 style="color: #FF5722;">{choice['msg']}</h2>
        </div>
        <style>
        @keyframes bounce {{
            0%, 20%, 50%, 80%, 100% {{transform: translateY(0);}}
            40% {{transform: translateY(-30px);}}
            60% {{transform: translateY(-15px);}}
        }}
        </style>
    """, unsafe_allow_html=True)

# === 🖥️ 主界面 ===
st.title("🦖 算术大冒险")

# 顶部状态栏
col1, col2 = st.columns(2)
col1.metric("🌟 获得星星", st.session_state.score)
col2.metric("📝 完成题目", st.session_state.total_count)
st.progress(min(st.session_state.score * 10, 100)) # 简单的进度条

st.divider()

# 显示题目
q_str = f"{st.session_state.current_num1} {st.session_state.operator} {st.session_state.current_num2} = ?"
st.markdown(f"<h1 style='text-align: center; font-size: 80px; color: #4CAF50;'>{q_str}</h1>", unsafe_allow_html=True)

# === 🧠 答题逻辑区 ===

# 如果还没有答对，显示输入框
if not st.session_state.answered_correctly:
    
    # 这里的 show_reward 检查非常关键：
    # 如果刷新后发现标记为 True，说明刚才答对了，赶紧播放动画！
    if st.session_state.show_reward:
        show_random_reward()
        st.session_state.show_reward = False # 播完就关掉，防止一直播

    with st.form(key='math_form'):
        user_ans = st.number_input("答案是几？", min_value=0, max_value=100, step=1, label_visibility="collapsed")
        # 按钮样式做大一点
        submit = st.form_submit_button("🚀 发射答案！", use_container_width=True, type="primary")
        
    if submit:
        # 计算正确答案
        if st.session_state.operator == '+':
            real_ans = st.session_state.current_num1 + st.session_state.current_num2
        else:
            real_ans = st.session_state.current_num1 - st.session_state.current_num2
            
        if user_ans == real_ans:
            # ✅ 答对了！
            st.session_state.score += 1
            st.session_state.total_count += 1
            st.session_state.answered_correctly = True 
            st.session_state.show_reward = True # 标记：下次刷新时播放动画
            st.rerun() # 强制刷新，触发“答对状态”的界面
        else:
            # ❌ 答错了
            st.error(f"😅 哎呀，不对哦！再想一想！")

# 如果答对了，隐藏输入框，显示“下一题”按钮和奖励
else:
    # 刚进入这个状态时，因为 show_reward 是 True，所以会先执行上面的 show_random_reward()
    # 然后这里显示“下一题”按钮
    
    # 再次调用奖励显示，确保动画在“下一题”界面也能看到
    if st.session_state.show_reward:
         show_random_reward()
         st.session_state.show_reward = False

    st.success("🎉 答对啦！真棒！")
    
    if st.button("👉 继续挑战下一关！(Next)", type="primary", use_container_width=True):
        generate_question()
        st.rerun()

st.divider()
st.caption("❤️ 爸爸为宝贝开发的专属游戏")
