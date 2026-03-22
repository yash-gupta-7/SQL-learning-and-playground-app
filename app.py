import gradio as gr
import json
import db
import pandas as pd

try:
    db.init_db()
except Exception as e:
    print(f"Error initialising DB: {e}")

with open('branding.json') as f:
    brand_data = json.load(f)
    brand = brand_data['brand']

SQL_MASTERY = """
# SQL MASTERY GUIDE

- SELECT -> Retrieve data
- INSERT -> add a record
- UPDATE -> modify data
- DELETE -> remove data
- JOIN -> Combine data
- GROUP BY -> Aggregate data
- WINDOW -> Rank / Analyze data
"""
with gr.Blocks(title=brand['organizationShortName']) as app:
    gr.Markdown(f"# {brand['organizationShortName']}\n### {brand['slogan']}")

    with gr.Tab("1. DATA ENTRY"):
        with gr.Row():
            with gr.Column():
                s_name = gr.Textbox(label="Student Name")
                s_age = gr.Number(label="Student Age", value=20)
                add_s_btn = gr.Button("Add Student")

            with gr.Column():
                c_name = gr.Textbox(label="Course Name")
                add_c_btn = gr.Button("Add Course")

            with gr.Column():
                s_sid = gr.Number(label="Student ID")
                s_cid = gr.Number(label="Course ID")
                en_marks = gr.Number(label="Marks")
                en_btn = gr.Button("Enroll")
        
        status = gr.Textbox(label="Status")

        add_s_btn.click(db.add_student, [s_name, s_age], status)
        add_c_btn.click(db.add_course, [c_name], status)
        en_btn.click(db.enroll, [s_sid, s_cid, en_marks], status)

    with gr.Tab("2. CRUD TABS"):
        with gr.Tab("Read"):
            read_btn = gr.Button("Show Joined Data")
            read_out = gr.DataFrame()
            read_btn.click(lambda : db.get_join_data()[0], None, read_out)
        
        with gr.Tab("Update"):
            up_id = gr.Number(label="Update ID")
            up_name = gr.Textbox(label="New Name")
            up_age = gr.Number(label="New Age")
            up_btn = gr.Button("Update Student")

            up_btn.click(db.update_student, [up_id, up_name, up_age], status)
        
        with gr.Tab("Delete"):
            del_id = gr.Number(label="Delete ID")
            del_btn = gr.Button("Delete Student")
            del_btn.click(db.delete_student, [del_id], status)
    
    with gr.Tab("3. SQL CONCEPT EXPLORER"):
        concept_btn = gr.Radio(
            ["INNER JOIN", "LEFT JOIN","GROUP BY", "SUBQUERY", "WINDOW FUNCTION"],
            label="SELECT Concept"
        )
        concept_query = gr.Code(language="sql", label="SQL Query")
        concept_out = gr.DataFrame()

        def explore(choice):
            queries = {
                "INNER JOIN": "SELECT s.name, c.name, e.marks FROM students s INNER JOIN enrollments e ON s.id = e.sid INNER JOIN courses c ON e.cid = c.id",
                "LEFT JOIN": "SELECT s.name, e.marks FROM students s LEFT JOIN enrollments e ON s.id = e.sid",
                "GROUP BY": "SELECT age, COUNT(*) as Count FROM students GROUP BY age",
                "SUBQUERY": "SELECT name FROM students WHERE id IN (SELECT sid FROM enrollments WHERE marks > 80)",
                "WINDOW FUNCTION": "SELECT sid, marks, RANK() OVER (ORDER BY marks DESC) as ranking FROM enrollments"
            }
            q = queries[choice]
            df, _ = db.execute_sql(q)

            return q, df
    
    concept_btn.change(explore, concept_btn, [concept_query, concept_out])

    with gr.Tab("4. SQL Playground"):
        custom_sql = gr.Textbox(
            label="Custom SQL Query",
            placeholder="SELECT * FROM students"
        )
        run_btn = gr.Button("Run SQL")
        playground_out = gr.DataFrame()
        error_box = gr.Textbox(label="Log/Error")

        def play(q):
            df, msg = db.execute_sql(q)
            return df, msg 
        
        run_btn.click(play, custom_sql, [playground_out, error_box])

    with gr.Tab("5. SQL MASTERY GUIDE"):
        gr.Markdown(SQL_MASTERY)

if __name__ == "__main__":
    app.launch()
