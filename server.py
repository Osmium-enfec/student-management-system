from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
import store
from views.pages import index_page, add_page, student_page

students = store.load_students()




class StudentHandler(BaseHTTPRequestHandler):
    def _send_html(self, html: str, status: int = 200):
        html_bytes = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html_bytes)))
        self.end_headers()
        self.wfile.write(html_bytes)

    def _redirect(self, location: str, flash_msg: str = ""):
        self.send_response(303)
        self.send_header("Location", location)
        if flash_msg:
            self.send_header("Set-Cookie", f"flash={flash_msg}; Path=/")
        self.end_headers()

    def _read_form(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        return {k: v[0] for k, v in parse_qs(body).items()}

    def _get_flash(self) -> str:
        cookie = self.headers.get("Cookie", "")
        msg = ""
        for part in cookie.split(";"):
            part = part.strip()
            if part.startswith("flash="):
                msg = part[len("flash=")]
        return msg
    def _clear_flash(self):
        self.send_header("Set-Cookie", "flash=; Max-Age=0; Path=/")





    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        flash_msg = self._get_flash()

        if path == "/":
            html = index_page(students)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            if flash_msg:
                self._clear_flash()
            html_bytes = html.replace("{{flash}}", f'<div class="msg">{flash_msg}</div>' if flash_msg else "").encode("utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)
            return

        if path == "/add":
            html = add_page()
            self._send_html(html.replace("{{flash}}", f'<div class="msg">{flash_msg}</div>' if flash_msg else ""))
            return

        if path.startswith("/student/"):
            parts = path.split("/")
            if len(parts) >= 3:
                roll_no = parts[2]
                s = students.get(roll_no)
                if not s:
                    self._send_html("<h3>Student not found</h3>", status = 404)
                    return
                html = student_page(roll_no, s)
                self._send_html(html.replace("{{flash}}", f'<div class="msg">{flash_msg}</div>' if flash_msg else ""))
                return
        self._send_html("<h3>Not Found</h3>", status=404)

    def do_POST(self):
        global students
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        form = self._read_form()

        if path == "/add":
            roll_no = form.get("roll_no", "").strip()
            name = form.get("name", "").strip()
            if not roll_no or not name:
                self._redirect("/add", "Roll No and Name are Required")
                return
            if roll_no in students:
                self._redirect("/add", "Student already exists")
                return
            students[roll_no] = {"name": name, "grade": None, "attendance": 0, "fees_paid": False}
            store.save_students(students)
            self._redirect("/", f"Student {name} added.")
            return

        if path.startswith("/student/"):
            parts = path.split("/")
            if len(parts) < 4:
                self._send_html("<h3>Invalid action.<h3>", status=400)
                return
            roll_no, action = parts[2], parts[3]
            if roll_no not in students:
                self._redirect("/", "Student not found")
                return
            if action == "grade":
                grade = form.get("grade", "").strip()
                students[roll_no]["grade"] = grade
                store.save_students(students)
                self._redirect(f"/student/{roll_no}", "Grade Updated")
                return
            if action == "attendance":
                present = form.get("present", "y") == "y"
                if present:
                    students[roll_no]["attendance"] = int(
                        students[roll_no].get("attendance", 0)) + 1
                store.save_students(students)
                self._redirect(f"/student/{roll_no}", "Attendance updated.")
                return
            if action == "fees":
                paid = form.get("paid", "y") == "y"
                students[roll_no]["fees_paid"] = bool(paid)
                store.save_students(students)
                self._redirect(f"/student/{roll_no}", "Fee status updated.")
                return
            if action == "delete":
                name = students[roll_no].get("name", "")
                del students[roll_no]
                store.save_students(students)
                self._redirect("/", f"Deleted {name or roll_no}.")
                return
            self._send_html("<h3>Unknown action.</h3>", status = 404)
            return
        self._send_html("<h3>Not Found</h3>", status = 404)

    def log_message(self, format, *args):
        pass

def run(host="localhost", port=8080):
    server = ThreadingHTTPServer((host, port), StudentHandler)
    print(f"Server running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting Down...")
    finally:
        server.server_close()

if __name__ == "__main__":
    run()


