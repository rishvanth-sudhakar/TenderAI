from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from pymongo import MongoClient         #database
from datetime import datetime           #current datetime
import io
import os
import requests                         # for Groq API calls
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics import renderPDF
from reportlab.lib.enums import TA_CENTER

app = Flask(__name__)
app.secret_key = 'tenderai_secret_key_2024'

client = MongoClient('mongodb://localhost:27017/')
db = client['tenderai_db']

users_col = db['users']
projects_col = db['projects']
vendor_summary_col = db['vendor_summary']

# ─────────────────────────────────────────────
#  GROQ AI CONFIGURATION
#  Get your FREE API key from: https://console.groq.com
#  It's completely free — no credit card needed
# ─────────────────────────────────────────────
GROQ_API_KEY = "your_groq_api_key_here"

GROQ_MODEL = "llama-3.1-8b-instant"          # Free model on Groq


def ask_groq(prompt: str) -> str:
    """
    Send a prompt to Groq AI and return the text response.
    Falls back gracefully if the API call fails.
    """
    if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
        return "⚠️ Groq API key not configured. Please set GROQ_API_KEY in app.py."

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 600,
                "temperature": 0.4
            },
            timeout=20
        )
        data = response.json()

        # Handle API error responses
        if "error" in data:
            return f"Groq Error: {data['error'].get('message', str(data['error']))}"

        # Handle missing choices
        if "choices" not in data or not data["choices"]:
            return f"No response from AI. Raw: {str(data)[:200]}"

        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return "AI request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Cannot connect to Groq API. Check your internet connection."
    except Exception as e:
        return f"AI unavailable: {str(e)}"


# ─────────────────────────────────────────────
#  AI FEATURE 1 — Vendor Recommendation Summary
# ─────────────────────────────────────────────
def get_ai_vendor_summary(project, top_vendors):
    """
    Ask Groq AI to write a human-readable recommendation
    explaining why the top vendor was selected.
    """
    if not top_vendors:
        return "No approved vendor bids available for AI analysis."

    top = top_vendors[0]
    prompt = f"""
You are a construction project expert. Based on the following data, write a 
clear 3–4 sentence recommendation explaining why the top vendor was selected.
Be specific and professional. Do not use bullet points.

Project Name: {project.get('project_name')}
Work Type: {project.get('work_type')}
Budget: Rs. {project.get('original_budget')}
Planned Duration: {project.get('planned_duration')} months
Project Tier: {classify_project_tier(project.get('original_budget', 0))}

Top Recommended Vendor:
- Company: {top['company_name']}
- AI Score: {top['score']} / 100
- Tier: {top['tier']}
- Experience: {top['experience']} years
- Projects Completed: {top['projects_completed']}
- Proposed Cost: Rs. {top['proposed_cost']}
- Proposed Time: {top['proposed_time']} months

Other Bidders Scores: {[{'company': v['company_name'], 'score': v['score']} for v in top_vendors[1:]]}

Write a professional recommendation paragraph:
"""
    return ask_groq(prompt)


# ─────────────────────────────────────────────
#  AI FEATURE 2 — Bid Anomaly Detection
# ─────────────────────────────────────────────
def get_ai_bid_anomalies(project, top_vendors):
    """
    Ask Groq AI to flag any suspicious or unusual bids.
    """
    if not top_vendors:
        return "No bids to analyse."

    bids_info = []
    for v in top_vendors:
        bids_info.append(
            f"{v['company_name']}: proposed Rs.{v['proposed_cost']} "
            f"in {v['proposed_time']} months (score={v['score']})"
        )

    prompt = f"""
You are a procurement auditor. Review these vendor bids for a construction project 
and flag any anomalies (unusually low/high cost, suspicious timelines, etc.).
Be concise — 2 to 3 sentences. If nothing is suspicious, say so.

Project Budget: Rs. {project.get('original_budget')}
Planned Duration: {project.get('planned_duration')} months

Bids:
{chr(10).join(bids_info)}

Your anomaly analysis:
"""
    return ask_groq(prompt)


