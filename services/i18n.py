"""Translations (English / Thai). Pages call tr(lang, key, **values)."""

LANGS = {"en": "EN", "th": "ไทย"}

STRINGS = {
    # ---------------------------------------------------------------- navigation
    "sec_overview": {"en": "Overview", "th": "ภาพรวม"},
    "sec_calc": {"en": "Calculators", "th": "เครื่องคำนวณ"},
    "sec_data": {"en": "Data & Innovation", "th": "ข้อมูลและนวัตกรรม"},
    "sec_team": {"en": "Team", "th": "ทีม"},
    "nav_home": {"en": "Home", "th": "หน้าแรก"},
    "nav_stats": {"en": "Statistics", "th": "สถิติพื้นฐาน"},
    "nav_bayes": {"en": "Bayes' Theorem", "th": "ทฤษฎีบทของเบย์ส"},
    "nav_markov": {"en": "Markov Text Prediction", "th": "ทำนายคำด้วย Markov"},
    "nav_data": {"en": "Data Viewer", "th": "ดูข้อมูลดิบ"},
    "nav_custom": {"en": "StudyCast (Custom App)", "th": "StudyCast (แอปประยุกต์)"},
    "nav_members": {"en": "Members", "th": "สมาชิกกลุ่ม"},
    "theme_dark": {"en": "Dark mode", "th": "โหมดมืด"},
    "theme_light": {"en": "Light mode", "th": "โหมดสว่าง"},
    "theme_help": {"en": "Switch between dark and light theme", "th": "สลับธีมมืด / สว่าง"},
    "lang_label": {"en": "Language", "th": "ภาษา"},
    "footer": {"en": "CS207 / ST207 · Section 227C · Group 1", "th": "CS207 / ST207 · Section 227C · กลุ่ม 1"},

    # ---------------------------------------------------------------- home
    "home_title": {"en": "📐 Stats & Math Lab", "th": "📐 Stats & Math Lab"},
    "home_tagline": {
        "en": "A web application for statistics, probability, Markov chains and applied mathematics",
        "th": "เว็บแอปพลิเคชันสำหรับการคำนวณสถิติ ความน่าจะเป็น Markov Chain และคณิตศาสตร์ประยุกต์",
    },
    "home_name_h": {"en": "Project name", "th": "ชื่อโปรเจกต์"},
    "home_name_rows": {
        "en": [("Project", "Stats & Math Lab"),
               ("Type", "Streamlit Web Application (Mono-repo, runs on localhost)"),
               ("Project folder", "sec227C-1-project"),
               ("Course", "CS207 / ST207 · Section 227C · Group 1")],
        "th": [("ชื่อโปรเจกต์", "Stats & Math Lab"),
               ("ประเภท", "Streamlit Web Application (Mono-repo รันผ่าน localhost)"),
               ("โฟลเดอร์โปรเจกต์", "sec227C-1-project"),
               ("รายวิชา", "CS207 / ST207 · Section 227C · กลุ่ม 1")],
    },
    "home_overview_h": {"en": "System overview", "th": "ภาพรวมของระบบ"},
    "home_overview": {
        "en": "Stats & Math Lab brings five math tools together in one web app: descriptive statistics, "
              "Bayes' theorem, Markov chain text prediction, a raw-data viewer, and **StudyCast**, our own app "
              "that predicts exam grades with Softmax/Sigmoid models built from matrices and derivatives.\n\n"
              "The code follows **Strict Separation of Concerns**: files in `pages/` only take input and show "
              "results, every calculation lives in `services/`, and raw data is read from `data/`.",
        "th": "Stats & Math Lab รวมเครื่องมือคณิตศาสตร์ 5 อย่างไว้ในเว็บแอปเดียว ได้แก่ สถิติเชิงพรรณนา, "
              "ทฤษฎีบทของเบย์ส, การทำนายคำด้วย Markov Chain, หน้าดูข้อมูลดิบ และ **StudyCast** "
              "แอปที่กลุ่มคิดขึ้นเองเพื่อทำนายเกรดด้วยโมเดล Softmax/Sigmoid ที่สร้างจากเมทริกซ์และอนุพันธ์\n\n"
              "โค้ดแยกส่วนตามหลัก **Strict Separation of Concerns**: ไฟล์ใน `pages/` ทำหน้าที่รับค่าและแสดงผลเท่านั้น, "
              "การคำนวณทั้งหมดอยู่ใน `services/` และข้อมูลดิบอ่านมาจาก `data/`",
    },
    "home_flow": {
        "en": "**How a request flows:** user input → `pages/*.py` (UI) → `services/*.py` (calculation) → result → UI shows it",
        "th": "**ลำดับการทำงาน:** ผู้ใช้กรอกค่า → `pages/*.py` (UI) → `services/*.py` (คำนวณ) → ส่งผลลัพธ์กลับ → UI แสดงผล",
    },
    "home_m_apps": {"en": "Sub-applications", "th": "แอปพลิเคชันย่อย"},
    "home_m_services": {"en": "Service modules", "th": "โมดูลคำนวณ (services)"},
    "home_m_data": {"en": "Data files", "th": "ไฟล์ข้อมูล"},
    "home_menu_h": {"en": "Main menu", "th": "เมนูหลัก"},
    "home_menu_hint": {"en": "Click a card to open the app (or use the sidebar).",
                       "th": "กดที่การ์ดเพื่อเข้าสู่แอปย่อย (หรือเลือกจากแถบเมนูด้านซ้าย)"},
    "home_open": {"en": "Open", "th": "เปิด"},
    "home_table_h": {"en": "Sub-application summary", "th": "ตารางสรุปหน้าแอปพลิเคชันย่อย"},
    "home_cols": {
        "en": ["Page", "UI file (pages/)", "Service file (services/)", "Math / concept", "What you can do"],
        "th": ["หน้า", "ไฟล์ UI (pages/)", "ไฟล์คำนวณ (services/)", "หลักการทางคณิตศาสตร์", "สิ่งที่ทำได้"],
    },
    "home_apps": {
        "en": [
            ("📊 Statistics", "statistics.py", "cal_statistics.py, cal_mode.py", "Mean, Median, Mode, SD, Variance",
             "Enter numbers → get all statistics with a step-by-step table and chart"),
            ("🎲 Bayes' Theorem", "bayes.py", "cal_bayes.py", "P(A|B) = P(B|A)·P(A) / P(B)",
             "Enter prior, likelihood, evidence → posterior, chart and 1,000-case explanation"),
            ("🔗 Markov Text Prediction", "markov.py", "text_prediction.py", "Transition probability matrix",
             "Pick a dataset → predict the next word, generate sentences, view the matrix"),
            ("🗂️ Data Viewer", "display_data.py", "data_loader.py", "Data summary / word frequency",
             "Browse raw_data.json, students.json, members.json as tables and charts"),
            ("🎓 StudyCast", "custom_app.py", "custom_service.py",
             "Matrices, Softmax, Sigmoid, Derivatives",
             "Enter study habits → predicted grade, pass chance, what-if curves, study hours needed"),
            ("👥 Members", "members.py", "data_loader.py", "-",
             "Names, student IDs, photos and responsibilities"),
        ],
        "th": [
            ("📊 สถิติพื้นฐาน", "statistics.py", "cal_statistics.py, cal_mode.py", "Mean, Median, Mode, SD, Variance",
             "กรอกชุดตัวเลข → ได้ค่าสถิติทั้งหมด พร้อมตารางวิธีทำและกราฟ"),
            ("🎲 ทฤษฎีบทของเบย์ส", "bayes.py", "cal_bayes.py", "P(A|B) = P(B|A)·P(A) / P(B)",
             "กรอก Prior, Likelihood, Evidence → ได้ Posterior พร้อมกราฟและคำอธิบายแบบ 1,000 กรณี"),
            ("🔗 ทำนายคำด้วย Markov", "markov.py", "text_prediction.py", "เมทริกซ์ความน่าจะเป็นการเปลี่ยนสถานะ",
             "เลือกชุดข้อมูล → ทำนายคำถัดไป สร้างประโยค และดูเมทริกซ์"),
            ("🗂️ ดูข้อมูลดิบ", "display_data.py", "data_loader.py", "สรุปข้อมูล / ความถี่ของคำ",
             "ดู raw_data.json, students.json, members.json ในรูปตารางและกราฟ"),
            ("🎓 StudyCast", "custom_app.py", "custom_service.py",
             "เมทริกซ์, Softmax, Sigmoid, อนุพันธ์",
             "กรอกพฤติกรรมการเรียน → ทำนายเกรด โอกาสผ่าน กราฟจำลองสถานการณ์ และชั่วโมงอ่านที่ต้องใช้"),
            ("👥 สมาชิกกลุ่ม", "members.py", "data_loader.py", "-",
             "ชื่อ รหัสนักศึกษา รูปถ่าย และหน้าที่ความรับผิดชอบ"),
        ],
    },
    "home_struct_h": {"en": "Project structure", "th": "โครงสร้างโปรเจกต์"},

    # ---------------------------------------------------------------- statistics
    "st_title": {"en": "📊 Descriptive Statistics", "th": "📊 สถิติเชิงพรรณนา"},
    "st_caption": {"en": "Enter numbers separated by commas, spaces or new lines.",
                   "th": "กรอกชุดตัวเลข คั่นด้วยจุลภาค เว้นวรรค หรือขึ้นบรรทัดใหม่"},
    "st_examples": {"en": "Load an example", "th": "โหลดตัวอย่าง"},
    "ex_teacher": {"en": "Teacher's example", "th": "ตัวอย่างจากอาจารย์"},
    "ex_scores": {"en": "Exam scores", "th": "คะแนนสอบ"},
    "ex_bimodal": {"en": "Bimodal", "th": "มีฐานนิยม 2 ค่า"},
    "st_data": {"en": "Data", "th": "ข้อมูล"},
    "st_kind": {"en": "Variance / SD type", "th": "ชนิดของความแปรปรวน / SD"},
    "st_pop": {"en": "Population (÷ n)", "th": "ประชากร (÷ n)"},
    "st_sample": {"en": "Sample (÷ n − 1)", "th": "กลุ่มตัวอย่าง (÷ n − 1)"},
    "m_mean": {"en": "Mean", "th": "ค่าเฉลี่ย (Mean)"},
    "m_median": {"en": "Median", "th": "มัธยฐาน (Median)"},
    "m_mode": {"en": "Mode", "th": "ฐานนิยม (Mode)"},
    "m_nomode": {"en": "No mode", "th": "ไม่มีฐานนิยม"},
    "m_nomode_help": {"en": "No mode = every value appears only once.",
                      "th": "ไม่มีฐานนิยม = ทุกค่าปรากฏเพียงครั้งเดียว"},
    "m_sd": {"en": "Standard Deviation", "th": "ส่วนเบี่ยงเบนมาตรฐาน (SD)"},
    "m_var": {"en": "Variance", "th": "ความแปรปรวน (Variance)"},
    "m_n": {"en": "n", "th": "จำนวนข้อมูล (n)"},
    "m_sum": {"en": "Sum", "th": "ผลรวม"},
    "m_min": {"en": "Min", "th": "ค่าต่ำสุด"},
    "m_max": {"en": "Max", "th": "ค่าสูงสุด"},
    "m_range": {"en": "Range", "th": "พิสัย"},
    "tab_chart": {"en": "Chart", "th": "กราฟ"},
    "tab_steps": {"en": "Step-by-step", "th": "วิธีทำทีละขั้น"},
    "tab_freq": {"en": "Frequency table", "th": "ตารางความถี่"},
    "ax_value": {"en": "Value", "th": "ค่า"},
    "ax_point": {"en": "Data point", "th": "ลำดับข้อมูล"},
    "st_sorted": {"en": "Sorted data: {d} → median = **{m}**", "th": "ข้อมูลเรียงลำดับ: {d} → มัธยฐาน = **{m}**"},
    "col_value": {"en": "value", "th": "ค่า"},
    "col_count": {"en": "count", "th": "ความถี่"},
    "err_empty": {"en": "Please enter at least one number.", "th": "กรุณากรอกตัวเลขอย่างน้อย 1 ค่า"},
    "err_nan": {"en": "'{t}' is not a number.", "th": "'{t}' ไม่ใช่ตัวเลข"},
    "err_sample2": {"en": "Sample variance needs at least 2 numbers.",
                    "th": "ความแปรปรวนของกลุ่มตัวอย่างต้องมีข้อมูลอย่างน้อย 2 ค่า"},

    # ---------------------------------------------------------------- bayes
    "by_title": {"en": "🎲 Bayes' Theorem", "th": "🎲 ทฤษฎีบทของเบย์ส (Bayes' Theorem)"},
    "by_scenario": {"en": "Example scenario", "th": "สถานการณ์ตัวอย่าง"},
    "by_custom": {"en": "Custom", "th": "กำหนดเอง"},
    "by_custom_desc": {"en": "Enter your own probabilities.", "th": "กรอกค่าความน่าจะเป็นเอง"},
    "by_mode": {"en": "How do you want to give the evidence P(B)?", "th": "ต้องการระบุ Evidence P(B) แบบไหน?"},
    "by_direct": {"en": "Enter P(B) directly", "th": "กรอก P(B) โดยตรง"},
    "by_total": {"en": "Compute P(B) from P(B|¬A)", "th": "คำนวณ P(B) จาก P(B|¬A)"},
    "by_prior": {"en": "Prior P(A)", "th": "Prior P(A) (ความเชื่อก่อนเห็นหลักฐาน)"},
    "by_lik": {"en": "Likelihood P(B|A)", "th": "Likelihood P(B|A)"},
    "by_ev": {"en": "Evidence P(B)", "th": "Evidence P(B)"},
    "by_false": {"en": "False alarm P(B|¬A)", "th": "ผลบวกลวง P(B|¬A)"},
    "by_post": {"en": "Posterior P(A|B)", "th": "Posterior P(A|B)"},
    "by_vs": {"en": "{d} vs prior", "th": "{d} เทียบกับ prior"},
    "by_joint": {"en": "Joint P(A ∩ B)", "th": "Joint P(A ∩ B)"},
    "by_chart": {"en": "**Prior vs Posterior**", "th": "**เปรียบเทียบ Prior กับ Posterior**"},
    "by_out_of": {"en": "**Out of {n} cases**", "th": "**ถ้ามี {n} กรณี**"},
    "by_freq": {
        "en": "- **{b}** cases show evidence B  \n- of those, **{ab}** are really A, and **{nab}** are not A  \n"
              "- so P(A|B) ≈ {ab} / {b} = **{p}**",
        "th": "- มี **{b}** กรณีที่พบหลักฐาน B  \n- ในนั้นเป็น A จริง **{ab}** กรณี และไม่ใช่ A **{nab}** กรณี  \n"
              "- ดังนั้น P(A|B) ≈ {ab} / {b} = **{p}**",
    },
    "by_err_range": {"en": "{name} must be between 0 and 1 (got {p}).", "th": "{name} ต้องอยู่ระหว่าง 0 ถึง 1 (ได้ {p})"},
    "by_err_zero": {"en": "P(B) cannot be 0 (division by zero).", "th": "P(B) ต้องไม่เป็น 0 (หารด้วยศูนย์ไม่ได้)"},
    "by_err_inconsistent": {
        "en": "These numbers are inconsistent: P(B|A)·P(A) = {j} is larger than P(B) = {e}, so P(A|B) would be "
              "{p} > 1. P(B) must be at least P(B|A)·P(A).",
        "th": "ค่าที่กรอกขัดแย้งกัน: P(B|A)·P(A) = {j} มากกว่า P(B) = {e} ทำให้ P(A|B) = {p} > 1 "
              "ค่า P(B) ต้องไม่น้อยกว่า P(B|A)·P(A)",
    },
    "by_interp": {
        "en": "Before seeing B we believed P(A) = {pr}. After observing B, the belief {verb} to P(A|B) = {po}.",
        "th": "ก่อนเห็นหลักฐาน B เราเชื่อว่า P(A) = {pr} หลังจากพบ B ความเชื่อ{verb}เป็น P(A|B) = {po}",
    },
    "by_up": {"en": "increased", "th": "เพิ่มขึ้น"},
    "by_down": {"en": "decreased", "th": "ลดลง"},
    "by_same": {"en": "did not change", "th": "ไม่เปลี่ยนแปลง คงที่"},

    # ---------------------------------------------------------------- markov
    "mk_title": {"en": "🔗 Markov Chain Text Prediction", "th": "🔗 ทำนายคำถัดไปด้วย Markov Chain"},
    "mk_data": {"en": "Training data (from data/raw_data.json)", "th": "ชุดข้อมูลสำหรับสร้างโมเดล (จาก data/raw_data.json)"},
    "mk_order": {"en": "Order (words of memory)", "th": "อันดับ (จำนวนคำที่ใช้จำ)"},
    "mk_order_help": {"en": "Order 1: next word depends on the last word. Order 2: on the last two words.",
                      "th": "อันดับ 1: คำถัดไปขึ้นกับคำสุดท้าย 1 คำ, อันดับ 2: ขึ้นกับ 2 คำสุดท้าย"},
    "mk_own": {"en": "Add my own sentences to the training data", "th": "เพิ่มประโยคของฉันเข้าไปในข้อมูล"},
    "mk_own_area": {"en": "One sentence per line", "th": "หนึ่งประโยคต่อหนึ่งบรรทัด"},
    "mk_show": {"en": "Show the {n} training sentences", "th": "แสดงประโยคทั้ง {n} ประโยค"},
    "mk_s1": {"en": "1 · Predict the next word", "th": "1 · ทำนายคำถัดไป"},
    "mk_quick": {"en": "Quick start", "th": "เริ่มด้วยคำ"},
    "mk_input": {"en": "Type the beginning of a sentence", "th": "พิมพ์ต้นประโยค (ภาษาอังกฤษ)"},
    "mk_top": {"en": "Show top", "th": "แสดงอันดับสูงสุด"},
    "mk_unseen": {"en": "The state **{s}** never appears in the training data, so there is no prediction.",
                  "th": "ไม่พบสถานะ **{s}** ในข้อมูล จึงทำนายไม่ได้"},
    "mk_backoff": {"en": "'{s}' was never seen, so we backed off to the last word '{w}'.",
                   "th": "ไม่พบ '{s}' ในข้อมูล จึงใช้แค่คำสุดท้าย '{w}' แทน (back-off)"},
    "mk_best": {"en": "Most likely next word: **{w}** ({p})", "th": "คำถัดไปที่น่าจะเป็นที่สุด: **{w}** ({p})"},
    "mk_end": {"en": "(end of sentence)", "th": "(จบประโยค)"},
    "ax_prob": {"en": "probability", "th": "ความน่าจะเป็น"},
    "mk_s2": {"en": "2 · Generate a sentence", "th": "2 · สร้างประโยคต่อ"},
    "mk_method": {"en": "Method", "th": "วิธี"},
    "mk_greedy": {"en": "greedy (most likely word)", "th": "greedy (เลือกคำที่น่าจะเป็นสูงสุด)"},
    "mk_random": {"en": "random (sample by probability)", "th": "random (สุ่มตามความน่าจะเป็น)"},
    "mk_len": {"en": "Max words", "th": "จำนวนคำสูงสุด"},
    "mk_seed": {"en": "Random seed", "th": "ค่า seed สำหรับสุ่ม"},
    "mk_seqprob": {"en": "Probability of this continuation = product of step probabilities = {p}",
                   "th": "ความน่าจะเป็นของประโยคนี้ = ผลคูณความน่าจะเป็นแต่ละขั้น = {p}"},
    "mk_s3": {"en": "3 · Transition probability matrix (order 1)", "th": "3 · เมทริกซ์ความน่าจะเป็นการเปลี่ยนสถานะ (order 1)"},
    "mk_nwords": {"en": "Most frequent words to show", "th": "จำนวนคำที่พบบ่อยที่สุดที่จะแสดง"},
    "mk_caption": {
        "en": "Each row is a current word; the full model has {n} states. "
              "Rows can sum to less than 1 here because only the most frequent words are shown.",
        "th": "แต่ละแถวคือคำปัจจุบัน โมเดลทั้งหมดมี {n} สถานะ "
              "ผลรวมของแถวอาจน้อยกว่า 1 เพราะแสดงเฉพาะคำที่พบบ่อยที่สุด",
    },

    # ---------------------------------------------------------------- data viewer
    "dd_title": {"en": "🗂️ Data Viewer", "th": "🗂️ ดูข้อมูลดิบ"},
    "dd_caption": {"en": "Everything below is read from files in the `data/` folder.",
                   "th": "ข้อมูลทั้งหมดในหน้านี้อ่านมาจากไฟล์ในโฟลเดอร์ `data/`"},
    "dd_dataset": {"en": "Dataset", "th": "ชุดข้อมูล"},
    "dd_topwords": {"en": "Most frequent words", "th": "คำที่พบบ่อยที่สุด"},
    "dd_rawjson": {"en": "Raw JSON", "th": "JSON ดิบ"},
    "dd_students": {"en": "**{n} synthetic students**: training data for the StudyCast custom app.",
                    "th": "**นักศึกษาจำลอง {n} คน** ใช้เป็นข้อมูลฝึกโมเดลของ StudyCast"},
    "dd_filter": {"en": "Filter by grade", "th": "กรองตามเกรด"},

    # ---------------------------------------------------------------- custom app
    "ca_title": {"en": "🎓 StudyCast: Exam Result Predictor", "th": "🎓 StudyCast: ระบบทำนายผลสอบ"},
    "ca_intro": {
        "en": "Tell StudyCast about your study habits. It predicts your **grade (A–F)** and your **chance of getting "
              "C or better**, and uses **derivatives** to find which habit helps you most. Both models are built "
              "**from scratch with NumPy matrices** and trained on 240 students.",
        "th": "กรอกพฤติกรรมการเรียนของคุณ แล้ว StudyCast จะทำนาย **เกรด (A–F)** และ **โอกาสได้เกรด C ขึ้นไป** "
              "พร้อมใช้ **อนุพันธ์** หาว่าพฤติกรรมไหนช่วยได้มากที่สุด โมเดลทั้งสองสร้าง **เองตั้งแต่ต้นด้วยเมทริกซ์ NumPy** "
              "และฝึกจากข้อมูลนักศึกษา 240 คน",
    },
    "ca_train": {"en": "⚙️ Training settings (gradient descent)", "th": "⚙️ ตั้งค่าการฝึกโมเดล (gradient descent)"},
    "ca_habits": {"en": "Your habits", "th": "พฤติกรรมการเรียนของคุณ"},
    "lbl_study_hours": {"en": "📚 Study hours / week", "th": "📚 ชั่วโมงอ่านหนังสือ / สัปดาห์"},
    "lbl_attendance": {"en": "🏫 Attendance (%)", "th": "🏫 การเข้าเรียน (%)"},
    "lbl_sleep_hours": {"en": "😴 Sleep hours / night", "th": "😴 ชั่วโมงนอน / คืน"},
    "lbl_assignments_done": {"en": "📝 Assignments done (of 10)", "th": "📝 งานที่ส่งแล้ว (จาก 10)"},
    "u_study_hours": {"en": "1 more study hour / week", "th": "อ่านหนังสือเพิ่ม 1 ชม./สัปดาห์"},
    "u_attendance": {"en": "1% more attendance", "th": "เข้าเรียนเพิ่ม 1%"},
    "u_sleep_hours": {"en": "1 more hour of sleep / night", "th": "นอนเพิ่ม 1 ชม./คืน"},
    "u_assignments_done": {"en": "1 more assignment done", "th": "ส่งงานเพิ่ม 1 ชิ้น"},
    "ca_tab1": {"en": "🔮 Prediction", "th": "🔮 ผลทำนาย"},
    "ca_tab2": {"en": "📈 What-if & derivatives", "th": "📈 จำลองสถานการณ์ & อนุพันธ์"},
    "ca_tab3": {"en": "🧠 How the model works", "th": "🧠 โมเดลทำงานอย่างไร"},
    "ca_best": {"en": "Most likely grade", "th": "เกรดที่น่าจะได้มากที่สุด"},
    "ca_conf": {"en": "{p} confidence", "th": "ความมั่นใจ {p}"},
    "ca_ppass": {"en": "P(grade C or better)", "th": "P(ได้เกรด C ขึ้นไป)"},
    "ca_ppass_help": {"en": "From the sigmoid model", "th": "คำนวณจากโมเดล sigmoid"},
    "ca_gpa": {"en": "Expected GPA", "th": "GPA ที่คาดหวัง"},
    "ca_gpa_help": {"en": "Σ P(grade) × grade points (A=4 … F=0)", "th": "Σ P(เกรด) × แต้มเกรด (A=4 … F=0)"},
    "ca_softmax_title": {"en": "Softmax output: P(grade)", "th": "ผลลัพธ์ Softmax: P(เกรด)"},
    "ax_grade": {"en": "Grade", "th": "เกรด"},
    "ca_need": {"en": "**🎯 How many study hours do I need?**", "th": "**🎯 ต้องอ่านหนังสือกี่ชั่วโมง?**"},
    "ca_target": {"en": "Target P(C or better)", "th": "เป้าหมาย P(ได้ C ขึ้นไป)"},
    "ca_need_ok": {"en": "Study about **{h} h/week** (you study {s} h now).",
                   "th": "ควรอ่านประมาณ **{h} ชม./สัปดาห์** (ตอนนี้อ่าน {s} ชม.)"},
    "ca_need_none": {"en": "Study hours do not increase the probability in this model.",
                     "th": "ในโมเดลนี้ชั่วโมงอ่านหนังสือไม่ได้เพิ่มโอกาสผ่าน"},
    "ca_need_already": {"en": "Already reached even with 0 study hours.", "th": "ถึงเป้าหมายแล้วแม้ไม่อ่านหนังสือเลย"},
    "ca_need_out": {"en": "Needs about {h} h/week, more than {hi} h which is outside the data range.",
                    "th": "ต้องอ่านประมาณ {h} ชม./สัปดาห์ ซึ่งเกิน {hi} ชม. (นอกช่วงข้อมูล)"},
    "ca_lever_head": {"en": "**💡 What helps you most right now?**", "th": "**💡 ตอนนี้อะไรช่วยคุณได้มากที่สุด?**"},
    "ca_lever_top": {"en": "**{c}** raises your pass chance by about **{p}**.",
                     "th": "**{c}** จะเพิ่มโอกาสผ่านประมาณ **{p}**"},
    "ca_vary": {"en": "Change one habit, keep the others fixed", "th": "เปลี่ยนพฤติกรรมทีละอย่าง (อย่างอื่นคงที่)"},
    "ca_curve_title": {"en": "Sigmoid curve and tangent line at your point",
                       "th": "เส้นโค้ง Sigmoid และเส้นสัมผัส ณ จุดของคุณ"},
    "ax_ppass": {"en": "P(C or better)", "th": "P(ได้ C ขึ้นไป)"},
    "ca_slope": {"en": "Slope of the tangent = {s} per unit: one more unit changes P(pass) by about {p}.",
                 "th": "ความชันของเส้นสัมผัส = {s} ต่อหน่วย: เพิ่ม 1 หน่วย โอกาสผ่านเปลี่ยนประมาณ {p}"},
    "ca_shift_title": {"en": "How the whole grade distribution shifts", "th": "การกระจายของเกรดเปลี่ยนไปอย่างไร"},
    "ax_softmax": {"en": "Softmax probability", "th": "ความน่าจะเป็น (Softmax)"},
    "ca_deriv_head": {
        "en": "**Derivatives at your current point** (analytic formula vs numeric check [f(x+h) − f(x−h)] / 2h)",
        "th": "**อนุพันธ์ ณ จุดปัจจุบัน** (สูตรวิเคราะห์ เทียบกับการตรวจเชิงตัวเลข [f(x+h) − f(x−h)] / 2h)",
    },
    "col_change": {"en": "change", "th": "การเปลี่ยนแปลง"},
    "ca_deriv_caption": {
        "en": "ΔGPA uses the softmax Jacobian: dE/dx = Σₖ gₖ·pₖ·(aₖ − ā), where aₖ = ∂zₖ/∂x. "
              "Sleep uses the chain rule because the model has both sleep and sleep² as features.",
        "th": "ΔGPA ใช้ Jacobian ของ softmax: dE/dx = Σₖ gₖ·pₖ·(aₖ − ā) โดย aₖ = ∂zₖ/∂x "
              "ส่วนชั่วโมงนอนใช้กฎลูกโซ่ (chain rule) เพราะโมเดลมีทั้ง sleep และ sleep² เป็น feature",
    },
    "ca_acc": {"en": "Grade accuracy (test)", "th": "ความแม่นยำของเกรด (ชุดทดสอบ)"},
    "ca_baseline": {"en": "baseline {p}", "th": "baseline {p}"},
    "ca_within": {"en": "Within ±1 grade", "th": "คลาดไม่เกิน ±1 เกรด"},
    "ca_passacc": {"en": "Pass/fail accuracy", "th": "ความแม่นยำ ผ่าน/ไม่ผ่าน"},
    "ca_split": {"en": "Train / test", "th": "ฝึก / ทดสอบ"},
    "ca_h1": {"en": "##### 1. Matrix form", "th": "##### 1. รูปแบบเมทริกซ์"},
    "ca_h2": {"en": "##### 2. Training with derivatives (gradient descent)",
              "th": "##### 2. ฝึกโมเดลด้วยอนุพันธ์ (gradient descent)"},
    "ca_h3": {"en": "##### 3. Learned weights", "th": "##### 3. ค่าน้ำหนักที่โมเดลเรียนรู้"},
    "ca_h4": {"en": "##### 4. Try softmax yourself", "th": "##### 4. ลองใช้ softmax ด้วยตัวเอง"},
    "ca_loss_title": {"en": "Loss goes down while training", "th": "ค่า Loss ลดลงระหว่างการฝึก"},
    "ca_conf_title": {"en": "Confusion matrix (test set)", "th": "Confusion matrix (ชุดทดสอบ)"},
    "ca_W_title": {"en": "Softmax weight matrix W (features × grades)", "th": "เมทริกซ์น้ำหนัก W ของ Softmax (feature × เกรด)"},
    "ca_w_title": {"en": "Sigmoid weight vector w", "th": "เวกเตอร์น้ำหนัก w ของ Sigmoid"},
    "ca_std_caption": {"en": "Features are standardised (z-scores), so the weights can be compared directly.",
                       "th": "feature ถูกปรับเป็นค่ามาตรฐาน (z-score) จึงเปรียบเทียบค่าน้ำหนักกันได้โดยตรง"},
    "ca_logits": {"en": "Scores (logits)", "th": "คะแนน (logits)"},
    "ca_temp_caption": {"en": "Low T → the largest score takes almost everything; high T → probabilities become equal.",
                        "th": "T ต่ำ → คะแนนสูงสุดได้ความน่าจะเป็นเกือบทั้งหมด, T สูง → ความน่าจะเป็นใกล้เคียงกัน"},

    # ---------------------------------------------------------------- members
    "mb_title": {"en": "👥 Team Members", "th": "👥 สมาชิกกลุ่ม"},
    "mb_id": {"en": "Student ID", "th": "รหัสนักศึกษา"},
    "mb_role": {"en": "Role", "th": "หน้าที่"},
    "mb_photo_btn": {"en": "Change photo", "th": "เปลี่ยนรูป"},
    "mb_photo_help": {"en": "Any size works: the photo is cropped to a square and resized to the same size as the others.",
                      "th": "ใส่รูปขนาดไหนก็ได้ ระบบจะครอปเป็นสี่เหลี่ยมจัตุรัสและย่อให้ขนาดเท่ารูปอื่นอัตโนมัติ"},
    "mb_photo_saved": {"en": "Photo updated.", "th": "อัปโหลดรูปแล้ว"},
    "mb_photo_kept": {"en": "Photo updated and saved to GitHub.", "th": "อัปโหลดรูปแล้ว และบันทึกลง GitHub แล้ว (รูปไม่หาย)"},
    "mb_photo_github_error": {"en": "Photo shown, but saving to GitHub failed: it may disappear when the app restarts.",
                              "th": "เปลี่ยนรูปแล้ว แต่บันทึกลง GitHub ไม่สำเร็จ รูปอาจหายเมื่อแอปรีสตาร์ท"},
    "mb_photo_error": {"en": "This file is not a readable image.", "th": "ไฟล์นี้ไม่ใช่รูปภาพที่อ่านได้"},
}


