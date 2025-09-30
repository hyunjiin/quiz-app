from docx import Document
import re
import json
import boto3
import time
import PATH from config
import get_explanation from utils

def parse_docx(path, n=None, add_explanation=False):
    doc = Document(path)
    questions = []
    current_q = None
    current_option = None
    current_option_shading = False
    in_question_body = False

    paragraphs = doc.paragraphs
    
    # 일부만 처리하는 경우 
    if n:
        paragraphs = paragraphs[:n]

    for para in paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # 새 문제 시작 : Question n 은아래 로직만 수행. 
        if text.startswith("Question"):
            # 이전 문제 저장
            if current_q:
                if current_option:
                    current_q["options"].append(current_option.strip())
                    if current_option_shading:
                        current_q["answer"] = current_option.strip()
                questions.append(current_q)

            # 새로운 문제 초기화
            current_q = {
                "id": len(questions) + 1,
                "question": text + "\n",  # Question 번호 포함
                "options": [],
                "answer": None,
                "explanation": None
            }

            current_option = None
            current_option_shading = False
            in_question_body = True
            continue

        # 옵션 시작 (A. B. C. D.)
        if re.match(r"^[A-D]\.", text):
            in_question_body = False
            if current_option:
                # 이전 옵션 저장
                current_q["options"].append(current_option.strip())
                if current_option_shading:
                    current_q["answer"] = current_option.strip()
            current_option = text.strip()
            current_option_shading = False

            # 현재 문단 내 shading 확인
            for run in para.runs:
                shd = run._element.xpath('.//w:shd')
                if shd:
                    current_option_shading = True
            continue

        # 옵션이 아닌 문단은 question 본문 또는 옵션 이어붙이기
        if in_question_body and current_q:
            current_q["question"] += text + "\n"

        # 옵션이 줄바꿈으로 존재하는 경우 처리 
        elif current_option:
            current_option += " " + text
            # 정답 확인
            for run in para.runs:
                shd = run._element.xpath('.//w:shd')
                if shd:
                    current_option_shading = True

    # 마지막 문제와 옵션 저장
    if current_q:
        if current_option:
            current_q["options"].append(current_option.strip())
            if current_option_shading:
                current_q["answer"] = current_option.strip()
        questions.append(current_q)

    if add_explanation:
        for q in questions:
            if q["answer"]:
                q["explanation"] = get_explanation(q["question"], q["answer"])
                #베드락 호출 제한을 위해 
                time.sleep(15)

    with open("questions.json", "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)


    return questions


if __name__ == "__main__":
    bedrock_client = boto3.client('bedrock-runtime', region_name='ap-northeast-2')  
    parse_docx(path,300,add_explanation=True)
