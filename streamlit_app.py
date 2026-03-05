import streamlit as st
import pandas as pd
import collections

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Baccarat Pattern Analyzer", layout="wide")

st.title("📊 Baccarat Smart Analyzer (AI Pattern)")
st.write("บันทึกข้อมูล Backup สถิติเพื่อประมวลผลโอกาสชนะในตาถัดไป")

# ส่วนที่ 1: การกรอกข้อมูล
st.sidebar.header("📥 Input Data")
raw_input = st.sidebar.text_area("กรอกผลย้อนหลัง (P = Player, B = Banker, T = Tie)", 
                                 "P,B,B,P,P,B,B,B,P,B,P,P,B,P,B,B", height=200)

# ส่วนที่ 2: ประมวลผลข้อมูล
if raw_input:
    # ทำความสะอาดข้อมูล
    data = [x.strip().upper() for x in raw_input.split(",") if x.strip().upper() in ['P', 'B', 'T']]
    
    if len(data) < 3:
        st.warning("กรุณากรอกข้อมูลอย่างน้อย 3 ตาเพื่อให้ระบบเริ่มวิเคราะห์ Pattern")
    else:
        # แสดงสถิติภาพรวม
        st.subheader("📈 สถิติภาพรวมจากข้อมูลของคุณ")
        counts = collections.Counter(data)
        total = len(data)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Player (P)", f"{counts['P']} ครั้ง", f"{(counts['P']/total)*100:.1f}%")
        col2.metric("Banker (B)", f"{counts['B']} ครั้ง", f"{(counts['B']/total)*100:.1f}%")
        col3.metric("Tie (T)", f"{counts['T']} ครั้ง", f"{(counts['T']/total)*100:.1f}%")

        # ส่วนที่ 3: Logic การเดา (Pattern Matching)
        st.divider()
        st.subheader("🎯 การประมวลผลหาโอกาสหน้า (AI Prediction)")
        
        # ดึง 3 ตาล่าสุดมาหา Pattern
        last_3 = data[-3:]
        st.write(f"รูปแบบล่าสุดที่คุณกรอก: **{' -> '.join(last_3)}**")

        # ค้นหาในอดีตว่าถ้าออกแบบนี้ ตาต่อไปออกอะไร
        next_outcomes = []
        for i in range(len(data) - 3):
            if data[i:i+3] == last_3:
                next_outcomes.append(data[i+3])
        
        if next_outcomes:
            prediction = collections.Counter(next_outcomes).most_common(1)[0][0]
            prob = (collections.Counter(next_outcomes)[prediction] / len(next_outcomes)) * 100
            
            if prediction == 'P':
                st.success(f"แนะให้เลือก: **PLAYER** (จากสถิติที่เคยเกิดหลัง {last_3} มีโอกาสแม่นยำ {prob:.1f}%)")
            elif prediction == 'B':
                st.error(f"แนะให้เลือก: **BANKER** (จากสถิติที่เคยเกิดหลัง {last_3} มีโอกาสแม่นยำ {prob:.1f}%)")
            else:
                st.warning(f"แนะให้เลือก: **TIE/เสมอ** (มีโอกาส {prob:.1f}%)")
        else:
            st.info("ยังไม่พบรูปแบบนี้ในอดีต ระบบจะอิงตามความน่าจะเป็นพื้นฐาน: **แนะให้เลือก BANKER** (House Edge ต่ำที่สุด)")

        # ส่วนที่ 4: ตารางบันทึก
        with st.expander("ดูตารางสถิติทั้งหมด"):
            st.table(pd.DataFrame(data, columns=["ผลการออก"]))

st.sidebar.markdown("---")
st.sidebar.info("💡 เคล็ดลับ: ยิ่งกรอกข้อมูล Backup เยอะ (50 ตาขึ้นไป) ระบบจะหา Pattern ได้แม่นยำขึ้น")
