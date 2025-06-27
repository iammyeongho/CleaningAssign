# 📋 GitHub 업로드 체크리스트

## 🎯 목표
GitHub Actions로 윈도우 + 맥 실행파일 자동 생성

## 📁 업로드 필수 파일 목록

### ✅ 메인 코드 파일
- [ ] `CleaningAssign.py` (메인 프로그램, 51KB)
- [ ] `CleaningAssign_windows.py` (윈도우 설정, 1.3KB)
- [ ] `CleaningAssign_mac.py` (맥 설정, 1.3KB)

### ✅ 빌드 설정 파일
- [ ] `requirements.txt` (파이썬 라이브러리 목록)
- [ ] `windows.spec` (윈도우 빌드 설정)
- [ ] `mac.spec` (맥 빌드 설정)

### ✅ 데이터 파일
- [ ] `zones.json` (기본 구역 목록)
- [ ] `names.json` (기본 담당자 목록)
- [ ] `exclusions.json` (기본 제외 설정)

### ✅ GitHub Actions 설정
- [ ] `.github/workflows/build.yml` (자동 빌드 설정)

### ✅ 문서 파일 (선택사항)
- [ ] `BUILD_INSTRUCTIONS.md` (빌드 가이드)
- [ ] `GITHUB_BUILD_GUIDE.md` (GitHub Actions 가이드)
- [ ] `README_배포.md` (사용법 안내)

### ✅ 폴더
- [ ] `settings/` 폴더 (빈 폴더라도 생성)

---

## 🚀 빠른 업로드 순서

### 1단계: 핵심 파일들 (필수)
```
1. CleaningAssign.py
2. CleaningAssign_windows.py
3. CleaningAssign_mac.py
4. requirements.txt
5. windows.spec
6. mac.spec
```

### 2단계: 데이터 파일들
```
7. zones.json
8. names.json
9. exclusions.json
```

### 3단계: GitHub Actions 설정
```
10. .github/workflows/build.yml
```

### 4단계: settings 폴더 생성
```
Add file → Create new file
파일명: settings/placeholder.txt
내용: empty
```

---

## ⚠️ 중요 체크포인트

### 파일명 정확히 확인
- [ ] `CleaningAssign.py` (대소문자 정확)
- [ ] `requirements.txt` (복수형 's' 포함)
- [ ] `.github/workflows/build.yml` (폴더 구조 정확)

### 파일 내용 확인
- [ ] `requirements.txt`에 3개 라이브러리 포함
- [ ] `zones.json`, `names.json`에 기본 데이터 포함
- [ ] `.spec` 파일들에 올바른 플랫폼 설정

### GitHub 저장소 설정
- [ ] Repository 이름: `CleaningAssign` (또는 원하는 이름)
- [ ] **Public** 저장소 (GitHub Actions 무료 사용)
- [ ] README 파일 자동 생성 체크

---

## 🎯 업로드 완료 후 확인사항

### 즉시 확인
- [ ] 모든 파일이 GitHub에 표시됨
- [ ] `Actions` 탭에서 빌드 시작됨
- [ ] 빌드 상태가 "진행 중" 표시

### 10분 후 확인
- [ ] 빌드 완료 (초록색 체크마크)
- [ ] `Artifacts` 섹션에 2개 파일 표시:
  - [ ] `CleaningAssign-Windows`
  - [ ] `CleaningAssign-macOS`

### 다운로드 테스트
- [ ] 윈도우 파일 다운로드 및 압축 해제
- [ ] 맥 파일 다운로드 및 압축 해제
- [ ] 각각 실행 파일 확인

---

## 🔧 문제 발생시 체크

### 빌드 실패시
1. [ ] `Actions` 탭에서 오류 로그 확인
2. [ ] 파일명 오타 확인
3. [ ] 파일 내용 확인
4. [ ] 다시 커밋 후 재시도

### 파일 누락시
1. [ ] 위 체크리스트 다시 확인
2. [ ] 누락된 파일 추가 업로드
3. [ ] 자동으로 새 빌드 시작됨

---

## 💡 꿀팁

### 한번에 여러 파일 업로드
1. `Upload files` 클릭
2. 여러 파일을 한번에 드래그&드롭
3. 한번에 커밋

### 파일 수정시
- GitHub에서 직접 파일 클릭 → 연필 아이콘 → 수정 → 커밋
- 수정시마다 자동으로 새 빌드 실행

### 빌드 시간 단축
- 불필요한 파일 제외
- 주요 변경사항만 커밋

---

🚀 **이 체크리스트를 따라하면 100% 성공합니다!**

문제 발생시 각 단계별로 체크해보세요. 대부분 파일명 오타나 누락이 원인입니다! 📝 