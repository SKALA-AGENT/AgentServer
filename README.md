# AI Startup Investment Evaluation Agent
AI 스타트업에 대한 기술력, 시장성, 리스크 등 다양한 요소를 기반으로 **투자 가능성을 자동 평가**하는 Agentic RAG 기반 프로젝트입니다.

## Overview

- Objective : AI 스타트업의 CEO 정보, 기술력, 시장성, 성장 가능성 등을 종합적으로 분석하여 투자 적합성 평가
- Method : AI Agent + Agentic RAG 
- Tools : 도구A, 도구B, 도구C

## Features
- 다양한 출처의 PDF 기반 정보 추출: IR 자료, 백서, 뉴스 기사 등 다양한 형식의 PDF 문서를 분석하여 기업의 핵심 정보를 추출합니다.
- 투자 기준별 세부 평가: 시장성, 팀 역량, 기술력, 경쟁 우위, 재무 안정성 등 다양한 투자 평가 기준에 따라 기업을 세분화하여 분석합니다.
- 종합 투자 판단 및 요약 보고서 생성: 수집된 정보를 종합하여 투자 적합성에 대한 판단을 내리고, 그 결과를 ‘투자 유망’, ‘보류’, ‘회피’ 등의 형태로 요약한 보고서를 제공합니다.

## Tech Stack 

| Category     | Tools & Frameworks                        |
|--------------|-------------------------------------------|
| Framework    | `LangGraph`, `LangChain`, `Python`        |
| LLM          | `GPT-4o-mini` via `OpenAI API`            |
| Retrieval    | `FAISS`, `Chroma`, `BM25`, `Hybrid`       |
| Data Tools   | `Tavily`, `WikipediaAPIWrapper`, `Pandas` |

## Agents
 
| Agent           | 역할 설명                                               |
|------------------|----------------------------------------------------------|
| `tech_agent`     | 기업의 AI 기술력, 차별성, R&D 수준 평가                     |
| `market_agent`   | 시장 규모, 경쟁력, BM, 고객 문제 분석                         |
| `ceo_agent`      | 대표자 학력, 경력, 창업 이력, 논문/특허 기반 평가               |
| `finance_agent`  | 수익 구조, 투자 단계, IR 지표 분석                            |
| `investment_agent` | 위 4가지 결과 종합 판단 (LLM 기반 판단)                  |
| `report_agent`   | 종합 리포트 출력 (markdown or PDF 등)                       |

## Architecture
![스크린샷 2025-04-30 오후 3 56 29](https://github.com/user-attachments/assets/417e48a2-7925-4f4c-957f-28949704f317)


## Directory Structure
![스크린샷 2025-04-30 오후 3 56 13](https://github.com/user-attachments/assets/f446d3dc-9a5d-4325-b79a-712b1c2c88ca)



## Contributors 

![스크린샷 2025-04-30 오후 3 51 49](https://github.com/user-attachments/assets/64475c46-50e2-4251-92e2-389164aaaab6)
