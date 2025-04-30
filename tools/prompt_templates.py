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