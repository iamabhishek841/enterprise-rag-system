import streamlit as st
import google.generativeai as genai

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Enterprise RAG System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;700&display=swap');

    .stApp { background-color: #0a0a0f; }
    .main .block-container { padding-top: 1rem; max-width: 1200px; }

    section[data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid #21262d;
    }
    section[data-testid="stSidebar"] * { color: #e0e0e0 !important; }

    .rag-header {
        background: linear-gradient(135deg, #0d1117, #161b22);
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 20px 28px;
        margin-bottom: 20px;
    }
    .rag-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: 2px;
        margin: 0;
    }
    .rag-subtitle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #555;
        letter-spacing: 2px;
        margin: 4px 0 0 0;
    }
    .msg-user {
        background: linear-gradient(135deg, #1a2332, #111820);
        border: 1px solid #1e3a5f;
        border-radius: 12px 12px 2px 12px;
        padding: 14px 18px;
        margin: 8px 0;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #ddd;
        text-align: right;
    }
    .msg-assistant {
        background: #111820;
        border: 1px solid #21262d;
        border-radius: 12px 12px 12px 2px;
        padding: 14px 18px;
        margin: 8px 0;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #ddd;
        line-height: 1.7;
    }
    .source-card {
        background: #0d1117;
        border: 1px solid #21262d;
        border-radius: 6px;
        padding: 4px 10px;
        margin: 3px 2px;
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #666;
    }
    .conf-high   { color:#00cc88;background:#00cc8822;border:1px solid #00cc8844;border-radius:10px;padding:2px 10px;font-size:11px; }
    .conf-medium { color:#ff8800;background:#ff880022;border:1px solid #ff880044;border-radius:10px;padding:2px 10px;font-size:11px; }
    .conf-low    { color:#ff4444;background:#ff444422;border:1px solid #ff444444;border-radius:10px;padding:2px 10px;font-size:11px; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stTextInput > div > div > input {
        background: #161b22 !important;
        border: 1px solid #21262d !important;
        color: #ddd !important;
        font-family: 'JetBrains Mono', monospace !important;
        border-radius: 8px !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #238636, #1a6e2a) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# ENTERPRISE DATA
# ============================================================
USERS = {
    "admin":           {"name": "Arjun Sharma", "role": "admin",           "dept": "IT",      "emoji": "👑", "color": "#ff4444"},
    "hr_manager":      {"name": "Priya Mehta",  "role": "hr_manager",      "dept": "HR",      "emoji": "👥", "color": "#ff8800"},
    "finance_analyst": {"name": "Rahul Gupta",  "role": "finance_analyst", "dept": "Finance", "emoji": "💰", "color": "#00cc88"},
    "intern":          {"name": "Sneha Patel",  "role": "intern",          "dept": "General", "emoji": "🎓", "color": "#4488ff"},
}

DOCUMENTS = [
    {"id":"doc_001","type":"PDF","access":["admin","hr_manager"],"title":"Employee Compensation Policy 2024","emoji":"📄",
     "content":"All employees at Grade 5+ receive annual bonuses of 15-20% of CTC. Grade 3-4 employees receive 8-12%. Performance ratings above 4.5/5 trigger additional 5% bonus. Salary revision cycle is April every year. CTC bands: L1=4-6LPA, L2=6-10LPA, L3=10-16LPA, L4=16-25LPA, L5=25-40LPA.",
     "source":"HR/Compensation_Policy_2024.pdf"},
    {"id":"doc_002","type":"PDF","access":["admin","finance_analyst"],"title":"Q4 2024 Financial Report","emoji":"📄",
     "content":"Revenue Q4 2024: Rs 847 Crores (up 23% YoY). Operating expenses: Rs 612 Crores. EBITDA margin: 28.2%. Net profit: Rs 165 Crores. Top revenue segment: SaaS Products (42%). Infrastructure costs reduced by 11% due to cloud migration. R&D spend: Rs 84 Crores (9.9% of revenue).",
     "source":"Finance/Q4_2024_Financial_Report.pdf"},
    {"id":"doc_003","type":"CSV","access":["admin","hr_manager"],"title":"Employee Database","emoji":"📊",
     "content":"EMP001,Ravi Kumar,Engineering,L3,Active,Pune. EMP002,Anita Singh,HR,L2,Active,Mumbai. EMP003,Deepak Joshi,Finance,L4,Active,Delhi. EMP004,Meera Nair,Marketing,L2,On Leave,Bangalore. Total headcount: 2847 employees across 12 offices.",
     "source":"HR/employee_db.csv"},
    {"id":"doc_004","type":"JSON","access":["admin","finance_analyst"],"title":"System Audit Logs - Nov 2024","emoji":"🔧",
     "content":"Critical events: 3 unauthorized access attempts on Finance portal (Nov 12, IP: 192.168.1.45). 2 failed login attempts on HR system. Data export events: 47 (all authorized). System uptime: 99.87%. Patch compliance: 94.2%. 3 high-severity vulnerabilities patched.",
     "source":"Logs/audit_nov2024.json"},
    {"id":"doc_005","type":"PDF","access":["all"],"title":"Company Leave Policy 2024","emoji":"📄",
     "content":"Annual leave: 21 days. Sick leave: 12 days. Casual leave: 6 days. Maternity leave: 26 weeks. Paternity leave: 15 days. Leave encashment allowed for up to 15 days per year. Carry forward maximum: 30 days. Leave application must be submitted 3 days in advance except emergency.",
     "source":"General/Leave_Policy_2024.pdf"},
    {"id":"doc_006","type":"PDF","access":["all"],"title":"IT Support & Remote Work Guidelines","emoji":"📄",
     "content":"VPN mandatory for remote work. Approved devices: company-issued laptops only. Video calls require virtual background. Work from home allowed 3 days/week for non-client roles. Hardware requests: submit ticket to IT helpdesk. Software installation requires IT approval. Password policy: min 12 chars, rotate every 90 days.",
     "source":"General/IT_Remote_Guidelines.pdf"},
    {"id":"doc_007","type":"CSV","access":["admin","finance_analyst"],"title":"Budget Allocation 2025","emoji":"📊",
     "content":"Engineering: Rs 145Cr. Sales & Marketing: Rs 89Cr. HR & Admin: Rs 34Cr. R&D: Rs 112Cr. Infrastructure: Rs 67Cr. Total budget: Rs 447Cr. Cloud budget: Rs 45Cr (AWS+Azure). Headcount addition budget: 180 new hires planned.",
     "source":"Finance/budget_2025.csv"},
    {"id":"doc_008","type":"JSON","access":["admin"],"title":"Security Incident Reports","emoji":"🔧",
     "content":"INC-2024-089: Phishing attempt on 12 employees (all reported correctly). INC-2024-091: USB data breach attempt - contained. INC-2024-095: Cloud misconfiguration exposing dev bucket - fixed in 2hrs. SOC response time avg: 8.3 minutes. Zero successful breaches in 2024.",
     "source":"Security/incidents_2024.json"},
    {"id":"doc_009","type":"PDF","access":["all"],"title":"Employee Code of Conduct","emoji":"📄",
     "content":"Professional behavior expected at all times. Zero tolerance for harassment or discrimination. Conflicts of interest must be disclosed. Social media policy: do not share confidential info. Whistleblower protection guaranteed. Violation reporting: ethics@company.com. Disciplinary process: verbal warning -> written warning -> termination.",
     "source":"General/Code_of_Conduct.pdf"},
]

SAMPLE_QUERIES = [
    "What is the annual leave policy?",
    "What was Q4 revenue and net profit?",
    "Salary bands and bonus structure?",
    "Recent security incidents?",
    "Work from home policy?",
    "Budget allocation for 2025?",
    "How many employees?",
    "Password security requirements?",
]

# ============================================================
# RBAC + RETRIEVAL
# ============================================================
def get_accessible_docs(user_role):
    return [d for d in DOCUMENTS if "all" in d["access"] or user_role in d["access"]]

def retrieve_context(docs, query, top_k=3):
    q = set(query.lower().split())
    scored = []
    for doc in docs:
        score = len(q & set(doc["title"].lower().split())) * 3 + len(q & set(doc["content"].lower().split()))
        if score > 0:
            scored.append({**doc, "score": score})
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]

# ============================================================
# GEMINI CALL
# ============================================================
def call_gemini(query, context_docs, user_name, user_role, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    if context_docs:
        ctx = "\n\n---\n\n".join([
            f"[Source {i+1}: {d['source']} | {d['type']}]\n{d['content']}"
            for i, d in enumerate(context_docs)
        ])
        prompt = (
            f"You are an Enterprise Intelligence Assistant.\n"
            f"User: {user_name} | Role: {user_role}\n\n"
            f"RULES: Answer ONLY from context. Cite [Source N]. Be concise.\n"
            f"End with exactly one of: Confidence: High | Confidence: Medium | Confidence: Low\n\n"
            f"Context:\n{ctx}\n\nQuery: {query}\nAnswer:"
        )
    else:
        prompt = (
            f"Enterprise Assistant. User {user_name} ({user_role}) asked: {query}\n"
            f"No relevant documents in their permitted knowledge base.\n"
            f"Politely say info not available. End with: Confidence: Low"
        )

    return model.generate_content(prompt).text

# ============================================================
# SESSION STATE
# ============================================================
if "messages"     not in st.session_state: st.session_state.messages     = []
if "current_user" not in st.session_state: st.session_state.current_user = "intern"
if "api_key"      not in st.session_state: st.session_state.api_key      = ""

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚡ RAG SYSTEM")
    st.markdown("---")

    st.markdown("**🔑 Gemini API Key**")
    api_key = st.text_input("API Key", type="password",
                             value=st.session_state.api_key,
                             placeholder="AIza...",
                             label_visibility="collapsed")
    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key set")
    else:
        st.warning("⚠️ [Get FREE key →](https://aistudio.google.com/apikey)")

    st.markdown("---")
    st.markdown("**👤 Select User**")

    user_options = {f"{u['emoji']} {u['name']}": k for k, u in USERS.items()}
    selected = st.selectbox("User", list(user_options.keys()),
                             index=list(user_options.values()).index(st.session_state.current_user),
                             label_visibility="collapsed")
    new_user = user_options[selected]
    if new_user != st.session_state.current_user:
        st.session_state.current_user = new_user
        st.session_state.messages = []
        st.rerun()

    user = USERS[st.session_state.current_user]
    accessible = get_accessible_docs(st.session_state.current_user)

    st.markdown(f"""
    <div style='background:#161b22;border:1px solid #21262d;border-radius:8px;
                padding:12px;margin:8px 0;font-family:monospace;font-size:12px;'>
        <div style='color:{user["color"]};font-weight:bold;'>{user["emoji"]} {user["name"]}</div>
        <div style='color:#888;margin-top:4px;'>Dept: {user["dept"]}</div>
        <div style='color:#00cc88;margin-top:4px;'>🔒 {len(accessible)}/{len(DOCUMENTS)} docs</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**📁 Your Documents**")
    for doc in accessible:
        st.markdown(f"""
        <div style='background:#0d1117;border:1px solid #21262d;border-radius:4px;
                    padding:5px 8px;margin:2px 0;font-size:10px;color:#888;font-family:monospace;'>
            {doc["emoji"]} [{doc["type"]}] {doc["title"][:32]}
        </div>""", unsafe_allow_html=True)

    restricted = [d for d in DOCUMENTS if d not in accessible]
    if restricted:
        st.markdown(f"**🔒 Restricted ({len(restricted)})**")
        for doc in restricted:
            st.markdown(f"""
            <div style='background:#0d1117;border:1px solid #21262d;border-radius:4px;
                        padding:5px 8px;margin:2px 0;font-size:10px;color:#333;font-family:monospace;'>
                ❌ {doc["title"][:32]}
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ CLEAR CHAT", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ============================================================
# MAIN
# ============================================================
st.markdown("""
<div class='rag-header'>
    <p class='rag-title'>⚡ ENTERPRISE RAG INTELLIGENCE SYSTEM</p>
    <p class='rag-subtitle'>SECURE · GROUNDED · RBAC-ENFORCED · MULTI-SOURCE · ZERO HALLUCINATION</p>
</div>""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Docs", len(DOCUMENTS))
c2.metric("Your Access", f"{len(accessible)}/{len(DOCUMENTS)}")
c3.metric("Data Types", "PDF·CSV·JSON")
c4.metric("AI Model", "Gemini Flash")

st.markdown("---")
st.markdown("**💡 Sample Queries:**")
cols = st.columns(4)
for i, q in enumerate(SAMPLE_QUERIES):
    with cols[i % 4]:
        if st.button(q[:28] + "…", key=f"s{i}"):
            st.session_state["prefill"] = q

st.markdown("---")

# Chat display
if not st.session_state.messages:
    st.markdown(f"""
    <div class='msg-assistant'>
        👋 Welcome <b>{user["name"]}</b>! Logged in as <b>{user["role"].upper().replace("_"," ")}</b>
        with access to <b>{len(accessible)} documents</b>.<br><br>
        Ask me anything — I answer only from your permitted documents.
    </div>""", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='msg-user'>🧑 {msg['content']}</div>", unsafe_allow_html=True)
    else:
        conf      = msg.get("confidence", "Medium")
        sources   = msg.get("sources", [])
        conf_cls  = f"conf-{conf.lower()}"
        conf_icon = {"High":"🟢","Medium":"🟡","Low":"🔴"}.get(conf,"⚪")

        st.markdown(f"""
        <div class='msg-assistant'>
            {msg['content']}
            <br><br><span class='{conf_cls}'>{conf_icon} Confidence: {conf}</span>
        </div>""", unsafe_allow_html=True)

        if sources:
            html = " ".join([f"<span class='source-card'>{s['emoji']} [{s['type']}] {s['source']} ▲{s['score']}</span>" for s in sources])
            st.markdown(f"<div>📚 {html}</div>", unsafe_allow_html=True)

# Input
st.markdown("---")
prefill = st.session_state.pop("prefill", "")
query   = st.text_input("Query", value=prefill,
                         placeholder="Ask anything about company data...",
                         label_visibility="collapsed")

sc1, sc2 = st.columns([5, 1])
with sc1:
    send = st.button("⚡ SEND", use_container_width=True)
with sc2:
    if st.button("🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if send and query.strip():
    if not st.session_state.api_key:
        st.error("⚠️ Enter your Gemini API key in the sidebar first!")
    else:
        accessible = get_accessible_docs(st.session_state.current_user)
        relevant   = retrieve_context(accessible, query)
        st.session_state.messages.append({"role": "user", "content": query})

        with st.spinner("⚡ Retrieving from knowledge base..."):
            try:
                answer = call_gemini(query, relevant, user["name"], user["role"], st.session_state.api_key)
                conf   = "Medium"
                for lvl in ["High", "Medium", "Low"]:
                    if f"Confidence: {lvl}" in answer:
                        conf   = lvl
                        answer = answer.replace(f"Confidence: {lvl}", "").strip()
                        break
                st.session_state.messages.append({
                    "role": "assistant", "content": answer,
                    "confidence": conf, "sources": relevant
                })
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
