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
# CEO 분석 프롬프트
CEO_AGENT_PROMPT = PromptTemplate.from_template("""
당신은 기업 대표자의 경력과 이력을 요약하는 인물 분석 AI입니다.

기업명: {company_name}
대표자: {ceo_name}

💡 한글 또는 영어로 작성된 대표자의 경력 정보가 존재한다면 모두 수집하세요.
특히 LinkedIn에서 영문 이름으로 제공되는 경우 우선적으로 반영하세요.

아래 검색 결과를 바탕으로 대표자의 정보를 분석하세요:
{search_results}

다음 항목을 중심으로 분석해주세요:
1. 학력 및 전문성
2. 주요 경력 및 성과
3. AI/기술 관련 전문성
4. 투자 관점에서의 강점

💡 주의사항:
✅ 언급된 내용은 그대로 사용
✅ 불완전한 단서는 조심스럽게 추론 가능
❌ 검색 기반이 아닌 창작, 추측, 날조는 절대 금지
❌ 정보가 없으면 '정보 없음'으로 표기

마크다운 형식으로 응답해주세요:

# {company_name} 대표자 분석

##기본 정보
- **기업명**: {company_name}
- **대표자**: {ceo_name}

학력 및 전문성
{학력_전문성}

주요 경력 및 성과
{주요_경력}

AI/기술 전문성
{기술_전문성}

투자 관점 강점
{투자_강점}

종합 평가
{종합_평가}
""")