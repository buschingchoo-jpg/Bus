import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="SA Table 1 Real-time Analyzer")

# 1. เชื่อมต่อ Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. ฟังก์ชันโหลดข้อมูลจาก Sheets
def get_data():
    return conn.read(worksheet="Sheet1")

# 3. ฟังก์ชันบันทึกข้อมูลใหม่ลง Sheets
def add_data(new_result):
    existing_data = get_data()
    new_row = pd.DataFrame([{"result": new_result}])
    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
    conn.update(worksheet="Sheet1", data=updated_df)
    st.cache_data.clear()

st.title("🔴🔵 SA Game Table 1 Tracker")

# ส่วนปุ่มกดบันทึกผล Real-time
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("PLAYER", use_container_width=True, type="primary"):
        add_data("P")
        st.rerun()
with col2:
    if st.button("BANKER", use_container_width=True, type="secondary"):
        add_data("B")
        st.rerun()
with col3:
    if st.button("TIE", use_container_width=True):
        add_data("T")
        st.rerun()

# 4. แสดงผลการวิเคราะห์จากฐานข้อมูลที่จำไว้
df = get_data()
if not df.empty:
    history = df['result'].tolist()
    st.write(f"📊 จำนวนข้อมูลที่จำได้ทั้งหมด: {len(history)} ตา")
    st.write(f"ลำดับล่าสุด: {' -> '.join(history[-10:])}")
    
    # Logic วิเคราะห์แพตเทิร์น (ตัวอย่าง Look-back 3)
    if len(history) >= 4:
        last_3 = history[-3:]
        next_val = []
        for i in range(len(history)-3):
            if history[i:i+3] == last_3:
                next_val.append(history[i+3])
        
        if next_val:
            import collections
            prediction = collections.Counter(next_val).most_common(1)[0][0]
            st.info(f"🎯 จากสถิติที่จำได้ ถ้าออกแบบ {last_3} ตาต่อไปมักออก: {prediction}")
else:
    st.info("เริ่มกดบันทึกผลเพื่อสร้างฐานข้อมูล")
