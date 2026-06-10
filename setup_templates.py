import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
os.makedirs(TEMPLATES_DIR, exist_ok=True)

templates = {}

# ──────────────────────────────────────────────────────────────────
# base.html
# ──────────────────────────────────────────────────────────────────
templates["base.html"] = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{% block title %}TenderAI{% endblock %}</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --navy: #0f2544; --blue: #1a3c5e; --accent: #2563eb; --gold: #f59e0b;
  --light: #f0f4ff; --white: #ffffff; --text: #1e293b; --muted: #64748b;
  --success: #10b981; --danger: #ef4444; --border: #e2e8f0;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:\'Sora\',sans-serif; background:#f8fafc; color:var(--text); }
.navbar {
  background: linear-gradient(135deg, var(--navy) 0%, var(--blue) 100%);
  padding: 0 2rem; display: flex; align-items: center; justify-content: space-between;
  height: 64px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}
.navbar-brand { color:white; font-size:1.4rem; font-weight:700; letter-spacing:-0.5px; text-decoration:none; }
.navbar-brand span { color:var(--gold); }
.navbar-nav { display:flex; gap:0.5rem; align-items:center; }
.nav-link { color:rgba(255,255,255,0.8); padding:0.4rem 1rem; border-radius:6px; text-decoration:none; font-size:0.875rem; font-weight:500; transition:all 0.2s; }
.nav-link:hover { background:rgba(255,255,255,0.15); color:white; }
.nav-link.logout { background:rgba(239,68,68,0.2); color:#fca5a5; }
.nav-link.logout:hover { background:rgba(239,68,68,0.4); color:white; }
.container { max-width:1200px; margin:0 auto; padding:2rem; }
.card { background:white; border-radius:12px; padding:1.5rem; box-shadow:0 1px 3px rgba(0,0,0,0.08); border:1px solid var(--border); margin-bottom:1rem; }
.page-title { font-size:1.75rem; font-weight:700; color:var(--navy); margin-bottom:0.5rem; }
.page-subtitle { color:var(--muted); margin-bottom:2rem; }
.btn { display:inline-flex; align-items:center; gap:0.4rem; padding:0.6rem 1.25rem; border-radius:8px; font-family:\'Sora\',sans-serif; font-size:0.875rem; font-weight:600; cursor:pointer; border:none; text-decoration:none; transition:all 0.2s; }
.btn-primary { background:var(--accent); color:white; }
.btn-primary:hover { background:#1d4ed8; transform:translateY(-1px); }
.btn-success { background:var(--success); color:white; }
.btn-danger { background:var(--danger); color:white; }
.btn-outline { background:transparent; color:var(--accent); border:1.5px solid var(--accent); }
.btn-outline:hover { background:var(--accent); color:white; }
.btn-gold { background:var(--gold); color:var(--navy); }
.btn-gold:hover { background:#d97706; }
.btn-disabled { background:#e2e8f0; color:#94a3b8; cursor:not-allowed; pointer-events:none; border:none; }
.form-group { margin-bottom:1.25rem; }
.form-label { display:block; font-size:0.875rem; font-weight:600; color:var(--text); margin-bottom:0.4rem; }
.form-control { width:100%; padding:0.6rem 0.9rem; border:1.5px solid var(--border); border-radius:8px; font-family:\'Sora\',sans-serif; font-size:0.875rem; transition:border-color 0.2s; background:white; }
.form-control:focus { outline:none; border-color:var(--accent); box-shadow:0 0 0 3px rgba(37,99,235,0.1); }
.form-grid { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
.section-header { background:linear-gradient(135deg, var(--navy), var(--blue)); color:white; padding:0.75rem 1.25rem; border-radius:8px; font-weight:600; font-size:0.95rem; margin:1.5rem 0 1rem; }
.badge { display:inline-block; padding:0.2rem 0.6rem; border-radius:999px; font-size:0.75rem; font-weight:600; }
.badge-success { background:#dcfce7; color:#16a34a; }
.badge-warning { background:#fef3c7; color:#d97706; }
.badge-danger { background:#fee2e2; color:#dc2626; }
.badge-info { background:#dbeafe; color:#2563eb; }
table { width:100%; border-collapse:collapse; }
th { background:var(--light); padding:0.75rem 1rem; text-align:left; font-size:0.8rem; font-weight:600; color:var(--muted); text-transform:uppercase; }
td { padding:0.75rem 1rem; border-bottom:1px solid var(--border); font-size:0.875rem; }
tr:hover td { background:#f8fafc; }
</style>
</head>
<body>
{% if session.get(\'user\') %}
<nav class="navbar">
  <a href="#" class="navbar-brand">Tender<span>AI</span></a>
  <div class="navbar-nav">
    {% if session.get(\'role\') == \'admin\' %}
      <a href="/admin" class="nav-link">Dashboard</a>
      <a href="/admin/create_vendor" class="nav-link">Create Vendor</a>
      <a href="/admin/add_work" class="nav-link">Add Work</a>
      <a href="/admin/new_project" class="nav-link">New Project</a>
      <a href="/admin/project_status" class="nav-link">Project Status</a>
    {% else %}
      <a href="/vendor" class="nav-link">Dashboard</a>
    {% endif %}
    <a href="/logout" class="nav-link logout">Logout</a>
  </div>
</nav>
{% endif %}
{% block content %}{% endblock %}
</body>
</html>'''

# ──────────────────────────────────────────────────────────────────
# login.html  (unchanged)
# ──────────────────────────────────────────────────────────────────
templates["login.html"] = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TenderAI - Login</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:\'Sora\',sans-serif; min-height:100vh; background: linear-gradient(135deg, #0f2544 0%, #1a3c5e 50%, #0f2544 100%); display:flex; align-items:center; justify-content:center; }
.login-wrapper { display:flex; width:900px; min-height:500px; border-radius:20px; overflow:hidden; box-shadow:0 25px 60px rgba(0,0,0,0.4); }
.login-left { flex:1; background:linear-gradient(160deg, #1e4080 0%, #0f2544 100%); padding:3rem; display:flex; flex-direction:column; justify-content:center; }
.brand { font-size:2.5rem; font-weight:800; color:white; letter-spacing:-1px; margin-bottom:0.5rem; }
.brand span { color:#f59e0b; }
.tagline { color:rgba(255,255,255,0.6); font-size:0.95rem; margin-bottom:2.5rem; line-height:1.6; }
.feature { display:flex; align-items:center; gap:0.75rem; margin-bottom:1rem; }
.feature-icon { width:36px; height:36px; border-radius:8px; background:rgba(37,99,235,0.3); display:flex; align-items:center; justify-content:center; font-size:1rem; flex-shrink:0; }
.feature-text { color:rgba(255,255,255,0.8); font-size:0.875rem; }
.login-right { width:380px; background:white; padding:3rem; display:flex; flex-direction:column; justify-content:center; }
.login-title { font-size:1.6rem; font-weight:700; color:#0f2544; margin-bottom:0.4rem; }
.login-subtitle { color:#64748b; font-size:0.875rem; margin-bottom:2rem; }
.form-group { margin-bottom:1.25rem; }
.form-label { display:block; font-size:0.8rem; font-weight:600; color:#475569; margin-bottom:0.4rem; text-transform:uppercase; letter-spacing:0.5px; }
.form-control { width:100%; padding:0.75rem 1rem; border:1.5px solid #e2e8f0; border-radius:10px; font-family:\'Sora\',sans-serif; font-size:0.9rem; transition:all 0.2s; background:#f8fafc; }
.form-control:focus { outline:none; border-color:#2563eb; background:white; box-shadow:0 0 0 3px rgba(37,99,235,0.1); }
.btn-login { width:100%; padding:0.85rem; background:linear-gradient(135deg, #2563eb, #1d4ed8); color:white; border:none; border-radius:10px; font-family:\'Sora\',sans-serif; font-size:0.95rem; font-weight:600; cursor:pointer; transition:all 0.2s; margin-top:0.5rem; }
.btn-login:hover { transform:translateY(-2px); box-shadow:0 8px 20px rgba(37,99,235,0.4); }
.alert-danger { background:#fef2f2; color:#dc2626; border:1px solid #fecaca; padding:0.75rem 1rem; border-radius:8px; margin-bottom:1rem; font-size:0.875rem; }
.hint { background:#f0f4ff; border-radius:8px; padding:0.75rem; margin-top:1.5rem; font-size:0.78rem; color:#475569; }
.hint strong { color:#1a3c5e; }
</style>
</head>
<body>
<div class="login-wrapper">
  <div class="login-left">
    <div class="brand">Tender<span>AI</span></div>
    <p class="tagline">Intelligent Vendor Evaluation &<br>Project Management Platform</p>
    <div class="feature"><div class="feature-icon">🤖</div><div class="feature-text">AI-powered vendor ranking & analysis</div></div>
    <div class="feature"><div class="feature-icon">📊</div><div class="feature-text">Tier-based fair vendor allocation</div></div>
    <div class="feature"><div class="feature-icon">📄</div><div class="feature-text">Automated PDF report generation</div></div>
    <div class="feature"><div class="feature-icon">🏗️</div><div class="feature-text">Complete project lifecycle tracking</div></div>
  </div>
  <div class="login-right">
    <div class="login-title">Welcome Back</div>
    <div class="login-subtitle">Sign in to your account</div>
    {% if error %}<div class="alert-danger">{{ error }}</div>{% endif %}
    <form method="POST">
      <div class="form-group">
        <label class="form-label">Username</label>
        <input type="text" name="username" class="form-control" placeholder="Enter username" required>
      </div>
      <div class="form-group">
        <label class="form-label">Password</label>
        <input type="password" name="password" class="form-control" placeholder="Enter password" required>
      </div>
      <button type="submit" class="btn-login">Sign In →</button>
    </form>
    <div class="hint">
      <strong>Admin:</strong> username: admin / password: admin@123<br>
      <strong>Vendor:</strong> username: 001 / password: 001@123
    </div>
  </div>
</div>
</body>
</html>'''

# ──────────────────────────────────────────────────────────────────
# admin_dashboard.html  — Analyse button locked until deadline
# ──────────────────────────────────────────────────────────────────
templates["admin_dashboard.html"] = '''{% extends "base.html" %}
{% block title %}Admin Dashboard - TenderAI{% endblock %}
{% block content %}
<div class="container" style="padding-top:2rem;">
  <div class="page-title">Admin Dashboard</div>
  <div class="page-subtitle">Welcome back, Administrator</div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-bottom:2rem;">
    <div class="card" style="text-align:center;border-top:4px solid #2563eb;">
      <div style="font-size:2rem;font-weight:800;color:#2563eb;">{{ vendors|length }}</div>
      <div style="color:#64748b;font-size:0.875rem;">Total Vendors</div>
    </div>
    <div class="card" style="text-align:center;border-top:4px solid #10b981;">
      <div style="font-size:2rem;font-weight:800;color:#10b981;">{{ projects|length }}</div>
      <div style="color:#64748b;font-size:0.875rem;">Total Projects</div>
    </div>
    <div class="card" style="text-align:center;border-top:4px solid #f59e0b;">
      <div style="font-size:2rem;font-weight:800;color:#f59e0b;">{{ projects|selectattr("status","eq","open")|list|length }}</div>
      <div style="color:#64748b;font-size:0.875rem;">Open Projects</div>
    </div>
    <div class="card" style="text-align:center;border-top:4px solid #8b5cf6;">
      <div style="font-size:2rem;font-weight:800;color:#8b5cf6;">{{ projects|selectattr("status","eq","closed")|list|length }}</div>
      <div style="color:#64748b;font-size:0.875rem;">Closed Projects</div>
    </div>
  </div>
  <div class="card" style="margin-bottom:2rem;">
    <div style="font-size:1.1rem;font-weight:700;color:#0f2544;margin-bottom:1rem;">Quick Actions</div>
    <div style="display:flex;gap:1rem;flex-wrap:wrap;">
      <a href="/admin/create_vendor" class="btn btn-primary">+ Create Vendor</a>
      <a href="/admin/add_work" class="btn btn-success">Add Vendor Work</a>
      <a href="/admin/new_project" class="btn btn-gold">New Project</a>
      <a href="/admin/project_status" class="btn btn-outline">Project Status</a>
    </div>
  </div>
  <div class="card" style="margin-bottom:2rem;">
    <div style="font-size:1.1rem;font-weight:700;color:#0f2544;margin-bottom:1rem;">Registered Vendors</div>
    {% if vendors %}
    <table>
      <thead><tr><th>ID</th><th>Company</th><th>Type</th><th>District</th><th>Contact</th><th>Experience</th></tr></thead>
      <tbody>
        {% for v in vendors %}
        <tr>
          <td><span class="badge badge-info">{{ v.username }}</span></td>
          <td><strong>{{ v.company_name or "-" }}</strong></td>
          <td>{{ v.company_type or "-" }}</td>
          <td>{{ v.head_office_district or "-" }}</td>
          <td>{{ v.contact_number or "-" }}</td>
          <td>{{ v.years_experience or 0 }} yrs</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <p style="color:#64748b;text-align:center;padding:2rem;">No vendors yet. <a href="/admin/create_vendor" style="color:#2563eb;">Create one</a></p>
    {% endif %}
  </div>
  <div class="card">
    <div style="font-size:1.1rem;font-weight:700;color:#0f2544;margin-bottom:1rem;">Recent Projects</div>
    {% if projects %}
    <table>
      <thead><tr><th>Project</th><th>Location</th><th>Work Type</th><th>Budget</th><th>Deadline</th><th>Status</th><th>Action</th></tr></thead>
      <tbody>
        {% for p in projects[-5:] %}
        <tr>
          <td><strong>{{ p.project_name }}</strong></td>
          <td>{{ p.project_location }}</td>
          <td>{{ p.work_type }}</td>
          <td>Rs.{{ p.original_budget }}</td>
          <td>
            {{ p.deadline_display }}
            {% if not p.deadline_passed %}
            <div style="font-size:0.72rem;color:#f59e0b;font-weight:600;">⏳ Deadline not reached</div>
            {% endif %}
          </td>
          <td>{% if p.status=="open" %}<span class="badge badge-success">Open</span>{% else %}<span class="badge badge-warning">Closed</span>{% endif %}</td>
          <td>
            {% if p.deadline_passed %}
              <a href="/admin/analyse/{{ p._id }}" class="btn btn-outline" style="padding:0.3rem 0.75rem;font-size:0.8rem;">Analyse</a>
            {% else %}
              <span class="btn btn-disabled" style="padding:0.3rem 0.75rem;font-size:0.8rem;" title="Available after deadline">🔒 Locked</span>
            {% endif %}
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
    {% else %}
    <p style="color:#64748b;text-align:center;padding:2rem;">No projects yet. <a href="/admin/new_project" style="color:#2563eb;">Create one</a></p>
    {% endif %}
  </div>
</div>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# vendor_created.html  (unchanged)
# ──────────────────────────────────────────────────────────────────
templates["vendor_created.html"] = '''{% extends "base.html" %}
{% block title %}Vendor Created - TenderAI{% endblock %}
{% block content %}
<div class="container" style="display:flex;align-items:center;justify-content:center;min-height:60vh;">
  <div class="card" style="text-align:center;max-width:480px;padding:3rem;">
    <div style="font-size:4rem;margin-bottom:1rem;">🎉</div>
    <div style="font-size:1.5rem;font-weight:700;color:#0f2544;margin-bottom:0.5rem;">Vendor Created!</div>
    <p style="color:#64748b;margin-bottom:2rem;">The vendor has been successfully registered.</p>
    <div style="background:#f0f4ff;border-radius:12px;padding:1.5rem;margin-bottom:2rem;">
      <div style="font-size:0.8rem;color:#64748b;margin-bottom:0.25rem;">VENDOR LOGIN CREDENTIALS</div>
      <div style="font-size:1.1rem;font-weight:700;color:#1a3c5e;">Username: <span style="color:#2563eb;">{{ vendor_id }}</span></div>
      <div style="font-size:1.1rem;font-weight:700;color:#1a3c5e;">Password: <span style="color:#2563eb;">{{ vendor_id }}@123</span></div>
    </div>
    <div style="display:flex;gap:1rem;justify-content:center;">
      <a href="/admin/create_vendor" class="btn btn-primary">Create Another</a>
      <a href="/admin" class="btn btn-outline">Back to Dashboard</a>
    </div>
  </div>
</div>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# create_vendor.html  (unchanged)
# ──────────────────────────────────────────────────────────────────
templates["create_vendor.html"] = '''{% extends "base.html" %}
{% block title %}Create Vendor - TenderAI{% endblock %}
{% block content %}
<div class="container">
  <div class="page-title">Create New Vendor</div>
  <div class="page-subtitle">Register a new vendor/contractor in the system</div>
  <div class="card">
    <form method="POST">
      <div class="section-header">1. Basic Company Information</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Company Name *</label><input type="text" name="company_name" class="form-control" required></div>
        <div class="form-group"><label class="form-label">Type of Company *</label>
          <select name="company_type" class="form-control" required><option value="">Select...</option><option>Proprietorship</option><option>Partnership</option><option>Pvt Ltd</option><option>Ltd</option></select></div>
        <div class="form-group"><label class="form-label">Year of Establishment</label><input type="number" name="year_established" class="form-control"></div>
        <div class="form-group"><label class="form-label">Registration Number</label><input type="text" name="reg_number" class="form-control"></div>
        <div class="form-group"><label class="form-label">GST Number</label><input type="text" name="gst_number" class="form-control"></div>
        <div class="form-group"><label class="form-label">PAN Number</label><input type="text" name="pan_number" class="form-control"></div>
        <div class="form-group"><label class="form-label">Head Office District *</label>
          <select name="head_office_district" class="form-control" required><option value="">Select...</option>{% for d in districts %}<option>{{ d }}</option>{% endfor %}</select></div>
        <div class="form-group"><label class="form-label">Contact Number *</label><input type="text" name="contact_number" class="form-control" required></div>
        <div class="form-group"><label class="form-label">Official Email *</label><input type="email" name="email" class="form-control" required></div>
        <div class="form-group"><label class="form-label">Website</label><input type="text" name="website" class="form-control"></div>
        <div class="form-group" style="grid-column:span 2"><label class="form-label">Branch Office Locations</label><input type="text" name="branch_locations" class="form-control"></div>
      </div>
      <div class="section-header">2. Ownership & Management</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Owner / MD Name *</label><input type="text" name="owner_name" class="form-control" required></div>
        <div class="form-group"><label class="form-label">Key Decision Maker</label><input type="text" name="key_decision_maker" class="form-control"></div>
        <div class="form-group"><label class="form-label">Total Employees</label><input type="number" name="total_employees" class="form-control"></div>
        <div class="form-group"><label class="form-label">Organizational Structure</label><input type="text" name="org_structure" class="form-control"></div>
        <div class="form-group" style="grid-column:span 2"><label class="form-label">Board of Directors</label><input type="text" name="board_of_directors" class="form-control"></div>
      </div>
      <div class="section-header">3. Business Profile</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Nature of Business</label><input type="text" name="nature_of_business" class="form-control"></div>
        <div class="form-group"><label class="form-label">Core Specialization</label><input type="text" name="core_specialization" class="form-control"></div>
        <div class="form-group"><label class="form-label">Service Areas</label><input type="text" name="service_areas" class="form-control"></div>
        <div class="form-group"><label class="form-label">Years of Experience *</label><input type="number" name="years_experience" class="form-control" required value="0"></div>
        <div class="form-group"><label class="form-label">Avg Projects Per Year</label><input type="number" name="avg_projects_per_year" class="form-control"></div>
      </div>
      <div class="section-header">4. Financial Profile</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Avg Annual Turnover (Rs.)</label><input type="text" name="avg_annual_turnover" class="form-control"></div>
        <div class="form-group"><label class="form-label">Net Worth (Rs.)</label><input type="text" name="net_worth" class="form-control"></div>
        <div class="form-group"><label class="form-label">Financial Stability</label>
          <select name="financial_stability" class="form-control"><option>Stable</option><option>Moderate</option><option>At Risk</option></select></div>
        <div class="form-group"><label class="form-label">Financial Commitments</label><input type="text" name="financial_commitments" class="form-control"></div>
      </div>
      <div class="section-header">5. Technical Capacity</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Total Engineers</label><input type="number" name="total_engineers" class="form-control"></div>
        <div class="form-group"><label class="form-label">Total Technical Staff</label><input type="number" name="total_technical_staff" class="form-control"></div>
        <div class="form-group"><label class="form-label">Major Machinery</label><input type="text" name="major_machinery" class="form-control"></div>
        <div class="form-group"><label class="form-label">Equipment Capacity</label>
          <select name="equipment_capacity" class="form-control"><option>Low</option><option>Medium</option><option>High</option></select></div>
      </div>
      <div class="section-header">6. Performance History</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Total Projects Completed *</label><input type="number" name="total_projects_completed" class="form-control" required value="0"></div>
        <div class="form-group"><label class="form-label">Ongoing Projects</label><input type="number" name="ongoing_projects" class="form-control"></div>
        <div class="form-group"><label class="form-label">Govt Project Experience</label>
          <select name="govt_experience" class="form-control"><option>Yes</option><option>No</option></select></div>
        <div class="form-group"><label class="form-label">Blacklisting History</label>
          <select name="blacklisting_history" class="form-control"><option>No</option><option>Yes</option></select></div>
        <div class="form-group"><label class="form-label">Legal Disputes</label>
          <select name="legal_disputes" class="form-control"><option>No</option><option>Yes</option></select></div>
      </div>
      <div class="section-header">7. Compliance & Certifications</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">ISO Certification</label>
          <select name="iso_certification" class="form-control"><option>Not Certified</option><option>ISO 9001</option><option>ISO 14001</option><option>ISO 45001</option><option>Multiple</option></select></div>
        <div class="form-group"><label class="form-label">Safety Compliance</label>
          <select name="safety_compliance" class="form-control"><option>High</option><option>Medium</option><option>Low</option></select></div>
        <div class="form-group"><label class="form-label">Environmental Compliance</label>
          <select name="env_compliance" class="form-control"><option>Compliant</option><option>Partial</option><option>Non-Compliant</option></select></div>
        <div class="form-group"><label class="form-label">Labour Law Compliance</label>
          <select name="labour_compliance" class="form-control"><option>Compliant</option><option>Partial</option><option>Non-Compliant</option></select></div>
      </div>
      <div style="margin-top:2rem;display:flex;gap:1rem;">
        <button type="submit" class="btn btn-primary">Create Vendor</button>
        <a href="/admin" class="btn btn-outline">Cancel</a>
      </div>
    </form>
  </div>
</div>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# add_work.html  (unchanged)
# ──────────────────────────────────────────────────────────────────
templates["add_work.html"] = '''{% extends "base.html" %}
{% block title %}Add Work - TenderAI{% endblock %}
{% block content %}
<div class="container">
  <div class="page-title">Add Vendor Work History</div>
  <div class="page-subtitle">Record past project experience for a vendor</div>
  <div class="card">
    <form method="POST">
      <div class="form-group"><label class="form-label">Select Vendor *</label>
        <select name="vendor_username" class="form-control" required>
          <option value="">Select Vendor...</option>
          {% for v in vendors %}<option value="{{ v.username }}">{{ v.username }} - {{ v.company_name or "N/A" }}</option>{% endfor %}
        </select></div>
      <div class="section-header">1. Basic Project Identification</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Project Name *</label><input type="text" name="project_name" class="form-control" required></div>
        <div class="form-group"><label class="form-label">Location (District)</label>
          <select name="project_location" class="form-control"><option value="">Select...</option>{% for d in districts %}<option>{{ d }}</option>{% endfor %}</select></div>
        <div class="form-group"><label class="form-label">Client Name</label><input type="text" name="client_name" class="form-control"></div>
        <div class="form-group"><label class="form-label">Client Type</label>
          <select name="client_type" class="form-control"><option>Govt</option><option>PSU</option><option>Private</option><option>Individual</option></select></div>
        <div class="form-group"><label class="form-label">Year of Award</label><input type="number" name="year_award" class="form-control"></div>
        <div class="form-group"><label class="form-label">Year of Completion</label><input type="number" name="year_completion" class="form-control"></div>
      </div>
      <div class="section-header">2. Type of Work</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Work Type *</label>
          <select name="work_type" class="form-control" required><option value="">Select...</option>{% for wt in work_types %}<option>{{ wt }}</option>{% endfor %}</select></div>
        <div class="form-group"><label class="form-label">If Other, Specify</label><input type="text" name="work_type_other" class="form-control"></div>
      </div>
      <div class="section-header">3. Financial Details</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Original Budget (Rs.)</label><input type="text" name="original_budget" class="form-control"></div>
        <div class="form-group"><label class="form-label">Final Cost (Rs.)</label><input type="text" name="final_cost" class="form-control"></div>
        <div class="form-group"><label class="form-label">Budget Variation (Rs.)</label><input type="text" name="budget_variation" class="form-control"></div>
        <div class="form-group"><label class="form-label">Budget Overrun (%)</label><input type="number" name="budget_overrun_pct" class="form-control" step="0.01"></div>
        <div class="form-group" style="grid-column:span 2"><label class="form-label">Reason for Cost Increase</label><input type="text" name="cost_increase_reason" class="form-control"></div>
      </div>
      <div class="section-header">4. Time & Completion</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Planned Start</label><input type="date" name="planned_start" class="form-control"></div>
        <div class="form-group"><label class="form-label">Planned Completion</label><input type="date" name="planned_completion" class="form-control"></div>
        <div class="form-group"><label class="form-label">Actual Completion</label><input type="date" name="actual_completion" class="form-control"></div>
        <div class="form-group"><label class="form-label">Planned Duration (months)</label><input type="number" name="planned_duration" class="form-control"></div>
        <div class="form-group"><label class="form-label">Actual Duration (months)</label><input type="number" name="actual_duration" class="form-control"></div>
        <div class="form-group"><label class="form-label">Delay (months)</label><input type="number" name="delay_months" class="form-control"></div>
        <div class="form-group" style="grid-column:span 2"><label class="form-label">Reason for Delay</label><input type="text" name="delay_reason" class="form-control"></div>
      </div>
      <div class="section-header">5. Performance Metrics</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Work Completed (%)</label><input type="number" name="work_completed_pct" class="form-control" max="100"></div>
        <div class="form-group"><label class="form-label">Completed On Time?</label>
          <select name="completed_on_time" class="form-control"><option>Yes</option><option>No</option></select></div>
        <div class="form-group"><label class="form-label">Within Budget?</label>
          <select name="completed_within_budget" class="form-control"><option>Yes</option><option>No</option></select></div>
        <div class="form-group"><label class="form-label">Client Satisfaction (1-5)</label>
          <select name="client_satisfaction" class="form-control"><option>5</option><option>4</option><option>3</option><option>2</option><option>1</option></select></div>
        <div class="form-group"><label class="form-label">Penalty Imposed?</label>
          <select name="penalty_imposed" class="form-control"><option>No</option><option>Yes</option></select></div>
        <div class="form-group"><label class="form-label">Early Completion Bonus?</label>
          <select name="early_completion_bonus" class="form-control"><option>No</option><option>Yes</option></select></div>
      </div>
      <div class="section-header">6. Scope & Risk</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Built-up Area (sqft)</label><input type="text" name="built_up_area" class="form-control"></div>
        <div class="form-group"><label class="form-label">Length/Area Covered</label><input type="text" name="length_area_covered" class="form-control"></div>
        <div class="form-group"><label class="form-label">Units Completed</label><input type="number" name="units_completed" class="form-control"></div>
        <div class="form-group"><label class="form-label">Complexity Level</label>
          <select name="complexity_level" class="form-control"><option>Low</option><option>Medium</option><option>High</option></select></div>
        <div class="form-group" style="grid-column:span 2"><label class="form-label">Major Challenges</label><textarea name="major_challenges" class="form-control" rows="2"></textarea></div>
        <div class="form-group"><label class="form-label">Legal Disputes?</label>
          <select name="legal_disputes" class="form-control"><option>No</option><option>Yes</option></select></div>
        <div class="form-group"><label class="form-label">Arbitration Cases</label><input type="text" name="arbitration_cases" class="form-control"></div>
      </div>
      <div style="margin-top:2rem;display:flex;gap:1rem;">
        <button type="submit" class="btn btn-primary">Save Work Record</button>
        <a href="/admin" class="btn btn-outline">Cancel</a>
      </div>
    </form>
  </div>
</div>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# new_project.html  — deadline changed to datetime-local
# ──────────────────────────────────────────────────────────────────
templates["new_project.html"] = '''{% extends "base.html" %}
{% block title %}New Project - TenderAI{% endblock %}
{% block content %}
<div class="container">
  <div class="page-title">Create New Project</div>
  <div class="page-subtitle">Post a new tender project for vendor bidding</div>
  <div class="card">
    <form method="POST">
      <div class="section-header">1. Basic Project Identification</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Project Name *</label><input type="text" name="project_name" class="form-control" required></div>
        <div class="form-group"><label class="form-label">Location *</label>
          <select name="project_location" class="form-control" required><option value="">Select District...</option>{% for d in districts %}<option>{{ d }}</option>{% endfor %}</select></div>
        <div class="form-group"><label class="form-label">Client Name</label><input type="text" name="client_name" class="form-control"></div>
        <div class="form-group"><label class="form-label">Client Type</label>
          <select name="client_type" class="form-control"><option>Govt</option><option>PSU</option><option>Private</option><option>Individual</option></select></div>
        <div class="form-group"><label class="form-label">Year of Award</label><input type="number" name="year_award" class="form-control"></div>
        <div class="form-group"><label class="form-label">Year of Completion</label><input type="number" name="year_completion" class="form-control"></div>
      </div>
      <div class="section-header">2. Type of Work</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Work Type *</label>
          <select name="work_type" class="form-control" required><option value="">Select...</option>{% for wt in work_types %}<option>{{ wt }}</option>{% endfor %}</select></div>
        <div class="form-group"><label class="form-label">If Other, Specify</label><input type="text" name="work_type_other" class="form-control"></div>
      </div>
      <div class="section-header">3. Financial Details</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Original Budget (Rs.) *</label><input type="text" name="original_budget" class="form-control" required></div>
        <div class="form-group"><label class="form-label">Final Project Cost (Rs.)</label><input type="text" name="final_cost" class="form-control"></div>
        <div class="form-group"><label class="form-label">Budget Variation (Rs.)</label><input type="text" name="budget_variation" class="form-control"></div>
        <div class="form-group"><label class="form-label">Budget Overrun (%)</label><input type="number" name="budget_overrun_pct" class="form-control" step="0.01"></div>
      </div>
      <div class="section-header">4. Time & Completion</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Planned Start</label><input type="date" name="planned_start" class="form-control"></div>
        <div class="form-group"><label class="form-label">Planned Completion</label><input type="date" name="planned_completion" class="form-control"></div>
        <div class="form-group"><label class="form-label">Planned Duration (months)</label><input type="number" name="planned_duration" class="form-control"></div>
        <div class="form-group"><label class="form-label">Complexity Level</label>
          <select name="complexity_level" class="form-control"><option>Low</option><option>Medium</option><option>High</option></select></div>
      </div>
      <div class="section-header">5. Scope & Risk</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Built-up Area (sqft)</label><input type="text" name="built_up_area" class="form-control"></div>
        <div class="form-group"><label class="form-label">Length/Area Covered</label><input type="text" name="length_area_covered" class="form-control"></div>
        <div class="form-group" style="grid-column:span 2"><label class="form-label">Major Challenges Expected</label><textarea name="major_challenges" class="form-control" rows="2"></textarea></div>
        <div class="form-group"><label class="form-label">Legal Disputes History?</label>
          <select name="legal_disputes" class="form-control"><option>No</option><option>Yes</option></select></div>
      </div>
      <div class="section-header">Submission Deadline</div>
      <div class="form-grid" style="max-width:600px;">
        <div class="form-group">
          <label class="form-label">Deadline Date *</label>
          <input type="date" name="deadline_date" id="deadline_date" class="form-control" required>
        </div>
        <div class="form-group">
          <label class="form-label">Deadline Time *</label>
          <input type="time" name="deadline_time" id="deadline_time" class="form-control" required>
        </div>
      </div>
      <input type="hidden" name="submission_deadline_dt" id="submission_deadline_dt">
      <div style="background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:0.75rem 1rem;margin-bottom:1rem;font-size:0.82rem;color:#9a3412;max-width:600px;">
        ⏰ <strong>Important:</strong> The Analyse button will be locked for this project until the above deadline date & time has passed.
      </div>
      <div style="margin-top:2rem;display:flex;gap:1rem;">
        <button type="submit" class="btn btn-gold" onclick="combineDatetime()">Create Project</button>
        <a href="/admin" class="btn btn-outline">Cancel</a>
      </div>
    </form>
  </div>
</div>
<script>
function combineDatetime() {
  var d = document.getElementById("deadline_date").value;
  var t = document.getElementById("deadline_time").value;
  if (d && t) {
    document.getElementById("submission_deadline_dt").value = d + "T" + t;
  }
}
// Also combine on form submit
document.querySelector("form").addEventListener("submit", function() { combineDatetime(); });
</script>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# project_status.html  — Analyse button locked until deadline
# ──────────────────────────────────────────────────────────────────
templates["project_status.html"] = '''{% extends "base.html" %}
{% block title %}Project Status - TenderAI{% endblock %}
{% block content %}
<div class="container">
  <div class="page-title">Project Status</div>
  <div class="page-subtitle">Overview of all tender projects</div>
  {% if projects %}
  <div style="display:grid;gap:1.25rem;">
    {% for p in projects %}
    <div class="card" style="border-left:4px solid {% if p.status=="open" %}#10b981{% else %}#f59e0b{% endif %};">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
        <div>
          <div style="font-size:1.1rem;font-weight:700;color:#0f2544;">{{ p.project_name }}</div>
          <div style="color:#64748b;font-size:0.875rem;margin-top:0.2rem;">
            {{ p.project_location }} | {{ p.work_type }} | Rs.{{ p.original_budget }}
          </div>
          <div style="color:#64748b;font-size:0.875rem;">
            Deadline: <strong>{{ p.deadline_display }}</strong> | Responses: {{ p.vendor_responses|length if p.vendor_responses else 0 }}
          </div>
          {% if not p.deadline_passed %}
          <div style="font-size:0.78rem;color:#f59e0b;font-weight:600;margin-top:0.25rem;">⏳ Deadline not reached — Analyse locked</div>
          {% else %}
          <div style="font-size:0.78rem;color:#10b981;font-weight:600;margin-top:0.25rem;">✅ Deadline passed — Analyse available</div>
          {% endif %}
        </div>
        <div style="display:flex;gap:0.75rem;align-items:center;flex-wrap:wrap;">
          {% if p.status=="open" %}<span class="badge badge-success">Open</span>{% else %}<span class="badge badge-warning">Closed</span>{% endif %}
          {% if p.deadline_passed %}
            <a href="/admin/analyse/{{ p._id }}" class="btn btn-primary" style="padding:0.4rem 1rem;font-size:0.85rem;">Analyse</a>
            <a href="/admin/generate_pdf/{{ p._id }}" class="btn btn-gold" style="padding:0.4rem 1rem;font-size:0.85rem;">PDF</a>
          {% else %}
            <span class="btn btn-disabled" style="padding:0.4rem 1rem;font-size:0.85rem;" title="Locked until deadline passes">🔒 Analyse</span>
            <span class="btn btn-disabled" style="padding:0.4rem 1rem;font-size:0.85rem;" title="Locked until deadline passes">🔒 PDF</span>
          {% endif %}
          <a href="/admin/edit_project/{{ p._id }}" class="btn btn-outline" style="padding:0.4rem 1rem;font-size:0.85rem;">✏️ Modify</a>
          <form method="POST" action="/admin/delete_project/{{ p._id }}" style="display:inline;" onsubmit="return confirm(\'Are you sure you want to delete this project? This cannot be undone.\')">
            <button type="submit" class="btn btn-danger" style="padding:0.4rem 1rem;font-size:0.85rem;">🗑 Delete</button>
          </form>
        </div>
      </div>
      {% if p.vendor_responses %}
      <div style="margin-top:1rem;border-top:1px solid #e2e8f0;padding-top:1rem;">
        <div style="font-size:0.8rem;font-weight:600;color:#64748b;margin-bottom:0.5rem;">VENDOR RESPONSES</div>
        <div style="display:flex;gap:0.5rem;flex-wrap:wrap;">
          {% for vname, resp in p.vendor_responses.items() %}
          <span class="badge {% if resp.decision=="approve" %}badge-success{% else %}badge-danger{% endif %}">{{ vname }}: {{ resp.decision|upper }}</span>
          {% endfor %}
        </div>
      </div>
      {% endif %}
    </div>
    {% endfor %}
  </div>
  {% else %}
  <div class="card" style="text-align:center;padding:3rem;">
    <p style="color:#64748b;">No projects yet. <a href="/admin/new_project" style="color:#2563eb;">Create one</a></p>
  </div>
  {% endif %}
</div>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# analyse.html  — blocks if deadline not passed; shows approved-only top 5
#                 with proposed cost & time columns
# ──────────────────────────────────────────────────────────────────
templates["analyse.html"] = '''{% extends "base.html" %}
{% block title %}Analyse - TenderAI{% endblock %}
{% block content %}
<div class="container">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;">
    <div>
      <div class="page-title">AI Project Analysis</div>
      <div class="page-subtitle">{{ project.project_name }}</div>
    </div>
    <div style="display:flex;gap:0.75rem;">
      {% if deadline_passed %}
        <a href="/admin/generate_pdf/{{ project._id }}" class="btn btn-gold">Download PDF</a>
      {% endif %}
      <a href="/admin/project_status" class="btn btn-outline">Back</a>
    </div>
  </div>

  {% if not deadline_passed %}
  <!-- ── DEADLINE NOT PASSED — LOCKED STATE ── -->
  <div style="background:#fff7ed;border:2px solid #fed7aa;border-radius:16px;padding:3rem;text-align:center;margin-bottom:1.5rem;">
    <div style="font-size:4rem;margin-bottom:1rem;">🔒</div>
    <div style="font-size:1.4rem;font-weight:700;color:#9a3412;margin-bottom:0.5rem;">Analysis Locked</div>
    <p style="color:#c2410c;font-size:0.95rem;margin-bottom:1.5rem;">
      This project\'s submission deadline has <strong>not yet passed</strong>.<br>
      AI analysis and vendor recommendations will be available after the deadline.
    </p>
    <div style="display:inline-block;background:#fef3c7;border:1.5px solid #f59e0b;border-radius:10px;padding:1rem 2rem;">
      <div style="font-size:0.8rem;color:#92400e;margin-bottom:0.25rem;">SUBMISSION DEADLINE</div>
      <div style="font-size:1.3rem;font-weight:800;color:#92400e;">{{ deadline_display }}</div>
    </div>
  </div>
  {% endif %}

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.25rem;margin-bottom:1.5rem;">
    <div class="card">
      <div style="font-weight:700;color:#0f2544;margin-bottom:1rem;">Project Details</div>
      <table style="font-size:0.875rem;">
        <tr><td style="color:#64748b;padding:0.3rem 1rem 0.3rem 0;width:140px;">Name</td><td><strong>{{ project.project_name }}</strong></td></tr>
        <tr><td style="color:#64748b;padding:0.3rem 1rem 0.3rem 0;">Location</td><td>{{ project.project_location }}</td></tr>
        <tr><td style="color:#64748b;padding:0.3rem 1rem 0.3rem 0;">Work Type</td><td>{{ project.work_type }}</td></tr>
        <tr><td style="color:#64748b;padding:0.3rem 1rem 0.3rem 0;">Budget</td><td><strong style="color:#10b981;">Rs.{{ project.original_budget }}</strong></td></tr>
        <tr><td style="color:#64748b;padding:0.3rem 1rem 0.3rem 0;">Deadline</td><td>{{ deadline_display }}</td></tr>
        <tr><td style="color:#64748b;padding:0.3rem 1rem 0.3rem 0;">Complexity</td><td>{{ project.complexity_level }}</td></tr>
      </table>
    </div>
    <div class="card">
      <div style="font-weight:700;color:#0f2544;margin-bottom:1rem;">AI Assessment</div>
      <div style="margin-bottom:1rem;">
        <div style="font-size:0.8rem;color:#64748b;margin-bottom:0.3rem;">PROJECT TIER</div>
        <span class="badge {% if project_tier=="High" %}badge-danger{% elif project_tier=="Medium" %}badge-warning{% else %}badge-success{% endif %}" style="font-size:1rem;padding:0.4rem 1rem;">{{ project_tier }} Value</span>
      </div>
      <div style="margin-bottom:1rem;">
        <div style="font-size:0.8rem;color:#64748b;margin-bottom:0.3rem;">VENDOR RESPONSES</div>
        {% if project.vendor_responses %}
          {% for vname, resp in project.vendor_responses.items() %}
          <span class="badge {% if resp.decision=="approve" %}badge-success{% else %}badge-danger{% endif %}" style="margin-right:0.3rem;">{{ vname }}: {{ resp.decision|upper }}</span>
          {% endfor %}
        {% else %}<span style="color:#64748b;font-size:0.875rem;">No responses yet</span>{% endif %}
      </div>
      <div style="font-size:0.875rem;color:#1e293b;">
        {% if project_tier=="High" %}Tier A vendors recommended (High experience required)
        {% elif project_tier=="Medium" %}Tier A + Tier B vendors eligible
        {% else %}Tier C vendors preferred (Equal opportunity for new vendors){% endif %}
      </div>
    </div>
  </div>

  {% if deadline_passed %}
  <div class="card">
    <div style="font-size:1.1rem;font-weight:700;color:#0f2544;margin-bottom:0.5rem;">Top Recommended Vendors (AI Ranked)</div>
    <div style="font-size:0.82rem;color:#64748b;margin-bottom:1.25rem;">
      ✅ Only vendors who <strong>approved</strong> the project are included. Ranked by AI score incorporating experience, track record, proposed cost vs budget, and proposed time vs planned duration.
    </div>
    {% if top_vendors %}
    <div style="display:grid;gap:1rem;">
      {% for v in top_vendors %}
      <div style="display:flex;align-items:center;gap:1.25rem;padding:1rem;border-radius:10px;border:1.5px solid {% if loop.index==1 %}#f59e0b{% else %}#e2e8f0{% endif %};background:{% if loop.index==1 %}#fffbeb{% else %}#f8fafc{% endif %};">
        <div style="width:48px;height:48px;border-radius:50%;background:{% if loop.index==1 %}#f59e0b{% elif loop.index==2 %}#94a3b8{% elif loop.index==3 %}#b45309{% else %}#1a3c5e{% endif %};color:white;display:flex;align-items:center;justify-content:center;font-size:1.2rem;font-weight:800;flex-shrink:0;">{{ loop.index }}</div>
        <div style="flex:1;">
          <div style="font-weight:700;color:#0f2544;">{{ v.company_name }}</div>
          <div style="font-size:0.8rem;color:#64748b;">ID: {{ v.username }} | Exp: {{ v.experience }} yrs | Projects: {{ v.projects_completed }}</div>
          <div style="font-size:0.8rem;color:#0f2544;margin-top:0.2rem;">
            💰 Proposed: <strong style="color:#10b981;">Rs.{{ v.proposed_cost }}</strong>
            &nbsp;&nbsp;⏱ Time: <strong style="color:#2563eb;">{{ v.proposed_time }} months</strong>
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:1.2rem;font-weight:800;color:#2563eb;">{{ v.score }}</div>
          <div style="font-size:0.75rem;color:#64748b;">AI Score</div>
        </div>
        <span class="badge {% if v.tier=="A" %}badge-success{% elif v.tier=="B" %}badge-warning{% else %}badge-info{% endif %}" style="font-size:0.9rem;padding:0.3rem 0.8rem;">Tier {{ v.tier }}</span>
      </div>
      {% endfor %}
    </div>
    <div style="margin-top:1.5rem;padding:1rem;background:#f0f4ff;border-radius:8px;font-size:0.85rem;color:#1a3c5e;">
      <strong>Scoring criteria:</strong> Experience (20pts) + On-time delivery (20pts) + Budget adherence (20pts) + Financial capacity (20pts) + Clean record (20pts) + Tier &amp; work-type match bonus + Proposed cost vs budget (max +20pts) + Proposed time vs planned duration (max +15pts).
    </div>
    {% if top_vendors %}
    <!-- Charts Section -->
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-top:1.5rem;">
      <div class="card" style="padding:1.25rem;">
        <div style="font-weight:700;color:#0f2544;margin-bottom:1rem;font-size:0.95rem;">📊 AI Score Comparison</div>
        <canvas id="scoreChart" height="220"></canvas>
      </div>
      <div class="card" style="padding:1.25rem;">
        <div style="font-weight:700;color:#0f2544;margin-bottom:1rem;font-size:0.95rem;">💰 Proposed Cost vs Budget</div>
        <canvas id="costChart" height="220"></canvas>
      </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
    <script>
    (function() {
      var vendors = {{ top_vendors | tojson }};
      var labels = vendors.map(function(v){ return v.company_name.length > 12 ? v.company_name.substring(0,12)+"…" : v.company_name; });
      var scores = vendors.map(function(v){ return v.score; });
      var costs = vendors.map(function(v){
        var c = parseFloat(String(v.proposed_cost).replace(/,/g,""));
        return isNaN(c) ? 0 : c;
      });
      var budget = parseFloat("{{ project.original_budget }}".replace(/,/g,"")) || 0;
      var palette = ["#2563eb","#10b981","#f59e0b","#8b5cf6","#ef4444"];

      // Chart 1 — AI Scores horizontal bar
      new Chart(document.getElementById("scoreChart"), {
        type: "bar",
        data: {
          labels: labels,
          datasets: [{
            label: "AI Score",
            data: scores,
            backgroundColor: palette,
            borderRadius: 6,
          }]
        },
        options: {
          indexAxis: "y",
          plugins: { legend: { display: false } },
          scales: {
            x: { beginAtZero: true, grid: { color: "#e2e8f0" }, ticks: { font: { size: 11 } } },
            y: { grid: { display: false }, ticks: { font: { size: 11 } } }
          }
        }
      });

      // Chart 2 — Proposed Cost vs Budget
      var costDatasets = [{
        label: "Proposed Cost",
        data: costs,
        backgroundColor: palette,
        borderRadius: 6,
      }];
      new Chart(document.getElementById("costChart"), {
        type: "bar",
        data: { labels: labels, datasets: costDatasets },
        options: {
          plugins: {
            legend: { display: false },
            annotation: {}
          },
          scales: {
            x: { ticks: { font: { size: 11 } }, grid: { color: "#e2e8f0" } },
            y: {
              beginAtZero: true,
              grid: { display: false },
              ticks: {
                font: { size: 10 },
                callback: function(v){ return "Rs."+(v>=10000000?(v/10000000).toFixed(1)+"Cr":v>=100000?(v/100000).toFixed(1)+"L":v); }
              }
            }
          }
        },
        plugins: [{
          id: "budgetLine",
          afterDraw: function(chart) {
            if (!budget) return;
            var yScale = chart.scales.y;
            var xScale = chart.scales.x;
            var ctx2 = chart.ctx;
            var yPixel = yScale.getPixelForValue(budget);
            ctx2.save();
            ctx2.beginPath();
            ctx2.moveTo(xScale.left, yPixel);
            ctx2.lineTo(xScale.right, yPixel);
            ctx2.strokeStyle = "#ef4444";
            ctx2.lineWidth = 2;
            ctx2.setLineDash([6,3]);
            ctx2.stroke();
            ctx2.fillStyle = "#ef4444";
            ctx2.font = "bold 10px sans-serif";
            ctx2.fillText("Budget", xScale.right - 50, yPixel - 4);
            ctx2.restore();
          }
        }]
      });
    })();
    </script>
    {% endif %}
    {% else %}
    <div style="text-align:center;padding:2.5rem;color:#64748b;">
      <div style="font-size:2.5rem;margin-bottom:0.75rem;">📭</div>
      <strong>No approved bids yet.</strong><br>
      <span style="font-size:0.875rem;">Vendors who click Approve and submit a cost & time proposal will appear here.</span>
    </div>
    {% endif %}
  </div>
  {% endif %}
</div>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# vendor_dashboard.html  — shows formatted deadline
# ──────────────────────────────────────────────────────────────────
templates["vendor_dashboard.html"] = '''{% extends "base.html" %}
{% block title %}Vendor Dashboard - TenderAI{% endblock %}
{% block content %}
<div class="container">
  <div class="page-title">Vendor Dashboard</div>
  <div class="page-subtitle">Welcome, {{ vendor.company_name if vendor else session["user"] }} (ID: {{ session["user"] }})</div>
  {% if vendor %}
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem;">
    <div class="card" style="text-align:center;border-top:4px solid #2563eb;">
      <div style="font-size:1.5rem;font-weight:800;color:#2563eb;">{{ vendor.years_experience or 0 }}</div>
      <div style="color:#64748b;font-size:0.875rem;">Years Experience</div>
    </div>
    <div class="card" style="text-align:center;border-top:4px solid #10b981;">
      <div style="font-size:1.5rem;font-weight:800;color:#10b981;">{{ vendor.total_projects_completed or 0 }}</div>
      <div style="color:#64748b;font-size:0.875rem;">Projects Completed</div>
    </div>
    <div class="card" style="text-align:center;border-top:4px solid #f59e0b;">
      <div style="font-size:1.5rem;font-weight:800;color:#f59e0b;">{{ vendor.head_office_district or "-" }}</div>
      <div style="color:#64748b;font-size:0.875rem;">Head Office</div>
    </div>
  </div>
  {% endif %}
  <div class="card">
    <div style="font-size:1.1rem;font-weight:700;color:#0f2544;margin-bottom:1rem;">Open Projects — Approve or Deny</div>
    {% if projects %}
    <div style="display:grid;gap:1rem;">
      {% for p in projects %}
      {% set already_responded = p.vendor_responses and session["user"] in p.vendor_responses %}
      <div style="border:1.5px solid {% if already_responded %}#bbf7d0{% else %}#e2e8f0{% endif %};border-radius:10px;padding:1.25rem;background:{% if already_responded %}#f0fdf4{% else %}white{% endif %};">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;">
          <div>
            <div style="font-weight:700;font-size:1rem;color:#0f2544;">{{ p.project_name }}</div>
            <div style="font-size:0.875rem;color:#64748b;margin-top:0.3rem;">{{ p.project_location }} | {{ p.work_type }} | Rs.{{ p.original_budget }}</div>
            <div style="font-size:0.875rem;color:#64748b;">Deadline: <strong>{{ p.deadline_display }}</strong></div>
          </div>
          <div>
            {% if already_responded %}
              {% set resp = p.vendor_responses[session["user"]] %}
              <span class="badge {% if resp.decision=="approve" %}badge-success{% else %}badge-danger{% endif %}" style="font-size:0.9rem;padding:0.4rem 1rem;">{{ resp.decision|upper }}</span>
              {% if resp.decision=="approve" %}
              <div style="font-size:0.8rem;color:#64748b;margin-top:0.4rem;">Cost: Rs.{{ resp.proposed_cost }} | Time: {{ resp.completion_time }} months</div>
              {% endif %}
            {% else %}
              <a href="/vendor/respond/{{ p._id }}" class="btn btn-primary">Respond</a>
            {% endif %}
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
    {% else %}
    <div style="text-align:center;padding:3rem;color:#64748b;">No open projects at the moment.</div>
    {% endif %}
  </div>
</div>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# vendor_respond.html  — shows formatted deadline
# ──────────────────────────────────────────────────────────────────
templates["vendor_respond.html"] = '''{% extends "base.html" %}
{% block title %}Respond - TenderAI{% endblock %}
{% block content %}
<div class="container" style="max-width:700px;">
  <div class="page-title">Respond to Project</div>
  <div class="page-subtitle">{{ project.project_name }}</div>
  <div class="card" style="margin-bottom:1.5rem;">
    <div style="font-weight:700;color:#0f2544;margin-bottom:1rem;">Project Details</div>
    <div class="form-grid">
      <div><span style="color:#64748b;font-size:0.8rem;">LOCATION</span><br><strong>{{ project.project_location }}</strong></div>
      <div><span style="color:#64748b;font-size:0.8rem;">WORK TYPE</span><br><strong>{{ project.work_type }}</strong></div>
      <div><span style="color:#64748b;font-size:0.8rem;">BUDGET</span><br><strong style="color:#10b981;">Rs.{{ project.original_budget }}</strong></div>
      <div><span style="color:#64748b;font-size:0.8rem;">DEADLINE</span><br><strong>{{ project.deadline_display }}</strong></div>
    </div>
  </div>
  <div class="card">
    <div style="font-weight:700;color:#0f2544;margin-bottom:1.5rem;">Your Response</div>
    <form method="POST" id="responseForm">
      <div class="form-group">
        <label class="form-label">Decision *</label>
        <div style="display:flex;gap:1rem;">
          <label style="flex:1;cursor:pointer;">
            <input type="radio" name="decision" value="approve" style="display:none;" onchange="toggleApprove(true)">
            <div id="approveBtn" style="border:2px solid #e2e8f0;border-radius:10px;padding:1rem;text-align:center;transition:all 0.2s;">
              <div style="font-size:1.5rem;">✅</div>
              <div style="font-weight:600;color:#10b981;">APPROVE</div>
              <div style="font-size:0.8rem;color:#64748b;">I want to bid for this project</div>
            </div>
          </label>
          <label style="flex:1;cursor:pointer;">
            <input type="radio" name="decision" value="deny" style="display:none;" onchange="toggleApprove(false)">
            <div id="denyBtn" style="border:2px solid #e2e8f0;border-radius:10px;padding:1rem;text-align:center;transition:all 0.2s;">
              <div style="font-size:1.5rem;">❌</div>
              <div style="font-weight:600;color:#ef4444;">DENY</div>
              <div style="font-size:0.8rem;color:#64748b;">Not interested</div>
            </div>
          </label>
        </div>
      </div>
      <div id="approveFields" style="display:none;">
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:8px;padding:1rem;margin-bottom:1rem;font-size:0.82rem;color:#166534;">
          💡 Your proposed cost and time will be compared against the project budget and planned duration to determine your AI ranking.
        </div>
        <div class="form-grid">
          <div class="form-group"><label class="form-label">Proposed Cost (Rs.) *</label><input type="text" name="proposed_cost" class="form-control"></div>
          <div class="form-group"><label class="form-label">Completion Time (months) *</label><input type="number" name="completion_time" class="form-control"></div>
        </div>
      </div>
      <div style="margin-top:1.5rem;display:flex;gap:1rem;">
        <button type="submit" class="btn btn-primary">Submit Response</button>
        <a href="/vendor" class="btn btn-outline">Cancel</a>
      </div>
    </form>
  </div>
</div>
<script>
function toggleApprove(show) {
  document.getElementById("approveFields").style.display = show ? "block" : "none";
  document.getElementById("approveBtn").style.borderColor = show ? "#10b981" : "#e2e8f0";
  document.getElementById("approveBtn").style.background = show ? "#f0fdf4" : "white";
  document.getElementById("denyBtn").style.borderColor = !show ? "#ef4444" : "#e2e8f0";
  document.getElementById("denyBtn").style.background = !show ? "#fef2f2" : "white";
}
</script>
{% endblock %}'''


# ──────────────────────────────────────────────────────────────────
# edit_project.html  — Modify existing project
# ──────────────────────────────────────────────────────────────────
templates["edit_project.html"] = '''{% extends "base.html" %}
{% block title %}Edit Project - TenderAI{% endblock %}
{% block content %}
<div class="container" style="max-width:800px;">
  <div class="page-title">Modify Project</div>
  <div class="page-subtitle">Edit project details — vendor responses will be preserved</div>
  <div class="card">
    <form method="POST">
      <div class="section-header">1. Project Information</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Project Name *</label>
          <input type="text" name="project_name" class="form-control" value="{{ project.project_name }}" required></div>
        <div class="form-group"><label class="form-label">Project Location *</label>
          <select name="project_location" class="form-control" required>
            {% for d in districts %}<option {% if d==project.project_location %}selected{% endif %}>{{ d }}</option>{% endfor %}
          </select></div>
        <div class="form-group"><label class="form-label">Client Name</label>
          <input type="text" name="client_name" class="form-control" value="{{ project.client_name or \'\' }}"></div>
        <div class="form-group"><label class="form-label">Client Type</label>
          <select name="client_type" class="form-control">
            <option {% if project.client_type=="Government" %}selected{% endif %}>Government</option>
            <option {% if project.client_type=="Semi-Government" %}selected{% endif %}>Semi-Government</option>
            <option {% if project.client_type=="Private" %}selected{% endif %}>Private</option>
          </select></div>
      </div>
      <div class="section-header">2. Work Details</div>
      <div class="form-grid">
        <div class="form-group"><label class="form-label">Work Type *</label>
          <select name="work_type" class="form-control" required>
            {% for w in work_types %}<option {% if w==project.work_type %}selected{% endif %}>{{ w }}</option>{% endfor %}
          </select></div>
        <div class="form-group"><label class="form-label">Original Budget (Rs.) *</label>
          <input type="text" name="original_budget" class="form-control" value="{{ project.original_budget }}" required></div>
        <div class="form-group"><label class="form-label">Planned Duration (months)</label>
          <input type="number" name="planned_duration" class="form-control" value="{{ project.planned_duration or \'\' }}"></div>
        <div class="form-group"><label class="form-label">Complexity Level</label>
          <select name="complexity_level" class="form-control">
            <option {% if project.complexity_level=="Low" %}selected{% endif %}>Low</option>
            <option {% if project.complexity_level=="Medium" %}selected{% endif %}>Medium</option>
            <option {% if project.complexity_level=="High" %}selected{% endif %}>High</option>
          </select></div>
      </div>
      <div class="section-header">Submission Deadline</div>
      <div class="form-grid" style="max-width:600px;">
        <div class="form-group">
          <label class="form-label">Deadline Date *</label>
          <input type="date" name="deadline_date" id="deadline_date" class="form-control" required
                 value="{{ project.submission_deadline[:10] if project.submission_deadline else \'\' }}">
        </div>
        <div class="form-group">
          <label class="form-label">Deadline Time *</label>
          <input type="time" name="deadline_time" id="deadline_time" class="form-control" required
                 value="{{ project.submission_deadline[11:16] if project.submission_deadline and \'T\' in project.submission_deadline else \'23:59\' }}">
        </div>
      </div>
      <input type="hidden" name="submission_deadline_dt" id="submission_deadline_dt">
      <div style="margin-top:2rem;display:flex;gap:1rem;">
        <button type="submit" class="btn btn-primary" onclick="combineDatetime()">Save Changes</button>
        <a href="/admin/project_status" class="btn btn-outline">Cancel</a>
      </div>
    </form>
  </div>
</div>
<script>
function combineDatetime() {
  var d = document.getElementById("deadline_date").value;
  var t = document.getElementById("deadline_time").value;
  if (d && t) { document.getElementById("submission_deadline_dt").value = d + "T" + t; }
}
document.querySelector("form").addEventListener("submit", function() { combineDatetime(); });
</script>
{% endblock %}'''

# ──────────────────────────────────────────────────────────────────
# Write all templates to disk
# ──────────────────────────────────────────────────────────────────
for filename, content in templates.items():
    filepath = os.path.join(TEMPLATES_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {filename}")

print("\n✅ All templates created successfully!")
print(f"Location: {TEMPLATES_DIR}")