STRINGS.update({
    # ---------------------------------------------------------------- text editor
    "ed_button": {"en": "Edit text", "th": "แก้ไขข้อความ"},
    "ed_title": {"en": "Edit text on this page", "th": "แก้ไขข้อความในหน้านี้"},
    "ed_intro": {
        "en": "Changes are saved to data/custom_text.json for the current language ({language}). "
              "Keep anything in {{curly braces}}: the app fills those in.",
        "th": "การแก้ไขจะบันทึกลง data/custom_text.json สำหรับภาษาปัจจุบัน ({language}) "
              "ห้ามลบข้อความในวงเล็บปีกกา {{ }} เพราะแอปใช้เติมตัวเลข",
    },
    "ed_tab_page": {"en": "This page", "th": "หน้านี้"},
    "ed_tab_nav": {"en": "Menu & sidebar", "th": "เมนูและแถบด้านข้าง"},
    "ed_tab_members": {"en": "Member details", "th": "ข้อมูลสมาชิก"},
    "ed_save": {"en": "Save", "th": "บันทึก"},
    "ed_reset": {"en": "Restore defaults for this page", "th": "คืนค่าเริ่มต้นของหน้านี้"},
    "ed_saved": {"en": "Saved {n} change(s).", "th": "บันทึกแล้ว {n} รายการ"},
    "ed_nochange": {"en": "Nothing changed.", "th": "ไม่มีการเปลี่ยนแปลง"},
    "ed_err_placeholder": {"en": "\"{name}\" must keep {ph}.", "th": "\"{name}\" ต้องมี {ph} เหมือนเดิม"},
    "ed_edited": {"en": "edited", "th": "แก้ไขแล้ว"},
    "ed_mem_cols": {"en": ["Name", "Student ID", "Role", "Responsibilities (one per line)"],
                    "th": ["ชื่อ", "รหัสนักศึกษา", "หน้าที่", "ความรับผิดชอบ (บรรทัดละ 1 ข้อ)"]},
    "ed_mem_save": {"en": "Save member details", "th": "บันทึกข้อมูลสมาชิก"},
})

