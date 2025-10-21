# app.py
from flask import Flask, request, jsonify, render_template_string
from calculator import OPERATIONS
import math
import time
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
          <div style="margin-top:1rem;">
            <button id="load-btn" type="button">Run load test (1000 ops)</button>
            <div class="result" id="load-result" style="margin-top:0.5rem;">Load test results will appear here…</div>
          </div>

        

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
            // Load test button
            const loadBtn = document.getElementById('load-btn');
            const loadOut = document.getElementById('load-result');
            loadBtn.addEventListener('click', async () => {
              const ops = 1000; // default number of operations; adjust as needed
              loadBtn.disabled = true;
              loadOut.textContent = `Running ${ops} ops...`; 
              try {
                const res = await fetch(`/load?ops=${ops}`);
                const data = await res.json();
                if (res.ok) {
                  loadOut.textContent = `Completed ${data.ops} ops in ${data.duration.toFixed(3)}s (acc=${data.acc.toFixed(3)})`;
                } else {
                  loadOut.textContent = `Error: ${data.error || 'unknown'}`;
                }
              } catch (err) {
                loadOut.textContent = `Request failed: ${err.message}`;
              } finally {
                loadBtn.disabled = false;
              }
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

    @app.get('/load')
    def load():
        # Simple CPU-bound workload for load testing
        ops = request.args.get('ops', default=1000, type=int)
        if ops < 1 or ops > 10_000_000:
            return jsonify(error='ops out of range (1..10000000)'), 400
        start = time.time()
        acc = 0.0
        # perform floating point math to consume CPU
        for i in range(1, ops + 1):
            acc += math.sqrt(i) * math.sin(i) * math.cos(i)
        duration = time.time() - start
        return jsonify(ops=ops, duration=duration, acc=acc)

    return app

app = create_app()

if __name__ == "__main__":
    # Run with a fixed port (5000) and bind all interfaces so the container is reachable
    app.run(host="0.0.0.0", port=5000, debug=True)
