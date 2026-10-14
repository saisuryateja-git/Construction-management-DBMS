
"""Local web interface for the Construction DBMS starter project.

Run with: python3 web.py
Then open: http://127.0.0.1:8000
Uses Python's standard library; no extra packages required.
"""

import os
import html
import sqlite3

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from app.main import ROOT, initialize, connect


HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", "8000"))
STATUSES = ["Planned", "Active", "On Hold", "Completed", "Cancelled"]


CSS = """
:root {
    --bg: #0a1018;
    --panel: #111c29;
    --panel2: #152334;
    --line: #26384a;
    --text: #f3f7fb;
    --muted: #9eafc1;
    --green: #21d3a2;
    --blue: #6aa9ff;
    --red: #ff7b86;
}
* { box-sizing: border-box; }
body {
    margin: 0;
    background: radial-gradient(ellipse at 15% 0%, #122a38 0, transparent 38%), var(--bg);
    color: var(--text);
    font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
a { color: inherit; text-decoration: none; }
.shell { max-width: 1180px; margin: auto; padding: 28px 22px 50px; }
.top {
    display: flex; justify-content: space-between; align-items: center;
    gap: 20px; margin-bottom: 30px;
}
.brand { display: flex; gap: 13px; align-items: center; }
.logo {
    width: 44px; height: 44px; border-radius: 13px;
    background: linear-gradient(135deg, var(--green), #4b9cff);
    display: grid; place-items: center; color: #07131b;
    font-weight: 900; font-size: 20px;
}
.eyebrow {
    color: var(--green); font-size: 11px; font-weight: 800;
    letter-spacing: 2px; text-transform: uppercase;
}
.brand h1 { font-size: 17px; margin: 2px 0 0; letter-spacing: .2px; }
.pill {
    border: 1px solid var(--line); border-radius: 999px;
    padding: 7px 12px; color: var(--muted); font-size: 12px;
}
.hero {
    display: flex; justify-content: space-between; align-items: end;
    gap: 22px; margin: 28px 0;
}
.hero h2 {
    font-size: clamp(27px, 4vw, 40px); line-height: 1.12;
    margin: 8px 0 10px; max-width: 700px;
}
.hero p { color: var(--muted); margin: 0; max-width: 680px; }
.grid {
    display: grid; grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px; margin: 22px 0;
}
.stat, .panel {
    background: linear-gradient(145deg, var(--panel), #0e1823);
    border: 1px solid var(--line); border-radius: 17px;
}
.stat { padding: 21px; }
.stat .label { color: var(--muted); font-size: 12px; }
.stat .num { font-size: 27px; font-weight: 750; margin-top: 6px; }
.stat .hint { font-size: 12px; color: var(--green); margin-top: 5px; }
.panel { padding: 22px; margin-top: 18px; }
.panelhead {
    display: flex; align-items: center; justify-content: space-between;
    gap: 12px; margin-bottom: 18px;
}
.panel h3 { margin: 0; font-size: 17px; }
.sub { color: var(--muted); font-size: 12px; margin-top: 4px; }
.btn {
    display: inline-flex; align-items: center; justify-content: center;
    border: 0; border-radius: 10px; padding: 10px 15px;
    background: var(--green); color: #04140f;
    font-weight: 800; cursor: pointer; font-size: 13px;
}
.btn.secondary {
    background: var(--panel2); border: 1px solid var(--line); color: var(--text);
}
.tablewrap { overflow: auto; }
table { border-collapse: collapse; width: 100%; min-width: 560px; }
th {
    text-align: left; color: var(--muted); font-size: 11px;
    text-transform: uppercase; letter-spacing: 1px; font-weight: 700;
    padding: 12px; border-bottom: 1px solid var(--line);
}
td { padding: 14px 12px; border-bottom: 1px solid #1d2b39; }
tr:last-child td { border-bottom: 0; }
.status {
    display: inline-block; border-radius: 999px; padding: 4px 9px;
    font-size: 11px; background: #123b35; color: #71efc8;
}
.status.hold { background: #3d3020; color: #ffd18a; }
.status.done { background: #1b2e46; color: #a7caff; }
.stock { color: var(--green); font-size: 12px; font-weight: 700; }
.stock.reorder { color: var(--red); }
.layout { display: grid; grid-template-columns: 1.3fr .7fr; gap: 18px; }
.formgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 13px; }
.field { display: flex; flex-direction: column; gap: 7px; }
.field.full { grid-column: 1 / -1; }
label { font-size: 12px; color: var(--muted); }
input, select {
    width: 100%; padding: 12px 13px; border-radius: 10px;
    border: 1px solid var(--line); background: #09121c;
    color: var(--text); outline: none;
}
input:focus, select:focus { border-color: var(--green); }
.notice {
    border: 1px solid #20594b; background: #102b28;
    color: #a5f4db; padding: 12px 14px;
    border-radius: 11px; margin: 15px 0;
}
.notice.error { border-color: #693a43; background: #301a21; color: #ffb7bd; }
.empty { padding: 25px; text-align: center; color: var(--muted); }
.footer { margin-top: 28px; color: #718396; font-size: 12px; text-align: center; }
.quick { display: flex; gap: 9px; flex-wrap: wrap; }
.quick a {
    padding: 9px 12px; border: 1px solid var(--line);
    border-radius: 10px; background: #101c28;
    font-size: 12px; color: #d5e0e9;
}
@media (max-width: 760px) {
    .grid, .layout { grid-template-columns: 1fr; }
    .hero { display: block; }
    .pill { display: none; }
    .shell { padding: 18px 13px 35px; }
    .formgrid { grid-template-columns: 1fr; }
    .field.full { grid-column: auto; }
}
"""


