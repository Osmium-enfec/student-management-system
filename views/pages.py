from utils import render_template, html_escape

def layout(content: str, flash_msg: str = "") -> str:
    return render_template("layout.html", content=content, flash=html_escape(flash_msg))

def index_page(students: dict) -> str:
    if not students:
        body = "<p>No Students Yet</p>"
    else:
        rows = []
        for roll_no, s in students.items():
            rows.append(f"""
            <tr>
              <td>{html_escape(roll_no)}</td>
              <td>{html_escape(s.get('name', ''))}</td>
              <td>{html_escape(s.get('grade')) if s.get('grade') is not None else '-'}</td>
              <td>{int(s.get('attendance', 0))}</td>    
              <td>{"Yes" if s.get('fees_paid') else "No"}  </td>
              <td><a href="/student/{html_escape(roll_no)}">View</a></td>                                                               
            </tr>""")
        body = render_template("index.html", rows="".join(rows))
    return layout(body)

def add_page() -> str:
    return layout(render_template("add.html"))

def student_page(roll_no: str, s: dict) -> str:
    content = render_template("student.html",
                              roll_no=html_escape(roll_no),
                              student_name=html_escape(s.get("name", "")),
                              grade_disp=(html_escape(s.get("grade"))
                                           if s.get("grade") is not None else "-"),
                              attendance=int(s.get("attendance", 0)),
                              fees_paid_text=("Yes" if s.get('fees_paid') else "No"),
    )
    return layout(content)