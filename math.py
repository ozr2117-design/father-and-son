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
    st.session_state.answered_correctly = False 
if 'show_reward' not in st.session_state:
    st.session_state.show_reward = False 

# === ⚙️ 爸爸的控制台 (侧边栏) ===
with st.sidebar:
    st.header("⚙️ 难度设置")
    max_num = st.slider("最大数字 (几以内加减法)", 5, 50, 10)
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

# === 🎉 奖励展示系统 (加入了新彩蛋角色) ===
def show_random_reward():
    # 儿子喜欢的元素列表 + 新增彩蛋
    rewards = [
        {"icon": "🛡️", "msg": "炫卡斗士：出击！正义的胜利！", "effect": "balloons"},
        {"icon": "🤖", "msg": "托宝战士：变换形态！你太强了！", "effect": "balloons"},
        {"icon": "🎧", "msg": "节奏盒子：嘿哈！这题感太棒了！", "effect": "snow"},
        {"icon": "🦾", "msg": "超级机器人：逻辑电路连接成功！", "effect": "balloons"},
        {"icon": "🐍", "msg": "巨大的蟒蛇：嘶~ 你的脑筋转得真快！", "effect": "snow"},
        {"icon": "🦖", "msg": "霸王龙：吼！你是算术之王！", "effect": "balloons"},
        {"icon": "🚜", "msg": "挖掘机：哔哔！挖到一个满分宝藏！", "effect": "snow"},
        {"icon": "🚒", "msg": "消防车：呜呜呜！你是灭火小英雄！", "effect": "balloons"},
    ]
    
    choice = random.choice(rewards)
    
    # 播放特效
    if choice["effect"] == "balloons":
        st.balloons()
    else:
        st.snow()
    
    # 弹窗提示
    st.toast(choice["msg"], icon=choice["icon"])
    
    # 中央动画
    st.markdown(f"""
        <div style="text-align: center; animation: hero-bounce 0.8s infinite;">
