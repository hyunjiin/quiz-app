from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import json
import math
from fastapi.staticfiles import StaticFiles 
from data import save_questions, load_questions
from config import QUESTION_JSON,QUESTIONS_PER_PAGE,PAGES_PER_BLOCK

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
questions = load_questions()


@app.get("/", response_class=HTMLResponse)
async def quiz(page: int = 1): 
    total_questions = len(questions)
    total_pages = math.ceil(total_questions / QUESTIONS_PER_PAGE)

    start_idx = (page - 1) * QUESTIONS_PER_PAGE
    end_idx = start_idx + QUESTIONS_PER_PAGE
    page_questions = questions[start_idx:end_idx]
 
    html = """
        <head>
            <title>Quiz</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        """

    for q in page_questions:
        html += f"<div class='question-box'>"
        html += f"<p><b>{q['question']}</b></p>"
        html += "<ul>"
        for opt in q["options"]:
            html += f"<li>{opt}</li>"
        html += "</ul>"

        # 답 보기 버튼
        html += f"<button class='answer-btn' id='answer-btn-{q['id']}' onclick='toggleAnswer({q['id']})'>답 보기</button>"
        html += f"<div class='answer' id='answer-{q['id']}'>{q['answer']}</div>"

        if "explanation" in q:
            html += f"<div class='explanation-container'>"
            html += f"<button class='btn' id='toggle-btn-{q['id']}' onclick='toggleExplanation({q['id']})'>해설 보기</button>"
            html += f"<div class='explanation' id='explanation-{q['id']}'>{q['explanation'].replace(chr(10), '<br>')}</div>"
            html += f"<div class='edit-container' id='edit-container-{q['id']}' style='display:none;'></div>"
            html += f"<button class='btn edit' onclick='editExplanation({q['id']})'>해설 수정</button>"
            html += "</div>"

        html += "</div>"

    # 페이지네이션
    current_block = (page - 1) // PAGES_PER_BLOCK
    block_start = current_block * PAGES_PER_BLOCK + 1
    block_end = min(block_start + PAGES_PER_BLOCK - 1, total_pages)

    html += "<div class='pagination'>"
    if block_start > 1:
        html += f"<a href='/?page={block_start - 1}'>◀ 이전</a>"
    for p in range(block_start, block_end + 1):
        if p == page:
            html += f"<b>{p}</b>"
        else:
            html += f"<a href='/?page={p}'>{p}</a>"
    if block_end < total_pages:
        html += f"<a href='/?page={block_end + 1}'>다음 ▶</a>"
    html += "</div>"

    # JS
    html += """
    <script src="/static/script.js"></script>
    """

    return html

# 수정 해설 업데이트 
@app.put("/update/{q_id}", response_class=JSONResponse)
async def update_explanation(q_id: int, request: Request):
    data = await request.json()
    new_explanation = data.get("explanation", "")
    for q in questions:
        if q["id"] == q_id:
            q["explanation"] = new_explanation
            break
    save_questions(questions)
    return {"status": "ok"}
