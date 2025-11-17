import streamlit as st
import os
from datetime import datetime

# --- 基础配置 ---
st.set_page_config(page_title="📝 内容分类记录器", layout="centered")
st.title("🗂️ 内容分类记录器")

# --- 数据存储目录 ---
BASE_DIR = "data_txt"
os.makedirs(BASE_DIR, exist_ok=True)

# --- 读取已有分类 ---
def load_categories():
    files = [f[:-4] for f in os.listdir(BASE_DIR) if f.endswith(".txt")]
    return sorted(files)

# 初始化 session state
if "categories" not in st.session_state:
    st.session_state.categories = load_categories() or ["工作灵感", "网摘", "生活随笔","沙雕网友","待办事项"]

if "show_add_category" not in st.session_state:
    st.session_state.show_add_category = False

# --- 隐藏/显示添加栏目 ---
if st.button("➕ 添加新栏目"):
    st.session_state.show_add_category = not st.session_state.show_add_category

if st.session_state.show_add_category:
    st.subheader("添加新栏目")
    new_category = st.text_input("输入新栏目名称：", placeholder="例如：灵感记录 / 项目日志")

    if st.button("确认添加栏目"):
        if new_category.strip():
            cat_name = new_category.strip()
            if cat_name not in st.session_state.categories:
                st.session_state.categories.append(cat_name)
                # 创建对应 txt 文件
                open(os.path.join(BASE_DIR, f"{cat_name}.txt"), "a", encoding="utf-8").close()
                st.success(f"✅ 已添加新栏目「{cat_name}」！")
            else:
                st.warning("该栏目已存在。")
        else:
            st.warning("请输入有效的栏目名称。")

st.divider()

# --- 选择栏目 ---
category = st.selectbox("选择一个栏目", st.session_state.categories)
file_path = os.path.join(BASE_DIR, f"{category}.txt")

# --- 输入内容 ---
text = st.text_area("输入内容（支持多行）", height=150, placeholder="在这里粘贴或输入内容...")

# --- 保存 ---
if st.button("💾 保存到该栏目"):
    if text.strip():
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}]\n{text.strip()}\n\n"
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(entry)
        st.success(f"已保存到「{category}」！")
    else:
        st.warning("请输入内容后再保存。")

# --- 下载并自动清空（需密码） ---
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    password = st.text_input("请输入下载密码", type="password")
    if st.button(f"📥 下载「{category}」内容（下载后自动清空）"):
        if password == "kkkkk":
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            st.download_button(
                label=f"点击下载「{category}」内容",
                data=content,
                file_name=f"{category}.txt",
                mime="text/plain"
            )
            # 清空文件
            open(file_path, "w", encoding="utf-8").close()
            st.success(f"「{category}」内容已下载并清空。")
        else:
            st.error("❌ 密码错误，无法下载内容。")
else:
    st.info(f"「{category}」目前还没有内容。")