# ─────────────────────────────────────────────
#  AI FEATURE 3 — Project Risk Assessment
# ─────────────────────────────────────────────
def get_ai_risk_assessment(project, top_vendors):
    """
    Ask Groq AI to assess project risks based on project data.
    """
    prompt = f"""
You are a construction risk analyst. Given the following project details, 
identify the top 2-3 risks and suggest brief mitigation strategies.
Keep it under 5 sentences total.

Project: {project.get('project_name')}
Work Type: {project.get('work_type')}
Location: {project.get('project_location')}
Budget: Rs. {project.get('original_budget')}
Complexity: {project.get('complexity_level')}
Number of Bidders: {len(top_vendors)}
Top Vendor Score: {top_vendors[0]['score'] if top_vendors else 'N/A'}

Risk assessment:
"""
    return ask_groq(prompt)


# ─────────────────────────────────────────────
#  HELPERS  (original — unchanged)
# ─────────────────────────────────────────────

def get_next_vendor_id():
    count = users_col.count_documents({"role": "vendor"})
    return str(count + 1).zfill(3)

def parse_deadline(deadline_str):
    if not deadline_str:
        return None
    try:
        if "T" in str(deadline_str):
            return datetime.fromisoformat(deadline_str)
        return datetime.strptime(deadline_str, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
    except Exception:
        return None

def is_deadline_passed(deadline_str):
    dt = parse_deadline(deadline_str)
    if dt is None:
        return True
    return datetime.now() >= dt

def format_deadline_display(deadline_str):
    dt = parse_deadline(deadline_str)
    if dt is None:
        return deadline_str or "N/A"
    return dt.strftime("%d %b %Y, %I:%M %p")

def calculate_vendor_score(vendor):
    score = 0
    work_col = db.get_collection(f"vendor_{vendor['username']}_works")
    works = list(work_col.find()) if work_col is not None else []

    exp = vendor.get("years_experience", 0)
    score += min(exp * 2, 20)

    if works:
        on_time = sum(1 for w in works if w.get("completed_on_time") == "Yes")
        within_budget = sum(1 for w in works if w.get("completed_within_budget") == "Yes")
        score += (on_time / len(works)) * 20
        score += (within_budget / len(works)) * 20

    turnover = vendor.get("avg_annual_turnover", 0)
    try:
        t = float(str(turnover).replace(",", ""))
        score += min(t / 10000000 * 10, 20)
    except Exception:
        pass

    if vendor.get("blacklisting_history") == "No":
        score += 10
    if vendor.get("legal_disputes") == "No":
        score += 10

    return round(score, 2)

def classify_vendor_tier(score):
    if score >= 60:
        return "A"
    elif score >= 35:
        return "B"
    return "C"

def classify_project_tier(budget):
    try:
        b = float(str(budget).replace(",", ""))
        if b >= 50000000:
            return "High"
        elif b >= 10000000:
            return "Medium"
        return "Low"
    except Exception:
        return "Medium"

def get_top_vendors(project):
    budget = project.get("original_budget", 0)
    project_tier = classify_project_tier(budget)
    work_type = project.get("work_type", "")
    vendor_responses = project.get("vendor_responses", {})

    approved_usernames = [
        u for u, r in vendor_responses.items() if r.get("decision") == "approve"
    ]
    if not approved_usernames:
        return []

    try:
        project_budget = float(str(budget).replace(",", ""))
    except Exception:
        project_budget = 0

    try:
        project_duration = float(str(project.get("planned_duration") or 0))
    except Exception:
        project_duration = 0

    vendors = list(users_col.find({"role": "vendor", "username": {"$in": approved_usernames}}))
    scored = []

    for v in vendors:
        uname = v["username"]
        resp = vendor_responses[uname]

        base = calculate_vendor_score(v)
        tier = classify_vendor_tier(base)
        s = base

        if project_tier == "High" and tier == "A":
            s += 20
        elif project_tier == "Medium" and tier in ["A", "B"]:
            s += 15
        elif project_tier == "Low" and tier == "C":
            s += 25
        elif project_tier == "Low" and tier == "B":
            s += 10

        summary = vendor_summary_col.find_one({"username": uname}) or {}
        if work_type in summary.get("work_types", []):
            s += 10

        try:
            pcost = float(str(resp.get("proposed_cost", 0) or 0).replace(",", ""))
            if project_budget > 0 and pcost > 0:
                r = pcost / project_budget
                s += 20 if r <= 1.00 else 15 if r <= 1.10 else 8 if r <= 1.25 else 0
        except Exception:
            pass

        try:
            ptime = float(str(resp.get("completion_time", 0) or 0))
            if project_duration > 0 and ptime > 0:
                r = ptime / project_duration
                s += 15 if r <= 1.00 else 10 if r <= 1.15 else 5 if r <= 1.30 else 0
        except Exception:
            pass

        scored.append({
            "username": uname,
            "company_name": v.get("company_name", uname),
            "score": round(s, 2),
            "tier": tier,
            "experience": v.get("years_experience", 0),
            "projects_completed": v.get("total_projects_completed", 0),
            "proposed_cost": resp.get("proposed_cost", "-"),
            "proposed_time": resp.get("completion_time", "-"),
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:5]


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username == 'admin' and password == 'admin@123':
            session['user'] = 'admin'
            session['role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        user = users_col.find_one({"username": username, "role": "vendor"})
        if user and password == f"{username}@123":
            session['user'] = username
            session['role'] = 'vendor'
            return redirect(url_for('vendor_dashboard'))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    vendors = list(users_col.find({"role": "vendor"}))
    projects = list(projects_col.find())
    for p in projects:
        p['deadline_passed'] = is_deadline_passed(p.get('submission_deadline', ''))
        p['deadline_display'] = format_deadline_display(p.get('submission_deadline', ''))
    return render_template('admin_dashboard.html', vendors=vendors, projects=projects)

@app.route('/admin/create_vendor', methods=['GET', 'POST'])
def create_vendor():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        vendor_id = get_next_vendor_id()
        data = {
            "username": vendor_id, "role": "vendor", "created_at": datetime.now(),
            "company_name": request.form.get('company_name'),
            "company_type": request.form.get('company_type'),
            "year_established": request.form.get('year_established'),
            "reg_number": request.form.get('reg_number'),
            "gst_number": request.form.get('gst_number'),
            "pan_number": request.form.get('pan_number'),
            "head_office_district": request.form.get('head_office_district'),
            "branch_locations": request.form.get('branch_locations'),
            "website": request.form.get('website'),
            "contact_number": request.form.get('contact_number'),
            "email": request.form.get('email'),
            "owner_name": request.form.get('owner_name'),
            "board_of_directors": request.form.get('board_of_directors'),
            "key_decision_maker": request.form.get('key_decision_maker'),
            "org_structure": request.form.get('org_structure'),
            "total_employees": request.form.get('total_employees'),
            "nature_of_business": request.form.get('nature_of_business'),
            "core_specialization": request.form.get('core_specialization'),
            "service_areas": request.form.get('service_areas'),
            "years_experience": int(request.form.get('years_experience', 0)),
            "avg_projects_per_year": request.form.get('avg_projects_per_year'),
            "avg_annual_turnover": request.form.get('avg_annual_turnover'),
            "net_worth": request.form.get('net_worth'),
            "financial_stability": request.form.get('financial_stability'),
            "financial_commitments": request.form.get('financial_commitments'),
            "total_engineers": request.form.get('total_engineers'),
            "total_technical_staff": request.form.get('total_technical_staff'),
            "major_machinery": request.form.get('major_machinery'),
            "equipment_capacity": request.form.get('equipment_capacity'),
            "total_projects_completed": int(request.form.get('total_projects_completed', 0)),
            "ongoing_projects": request.form.get('ongoing_projects'),
            "govt_experience": request.form.get('govt_experience'),
            "blacklisting_history": request.form.get('blacklisting_history'),
            "legal_disputes": request.form.get('legal_disputes'),
            "iso_certification": request.form.get('iso_certification'),
            "safety_compliance": request.form.get('safety_compliance'),
            "env_compliance": request.form.get('env_compliance'),
            "labour_compliance": request.form.get('labour_compliance'),
        }
        users_col.insert_one(data)
        vendor_summary_col.insert_one({"username": vendor_id, "total_works": 0, "work_types": []})
        return render_template('vendor_created.html', vendor_id=vendor_id)
    return render_template('create_vendor.html', districts=TAMIL_NADU_DISTRICTS)

@app.route('/admin/add_work', methods=['GET', 'POST'])
def add_work():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    vendors = list(users_col.find({"role": "vendor"}))
    if request.method == 'POST':
        vendor_username = request.form.get('vendor_username')
        work_data = {
            "project_name": request.form.get('project_name'),
            "project_location": request.form.get('project_location'),
            "client_name": request.form.get('client_name'),
            "client_type": request.form.get('client_type'),
            "year_award": request.form.get('year_award'),
            "year_completion": request.form.get('year_completion'),
            "work_type": request.form.get('work_type'),
            "work_type_other": request.form.get('work_type_other'),
            "original_budget": request.form.get('original_budget'),
            "final_cost": request.form.get('final_cost'),
            "budget_variation": request.form.get('budget_variation'),
            "budget_overrun_pct": request.form.get('budget_overrun_pct'),
            "cost_increase_reason": request.form.get('cost_increase_reason'),
            "planned_start": request.form.get('planned_start'),
            "planned_completion": request.form.get('planned_completion'),
            "actual_completion": request.form.get('actual_completion'),
            "planned_duration": request.form.get('planned_duration'),
            "actual_duration": request.form.get('actual_duration'),
            "delay_months": request.form.get('delay_months'),
            "delay_reason": request.form.get('delay_reason'),
            "work_completed_pct": request.form.get('work_completed_pct'),
            "completed_on_time": request.form.get('completed_on_time'),
            "completed_within_budget": request.form.get('completed_within_budget'),
            "client_satisfaction": request.form.get('client_satisfaction'),
            "penalty_imposed": request.form.get('penalty_imposed'),
            "early_completion_bonus": request.form.get('early_completion_bonus'),
            "built_up_area": request.form.get('built_up_area'),
            "length_area_covered": request.form.get('length_area_covered'),
            "units_completed": request.form.get('units_completed'),
            "complexity_level": request.form.get('complexity_level'),
            "major_challenges": request.form.get('major_challenges'),
            "safety_incidents": request.form.get('safety_incidents'),
            "legal_disputes": request.form.get('legal_disputes'),
            "arbitration_cases": request.form.get('arbitration_cases'),
            "added_at": datetime.now()
        }
        work_col = db[f"vendor_{vendor_username}_works"]
        work_col.insert_one(work_data)
        vendor_summary_col.update_one(
            {"username": vendor_username},
            {"$inc": {"total_works": 1}, "$addToSet": {"work_types": work_data["work_type"]}}
        )
        return redirect(url_for('admin_dashboard'))
    return render_template('add_work.html', vendors=vendors, districts=TAMIL_NADU_DISTRICTS, work_types=WORK_TYPES)

@app.route('/admin/new_project', methods=['GET', 'POST'])
def new_project():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    if request.method == 'POST':
        deadline_raw = request.form.get('submission_deadline_dt', '').strip()
        project_data = {
            "project_name": request.form.get('project_name'),
            "project_location": request.form.get('project_location'),
            "client_name": request.form.get('client_name'),
            "client_type": request.form.get('client_type'),
            "year_award": request.form.get('year_award'),
            "year_completion": request.form.get('year_completion'),
            "work_type": request.form.get('work_type'),
            "work_type_other": request.form.get('work_type_other'),
            "original_budget": request.form.get('original_budget'),
            "final_cost": request.form.get('final_cost'),
            "budget_variation": request.form.get('budget_variation'),
            "budget_overrun_pct": request.form.get('budget_overrun_pct'),
            "planned_start": request.form.get('planned_start'),
            "planned_completion": request.form.get('planned_completion'),
            "planned_duration": request.form.get('planned_duration'),
            "complexity_level": request.form.get('complexity_level'),
            "built_up_area": request.form.get('built_up_area'),
            "length_area_covered": request.form.get('length_area_covered'),
            "major_challenges": request.form.get('major_challenges'),
            "legal_disputes": request.form.get('legal_disputes'),
            "submission_deadline": deadline_raw,
            "status": "open",
            "vendor_responses": {},
            "created_at": datetime.now()
        }
        projects_col.insert_one(project_data)
        return redirect(url_for('admin_dashboard'))
    return render_template('new_project.html', districts=TAMIL_NADU_DISTRICTS, work_types=WORK_TYPES)

@app.route('/admin/project_status')
def project_status():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    projects = list(projects_col.find())
    for p in projects:
        p['deadline_passed'] = is_deadline_passed(p.get('submission_deadline', ''))
        p['deadline_display'] = format_deadline_display(p.get('submission_deadline', ''))
    return render_template('project_status.html', projects=projects)


# ─────────────────────────────────────────────
#  ANALYSE ROUTE — NOW WITH AI INSIGHTS
# ─────────────────────────────────────────────
@app.route('/admin/analyse/<project_id>')
def analyse_project(project_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    from bson import ObjectId
    project = projects_col.find_one({"_id": ObjectId(project_id)})
    if not project:
        return "Project not found", 404

    passed = is_deadline_passed(project.get('submission_deadline', ''))
    deadline_display = format_deadline_display(project.get('submission_deadline', ''))
    budget = project.get("original_budget", 0)
    project_tier = classify_project_tier(budget)

    if not passed:
        return render_template('analyse.html', project=project, top_vendors=[],
                               project_tier=project_tier, deadline_passed=False,
                               deadline_display=deadline_display,
                               ai_recommendation=None,
                               ai_anomalies=None,
                               ai_risk=None)

    top_vendors = get_top_vendors(project)

    # ── Call Groq AI for all three insights ──────────────────────────
    ai_recommendation = get_ai_vendor_summary(project, top_vendors)
    ai_anomalies      = get_ai_bid_anomalies(project, top_vendors)
    ai_risk           = get_ai_risk_assessment(project, top_vendors)
    # ─────────────────────────────────────────────────────────────────

    return render_template('analyse.html',
                           project=project,
                           top_vendors=top_vendors,
                           project_tier=project_tier,
                           deadline_passed=True,
                           deadline_display=deadline_display,
                           ai_recommendation=ai_recommendation,
                           ai_anomalies=ai_anomalies,
                           ai_risk=ai_risk)


# ─────────────────────────────────────────────
#  NEW ROUTE — Ask AI anything about a project
# ─────────────────────────────────────────────
@app.route('/admin/ai_chat/<project_id>', methods=['POST'])
def ai_chat(project_id):
    """
    AJAX endpoint — admin can ask any question about a project.
    Returns JSON with AI answer.
    """
    if session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    from bson import ObjectId
    project = projects_col.find_one({"_id": ObjectId(project_id)})
    if not project:
        return jsonify({"error": "Project not found"}), 404

    user_question = request.json.get("question", "")
    top_vendors = get_top_vendors(project)

    prompt = f"""
You are TenderAI assistant. Answer the admin's question about this project.
Be helpful, concise and professional (max 4 sentences).

Project: {project.get('project_name')}
Work Type: {project.get('work_type')}
Budget: Rs. {project.get('original_budget')}
Location: {project.get('project_location')}
Top Vendors: {[v['company_name'] + ' (score=' + str(v['score']) + ')' for v in top_vendors]}

Admin Question: {user_question}

Your Answer:
"""
    answer = ask_groq(prompt)
    return jsonify({"answer": answer})


@app.route('/admin/generate_pdf/<project_id>')
def generate_pdf(project_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    from bson import ObjectId
    project = projects_col.find_one({"_id": ObjectId(project_id)})
    if not project:
        return "Project not found", 404
    if not is_deadline_passed(project.get("submission_deadline", "")):
        return "PDF not available until submission deadline has passed.", 403

    top_vendors = get_top_vendors(project)

    # ── Generate AI recommendation for PDF ───────────────────────────
    ai_recommendation = get_ai_vendor_summary(project, top_vendors)
    ai_risk           = get_ai_risk_assessment(project, top_vendors)
    # ─────────────────────────────────────────────────────────────────

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    story = []

    title_style   = ParagraphStyle('Title',   parent=styles['Title'],   fontSize=20, textColor=colors.HexColor('#1a3c5e'), spaceAfter=6)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'],fontSize=13, textColor=colors.HexColor('#1a3c5e'), spaceAfter=4)
    normal_style  = ParagraphStyle('Normal',  parent=styles['Normal'],  fontSize=10, spaceAfter=3)
    ai_style      = ParagraphStyle('AI',      parent=styles['Normal'],  fontSize=10, spaceAfter=3,
                                   backColor=colors.HexColor('#f0f4ff'), leftIndent=8, rightIndent=8)
    center_style  = ParagraphStyle('Center',  parent=styles['Normal'],  fontSize=10, alignment=TA_CENTER)

    story.append(Paragraph("TENDERAI - PROJECT ANALYSIS REPORT", title_style))
    story.append(Paragraph("Tender Intelligence & Vendor Evaluation System", center_style))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a3c5e')))
    story.append(Spacer(1, 12))

    story.append(Paragraph("PROJECT DETAILS", heading_style))
    proj_data = [
        ["Project Name",        project.get("project_name", "")],
        ["Location",            project.get("project_location", "")],
        ["Client",              project.get("client_name", "")],
        ["Work Type",           project.get("work_type", "")],
        ["Budget",              f"Rs. {project.get('original_budget', '')}"],
        ["Submission Deadline", format_deadline_display(project.get("submission_deadline", ""))],
        ["Status",              project.get("status", "").upper()],
    ]
    t = Table(proj_data, colWidths=[2.5*inch, 4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#e8f0fe')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))

    # ── AI RECOMMENDATION SECTION in PDF ─────────────────────────────
    story.append(Paragraph("AI RECOMMENDATION", heading_style))
    story.append(Paragraph(f"🤖 {ai_recommendation}", ai_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("AI RISK ASSESSMENT", heading_style))
    story.append(Paragraph(f"⚠️ {ai_risk}", ai_style))
    story.append(Spacer(1, 16))
    # ─────────────────────────────────────────────────────────────────

    story.append(Paragraph("TOP 5 RECOMMENDED VENDORS (Approved Bidders Only)", heading_style))
    if top_vendors:
        vdata = [["Rank", "Company", "AI Score", "Tier", "Proposed Cost", "Proposed Time"]]
        for i, v in enumerate(top_vendors, 1):
            vdata.append([str(i), v["company_name"], str(v["score"]),
                          f"Tier {v['tier']}", f"Rs.{v['proposed_cost']}", f"{v['proposed_time']} mo"])
        vt = Table(vdata, colWidths=[0.5*inch, 2.2*inch, 1*inch, 1*inch, 1.5*inch, 1.2*inch])
        vt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3c5e')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 6),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f8ff')]),
        ]))
        story.append(vt)
        story.append(Spacer(1, 20))

        # Chart 1: AI Score Bar Chart
        story.append(Paragraph("CHART 1: Top 5 Vendor AI Scores", heading_style))
        chart_w, chart_h = 460, 160
        bar_colors_list = [
            colors.HexColor('#2563eb'), colors.HexColor('#10b981'),
            colors.HexColor('#f59e0b'), colors.HexColor('#8b5cf6'),
            colors.HexColor('#ef4444'),
        ]
        max_score = max(v['score'] for v in top_vendors) or 1
        bar_area_w = chart_w - 120
        bar_thickness = 22
        gap = 8
        d1 = Drawing(chart_w, chart_h + 30)
        d1.add(Rect(0, 0, chart_w, chart_h + 30, fillColor=colors.HexColor('#f8fafc'), strokeColor=colors.HexColor('#e2e8f0'), strokeWidth=1))
        for i, v in enumerate(top_vendors):
            y = chart_h - (i + 1) * (bar_thickness + gap) + gap
            bar_len = (v['score'] / max_score) * bar_area_w
            d1.add(Rect(100, y, bar_len, bar_thickness,
                        fillColor=bar_colors_list[i % len(bar_colors_list)],
                        strokeColor=colors.transparent))
            d1.add(String(95, y + bar_thickness / 2 - 4,
                          (v['company_name'][:14] + '..') if len(v['company_name']) > 14 else v['company_name'],
                          fontSize=8, fillColor=colors.HexColor('#1e293b'), textAnchor='end'))
            d1.add(String(100 + bar_len + 4, y + bar_thickness / 2 - 4,
                          str(v['score']),
                          fontSize=8, fillColor=colors.HexColor('#1a3c5e')))
        d1.add(Line(100, chart_h - len(top_vendors) * (bar_thickness + gap),
                    100 + bar_area_w, chart_h - len(top_vendors) * (bar_thickness + gap),
                    strokeColor=colors.HexColor('#94a3b8'), strokeWidth=0.5))
        d1.add(String(chart_w / 2, chart_h + 14, "AI Score Comparison (Top 5 Vendors)",
                      fontSize=9, fillColor=colors.HexColor('#0f2544'), textAnchor='middle'))
        story.append(d1)
        story.append(Spacer(1, 16))

        # Chart 2: Proposed Cost Bar Chart
        story.append(Paragraph("CHART 2: Proposed Cost vs Project Budget", heading_style))
        try:
            proj_budget = float(str(project.get('original_budget', 0)).replace(',', ''))
        except Exception:
            proj_budget = 0
        cost_vendors = [v for v in top_vendors if v['proposed_cost'] not in ('-', '', None)]
        if cost_vendors:
            max_cost = max(
                [float(str(v['proposed_cost']).replace(',', '')) for v in cost_vendors] + [proj_budget]
            ) or 1
            d2 = Drawing(chart_w, chart_h + 30)
            d2.add(Rect(0, 0, chart_w, chart_h + 30, fillColor=colors.HexColor('#f8fafc'),
                        strokeColor=colors.HexColor('#e2e8f0'), strokeWidth=1))
            for i, v in enumerate(cost_vendors):
                y = chart_h - (i + 1) * (bar_thickness + gap) + gap
                try:
                    pcost = float(str(v['proposed_cost']).replace(',', ''))
                except Exception:
                    pcost = 0
                bar_len = (pcost / max_cost) * bar_area_w
                budget_x = 100 + (proj_budget / max_cost) * bar_area_w
                d2.add(Line(budget_x, 0, budget_x, chart_h,
                            strokeColor=colors.HexColor('#ef4444'), strokeWidth=1, strokeDashArray=[3, 3]))
                d2.add(Rect(100, y, bar_len, bar_thickness,
                            fillColor=bar_colors_list[i % len(bar_colors_list)],
                            strokeColor=colors.transparent))
                d2.add(String(95, y + bar_thickness / 2 - 4,
                              (v['company_name'][:14] + '..') if len(v['company_name']) > 14 else v['company_name'],
                              fontSize=8, fillColor=colors.HexColor('#1e293b'), textAnchor='end'))
                cost_label = f"Rs.{int(pcost):,}"
                d2.add(String(100 + bar_len + 4, y + bar_thickness / 2 - 4,
                              cost_label, fontSize=7, fillColor=colors.HexColor('#1a3c5e')))
            d2.add(String(chart_w / 2, chart_h + 14,
                          "Proposed Cost (Red dashed = Project Budget)",
                          fontSize=9, fillColor=colors.HexColor('#0f2544'), textAnchor='middle'))
            story.append(d2)
        else:
            story.append(Paragraph("No cost data available for chart.", normal_style))

    else:
        story.append(Paragraph("No approved vendor bids for this project.", normal_style))

    story.append(Spacer(1, 16))
    story.append(Paragraph("ALL VENDOR RESPONSES", heading_style))
    responses = project.get("vendor_responses", {})
    if responses:
        rdata = [["Vendor", "Decision", "Proposed Cost", "Completion Time"]]
        for vname, resp in responses.items():
            rdata.append([vname, resp.get("decision","").upper(),
                          resp.get("proposed_cost","—"), resp.get("completion_time","—")])
        rt = Table(rdata, colWidths=[2*inch, 1.5*inch, 2*inch, 2*inch])
        rt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3c5e')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(rt)
    else:
        story.append(Paragraph("No vendor responses yet.", normal_style))

    story.append(Spacer(1, 40))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 12))
    sig_data = [
        ["Admin Signature", "", "Date"],
        ["_______________________", "", datetime.now().strftime("%d-%m-%Y")],
        ["Authorized Signatory", "", ""],
    ]
    st = Table(sig_data, colWidths=[3*inch, 1*inch, 3*inch])
    st.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
    ]))
    story.append(st)
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     download_name=f"project_report_{project_id}.pdf",
                     mimetype='application/pdf')