def esc(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def money(value):
    return "₹" + format(float(value or 0), ",.2f")


def badge(status):
    cls = "hold" if status == "On Hold" else "done" if status == "Completed" else ""
    return f'<span class="status {cls}">{esc(status)}</span>'


def page(title, body, message="", error=False):
    note = (
        f'<div class="notice{" error" if error else ""}">{esc(message)}</div>'
        if message else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · SitePilot</title>
<style>{CSS}</style>
</head>
<body>
<div class="shell">
<header class="top">
<a class="brand" href="/">
<div class="logo">S</div>
<div>
<div class="eyebrow">Construction operations</div>
<h1>SitePilot <span style="color:var(--muted);font-weight:400">/ DBMS</span></h1>
</div>
</a>
<span class="pill">CONSTRUCTION MANAGEMENT</span>
</header>
{note}
{body}
<div class="footer">
Construction Material &amp; Site Progress Management · SQLite database
</div>
</div>
</body>
</html>"""


def dashboard(message="", error=False):
    with connect() as conn:
        projects = conn.execute(
            "SELECT project_id, project_name, budget, status "
            "FROM projects ORDER BY project_id DESC"
        ).fetchall()

        balance = conn.execute(
            "SELECT site_name, material_name, quantity, unit, stock_status "
            "FROM v_material_balance ORDER BY site_name, material_name"
        ).fetchall()

        totals = conn.execute(
            "SELECT COUNT(*) n, COALESCE(SUM(budget), 0) budget FROM projects"
        ).fetchone()

        active = conn.execute(
            "SELECT COUNT(*) n FROM projects WHERE status = 'Active'"
        ).fetchone()["n"]

    project_rows = "".join(
        f'<tr><td><strong>{esc(r["project_name"])}</strong>'
        f'<div class="sub">Project #{r["project_id"]}</div></td>'
        f'<td>{money(r["budget"])}</td>'
        f'<td>{badge(r["status"])}</td></tr>'
        for r in projects
    )

    if not project_rows:
        project_rows = (
            '<tr><td colspan="3" class="empty">'
            "No projects yet. Add your first project using the form."
            "</td></tr>"
        )

    stock_rows = "".join(
        f'<tr><td>{esc(r["site_name"])}</td>'
        f'<td><strong>{esc(r["material_name"])}</strong></td>'
        f'<td>{esc(r["quantity"])} {esc(r["unit"])}</td>'
        f'<td><span class="stock{" reorder" if r["stock_status"] == "REORDER" else ""}">'
        f'{esc(r["stock_status"])}</span></td></tr>'
        for r in balance
    )

    if not stock_rows:
        stock_rows = (
            '<tr><td colspan="4" class="empty">'
            "No material stock records found."
            "</td></tr>"
        )

    options = "".join(f"<option>{esc(s)}</option>" for s in STATUSES)

    body = f"""
<section class="hero">
<div>
<div class="eyebrow">Project overview / 01</div>
<h2>Construction site<br>command center.</h2>
<p>Track project budgets, monitor material availability, and manage construction projects from one dashboard.</p>
</div>
<a class="btn" href="#add-project">＋ Add project</a>
</section>

<section class="grid">
<div class="stat">
<div class="label">TOTAL PROJECTS</div>
<div class="num">{totals["n"]}</div>
<div class="hint">Across your project register</div>
</div>
<div class="stat">
<div class="label">ACTIVE PROJECTS</div>
<div class="num">{active}</div>
<div class="hint">Currently marked active</div>
</div>
<div class="stat">
<div class="label">COMBINED BUDGET</div>
<div class="num" style="font-size:clamp(19px,3vw,27px)">{money(totals["budget"])}</div>
<div class="hint">Total registered project budgets</div>
</div>
</section>

<section class="panel">
<div class="panelhead">
<div><h3>Project register</h3>
<div class="sub">Projects and approved budget/status fields</div></div>
<a class="btn secondary" href="#add-project">New project</a>
</div>
<div class="tablewrap">
<table>
<thead><tr><th>Project</th><th>Budget</th><th>Status</th></tr></thead>
<tbody>{project_rows}</tbody>
</table>
</div>
</section>

<section class="panel">
<div class="panelhead">
<div><h3>Site material balance</h3>
<div class="sub">Current quantities compared with material reorder levels</div></div>
<span class="pill">{len(balance)} stock records</span>
</div>
<div class="tablewrap">
<table>
<thead><tr><th>Site</th><th>Material</th><th>Available quantity</th><th>Stock status</th></tr></thead>
<tbody>{stock_rows}</tbody>
</table>
</div>
</section>

<section class="layout">
<div class="panel" id="add-project">
<div class="panelhead">
<div><h3>Add a project</h3>
<div class="sub">Saved directly to the SQLite database</div></div>
</div>
<form method="post" action="/add">
<div class="formgrid">
<div class="field full">
<label for="name">PROJECT NAME</label>
<input id="name" name="name" placeholder="e.g. Riverfront Commercial Tower"
required maxlength="150">
</div>
<div class="field">
<label for="budget">BUDGET (₹)</label>
<input id="budget" name="budget" type="number" min="0" step="0.01"
placeholder="500000" required>
</div>
<div class="field">
<label for="status">PROJECT STATUS</label>
<select id="status" name="status">{options}</select>
</div>
<div class="field full">
<button class="btn" type="submit">Save project →</button>
</div>
</div>
</form>
</div>

<div class="panel">
<div class="panelhead">
<div><h3>Quick links</h3><div class="sub">Core demo modules</div></div>
</div>
<div class="quick">
<a href="/">Dashboard</a>
<a href="/projects">All projects</a>
<a href="/materials">Material balance</a>
</div>
<p class="sub" style="margin-top:18px">
This starter web interface implements the dashboard, project listing,
material balance, and project creation. Other database tables do not
yet have web screens.
</p>
</div>
</section>
"""
    return page("Dashboard", body, message, error)


def projects_page():
    with connect() as conn:
        rows = conn.execute(
            "SELECT project_id, project_name, start_date, end_date, budget, status "
            "FROM projects ORDER BY project_id DESC"
        ).fetchall()

    trs = "".join(
        f'<tr><td>#{r["project_id"]}</td>'
        f'<td><strong>{esc(r["project_name"])}</strong></td>'
        f'<td>{esc(r["start_date"] or "—")}</td>'
        f'<td>{esc(r["end_date"] or "—")}</td>'
        f'<td>{money(r["budget"])}</td>'
        f'<td>{badge(r["status"])}</td></tr>'
        for r in rows
    )

    if not trs:
        trs = '<tr><td colspan="6" class="empty">No projects found.</td></tr>'

    body = f"""
<section class="hero">
<div>
<div class="eyebrow">Project register / 02</div>
<h2>All projects</h2>
<p>Review every project currently stored in the database.</p>
</div>
<a class="btn" href="/#add-project">＋ Add project</a>
</section>
<section class="panel">
<div class="tablewrap">
<table>
<thead><tr><th>ID</th><th>Project name</th><th>Start date</th>
<th>End date</th><th>Budget</th><th>Status</th></tr></thead>
<tbody>{trs}</tbody>
</table>
</div>
</section>
<p><a class="btn secondary" href="/">← Back to dashboard</a></p>
"""
    return page("All Projects", body)


def materials_page():
    with connect() as conn:
        rows = conn.execute(
            "SELECT site_name, material_name, quantity, unit, reorder_level, stock_status "
            "FROM v_material_balance ORDER BY site_name, material_name"
        ).fetchall()

    trs = "".join(
        f'<tr><td>{esc(r["site_name"])}</td>'
        f'<td><strong>{esc(r["material_name"])}</strong></td>'
        f'<td>{esc(r["quantity"])} {esc(r["unit"])}</td>'
        f'<td>{esc(r["reorder_level"])} {esc(r["unit"])}</td>'
        f'<td><span class="stock{" reorder" if r["stock_status"] == "REORDER" else ""}">'
        f'{esc(r["stock_status"])}</span></td></tr>'
        for r in rows
    )

    if not trs:
        trs = '<tr><td colspan="5" class="empty">No stock records found.</td></tr>'

    body = f"""
<section class="hero">
<div>
<div class="eyebrow">Inventory / 03</div>
<h2>Material balance</h2>
<p>Check available stock and compare quantities with reorder thresholds.</p>
</div>
</section>
<section class="panel">
<div class="tablewrap">
<table>
<thead><tr><th>Site</th><th>Material</th><th>Available</th>
<th>Reorder level</th><th>Status</th></tr></thead>
<tbody>{trs}</tbody>
</table>
</div>
</section>
<p><a class="btn secondary" href="/">← Back to dashboard</a></p>
"""
    return page("Material Balance", body)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        initialize()
        path = urlparse(self.path).path

        if path == "/":
            content = dashboard()
            status = 200
        elif path == "/projects":
            content = projects_page()
            status = 200
        elif path == "/materials":
            content = materials_page()
            status = 200
        else:
            content = page(
                "Not found",
                '<section class="hero"><div><h2>Page not found</h2>'
                '<p>The requested page does not exist.</p>'
                '<a class="btn" href="/">Go to dashboard</a></div></section>',
            )
            status = 404

        self._send(content, status)

    def do_POST(self):
        initialize()

        if urlparse(self.path).path != "/add":
            return self._send(page("Not found", '<a class="btn" href="/">Back</a>'), 404)

        length = int(self.headers.get("Content-Length", "0"))
        form = parse_qs(
            self.rfile.read(length).decode("utf-8"),
            keep_blank_values=True,
        )

        name = form.get("name", [""])[0].strip()
        raw_budget = form.get("budget", [""])[0].strip()
        status = form.get("status", ["Planned"])[0].strip()

        if not name:
            return self._send(dashboard("Project name is required.", True), 400)

        try:
            budget = float(raw_budget)
            if budget < 0:
                raise ValueError
        except ValueError:
            return self._send(
                dashboard("Enter a valid budget greater than or equal to zero.", True),
                400,
            )

        if status not in STATUSES:
            return self._send(dashboard("Choose a valid project status.", True), 400)

        try:
            with connect() as conn:
                conn.execute(
                    "INSERT INTO projects(project_name, budget, status) VALUES (?, ?, ?)",
                    (name, budget, status),
                )
        except sqlite3.IntegrityError as exc:
            msg = (
                "A project with that name already exists."
                if "UNIQUE" in str(exc).upper()
                else "The project could not be saved. Check the submitted values."
            )
            return self._send(dashboard(msg, True), 400)

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def _send(self, content, status=200):
        data = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print("[web] %s - %s" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    initialize()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"\nConstruction DBMS website running on port {PORT}")
    print("Press Ctrl+C to stop the server.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nLocal web server stopped.")
    finally:
        server.server_close()
