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
당신은 시장과 산업 분석 전문가입니다.
다음 정보를 바탕으로 시장 분석을 수행해주세요:

검색 결과: {search_result}

분석 포인트:
1. 시장 규모와 성장성
2. 산업 동향
3. 경쟁 구도
4. 시장 진입 장벽

질문: {question}
""")

# 투자 보고서 작성 프롬프트
REPORT_PROMPT = PromptTemplate.from_template("""
기업명: {company_name}
재무정보: {finance}
기술요약: {tech}
시장성: {market}
대표자: {ceo}
투자 판단: {judgement}

위 정보를 기반으로 정돈된 투자 보고서를 작성해 주세요.
""") 