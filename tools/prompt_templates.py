from langchain.prompts import PromptTemplate, ChatPromptTemplate


# 재무 분석 프롬프트
FINANCE_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "당신은 숙련된 투자 분석가입니다.\n\n"
        "사용자가 입력한 '회사명'을 기반으로, 해당 기업의 재무 정보를 `financial_search` 도구를 이용해 검색한 후, "
        "투자 관점에서 다음 항목에 따라 정밀 분석을 수행해주세요:\n\n"
        "1. 최근 3개년 주요 재무제표 요약 (매출, 영업이익, 순이익, 자산/부채/자본 등)\n"
        "2. 핵심 재무 비율 분석 (수익성, 성장성, 안정성, 활동성)\n"
        "3. 전년도 대비 주요 수치 변화 및 원인 해석\n"
        "4. 재무 구조의 강점 및 위험 요인 도출\n"
        "5. 투자자 관점에서 주의해야 할 점 및 종합 의견\n\n"
        "당신은 retriever 도구로 얻은 문서를 기반으로만 판단해야 하며, 검색 결과에 기반하지 않은 추론은 삼가야 합니다.\n"
        "사용자 입력은 단 하나의 회사명만 주어지므로, 정보 탐색 → 분석 → 요약 전 과정을 스스로 수행해야 합니다.\n\n"
        "최종 출력은 투자자가 이해할 수 있도록 간결하고 논리적으로 작성해주세요."
    ),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

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
REPORT_PROMPT = PromptTemplate.from_template(
    input_variables=[
        "company_name",
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
    ],
    template="""
[투자 평가 리포트]

기업명: {company_name}

* 항목별 점수 : (획득 점수)/(항목별 비중)
    * 창업자 : {founder_score} / {founder_weight}%
    * 시장성 : {market_score} / {market_weight}%
    * 제품/기술력 : {product_score} / {product_weight}%
    * 경쟁 환경 : {competition_score} / {competition_weight}%
    * 마케팅/영업/파트너 : {marketing_score} / {marketing_weight}%
    * 추가 자금 조달 필요성 : {funding_score} / {funding_weight}%
    * 기타 요인 : {others_score} / {others_weight}%

* 총점 : {total_score} 

* 판단 이유 :
    * 창업자 : {founder_comment}
    * 시장성 : {market_comment}
    * 제품/기술력 : {product_comment}
    * 경쟁 환경 : {competition_comment}
    * 마케팅/영업/파트너 : {marketing_comment}
    * 추가 자금 조달 필요성 : {funding_comment}
    * 기타 요인 : {others_comment}

위 항목을 반드시 고수할 것, 한글로 결과를 출력할 것.
"""
)


# 투자 판단 프롬프트
INVESTMENT_PROMPT = PromptTemplate.from_template("""
Act as a venture capital analyst evaluating a pre-revenue startup based on the criteria outlined in the Scorecard Valuation Worksheet.

**Input Startup Information:**
financial_information :
{financial_information}
market_information :
{market_information}
tech_information :
{tech_information}
ceo_information :
{ceo_information}

**Task:**
Evaluate the startup described above using the following factors and weighting guidelines:

1.  **창업자 (Strength of the Management Team) (Weight: 0-30%):** Assess experience (general business, sector-specific, leadership roles), completeness of the team, and founder coachability.
2.  **시장성 (Size of the Opportunity) (Weight: 0-25%):** Evaluate target market size and 5-year revenue potential.
3.  **제품/기술력 (Strength of the Product and Intellectual Property) (Weight: 0-15%):** Analyze product development stage, customer traction/feedback, product necessity/compelling nature, and IP protection/differentiation.
4.  **경쟁 환경 (Competitive Environment) (Weight: 0-10%):** Assess the strength and structure of the competition.
5.  **마케팅/영업/파트너 (Marketing/Sales/Partners) (Weight: 0-10%):** Evaluate the status of sales channels and strategic partnerships.
6.  **추가 자금 조달 필요성 (Need for additional rounds of funding) (Weight: 0-5%):** Consider the requirement for future funding rounds.
7.  **기타 요인 (Other Factors) (Weight: 0-5%):** Include any other significant positive or negative factors.

**Output Format:**
Provide the evaluation in the following format. **Crucially, the entire output, including scores and justifications, must be written in Korean.**

* **항목별 점수 : **
    * 창업자 : [Score based on assessment] / [Max Weight %]
    * 시장성 : [Score based on assessment] / [Max Weight %]
    * 제품/기술력 : [Score based on assessment] / [Max Weight %]
    * 경쟁 환경 : [Score based on assessment] / [Max Weight %]
    * 마케팅/영업/파트너 : [Score based on assessment] / [Max Weight %]
    * 추가 자금 조달 필요성 : [Score based on assessment] / [Max Weight %]
    * 기타 요인 : [Score based on assessment] / [Max Weight %]
* **총점 : ** [Calculated Total Score based on section scores and weights]
* **판단 이유 : **
    * 창업자 : [Brief explanation for the score in Korean]
    * 시장성 : [Brief explanation for the score in Korean]
    * 제품/기술력 : [Brief explanation for the score in Korean]
    * 경쟁 환경 : [Brief explanation for the score in Korean]
    * 마케팅/영업/파트너 : [Brief explanation for the score in Korean]
    * 추가 자금 조달 필요성 : [Brief explanation for the score in Korean]
    * 기타 요인 : [Brief explanation for the score in Korean]

Ensure the justifications are concise and directly related to the criteria and the provided startup information.
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

가능한 구체적인 수치와 데이터를 포함해주세요. 불확실한 정보는 '정보 부족'으로 표시하세요.
결과는 간결하고 명확한 문단 형식으로 제공해주세요.
""")

# 최종 시장 분석 프롬프트 (새로 추가)
MARKET_ANALYSIS_PROMPT = PromptTemplate.from_template("""
다음 검색 결과를 종합하여 '{startup_name}'의 시장성과 경쟁력에 대한 상세 분석을 제공해주세요:

{combined_result}

다음 항목을 반드시 포함해 주세요:
1. 시장 규모 및 성장률
2. 주요 경쟁사 목록
3. 시장 점유율(추정치 포함)
4. 주요 시장 동향
5. 진입 장벽
6. 경쟁 우위 요소
7. 전반적인 시장성 평가(높음/중간/낮음)

분석 결과는 명확한 문단 구조로 제공해 주세요.
정보가 부족한 경우, '정보 부족'이라고 명시해 주세요.
>>>>>>> Stashed changes
""")