# ---------------------------------------------------------------- editable text
import json  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

OVERRIDES_FILE = Path(__file__).resolve().parent.parent / "data" / "custom_text.json"
_cache = {"mtime": None, "data": {}}

# which text keys belong to which page (by prefix)
PAGE_PREFIXES = {
    "home": ["home_"],
    "statistics": ["st_", "m_", "tab_", "ex_", "ax_value", "ax_point", "col_value", "col_count", "err_"],
    "bayes": ["by_"],
    "markov": ["mk_", "ax_prob"],
    "display_data": ["dd_"],
    "custom_app": ["ca_", "lbl_", "u_", "ax_grade", "ax_ppass", "ax_softmax", "col_change"],
    "members": ["mb_"],
    "nav": ["sec_", "nav_", "theme_", "footer", "lang_label"],
}


def load_overrides() -> dict:
    """User edits from data/custom_text.json ({"th": {key: text}, "en": {...}}), re-read when the file changes."""
    try:
        mtime = os.path.getmtime(OVERRIDES_FILE)
    except OSError:
        return {}
    if mtime != _cache["mtime"]:
        with open(OVERRIDES_FILE, encoding="utf-8") as f:
            _cache["data"] = json.load(f)
        _cache["mtime"] = mtime
    return _cache["data"]


