# app.py
from flask import Flask, request, jsonify, render_template_string, session, redirect, url_for
from calculator import OPERATIONS
import math

def create_app():
    app = Flask(__name__)
    app.secret_key = "change-me"

    INDEX_HTML = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Scientific Calculator</title>
        <style>
          :root { --bg: #ffffff; --fg: #111111; --panel: #f7f7f9; --btn: #e8eaed; --accent: #1a73e8; }
          .dark { --bg: #0b0c0f; --fg: #eaeef2; --panel: #1b1f27; --btn: #2d3139; --accent: #4a9eff; }

          body {
            background: var(--bg);
            color: var(--fg);
            font: 16px/1.4 system-ui, sans-serif;
            margin: 0;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: background .2s, color .2s;
          }

          .container {
            max-width: 560px;
            width: 100%;
            background: var(--panel);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
          }

          input, select, button {
            padding: 0.5rem;
            font-size: 1rem;
            border-radius: 6px;
            border: 1px solid var(--panel);
          }

          button {
            background: var(--btn);
            color: var(--fg);
            cursor: pointer;
          }
          button:hover { opacity: 0.8; }

          .row { display: flex; gap: 0.5rem; align-items: center; margin: 0.5rem 0; }
          .result { margin-top: 1rem; padding: 0.75rem; background: var(--bg); border-radius: 8px; font-weight: 500; text-align:center; }
          .toolbar { display:flex; gap:.5rem; align-items:center; justify-content:center; margin-bottom: 1.5rem; }
          .tag { font-size: .875rem; padding: .25rem .6rem; border-radius: 999px; background: var(--btn); }
          .mode-selector { margin: 1rem 0; text-align:center; }
          .constants { display: flex; gap: 0.5rem; flex-wrap: wrap; justify-content:center; margin: 0.5rem 0; }
          .constants button { padding: 0.4rem 0.8rem; font-size: 0.9rem; }
          h1, h2 { text-align:center; color: var(--accent); }
        </style>
      </head>
      <body class="{{ 'dark' if session.get('theme')=='dark' else '' }}">
        <div class="container">
          <h1>Flaksulator</h1>

          <div class="toolbar">
            <form action="{{ url_for('set_theme') }}" method="post">
              <input type="hidden" name="theme" value="{{ 'light' if session.get('theme')=='dark' else 'dark' }}">
              <button type="submit">🌓 Toggle Theme</button>
            </form>
            <span class="tag">{{ session.get('theme','light').title() }} Mode</span>
          </div>

          <h2>Basic Operations</h2>
          <form id="calc-form">
            <div class="row">
              <label>A <input name="a" type="number" step="any" required /></label>
              <select name="op">
                <option value="add">+</option>
                <option value="sub">−</option>
                <option value="mul">×</option>
                <option value="div">÷</option>
                <option value="mod">mod</option>
                <option value="pow">^</option>
              </select>
              <label>B <input name="b" type="number" step="any" required /></label>
              <button type="submit">=</button>
            </div>
          </form>

          <h2>Scientific Functions</h2>
          <form id="sci-form">
            <div class="mode-selector">
              <label>
                <input type="radio" name="angleMode" value="radians" checked> Radians
              </label>
              <label style="margin-left: 1rem;">
                <input type="radio" name="angleMode" value="degrees"> Degrees
              </label>
            </div>
            <div class="row">
              <label>Value <input name="a" type="number" step="any" required /></label>
              <select name="op">
                <optgroup label="Trigonometry (rad)">
                  <option value="sin">sin</option>
                  <option value="cos">cos</option>
                  <option value="tan">tan</option>
                  <option value="asin">asin</option>
                  <option value="acos">acos</option>
                  <option value="atan">atan</option>
                </optgroup>
                <optgroup label="Trigonometry (deg)">
                  <option value="sind">sin°</option>
                  <option value="cosd">cos°</option>
                  <option value="tand">tan°</option>
                </optgroup>
                <optgroup label="Other">
                  <option value="sqrt">√</option>
                  <option value="log">log₁₀</option>
                  <option value="ln">ln</option>
                  <option value="exp">eˣ</option>
                </optgroup>
              </select>
              <button type="submit">Calculate</button>
            </div>
          </form>

          <div class="constants">
            <button onclick="insertConstant('pi')">π (3.14159...)</button>
            <button onclick="insertConstant('e')">e (2.71828...)</button>
          </div>

          <div class="result" id="result">Result will appear here…</div>
        </div>

        <script>
          const basicForm = document.getElementById('calc-form');
          const sciForm = document.getElementById('sci-form');
          const out = document.getElementById('result');

          basicForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fd = new FormData(basicForm);
            const params = new URLSearchParams(fd);
            const res = await fetch('/calc?' + params.toString());
            const data = await res.json();
            out.textContent = res.ok ? `= ${data.result}` : `Error: ${data.error}`;
          });

          sciForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fd = new FormData(sciForm);
            const params = new URLSearchParams(fd);
            params.set('b', '0');
            const res = await fetch('/calc?' + params.toString());
            const data = await res.json();
            out.textContent = res.ok ? `= ${data.result}` : `Error: ${data.error}`;
          });

          function insertConstant(name) {
            const val = name === 'pi' ? Math.PI : Math.E;
            sciForm.querySelector('input[name="a"]').value = val;
          }
        </script>
      </body>
    </html>
    """

    def parse_number(value, name):
        try:
            return float(value)
        except (TypeError, ValueError):
            raise ValueError(f"'{name}' must be a number")

    @app.get("/")
    def index():
        session.setdefault("theme", "light")
        return render_template_string(INDEX_HTML)

    @app.post("/theme")
    def set_theme():
        theme = request.form.get("theme", "light")
        session["theme"] = "dark" if theme == "dark" else "light"
        return redirect(url_for("index"))

    @app.route("/calc", methods=["GET", "POST"])
    def calc():
        if request.method == "POST":
            data = request.get_json(silent=True) or {}
            op, a, b = data.get("op"), data.get("a"), data.get("b")
        else:
            op = request.args.get("op")
            a = request.args.get("a")
            b = request.args.get("b")

        if op not in OPERATIONS:
            return jsonify(error=f"Unsupported op '{op}'. Allowed: {sorted(OPERATIONS.keys())}"), 400
        
        try:
            a = parse_number(a, "a")
            # For scientific functions, b is optional
            if b is not None:
                b = parse_number(b, "b")
            result = OPERATIONS[op](a, b)
            
            # Check for invalid results
            if not math.isfinite(result):
                raise ValueError("Result is not a finite number")
                
        except ZeroDivisionError as e:
            return jsonify(error=str(e)), 400
        except ValueError as e:
            return jsonify(error=str(e)), 400
        except Exception as e:
            return jsonify(error=f"Calculation error: {str(e)}"), 400
            
        return jsonify(op=op, a=a, b=b, result=result)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
