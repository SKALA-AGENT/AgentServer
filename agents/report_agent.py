import re
from langchain_openai import ChatOpenAI
from prompt_templates import REPORT_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

def parse_investment_text(text):
    result = {}
    # 항목별 점수/가중치
    item_pattern = r"\*\s*(창업자|시장성|제품/기술력|경쟁 환경|마케팅/영업/파트너|추가 자금 조달 필요성|기타 요인)\s*:\s*(\d+)\s*/\s*(\d+)%"
    for kor, score, weight in re.findall(item_pattern, text):
        eng_map = {
            "창업자": "founder",
            "시장성": "market",
            "제품/기술력": "product",
            "경쟁 환경": "competition",
            "마케팅/영업/파트너": "marketing",
            "추가 자금 조달 필요성": "funding",
            "기타 요인": "others"
        }
        k = eng_map[kor]
        result[f"{k}_score"] = score
        result[f"{k}_weight"] = weight

    # 총점
    total_match = re.search(r"\*\s*\*\*총점\s*[:：]*\s*(\d+)\s*/\s*(\d+)", text)
    result["total_score"] = (total_match.group(1) if total_match else "")
    result["total_weight"] = (total_match.group(2) if total_match else "")

    # 판단 이유
    reason_start = text.find("* **판단 이유")
    reason_lines = text[reason_start:].split('\n')[1:] if reason_start != -1 else []
    eng_map = {
        "창업자": "founder_comment",
        "시장성": "market_comment",
        "제품/기술력": "product_comment",
        "경쟁 환경": "competition_comment",
        "마케팅/영업/파트너": "marketing_comment",
        "추가 자금 조달 필요성": "funding_comment",
        "기타 요인": "others_comment"
    }
    for line in reason_lines:
        m = re.match(r"\*\s*(.+?)\s*:\s*(.+)", line.strip())
        if m and m.group(1) in eng_map:
            result[eng_map[m.group(1)]] = m.group(2).strip()

    # 누락 키는 빈 값으로!
    flds = [
        "founder_score", "founder_weight",
        "market_score", "market_weight",
        "product_score", "product_weight",
        "competition_score", "competition_weight",
        "marketing_score", "marketing_weight",
        "funding_score", "funding_weight",
        "others_score", "others_weight",
        "total_score", "total_weight",
        "founder_comment", "market_comment", "product_comment",
        "competition_comment", "marketing_comment",
        "funding_comment", "others_comment"
    ]
    for k in flds:
        if k not in result: result[k] = ""
    return result

def write_pdf_report(report_text, file_path: str):
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('Nanum', '', 'NanumSquareRoundB.ttf', uni=True)
    pdf.set_font('Nanum', size=12)
    for line in report_text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(file_path)

def generate_report_from_state(agent_state, out_dir="./reports"):
    # 회사명은 company 에이전트에서
    company_name = agent_state["company"][-1].content if agent_state.get("company") else "알수없음"
    # investment 평가 결과는 이전처럼 파싱
    investment_text = agent_state["investment"][-1].content if agent_state.get("investment") else ""
    parsed = parse_investment_text(investment_text)
    prompt_inputs = {"company_name": company_name, **parsed}
    # 파일명 안전화
    safe_company_name = "".join([c for c in company_name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(' ', '_')
    if not safe_company_name:
        safe_company_name = "알수없음"
    os.makedirs(out_dir, exist_ok=True)
    out_path = f"{out_dir}/{safe_company_name}_투자보고서.pdf"

    llm = ChatOpenAI()
    report_chain = REPORT_PROMPT | llm
    report_text = report_chain.invoke(prompt_inputs)
    if hasattr(report_text, "content"):
        report_text = report_text.content
    write_pdf_report(report_text, out_path)
    return out_path

if __name__ == "__main__":
    from agent_state import test_agent_state
    out_path = generate_report_from_state(test_agent_state)
    print(f"테스트 보고서가 {out_path}에 생성되었습니다.")
