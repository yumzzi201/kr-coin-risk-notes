from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class RiskSignal:
    key: str
    severity: str
    label: str
    explanation: str
    points: int


SIGNALS: dict[str, RiskSignal] = {
    "guaranteed_return": RiskSignal(
        key="guaranteed_return",
        severity="high",
        label="수익 보장 표현",
        explanation="가상자산에서 확정 수익을 보장한다는 표현은 고위험 신호일 수 있습니다.",
        points=25,
    ),
    "exchange_listing_promises": RiskSignal(
        key="exchange_listing_promises",
        severity="high",
        label="거래소 상장 확정 홍보",
        explanation="검증되지 않은 상장 확정 홍보는 투자자를 조급하게 만들 수 있습니다.",
        points=20,
    ),
    "anonymous_team": RiskSignal(
        key="anonymous_team",
        severity="medium",
        label="팀 정보 불명확",
        explanation="팀과 책임 주체가 불명확하면 문제 발생 시 확인과 대응이 어렵습니다.",
        points=15,
    ),
    "no_public_code": RiskSignal(
        key="no_public_code",
        severity="medium",
        label="공개 코드 없음",
        explanation="기술 프로젝트라면 코드 공개 여부가 검증 가능성에 영향을 줄 수 있습니다.",
        points=10,
    ),
    "no_whitepaper": RiskSignal(
        key="no_whitepaper",
        severity="medium",
        label="백서 또는 설명서 없음",
        explanation="프로젝트의 목적, 구조, 책임 범위를 확인하기 어렵습니다.",
        points=10,
    ),
    "unclear_tokenomics": RiskSignal(
        key="unclear_tokenomics",
        severity="high",
        label="토큰 구조 불명확",
        explanation="발행량, 분배, 유통 계획이 불명확하면 가격 변동 위험을 이해하기 어렵습니다.",
        points=15,
    ),
    "no_lockup_info": RiskSignal(
        key="no_lockup_info",
        severity="high",
        label="락업 정보 없음",
        explanation="팀/초기 투자자 물량의 락업 정보가 없으면 대량 매도 위험을 판단하기 어렵습니다.",
        points=15,
    ),
    "high_pressure_marketing": RiskSignal(
        key="high_pressure_marketing",
        severity="medium",
        label="압박성 마케팅",
        explanation="지금 사지 않으면 늦는다는 식의 홍보는 냉정한 검토를 방해할 수 있습니다.",
        points=10,
    ),
}

KEYWORD_RULES: dict[str, list[str]] = {
    "guaranteed_return": ["수익 보장", "확정 수익", "원금 보장", "매월 고정 수익", "무조건 수익"],
    "exchange_listing_promises": ["상장 확정", "대형 거래소 상장", "곧 상장", "거래소 확정"],
    "high_pressure_marketing": ["오늘만", "마감 임박", "선착순", "지금 안 사면", "놓치면 후회"],
}


def _contains_keyword(text: str, keywords: list[str]) -> bool:
    normalized = text.lower()
    return any(keyword.lower() in normalized for keyword in keywords)


def _risk_level(score: int) -> str:
    if score >= 60:
        return "high"
    if score >= 30:
        return "medium"
    return "low"


def analyze_project(project: dict[str, Any]) -> dict[str, Any]:
    """Analyze a project dictionary and return risk flags.

    This is an educational checklist, not financial advice.
    """
    description = str(project.get("description", ""))
    triggered: list[RiskSignal] = []

    for key, keywords in KEYWORD_RULES.items():
        if _contains_keyword(description, keywords):
            triggered.append(SIGNALS[key])

    boolean_rules = {
        "anonymous_team": bool(project.get("anonymous_team", False)),
        "no_public_code": not bool(project.get("has_public_code", True)),
        "no_whitepaper": not bool(project.get("has_whitepaper", True)),
        "unclear_tokenomics": not bool(project.get("has_tokenomics", True)),
        "no_lockup_info": not bool(project.get("has_lockup_info", True)),
    }

    for key, is_triggered in boolean_rules.items():
        if is_triggered:
            triggered.append(SIGNALS[key])

    # Deduplicate while preserving order.
    seen: set[str] = set()
    unique_flags: list[RiskSignal] = []
    for signal in triggered:
        if signal.key not in seen:
            unique_flags.append(signal)
            seen.add(signal.key)

    score = min(100, sum(signal.points for signal in unique_flags))
    return {
        "project": project.get("name", "unknown"),
        "score": score,
        "risk_level": _risk_level(score),
        "flags": [
            {k: v for k, v in asdict(signal).items() if k != "points"}
            for signal in unique_flags
        ],
        "disclaimer": "교육용 체크리스트이며 투자 조언이 아닙니다.",
    }