def default_text(lang: str, key: str):
    entry = STRINGS[key]
    return entry.get(lang, entry["en"])


def tr(lang: str, key: str, /, **values):
    """Text for `key` in `lang`: the user's edit if there is one, else the built-in text.
    Strings are formatted with `values`."""
    text = load_overrides().get(lang, {}).get(key, default_text(lang, key))
    return text.format(**values) if values and isinstance(text, str) else text


def page_text_items(page: str, lang: str) -> list[dict]:
    """Every editable text on a page: key, built-in default, current value, kind (text / table)."""
    prefixes = PAGE_PREFIXES.get(page, [])
    items = []
    for key in STRINGS:
        if key.startswith("ed_") or not any(key.startswith(p) for p in prefixes):
            continue
        default = default_text(lang, key)
        current = tr(lang, key)
        kind = "text" if isinstance(default, str) else "table"
        if kind == "table":
            default = [list(r) if isinstance(r, (list, tuple)) else [r] for r in default]
            current = [list(r) if isinstance(r, (list, tuple)) else [r] for r in current]
        items.append({"key": key, "default": default, "current": current, "kind": kind,
                      "edited": current != default, "long": kind == "text" and (len(default) > 70 or "\n" in default)})
    return items


def _placeholders(text: str) -> set[str]:
    return set(re.findall(r"\{(\w+)\}", text))


