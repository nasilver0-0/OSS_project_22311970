<refrigeGO_project 실행법 - Windows기준>

1. 아래의 링크에서 Python 설치
https://www.python.org/downloads/windows/
(Python 3.14.0b2-  Windows installer (64-bit))
: 설치 실행 시 반드시 "Add Python to PATH", "Install pip" 등 모든 체크박스 체크

2. 압축 해제
: 제출한 압축파일을 "파일명 폴더에 풀기"를 이용해 압축을 해제하세요.

3. 명령 프롬프트(cmd) 실행 및 경로 이동
: 다음 명령어를 입력해 프로젝트 폴더로 이동하세요.
(탐색기에서 상단의 전체 경로를 복사해서 붙여넣으세요.)
  cd 파일경로

4. 가상환경 생성 및 패키지 설치
  1) 가상환경 생성:
    python -m venv venv

  2) 가상환경 진입:
    venv\Scripts\activate

  3) 필수 라이브러리 설치:
 python -m pip install -r requirements.txt

5. 데이터베이스 초기화 (최초 실행 시)
 python manage.py makemigrations  
 python manage.py migrate

6. 관리자 계정 생성 (최초 1회만)
 python manage.py createsuperuser  
-> 사용자명 / 이메일 / 비밀번호 입력

7. 개발 서버 실행
 python manage.py runserver

8. 브라우저에서 아래 주소로 접속
 http://127.0.0.1:8000/