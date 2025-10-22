# tests/test_app.py
import json
from app import app

client = app.test_client()

def test_get_add_ok():
    resp = client.get("/calc?op=add&a=2&b=3")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["result"] == 5

def test_post_div_ok():
    resp = client.post("/calc", data=json.dumps({"op":"div","a":6,"b":2}),
                       content_type="application/json")
    assert resp.status_code == 200
    assert resp.get_json()["result"] == 3

def test_div_by_zero_400():
    resp = client.get("/calc?op=div&a=1&b=0")
    assert resp.status_code == 400
    assert "division by zero" in resp.get_json()["error"]

def test_invalid_op_400():
    resp = client.get("/calc?op=invalid_operation&a=9&b=0")
    assert resp.status_code == 400
    assert "Unsupported op" in resp.get_json()["error"]

def test_non_number_400():
    resp = client.get("/calc?op=add&a=hello&b=2")
    assert resp.status_code == 400
    assert "'a' must be a number" in resp.get_json()["error"]