@app.route('/admin/edit_project/<project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    from bson import ObjectId
    project = projects_col.find_one({"_id": ObjectId(project_id)})
    if not project:
        return "Project not found", 404
    if request.method == 'POST':
        deadline_raw = request.form.get('submission_deadline_dt', '').strip()
        update_data = {
            "project_name": request.form.get('project_name'),
            "project_location": request.form.get('project_location'),
            "client_name": request.form.get('client_name'),
            "client_type": request.form.get('client_type'),
            "work_type": request.form.get('work_type'),
            "original_budget": request.form.get('original_budget'),
            "planned_duration": request.form.get('planned_duration'),
            "complexity_level": request.form.get('complexity_level'),
            "submission_deadline": deadline_raw,
        }
        projects_col.update_one({"_id": ObjectId(project_id)}, {"$set": update_data})
        return redirect(url_for('project_status'))
    project['deadline_display'] = format_deadline_display(project.get('submission_deadline', ''))
    return render_template('edit_project.html', project=project, work_types=WORK_TYPES,
                           districts=TAMIL_NADU_DISTRICTS)

@app.route('/admin/delete_project/<project_id>', methods=['POST'])
def delete_project(project_id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    from bson import ObjectId
    projects_col.delete_one({"_id": ObjectId(project_id)})
    return redirect(url_for('project_status'))

@app.route('/vendor')
def vendor_dashboard():
    if session.get('role') != 'vendor':
        return redirect(url_for('login'))
    username = session['user']
    projects = list(projects_col.find({"status": "open"}))
    for p in projects:
        p['deadline_display'] = format_deadline_display(p.get('submission_deadline', ''))
    vendor_info = users_col.find_one({"username": username})
    return render_template('vendor_dashboard.html', projects=projects, vendor=vendor_info)

@app.route('/vendor/respond/<project_id>', methods=['GET', 'POST'])
def vendor_respond(project_id):
    if session.get('role') != 'vendor':
        return redirect(url_for('login'))
    from bson import ObjectId
    project = projects_col.find_one({"_id": ObjectId(project_id)})
    if not project:
        return "Project not found", 404
    project['deadline_display'] = format_deadline_display(project.get('submission_deadline', ''))
    username = session['user']
    if request.method == 'POST':
        decision = request.form.get('decision')
        response = {"decision": decision, "responded_at": datetime.now().isoformat()}
        if decision == "approve":
            response["proposed_cost"] = request.form.get('proposed_cost')
            response["completion_time"] = request.form.get('completion_time')
        projects_col.update_one(
            {"_id": ObjectId(project_id)},
            {"$set": {f"vendor_responses.{username}": response}}
        )
        return redirect(url_for('vendor_dashboard'))
    return render_template('vendor_respond.html', project=project)


TAMIL_NADU_DISTRICTS = [
    "Ariyalur","Chengalpattu","Chennai","Coimbatore","Cuddalore","Dharmapuri",
    "Dindigul","Erode","Kallakurichi","Kancheepuram","Kanniyakumari","Karur",
    "Krishnagiri","Madurai","Mayiladuthurai","Nagapattinam","Namakkal","Nilgiris",
    "Perambalur","Pudukkottai","Ramanathapuram","Ranipet","Salem","Sivaganga",
    "Tenkasi","Thanjavur","Theni","Thoothukudi","Tiruchirappalli","Tirunelveli",
    "Tirupathur","Tiruppur","Tiruvallur","Tiruvannamalai","Tiruvarur","Vellore",
    "Viluppuram","Virudhunagar"
]

WORK_TYPES = [
    "Residential Building","Commercial Building","Industrial Construction",
    "Road Work","Bridge Work","Drainage / Sewerage","Water Supply",
    "Electrical Works","Renovation / Maintenance","Infrastructure Development","Other"
]

if __name__ == '__main__':
    app.run(debug=True, port=5000)
