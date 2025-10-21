# app.py
from flask import Flask, request, jsonify, render_template_string
from calculator import OPERATIONS
def create_app():
    app = Flask(__name__)

    INDEX_HTML = """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <title>Flask Calculator</title>
        <style>
          body { font: 16px/1.4 system-ui, sans-serif; margin: 2rem; }
          form, .result { max-width: 560px; }
          input, select, button { padding: 0.5rem; font-size: 1rem; }
          .row { display: flex; gap: 0.5rem; align-items: center; margin: 0.5rem 0; }
          .result { margin-top: 1rem; padding: 0.75rem; background: #f7f7f9; border-radius: 8px; }
          code { background: #eee; padding: 0.1rem 0.3rem; border-radius: 4px; }
        </style>
      </head>
      <body>
        <h1>Flask Calculator</h1>
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
        <div class="result" id="result">Result will appear here…</div>

        

        <script>
          const form = document.getElementById('calc-form');
          const out  = document.getElementById('result');
          form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const fd = new FormData(form);
            const params = new URLSearchParams(fd);
            const res = await fetch('/calc?' + params.toString());
            const data = await res.json();
            out.textContent = res.ok ? `= ${data.result}` : `Error: ${data.error}`;
          });
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
        return render_template_string(INDEX_HTML)

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
            b = parse_number(b, "b")
            result = OPERATIONS[op](a, b)
        except ZeroDivisionError as e:
            return jsonify(error=str(e)), 400
        except ValueError as e:
            return jsonify(error=str(e)), 400
        return jsonify(op=op, a=a, b=b, result=result)

    return app

app = create_app()

if __name__ == "__main__":
    # Run with a fixed port (5000) and bind all interfaces so the container is reachable
    app.run(host="0.0.0.0", port=5000, debug=True)
