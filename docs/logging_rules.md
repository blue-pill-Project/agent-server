# Logging 규칙

이 문서는 현재 코드에서 쓰는 로깅 패턴을 기준으로 팀원들이 같은 방식으로 남기도록 정리한 간단한 규칙입니다.

## 1. 기본 원칙

- 각 모듈에서 `logger = logging.getLogger(__name__)` 로 logger를 선언한다.
- 로깅은 "무엇이 시작되었고, 무엇이 완료되었고, 어떤 값이 중요한지" 중심으로 남긴다.
- 로그는 운영 중 문제를 빠르게 찾을 수 있도록, 식별 가능한 컨텍스트를 포함한다.
- 민감정보(토큰, 비밀번호, API 키, 사용자 개인 정보)는 로그에 남기지 않는다.

## 2. 로그 레벨 규칙

- `info`: 시작/완료/핵심 상태 변화
  - 예: "daily logs 시작", "search_memories 완료", "write_memory 완료"
- `debug`: 상세 파라미터, 쿼리, 유사도, 내부 계산값
  - 예: 검색 쿼리, rerank 결과, similarity 값
- `warning`: 잠재적 문제지만 흐름이 계속되는 경우
- `error`: 실제 실패, 예외 처리, 저장/호출 실패
- `exception`: 예외가 발생했을 때 stack trace를 함께 남길 때

## 3. 메시지 작성 규칙

로그 메시지 형식은 아래처럼 `event | key=value` 형태를 기본으로 한다.

```python
logger.info(
    "daily logs 시작 | room=%s | member=%s | timeslot=%s",
    log_room_id,
    log_room_member_id,
    timeslot,
)
```

```python
logger.debug("similarity | similarity=%s", references[0]["similarity"])
```

권장 포맷:

- 행동/상태: `daily logs 시작`, `search_memories 완료`
- 구분자: `|`
- key=value 패턴으로 값 전달
- 반드시 포함하면 좋은 값:
  - `user_id`
  - `log_room_id`
  - `log_room_member_id`
  - `timeslot`
  - `kind`, `query`, `similarity`, `result_count` 등

## 4. 로그를 남길 때의 기준

다음 상황은 거의 항상 로깅한다.

- 에이전트/그래프 시작
- 외부 저장소 조회/저장 완료
- 검색/생성/다듬기 단계 완료
- 결과 수, 필터, 쿼리, similarity 등 핵심 파라미터
- 실패 또는 예외 발생

다음은 남기지 않는 편이 좋다.

- 너무 자주 반복되는 noisy 로그
- 함수 내부의 모든 라인 단위 디버그
- 민감 정보와 같은 raw 데이터
- 값이 의미 없거나 추적 불가한 로그

## 5. 설정 규칙

기본 logging 설정은 아래처럼 구성한다.

- 루트 레벨: `INFO`
- `agents`, `domains`: `DEBUG`
- noisy 라이브러리: `WARNING`으로 낮춤

예시:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
```

## 6. 코드 예시

아래 패턴을 기준으로 작성한다.

```python
logger = logging.getLogger(__name__)

logger.info("search_memories 완료")
logger.debug("search query | query=%s | kind=%s", query, kind_hint)
```

```python
logger.info(
    "daily logs 저장 완료 | member=%s | log_saved=%s | plan_saved=%s",
    log_room_member_id,
    log_saved,
    plan_saved,
)
```

## 7. 팀 규칙 요약

- `info`는 비즈니스 단계 로그
- `debug`는 상세 파라미터 로그
- 메시지는 `event | key=value` 형식
- 컨텍스트 ID를 포함
- 민감정보 금지
- 로깅은 추적 가능하고 문제 재현에 도움이 되게 남긴다

이 패턴을 따르면 로그를 읽는 사람이 "무엇이 시작됐고, 어떤 값으로 동작했고, 어디서 끝났는지" 바로 확인할 수 있다.
