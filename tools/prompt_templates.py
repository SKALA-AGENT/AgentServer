#prompt_templates.py
from langchain.prompts import PromptTemplate


# 재무 분석 프롬프트
FINANCE_PROMPT = PromptTemplate.from_template("""
다음 재무 정보를 분석하여 투자 판단에 도움이 되는 인사이트를 제공해주세요:

{context}

질문: {question}
""")


# 기술 분석 프롬프트
TECH_PROMPT = PromptTemplate.from_template("""
당신은 기업의 기술력을 분석하는 전문가입니다.
다음 정보를 바탕으로 기업의 기술적 경쟁력을 분석해주세요:

검색 결과: {search_result}

분석 포인트:
1. 핵심 기술 스택
2. 기술 혁신성
3. R&D 역량
4. 기술적 경쟁 우위

질문: {question}
""")

# 시장 분석 프롬프트
MARKET_PROMPT = PromptTemplate.from_template("""
당신은 스타트업 투자 평가를 위한 시장 분석 전문가입니다.
다음 검색 결과를 바탕으로 해당 기업이나 산업의 시장성과 경쟁력을 상세히 분석해주세요.

검색 질문: {question}

검색 결과: {search_result}

다음 항목을 포함하여 분석해주세요:
1. 전체 시장 규모(TAM) 및 성장률
2. 주요 경쟁사 및 경쟁 구도
3. 해당 기업/산업의 경쟁 우위 요소
4. 시장 진입 장벽
5. 주요 시장 동향 및 기회 요인
6. 위협 요소 및 도전 과제

가능한 구체적인 수치와 데이터를 포함해주세요. 불확실한 정보는 '정보 부족'으로 표시하세요.
결과는 간결하고 명확한 문단 형식으로 제공해주세요.
""")