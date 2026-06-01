from coin_risk_notes_kr import analyze_project


def test_guaranteed_return_is_high_risk():
    result = analyze_project(
        {
            "name": "Test Coin",
            "description": "원금 보장과 매월 고정 수익을 홍보합니다.",
            "anonymous_team": False,
            "has_public_code": True,
            "has_whitepaper": True,
            "has_tokenomics": True,
            "has_lockup_info": True,
        }
    )

    keys = {flag["key"] for flag in result["flags"]}
    assert "guaranteed_return" in keys
    assert result["score"] >= 25


def test_clean_project_has_low_score():
    result = analyze_project(
        {
            "name": "Transparent Project",
            "description": "교육용 오픈소스 프로젝트입니다.",
            "anonymous_team": False,
            "has_public_code": True,
            "has_whitepaper": True,
            "has_tokenomics": True,
            "has_lockup_info": True,
        }
    )

    assert result["risk_level"] == "low"
    assert result["flags"] == []
