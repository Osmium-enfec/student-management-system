import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

def read_template(name: str) -> str:
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_template(name: str, **context) -> str:
    tpl = read_template(name)
    for k, v in context.items():
        tpl = tpl.replace(f"{{{{{k}}}}}", str(v))
    return tpl

def html_escape(val) -> str:
    if val is None:
        return ""
    return(str(val)
           .replace("&", "&amp;")
           .replace("<", "&lt;")
           .replace(">", "&gt;")
           .replace('"', "&quot;")
           .replace("'", "&#39;")
           )