def save_overrides(lang: str, changes: dict) -> dict:
    """Store edited texts for `lang`. A value equal to the default removes the override.
    Returns {"saved": n, "errors": [...]}; nothing is written if any placeholder was removed."""
    errors = []
    for key, value in changes.items():
        default = default_text(lang, key)
        if isinstance(default, str) and _placeholders(value) != _placeholders(default):
            ph = ", ".join("{" + p + "}" for p in sorted(_placeholders(default))) or "-"
            errors.append(tr(lang, "ed_err_placeholder", name=key, ph=ph))
    if errors:
        return {"saved": 0, "errors": errors}

    data = json.loads(json.dumps(load_overrides()))  # deep copy
    bucket = data.setdefault(lang, {})
    saved = 0
    for key, value in changes.items():
        default = default_text(lang, key)
        if not isinstance(default, str):
            # tables: compare as lists of strings; single-column tables are stored as a flat list
            default = [list(r) if isinstance(r, (list, tuple)) else r for r in default]
            if default and not isinstance(default[0], list):
                value = [row[0] for row in value]
        old = bucket.get(key, default)
        if value == old:
            continue
        saved += 1
        if value == default:
            bucket.pop(key, None)
        else:
            bucket[key] = value
    if saved:
        _write(data)
    return {"saved": saved, "errors": []}


def reset_overrides(lang: str, page: str) -> int:
    """Remove every edit of this page's texts for `lang`. Returns how many were removed."""
    data = json.loads(json.dumps(load_overrides()))
    bucket = data.get(lang, {})
    keys = [i["key"] for i in page_text_items(page, lang) if i["key"] in bucket]
    for k in keys:
        bucket.pop(k)
    if keys:
        _write(data)
    return len(keys)


def _write(data: dict) -> None:
    with open(OVERRIDES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
