# Git Flow 및 개발 규칙

이 문서는 팀 프로젝트에서 브랜치를 어떻게 사용하고, 코드를 작성할 때 어떤 규칙을 지킬지 정리한 문서입니다.

## 기본 개발 방향

이번 프로젝트의 1차 목표는 완성도 높은 모든 기능을 한 번에 만드는 것이 아니라, 프론트엔드와 백엔드가 연동 가능한 최소 기능을 빠르게 구현하는 것입니다.

따라서 개발할 때는 다음 원칙을 지킵니다.

1. 최소한의 기능만 먼저 구현한다.
2. 기능을 크게 만들기보다 작게 나누어 구현한다.
3. 각자 맡은 영역의 책임을 명확히 한다.
4. 당장 필요하지 않은 기능은 2차 개발로 미룬다.
5. 코드가 복잡해지면 먼저 구조를 단순하게 만든다.
6. 동작 확인이 끝난 기능만 Pull Request를 올린다.

1차 개발에서 제외하는 기능은 다음과 같습니다.

```text
- 결제 기능
- 당근페이 기능
- 알림 기능
- 이미지 업로드
- 채팅 읽음 처리
- 관리자 기능
- 복잡한 검색 및 필터링
```

## 브랜치 구조

이 프로젝트는 간단한 Git Flow 방식을 사용합니다.

```text
main
- 최종 제출 및 안정 버전 브랜치
- 직접 작업하지 않음
- develop에서 충분히 테스트된 코드만 병합

develop
- 개발 통합 브랜치
- 각 feature 브랜치의 작업 결과를 모아서 테스트하는 곳
- 직접 작업하지 않음

feature/db-docker
- DB 설계 및 Docker 환경 구성
- 담당: 재현

feature/auth-board
- 로그인, 회원가입, 게시판 API 개발
- 담당: 태규

feature/chat
- 채팅방, 실시간 메시지 개발
- 담당: 재용

feature/frontend
- 프론트엔드 화면 및 API 연동
- 담당: 프론트엔드 팀
```

## develop 브랜치가 필요한 이유

백엔드와 프론트엔드 개발자는 각자 `feature/*` 브랜치에서 작업합니다. 하지만 각자 만든 기능을 바로 `main`에 합치면 오류가 생겼을 때 안정 버전이 깨질 수 있습니다.

그래서 `develop` 브랜치를 중간 통합 브랜치로 사용합니다.

```text
feature/db-docker -> develop
feature/auth-board -> develop
feature/chat -> develop
feature/frontend -> develop

develop -> main
```

`develop`에서는 다음 내용을 확인합니다.

```text
- DB와 서버가 함께 실행되는지
- 로그인 API와 게시판 API가 함께 동작하는지
- 채팅 기능이 사용자 정보와 연결되는지
- 프론트엔드가 백엔드 API를 호출할 수 있는지
- Docker 환경에서 전체 서비스가 실행되는지
```

## 작업 흐름

각자 작업할 때는 아래 순서를 따릅니다.

1. 본인 담당 브랜치로 이동한다.
2. 맡은 기능을 최소 단위로 구현한다.
3. 직접 실행해서 동작을 확인한다.
4. 변경사항을 커밋한다.
5. GitHub에 push한다.
6. `develop` 브랜치로 Pull Request를 생성한다.
7. 팀원 리뷰 후 병합한다.
8. 1차 기능이 모두 안정화되면 `develop`을 `main`에 병합한다.

## 커밋 메시지 규칙

커밋 메시지는 아래 형식을 사용합니다.

```text
타입: 작업 내용
```

예시는 다음과 같습니다.

```text
feat: add login api
feat: create post entity
feat: add docker compose for database
feat: add frontend board page
fix: resolve database connection error
docs: update api specification
chore: update project settings
```

사용 가능한 타입은 다음과 같습니다.

```text
feat
- 새로운 기능 추가

fix
- 버그 수정

docs
- 문서 작성 또는 수정

style
- 코드 포맷, 세미콜론, 들여쓰기 등 기능 변화 없는 수정

refactor
- 기능 변화 없이 코드 구조 개선

test
- 테스트 코드 추가 또는 수정

chore
- 설정 파일, 패키지, 빌드 관련 수정
```

커밋 메시지 작성 시 주의할 점은 다음과 같습니다.

```text
- 한 커밋에는 하나의 목적만 담는다.
- 너무 큰 단위로 커밋하지 않는다.
- 메시지는 가능하면 영어로 작성한다.
- 무엇을 했는지 알 수 있게 구체적으로 작성한다.
```

좋은 예시는 다음과 같습니다.

```text
feat: add signup api
fix: handle invalid login password
chore: add mysql docker compose
```

피해야 할 예시는 다음과 같습니다.

```text
update
fix
작업함
수정
이것저것 고침
```

## Pull Request 규칙

Pull Request는 항상 본인 feature 브랜치에서 `develop` 브랜치로 생성합니다.

```text
feature/db-docker -> develop
feature/auth-board -> develop
feature/chat -> develop
feature/frontend -> develop
```

`main`으로 바로 Pull Request를 보내지 않습니다. `main` 병합은 1차 기능이 모두 합쳐지고 테스트된 뒤 진행합니다.

Pull Request 제목 예시는 다음과 같습니다.

```text
feat: add login and signup api
feat: add chat room message socket
chore: add docker database setup
docs: add api specification
```

Pull Request 설명에는 다음 내용을 적습니다.

```text
## 작업 내용
- 구현한 기능 요약

## 확인 방법
- 어떻게 실행하고 테스트했는지

## 참고 사항
- 아직 남은 작업 또는 주의할 점
```

## 코드 작성 규칙

코드를 작성할 때는 다음 규칙을 지킵니다.

```text
- 한 함수 또는 메서드는 하나의 역할만 하도록 작성한다.
- 같은 코드를 반복해서 작성하지 않는다.
- 변수명과 함수명은 역할이 드러나게 작성한다.
- 사용하지 않는 코드는 남기지 않는다.
- 임시 테스트용 코드는 커밋 전에 제거한다.
- 비밀번호, 토큰, DB 접속 정보는 코드에 직접 작성하지 않는다.
- 환경 변수는 .env 파일로 관리하고 .env는 Git에 올리지 않는다.
```

API를 작성할 때는 응답 형식을 최대한 통일합니다.

성공 응답 예시:

```json
{
  "success": true,
  "data": {},
  "message": "요청 성공"
}
```

실패 응답 예시:

```json
{
  "success": false,
  "error": {
    "code": "AUTH_REQUIRED",
    "message": "로그인이 필요합니다."
  }
}
```

## 1차 개발 범위

1차 개발에서는 프론트엔드와 연동 가능한 최소 기능만 구현합니다.

```text
- 회원가입
- 로그인
- 게시글 작성
- 게시글 목록 조회
- 게시글 상세 조회
- 게시글 수정
- 게시글 삭제
- 채팅방 목록 조회
- 채팅방 입장
- 실시간 메시지 전송
- 실시간 메시지 수신
- 메시지 DB 저장
- 프론트엔드 API 연동
```

1차 개발이 끝난 뒤 추가 기능을 논의합니다.
