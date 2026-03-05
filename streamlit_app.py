import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import collections

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="SA Table 1 Real-time Analyzer", layout="centered")

# 2. การเชื่อมต่อ Google Sheets (ต้องตั้งค่า Secrets ใน Streamlit ด้วย)
conn = st.connection("gsheets", type=GSheetsConnection)

# ฟังก์ชันสำหรับดึงข้อมูล
def get_data():
    try:
        # ดึงข้อมูลจากไฟล์ Google Sheets แถบที่ชื่อว่า Sheet1
        return conn.read(worksheet="Sheet1", ttl="0")
    except Exception as e:
        st.error(f"เชื่อมต่อ Google Sheets ไม่สำเร็จ: ตรวจสอบชื่อ Sheet1 และการแชร์ไฟล์")
        return pd.DataFrame(columns=["result"])

# ฟังก์ชันสำหรับบันทึกข้อมูลใหม่
def add_data(new_result):
    existing_data = get_data()
    new_row = pd.DataFrame([{"result": new_result}])
    updated_df = pd.concat([existing_data, new_row], ignore_index=True)
    # อัปเดตข้อมูลกลับไปยัง Google Sheets
    conn.update(worksheet="Sheet1", data=updated_df)
    st.cache_data.clear()

# --- ส่วนแสดงผลหน้าเว็บ ---
st.title("🔴🔵 SA Game Table 1 Tracker")
st.markdown("บันทึกผลเรียลไทม์ ข้อมูลจะถูกเก็บไว้ใน Google Sheets ตลอดไป")

# ส่วนปุ่มกดบันทึกผล
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔵 PLAYER", use_container_width=True, type="primary"):
        add_data("P")
        st.rerun()
with col2:
    if st.button("🔴 BANKER", use_container_width=True, type="secondary"):
        add_data("B")
        st.rerun()
with col3:
    if st.button("🟢 TIE", use_container_width=True):
        add_data("T")
        st.rerun()

st.divider()

# 3. ส่วนวิเคราะห์ผล (Logic การจำแพตเทิร์น)
df = get_data()
if not df.empty and 'result' in df.columns:
    history = df['result'].dropna().tolist()
    
    # แสดงสถิติล่าสุด
    st.subheader(f"📊 สถิติทั้งหมด: {len(history)} ตา")
    st.write(f"ลำดับล่าสุด: **{' -> '.join(history[-10:])}**")
    
    # วิเคราะห์แพตเทิร์น (Look-back 3)
    if len(history) >= 4:
        last_3 = history[-3:]
        next_val = []
        for i in range(len(history)-3):
            if history[i:i+3] == last_3:
                next_val.append(history[i+3])
        
        if next_val:
            prediction = collections.Counter(next_val).most_common(1)[0][0]
            prob = (collections.Counter(next_val)[prediction] / len(next_val)) * 100
            
            st.info(f"🎯 วิเคราะห์จากสถิติ: หลังออก **{last_3}** ตาต่อไปมักออก **{prediction}** (โอกาส {prob:.1f}%)")
        else:
            st.warning("⚠️ ยังไม่พบแพตเทิร์นนี้ในฐานข้อมูล")
    else:
        st.info("กรุณากดบันทึกผลให้ครบอย่างน้อย 4 ตา เพื่อเริ่มการวิเคราะห์")
else:
    st.error("ไม่พบข้อมูลใน Google Sheets หรือชื่อหัวข้อในช่อง A1 ไม่ใช่ 'result'")

# ส่วนล้างข้อมูล (เผื่อเริ่มขอนใหม่)
if st.sidebar.button("🧹 ล้างข้อมูลทั้งหมดใน Sheets"):
    empty_df = pd.DataFrame(columns=["result"])
    conn.update(worksheet="Sheet1", data=empty_df)
    st.cache_data.clear()
    st.rerun()
