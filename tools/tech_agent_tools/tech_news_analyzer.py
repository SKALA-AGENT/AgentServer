"""기술 뉴스 및 블로그 분석 도구"""

import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
from tavily import TavilyClient


class TechNewsAnalyzer:
    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        # 한국 테크/스타트업 관련 신뢰할 수 있는 도메인 목록
        self.korean_tech_domains = [
            "platum.kr",
            "venture.co.kr",
            "zdnet.co.kr",
            "theguru.co.kr",
            "startuptoday.kr",
            "techcrunch.kr",
            "rocketpunch.com",
            "ycombinator.com",
            "thevc.kr",
            "startupweekly.net",
            "bloter.net",
            "etnews.com",
            "venturesquare.net",
            "fntimes.com",
            "startuprecipe.co.kr",
            "the-pr.co.kr",
            "startup4.co.kr",
            "besuccess.com",
            "insidekorea.kr",
            "hankyung.com",
            "mk.co.kr",
            "tech.kakao.com",
            "woowabros.github.io",
            "toss.tech",
            "d2.naver.com",
            "netmarble.com",
        ]

        # 기술 스택 키워드 (한국어/영어)
        self.tech_keywords = [
            # 언어
            "자바",
            "파이썬",
            "javascript",
            "typescript",
            "kotlin",
            "swift",
            "go",
            "golang",
            "java",
            "python",
            "c#",
            "c++",
            "php",
            "ruby",
            "scala",
            "rust",
            "클로저",
            "clojure",
            # 프레임워크/라이브러리
            "스프링",
            "spring",
            "spring boot",
            "django",
            "flask",
            "fastapi",
            "express",
            "nestjs",
            "react",
            "리액트",
            "뷰",
            "vue",
            "앵귤러",
            "angular",
            "next.js",
            "nuxt.js",
            "svelte",
            "node.js",
            "노드",
            ".net",
            "dotnet",
            "rails",
            "laravel",
            "flutter",
            "플러터",
            # 인프라/클라우드
            "aws",
            "azure",
            "gcp",
            "네이버클라우드",
            "naver cloud",
            "카카오클라우드",
            "kakao cloud",
            "쿠버네티스",
            "kubernetes",
            "도커",
            "docker",
            "jenkins",
            "젠킨스",
            "terraform",
            "ansible",
            "ci/cd",
            "cicd",
            "devops",
            "데브옵스",
            "serverless",
            "서버리스",
            # 데이터/AI
            "빅데이터",
            "big data",
            "데이터 분석",
            "data analysis",
            "머신러닝",
            "machine learning",
            "딥러닝",
            "deep learning",
            "인공지능",
            "ai",
            "artificial intelligence",
            "tensorflow",
            "pytorch",
            "keras",
            "scikit-learn",
            "pandas",
            "numpy",
            "hadoop",
            "spark",
            "엘라스틱서치",
            "elasticsearch",
            "kibana",
            "grafana",
            # 데이터베이스
            "mysql",
            "postgresql",
            "oracle",
            "mongodb",
            "redis",
            "cassandra",
            "dynamodb",
            "mssql",
            "mariadb",
            "sqlite",
            "firebase",
            "파이어베이스",
            "neo4j",
            "cockroachdb",
            # 메시징/분산시스템
            "kafka",
            "카프카",
            "rabbitmq",
            "레빗엠큐",
            "pubsub",
            "activemq",
            "zeromq",
            "grpc",
            "graphql",
            "그래프큐엘",
            "rest api",
            "restful",
            "웹소켓",
            "websocket",
            # 보안/인증
            "oauth",
            "jwt",
            "인증",
            "authentication",
            "authorization",
            "인가",
            "sso",
            "single sign-on",
            "보안",
            "security",
            "암호화",
            "encryption",
            # 모바일
            "android",
            "안드로이드",
            "ios",
            "아이폰",
            "react native",
            "리액트 네이티브",
            "xamarin",
            "자마린",
            "코틀린",
            "스위프트",
        ]
        self.trusted_domains = [
            # 테크/스타트업 미디어
            "platum.kr",
            "venture.co.kr",
            "zdnet.co.kr",
            "theguru.co.kr",
            "startuptoday.kr",
            "techcrunch.kr",
            "venturesquare.net",
            "besuccess.com",
            "startupweekly.net",
            "bloter.net",
            "etnews.com",
            "startuprecipe.co.kr",
            "the-pr.co.kr",
            "startup4.co.kr",
            "insidekorea.kr",
            # 비즈니스/경제 미디어
            "hankyung.com",
            "mk.co.kr",
            "fntimes.com",
            "news.mtn.co.kr",
            "edaily.co.kr",
            "thebell.co.kr",
            "businesspost.co.kr",
            "biz.chosun.com",
            "etoday.co.kr",
            # 투자/VC 관련
            "thevc.kr",
            "rocketpunch.com",
            "vcnews.co.kr",
            "venture.or.kr",
            # 기술 블로그
            "tech.kakao.com",
            "woowabros.github.io",
            "toss.tech",
            "d2.naver.com",
            "engineering.linecorp.com",
            "netmarble.com",
            "medium.com",
            "brunch.co.kr",
            # 글로벌 참고 사이트
            "techcrunch.com",
            "wired.com",
            "forbes.com",
            "fortune.com",
            "businessinsider.com",
            "crunchbase.com",
        ]

    def analyze_technology_innovation(self, company_name: str) -> Dict[str, Any]:
        """회사의 기술력 및 혁신성 분석"""
        try:
            # API 호출 - 기술 및 혁신
            response = self.client.search(
                query=f"{company_name} (기술력 OR 핵심기술 OR 특허 OR 기술혁신 OR AI OR 인공지능 OR 머신러닝 OR 알고리즘 OR 문제점 OR 부정적 반응)",
                search_depth="advanced",
                max_results=5,
                include_domains=self.trusted_domains,
            )

            results = response.get("results", [])

            # 주요 기술 키워드 추출
            tech_keywords = {}
            tech_terms = [
                "인공지능",
                "AI",
                "머신러닝",
                "딥러닝",
                "자연어처리",
                "NLP",
                "컴퓨터비전",
                "빅데이터",
                "데이터분석",
                "알고리즘",
                "자동화",
                "로보틱스",
                "음성인식",
                "영상인식",
                "추천시스템",
                "예측모델",
                "특허",
                "API",
                "플랫폼",
                "SaaS",
                "클라우드",
                "블록체인",
                "생성형AI",
                "LLM",
                "대규모언어모델",
                "강화학습",
            ]

            for result in results:
                content = result.get("content", "").lower()
                for term in tech_terms:
                    term_lower = term.lower()
                    if term_lower in content:
                        tech_keywords[term] = tech_keywords.get(term, 0) + 1
            return {
                "key_technologies": sorted(
                    tech_keywords.items(), key=lambda x: x[1], reverse=True
                )[:5],
                "tech_innovations": [
                    {
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", None) or "",
                        "summary": (
                            result.get("content", "")[:300] + "..."
                            if result.get("content")
                            else ""
                        ),
                    }
                    for result in results[:5]
                ],
            }

        except Exception as e:
            print(f"Error in analyze_technology_innovation: {str(e)}")
            return {"key_technologies": [], "tech_innovations": []}


def tech_news_tool() -> TechNewsAnalyzer:
    """기술 뉴스 분석 도구 생성"""
    return TechNewsAnalyzer()
