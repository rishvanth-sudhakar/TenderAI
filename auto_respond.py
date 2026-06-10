"""
TenderAI — Bulk Vendor Auto-Responder
======================================
Makes all 50 vendors respond to a project instantly.
~60% approve with realistic cost & time, ~40% deny.

Usage:
  python3 auto_respond.py                  ← shows all open projects, pick one
  python3 auto_respond.py <project_id>     ← directly respond to that project
"""

from pymongo import MongoClient
from datetime import datetime
import random
import sys

client = MongoClient('mongodb://localhost:27017/')
db     = client['tenderai_db']

users_col    = db['users']
projects_col = db['projects']

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def fmt_inr(amount):
    return f"{amount:,.0f}"

def get_open_projects():
    return list(projects_col.find({"status": "open"}))

def pick_project():
    """Show open projects and let user pick one interactively."""
    projects = get_open_projects()
    if not projects:
        print("\n❌  No open projects found. Create a project first.\n")
        sys.exit(0)

    print("\n📋  Open Projects:")
    print("=" * 65)
    for i, p in enumerate(projects, 1):
        deadline = p.get("submission_deadline", "N/A")
        responses = len(p.get("vendor_responses", {}))
        print(f"  [{i}] {p['project_name']:<35} | Budget: Rs.{p.get('original_budget','?')}")
        print(f"       ID: {p['_id']}  |  Deadline: {deadline}  |  Responses so far: {responses}")
        print()

    while True:
        try:
            choice = input("  Enter project number to auto-respond (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                sys.exit(0)
            idx = int(choice) - 1
            if 0 <= idx < len(projects):
                return projects[idx]
            print(f"  ⚠️  Enter a number between 1 and {len(projects)}")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")

def get_project_by_id(project_id):
    from bson import ObjectId
    try:
        return projects_col.find_one({"_id": ObjectId(project_id)})
    except Exception:
        print(f"\n❌  Invalid project ID: {project_id}\n")
        sys.exit(1)

# ─────────────────────────────────────────────
#  RESPONSE GENERATOR
# ─────────────────────────────────────────────

def generate_response(vendor, project):
    """
    Generate a realistic approve/deny response.
    Tier A vendors approve more often with competitive bids.
    Tier C vendors approve less often with higher cost proposals.
    """
    years_exp  = vendor.get("years_experience", 1)
    total_proj = vendor.get("total_projects_completed", 1)

    # Determine tier
    if years_exp >= 15 and total_proj >= 30:
        tier = "A"
        approve_prob  = 0.75
        cost_factor   = random.uniform(0.85, 1.05)   # competitive / under budget
        time_factor   = random.uniform(0.85, 1.05)
    elif years_exp >= 7 and total_proj >= 12:
        tier = "B"
        approve_prob  = 0.65
        cost_factor   = random.uniform(0.90, 1.15)
        time_factor   = random.uniform(0.90, 1.15)
    else:
        tier = "C"
        approve_prob  = 0.50
        cost_factor   = random.uniform(0.95, 1.30)   # tend to go over budget
        time_factor   = random.uniform(0.95, 1.25)

    decision = "approve" if random.random() < approve_prob else "deny"

    response = {
        "decision":     decision,
        "responded_at": datetime.now().isoformat(),
    }

    if decision == "approve":
        # Calculate proposed cost from project budget
        try:
            project_budget = float(str(project.get("original_budget", "5000000")).replace(",", ""))
        except Exception:
            project_budget = 5_000_000

        proposed_cost = int(project_budget * cost_factor)

        # Calculate proposed time from planned duration
        try:
            planned_dur = float(str(project.get("planned_duration", "12") or "12"))
        except Exception:
            planned_dur = 12

        proposed_time = max(1, int(planned_dur * time_factor))

        response["proposed_cost"]    = fmt_inr(proposed_cost)
        response["completion_time"]  = str(proposed_time)

    return response, tier

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def auto_respond(project):
    from bson import ObjectId

    project_id   = project["_id"]
    project_name = project.get("project_name", "Unknown")
    budget       = project.get("original_budget", "?")
    existing     = project.get("vendor_responses", {})

    print(f"\n🚀  Auto-Responding to: {project_name}")
    print(f"    Budget  : Rs.{budget}")
    print(f"    Deadline: {project.get('submission_deadline','N/A')}")
    print("=" * 65)

    vendors = list(users_col.find({"role": "vendor"}).sort("username", 1))

    if not vendors:
        print("\n❌  No vendors found in DB.\n")
        sys.exit(1)

    approved_list = []
    denied_list   = []
    skipped_list  = []

    for vendor in vendors:
        uid = vendor["username"]

        # Skip if already responded
        if uid in existing:
            skipped_list.append(uid)
            continue

        response, tier = generate_response(vendor, project)

        # Write to DB
        projects_col.update_one(
            {"_id": project_id},
            {"$set": {f"vendor_responses.{uid}": response}}
        )

        if response["decision"] == "approve":
            approved_list.append({
                "uid":   uid,
                "name":  vendor.get("company_name", uid),
                "tier":  tier,
                "cost":  response.get("proposed_cost", "-"),
                "time":  response.get("completion_time", "-"),
            })
        else:
            denied_list.append({
                "uid":  uid,
                "name": vendor.get("company_name", uid),
                "tier": tier,
            })

    # ── Print summary ──────────────────────────────────────────
    print(f"\n  ✅ APPROVED  ({len(approved_list)} vendors)\n")
    for v in approved_list:
        print(f"     [{v['uid']}] Tier {v['tier']}  {v['name']:<40}  Rs.{v['cost']}  {v['time']} mo")

    print(f"\n  ❌ DENIED  ({len(denied_list)} vendors)\n")
    for v in denied_list:
        print(f"     [{v['uid']}] Tier {v['tier']}  {v['name']}")

    if skipped_list:
        print(f"\n  ⏭️  Already responded (skipped): {', '.join(skipped_list)}")

    total_responded = len(approved_list) + len(denied_list)
    print(f"\n{'=' * 65}")
    print(f"  ✅ Done! {total_responded} vendors responded in seconds.")
    print(f"     Approved : {len(approved_list)}")
    print(f"     Denied   : {len(denied_list)}")
    if skipped_list:
        print(f"     Skipped  : {len(skipped_list)}  (already had responses)")
    print(f"\n  👉 Go to Admin → Project Status → Analyse  to see AI rankings.\n")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("\n╔══════════════════════════════════════════════════════╗")
    print("║       TenderAI — Bulk Vendor Auto-Responder          ║")
    print("╚══════════════════════════════════════════════════════╝")

    if len(sys.argv) >= 2:
        # Project ID passed directly
        project_id = sys.argv[1].strip()
        project = get_project_by_id(project_id)
        if not project:
            print(f"\n❌  Project not found for ID: {project_id}\n")
            sys.exit(1)
    else:
        # Interactive mode — show list and pick
        project = pick_project()

    auto_respond(project)
