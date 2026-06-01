# kr-coin-risk-notes

한국어 사용자를 위한 **가상자산 프로젝트 리스크 체크리스트 CLI**입니다.

이 저장소는 특정 코인 매수/매도 판단을 대신하지 않습니다. 공개된 설명, 백서, 토큰 구조, 마케팅 문구 등을 사람이 다시 확인할 수 있도록 위험 신호를 정리해 주는 교육용 오픈소스 도구입니다.

## 왜 만들었나요?

가상자산 초보자는 “수익 보장”, “상장 확정”, “락업 정보 없음”, “팀 정보 불명확” 같은 표현을 제대로 걸러내기 어렵습니다. 이 프로젝트는 그런 문구와 구조적 위험 신호를 하나씩 체크하고, 결과를 JSON으로 남겨서 커뮤니티가 함께 개선할 수 있게 하는 것이 목표입니다.

## 주요 기능

- JSON 입력 파일을 받아 위험 신호를 점검합니다.
- “수익 보장”, “상장 확정” 같은 고위험 문구를 찾아냅니다.
- 결과를 JSON으로 출력합니다.
- 외부 API를 호출하지 않아서 개인정보나 거래내역이 전송되지 않습니다.

## 설치 없이 실행하기

Python 3.10 이상이 필요합니다.

```bash
python -m src.coin_risk_notes_kr.cli --input examples/sample-project.json
```

## 개발 모드 설치

```bash
python -m pip install -e .
coin-risk-notes-kr --input examples/sample-project.json
```

## 입력 예시

```json
{
  "name": "Example Coin",
  "description": "매월 고정 수익을 보장하며, 대형 거래소 상장이 확정되었다고 홍보합니다.",
  "anonymous_team": true,
  "has_public_code": false,
  "has_whitepaper": false,
  "has_tokenomics": false,
  "has_lockup_info": false
}
```

## 출력 예시

```json
{
  "project": "Example Coin",
  "score": 95,
  "risk_level": "high",
  "flags": [
    {
      "key": "guaranteed_return",
      "severity": "high",
      "label": "수익 보장 표현",
      "explanation": "가상자산에서 확정 수익을 보장한다는 표현은 고위험 신호일 수 있습니다."
    }
  ],
  "disclaimer": "교육용 체크리스트이며 투자 조언이 아닙니다."
}
```

## 로드맵

- [ ] 한국어 위험 문구 사전 확장
- [ ] CSV 입력 지원
- [ ] 웹 UI 예제 추가
- [ ] 커뮤니티 제보 기반 체크리스트 개선
- [ ] 영어/일본어 다국어 사전 추가

## 기여 방법

`CONTRIBUTING.md`를 읽고 이슈 또는 풀 리퀘스트를 열어 주세요. 초보자도 문구 추가, 설명 개선, 예제 추가로 기여할 수 있습니다.

## 라이선스

MIT License
