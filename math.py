import streamlit as st
import random
import time

# === 🎨 页面配置 ===
st.set_page_config(
    page_title="🦖 爸爸的算术大冒险 v2.0",
    page_icon="🤖",
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
    st.header("⚙️ 冒险难度")
    max_num = st.slider("数字范围", 5, 100, 10)
    allow_sub = st.checkbox("开启减法挑战", value=False)
    
    if st.button("重置冒险进度"):
        for key in list(st.session_state.keys()):
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

if st.session_state.total_count == 0 and st.session_state.current_num1 == 0:
    generate_question()

# === 🎉 动画片角色奖励库 (重点更新) ===
def show_random_reward():
    # 结合了炫卡斗士、托宝战士、迷你特工队、咖宝车神等角色
    rewards = [
        {"icon": "🛡️", "name": "炫卡斗士", "msg": "激战炫卡！正义之魂在燃烧！", "color": "#FF3D00"},
        {"icon": "🚗", "name": "咖宝车神", "msg": "咖宝车神，即刻变换！出发救援！", "color": "#2979FF"},
        {"icon": "🦊", "name": "迷你特工队", "msg": "特工召唤！弗特、露西为你点赞！", "color": "#D50000"},
        {"icon": "🤖", "name": "托宝战士", "msg": "托宝战士，变型！你是最棒的搭档！", "color": "#FFAB00"},
        {"icon": "⚡", "name": "迷你特工", "msg": "最强战士！能量全开，耶！", "color": "#00E5FF"},
        {"icon": "🏎️", "name": "咖宝车神", "msg": "超级变换！你是计算小能手！", "color": "#76FF03"},
        {"icon": "🦸", "name": "炫卡斗士", "msg": "英雄出击！下一题也难不倒你！", "color": "#AA00FF"},
    ]
    
    choice = random.choice(rewards)
    
    # 播放全屏效果
    if random.choice([True, False]):
        st.balloons()
    else:
        st.snow()
    
    # 炫酷的中央提示
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 20px; background: rgba(255,255,255,0.1); border: 3px solid {choice['color']}; animation: hero-pop 0.6s ease-out;">
            <div style="font-size: 110px; margin-bottom: 10px;">{choice['icon']}</div>
            <h2 style="color: {choice['color']}; font-family: 'MicroSoft YaHei';">{choice['name']}</h2>
            <h3 style="color: #333;">{choice['msg']}</h3>
        </div>
        <style>
        @keyframes hero-pop {{
            0% {{ transform: scale(0.5); opacity: 0; }}
            80% {{ transform: scale(1.1); opacity: 1; }}
            100% {{ transform: scale(1); }}
        }}
        </style>
    """, unsafe_allow_html=True)
    st.toast(f"{choice['name']} 发来贺电！", icon=choice["icon"])

# === 🖥️ 主界面 ===
st.title("🌟 英雄算术大冒险")

# 英雄得分板
cols = st.columns(3)
cols[0].metric("⭐ 英雄勋章", st.session_state.score)
cols[1].metric("⚔️ 击败怪兽", st.session_state.total_count)
cols[2].write(f"### 难度: {max_num}")
st.progress(min(st.session_state.score * 10, 100))

st.divider()

# 题目显示
q_str = f"{st.session_state.current_num1} {st.session_state.operator} {st.session_state.current_num2} = ?"
st.markdown(f"<div style='text-align: center;'><span style='font-size: 100px; font-weight: bold; color: #448AFF; border-bottom: 5px solid #448AFF;'>{q_str}</span></div>", unsafe_allow_html=True)
st.write("") # 留白

# === 🧠 答题逻辑区 ===
if not st.session_state.answered_correctly:
    
    # 即使在答题状态，如果刚刚答对了刷新回来，也会显示奖励
    if st.session_state.show_reward:
        show_random_reward()
        st.session_state.show_reward = False

    with st.form(key='hero_form', clear_on_submit=True):
        st.write("### ⌨️ 请输入英雄答案：")
        user_ans = st.number_input("答案", value=None, min_value=0, max_value=200, step=1, label_visibility="collapsed", placeholder="输入答案...")
        submit = st.form_submit_button("🔥 确认发射！", use_container_width=True, type="primary")
        
    if submit:
        if user_ans is None:
            st.warning("队长，请输入答案再发射！")
        else:
            real_ans = st.session_state.current_num1 + st.session_state.current_num2 if st.session_state.operator == '+' else st.session_state.current_num1 - st.session_state.current_num2
            if user_ans == real_ans:
                st.session_state.score += 1
                st.session_state.total_count += 1
                st.session_state.answered_correctly = True 
                st.session_state.show_reward = True 
                st.rerun()
            else:
                st.error(f"❌ 能量不足！再算一次，你可以的！")

else:
    # 答对状态显示
    show_random_reward()
    st.session_state.show_reward = False
    
    st.success("🎉 完美一击！")
    if st.button("👉 前往下一关 (Next Mission)", type="primary", use_container_width=True):
        generate_question()
        st.rerun()

st.divider()
st.caption("🛡️ 专属特工训练器 | 爸爸牌出品")
