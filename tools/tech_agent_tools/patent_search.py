"""AI 스타트업 특허정보 분석 기능"""

import os
import re
from typing import Dict, Any, List
from datetime import datetime
from tavily import TavilyClient


class PatentAnalyzer:
    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        # 특허 정보 관련 신뢰할 수 있는 도메인 목록
        self.patent_domains = [
            "kipris.or.kr",  # 한국특허정보원
            "patent.go.kr",  # 특허청
            "kipo.go.kr",  # 특허청
            "keywert.com",  # 키워트
            "wips.co.kr",  # 윕스
            "patent.gov.kr",  # 특허로
            "patentmap.or.kr",  # 특허맵
            "kipi.or.kr",  # 한국지식재산연구원
            "kista.re.kr",  # 한국과학기술정보연구원
            "patentstart.or.kr",  # 특허갭펀딩
            "ipnomics.co.kr",  # 아이피노믹스
            "newstap.co.kr",  # 뉴스탭
            "wipon.co.kr",  # 위폰
            "hankyung.com",  # 한국경제
            "mk.co.kr",  # 매일경제
            "edaily.co.kr",  # 이데일리
            "sedaily.com",  # 서울경제
            "koreanewswire.co.kr",  # 한국뉴스와이어
            "inews24.com",  # 아이뉴스24
            "ajunews.com",  # 아주경제
            "techm.kr",  # 테크M
            "thebigdata.co.kr",  # 더빅데이터
            "thelec.kr",  # 더일렉
            "elec4.co.kr",  # 전자신문
            "etnews.com",  # 전자신문
        ]

    def analyze_patents(self, company_name: str) -> Dict[str, Any]:
        """회사의 특허 정보 분석"""
        try:
            # API 호출 - 특허 정보
            response = self.client.search(
                query=f"{company_name} (특허 OR 실용신안 OR 특허등록 OR 지식재산권 OR 특허출원) -채용 -공고",
                search_depth="advanced",
                max_results=8,
                include_domains=self.patent_domains,
            )

            results = response.get("results", [])

            # 특허 정보 추출
            patents = []
            patent_keywords = set()

            for result in results:
                content = result.get("content", "")
                title = result.get("title", "")

                # 특허 번호 추출 시도 (10-2023-XXXXXXX 형식)
                patent_numbers = re.findall(r"10-\d{4}-\d{6,7}", content)
                patent_numbers.extend(re.findall(r"10-\d{4}-\d{6,7}", title))

                # 특허 분야 키워드 추출
                tech_fields = [
                    "인공지능",
                    "머신러닝",
                    "딥러닝",
                    "자연어처리",
                    "컴퓨터비전",
                    "빅데이터",
                    "블록체인",
                    "핀테크",
                    "로보틱스",
                    "IoT",
                    "자율주행",
                    "클라우드",
                    "AR",
                    "VR",
                    "메타버스",
                    "생체인식",
                    "보안",
                    "암호화",
                    "헬스케어",
                    "의료기기",
                    "바이오",
                    "반도체",
                    "디스플레이",
                    "통신",
                    "5G",
                    "네트워크",
                    "그린테크",
                    "신재생에너지",
                    "배터리",
                    "양자컴퓨팅",
                    "나노기술",
                ]

                found_fields = []
                for field in tech_fields:
                    if field in content or field in title:
                        found_fields.append(field)
                        patent_keywords.add(field)

                # 특허 출원/등록 연도 추출 시도
                years = re.findall(r"(20\d{2})년", content)
                years.extend(re.findall(r"(20\d{2})년", title))

                # 정보 저장
                patent_info = {
                    "title": title,
                    "url": result.get("url", ""),
                    "source": result.get("source", ""),
                    "published_date": result.get("published_date", ""),
                    "summary": content + "..." if content else "",
                    "patent_numbers": (
                        list(set(patent_numbers)) if patent_numbers else []
                    ),
                    "tech_fields": found_fields,
                    "years": list(set(years)) if years else [],
                }

                patents.append(patent_info)

            # 주요 특허 기술 분야 분석
            field_counts = {}
            for patent in patents:
                for field in patent.get("tech_fields", []):
                    field_counts[field] = field_counts.get(field, 0) + 1

            top_fields = sorted(field_counts.items(), key=lambda x: x[1], reverse=True)[
                :5
            ]

            # 연도별 특허 동향 분석
            year_counts = {}
            for patent in patents:
                for year in patent.get("years", []):
                    year_counts[year] = year_counts.get(year, 0) + 1

            year_trend = sorted(year_counts.items(), key=lambda x: x[0])

            return {
                "company_name": company_name,
                "patent_count": len(patents),
                "patents": patents,
                "top_tech_fields": top_fields,
                "year_trend": year_trend,
                "tech_keywords": list(patent_keywords),
            }

        except Exception as e:
            print(f"Error in analyze_patents: {str(e)}")
            return {
                "company_name": company_name,
                "patent_count": 0,
                "patents": [],
                "top_tech_fields": [],
                "year_trend": [],
                "tech_keywords": [],
            }

    def get_patent_details(self, patent_number: str) -> Dict[str, Any]:
        """특정 특허 번호에 대한 상세 정보 조회"""
        try:
            # API 호출 - 특허 상세 정보
            response = self.client.search(
                query=f'"{patent_number}" 특허 상세 정보',
                search_depth="advanced",
                max_results=1,
                include_domains=self.patent_domains,
            )

            results = response.get("results", [])

            if not results:
                return {
                    "patent_number": patent_number,
                    "details": "상세 정보를 찾을 수 없습니다.",
                }

            result = results[0]
            content = result.get("content", "")

            # 특허 상세 정보 추출 시도
            details = {
                "patent_number": patent_number,
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "source": result.get("source", ""),
                "summary": content[:500] + "..." if content else "내용 없음",
                "full_content": content,
            }

            # 발명자/출원인 추출 시도
            inventors = []
            applicants = []

            inventor_match = re.search(
                r"발명자[:\s]+(.*?)(?:출원인|IPC|요약|청구항|<\/)", content, re.DOTALL
            )
            if inventor_match:
                inventors = [
                    name.strip() for name in inventor_match.group(1).split(",")
                ]
                # 한 줄에 여러 이름이 있을 경우 처리
                if not inventors:
                    inventors = [
                        name.strip()
                        for name in inventor_match.group(1).split("\n")
                        if name.strip()
                    ]

            applicant_match = re.search(
                r"출원인[:\s]+(.*?)(?:발명자|IPC|요약|청구항|<\/)", content, re.DOTALL
            )
            if applicant_match:
                applicants = [
                    name.strip() for name in applicant_match.group(1).split(",")
                ]
                if not applicants:
                    applicants = [
                        name.strip()
                        for name in applicant_match.group(1).split("\n")
                        if name.strip()
                    ]

            details["inventors"] = inventors
            details["applicants"] = applicants

            return details

        except Exception as e:
            print(f"Error in get_patent_details: {str(e)}")
            return {
                "patent_number": patent_number,
                "details": "상세 정보 조회 중 오류가 발생했습니다.",
            }


def patent_search_tool() -> PatentAnalyzer:
    """특허 검색 도구 생성"""
    return PatentAnalyzer()
