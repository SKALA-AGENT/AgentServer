import json
from typing import Dict, Any, List
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from tools.tech_agent_tools.patent_search import patent_search_tool
from tools.tech_agent_tools.tech_news_analyzer import tech_news_tool


# 기술 정보 출력 형식 정의
class TechAnalysis(BaseModel):
    tech_stack: Dict[str, Any]
    innovation: Dict[str, Any]
    rd_capability: Dict[str, Any]
    tech_advantage: Dict[str, Any]
    patents: Dict[str, Any] = Field(description="특허 분석 결과")
    tech_news: Dict[str, Any] = Field(description="최근 기술 뉴스 및 트렌드 분석")


# 마크다운 템플릿
MARKDOWN_TEMPLATE = """
# {company_name} 기술 분석 보고서

## 1. 주요 기술 스택
{tech_stack}

## 2. 기술 혁신성
{innovation}

## 3. R&D 역량
{rd_capability}

## 4. 기술적 경쟁 우위
{tech_advantage}

## 5. 특허 분석
### 주요 특허 기술 분야
{top_tech_fields}

### 특허 동향
{year_trend}

## 6. 최근 기술 동향
### 최신 기술 뉴스
{recent_news}

### 주요 기술 트렌드
{trends}

### 기술 혁신 사례
{innovation}
"""

# 기술 분석 프롬프트
TECH_ANALYSIS_PROMPT = PromptTemplate(
    template="""당신은 스타트업의 기술력을 분석하는 전문가입니다.
다음 정보들을 바탕으로 종합적인 기술 분석을 수행해주세요:

회사명: {company_name}

2. 기술 뉴스 및 트렌드:
- 최근 뉴스: {recent_news}
- 기술 트렌드: {trends}
- 기술 혁신: {innovation}

다음 항목들에 대해 구체적이고 체계적으로 분석해주세요.
각 항목은 3가지 이상의 핵심 포인트 또는 사례를 포함하고, 가능하다면 bullet-point 형식으로 작성해주세요. 모호한 문장보다는 구체적인 기술명, 서비스명, 수치 등을 포함하세요.

1. 기술 내용 (tech):
- 주요 기술 스택 3가지 이상
- 기술별 사용 목적 또는 적용 서비스
- 최근 도입된 기술이 있다면 시기와 적용 사례 포함

2. 기술 혁신성 (innovation):
- 특허/지재권 보유 또는 출원 이력
- 시장/산업 내에서의 기술 트렌드와의 일치도
- 차별화된 기술 또는 독자 기술 요소

3. R&D 역량 (rd_capability):
- R&D 투자 방향 및 규모
- 특허 출원이나 등록 수 등 수치 기반 정보
- 조직/팀 구조 또는 연구 분야

4. 기술적 경쟁 우위 (tech_advantage):
- 경쟁사 대비 강점
- 고객 가치로 이어지는 기술적 요소
- 향후 기술력 기반 성장 전망

5. 특허 분석 (patents):
- 주요 특허 기술 분야 요약
- 연도별 출원 동향 분석
- 핵심 특허의 구체적 내용 또는 활용 예시

6. 기술 뉴스 (tech_news):
- 최근 기술 도입 사례 또는 보도
- 산업 내 반응 또는 평가
- 향후 기술 계획

결과는 마크다운 형식의 줄글 보고서로 작성해주세요. 각 항목은 명확한 문장과 예시를 포함한 문단 형식으로 작성되며, 필요 시 bullet point도 활용하세요.
""",
    input_variables=[
        "company_name",
        "tech_stack",
        "innovation",
        "rd_capability",
        "tech_advantage",
        "top_tech_fields",
        "year_trend",
        "recent_news",
        "trends",
    ],
)


def collect_tech_info(company_name: str) -> Dict[str, Any]:
    """기술 정보 수집"""
    # 특허 검색
    patent = patent_search_tool()
    patent_info = patent.analyze_patents(company_name)

    # 기술 뉴스 분석
    news = tech_news_tool()
    tech_innovation = news.analyze_technology_innovation(company_name)

    tech_news_info = {
        "recent_news": tech_innovation["tech_innovations"],
        "trends": tech_innovation["key_technologies"],
        "innovation": tech_innovation,
    }

    return {"patents": patent_info, "tech_news": tech_news_info}


# 기술 분석 에이전트 생성
def create_tech_analysis_agent(company_name: str) -> Runnable:

    parser = StrOutputParser()

    # 추가 기술 정보 수집
    tech_info = collect_tech_info(company_name)

    chain = (
        {
            "company_name": lambda x: company_name,
            "tech_stack": lambda x: "N/A",  # Or derive from other tools if needed
            "innovation": lambda x: tech_info["tech_news"]["innovation"],
            "rd_capability": lambda x: "N/A",
            "tech_advantage": lambda x: "N/A",
            "top_tech_fields": lambda x: tech_info["patents"]["top_tech_fields"],
            "year_trend": lambda x: tech_info["patents"]["year_trend"],
            "recent_news": lambda x: tech_info["tech_news"]["recent_news"],
            "trends": lambda x: tech_info["tech_news"]["trends"],
            "patents": lambda x: tech_info["patents"],
            "tech_news": lambda x: tech_info["tech_news"],
        }
        | TECH_ANALYSIS_PROMPT
        | ChatOpenAI(temperature=0.7)
        | parser
    )
    return chain
