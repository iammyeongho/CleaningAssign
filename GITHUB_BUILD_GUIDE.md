# 🚀 GitHub Actions 자동 빌드 완전 가이드

## 📋 개요
GitHub Actions를 사용하면 **코드를 업로드하기만 하면 윈도우와 맥 양쪽 실행파일이 자동으로 생성**됩니다!

## 🎯 최종 결과
- ✅ **윈도우용**: `CleaningAssign_windows.exe` 
- ✅ **맥용**: `CleaningAssign_mac`
- ⚡ **자동 빌드**: 코드 업로드 시 자동 실행
- 💾 **다운로드**: GitHub에서 직접 다운로드

---

## 📝 STEP 1: GitHub 저장소 만들기

### 1-1. GitHub 계정 로그인
- [GitHub.com](https://github.com) 접속 후 로그인

### 1-2. 새 저장소 생성
1. 우측 상단 `+` 버튼 → `New repository` 클릭
2. Repository name: `CleaningAssign` (또는 원하는 이름)
3. **Public** 선택 (GitHub Actions 무료 사용)
4. ✅ `Add a README file` 체크
5. `Create repository` 클릭

---

## 💻 STEP 2: 코드 업로드하기

### 2-1. 방법 A: 웹에서 직접 업로드 (쉬움)

#### 파일 하나씩 업로드:
1. GitHub 저장소 페이지에서 `Add file` → `Upload files`
2. 다음 파일들을 **순서대로** 업로드:

```
📁 업로드할 파일 목록:
├── CleaningAssign.py
├── CleaningAssign_windows.py  
├── CleaningAssign_mac.py
├── requirements.txt
├── windows.spec
├── mac.spec
├── zones.json
├── names.json
├── exclusions.json
└── BUILD_INSTRUCTIONS.md
```

3. 각 파일 업로드 후 `Commit changes` 클릭

#### 폴더 업로드:
1. `settings` 폴더의 내용이 있다면:
   - `Add file` → `Create new file`
   - 파일명에 `settings/example.json` 입력
   - 내용은 `{}` 입력 후 커밋

### 2-2. 방법 B: Git 명령어 사용 (고급)

```bash
# 현재 폴더에서 실행
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/CleaningAssign.git
git push -u origin main
```

---

## ⚙️ STEP 3: GitHub Actions 설정

### 3-1. GitHub Actions 파일 생성
1. GitHub 저장소에서 `Add file` → `Create new file`
2. 파일명: `.github/workflows/build.yml`
3. 내용 복사-붙여넣기:

```yaml
name: Build CleaningAssign

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-windows:
    runs-on: windows-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Build Windows executable
      run: pyinstaller windows.spec --clean --noconfirm
    
    - name: Upload Windows artifact
      uses: actions/upload-artifact@v3
      with:
        name: CleaningAssign-Windows
        path: dist/CleaningAssign_windows.exe

  build-macos:
    runs-on: macos-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Build macOS executable
      run: pyinstaller mac.spec --clean --noconfirm
    
    - name: Upload macOS artifact
      uses: actions/upload-artifact@v3
      with:
        name: CleaningAssign-macOS
        path: dist/CleaningAssign_mac
```

4. `Commit new file` 클릭

---

## 🔄 STEP 4: 자동 빌드 확인

### 4-1. 빌드 진행 상황 확인
1. GitHub 저장소 페이지에서 `Actions` 탭 클릭
2. 방금 커밋한 빌드가 실행 중인지 확인
3. 빌드 이름을 클릭하여 세부 진행 상황 확인

### 4-2. 빌드 시간
- **윈도우 빌드**: 약 3-5분
- **맥 빌드**: 약 5-8분
- **총 소요시간**: 약 10분 내외

### 4-3. 빌드 성공 확인
- ✅ 초록색 체크마크: 성공
- ❌ 빨간색 X: 실패 (로그 확인 필요)

---

## 📥 STEP 5: 빌드된 파일 다운로드

### 5-1. 다운로드 위치
1. `Actions` 탭 → 완료된 빌드 클릭
2. 페이지 하단 `Artifacts` 섹션 확인
3. 다음 파일들이 표시됨:
   - 📦 `CleaningAssign-Windows` (윈도우용)
   - 📦 `CleaningAssign-macOS` (맥용)

### 5-2. 다운로드 방법
1. 원하는 플랫폼 링크 클릭
2. ZIP 파일 자동 다운로드
3. 압축 해제하면 실행파일 획득!

---

## 🎉 STEP 6: 실행파일 사용

### 윈도우용 (`CleaningAssign_windows.exe`)
- 더블클릭으로 바로 실행
- Windows Defender 경고 시: "추가 정보" → "실행" 클릭

### 맥용 (`CleaningAssign_mac`)
- 터미널에서 실행 권한 부여: `chmod +x CleaningAssign_mac`
- 더블클릭 또는 터미널에서 `./CleaningAssign_mac` 실행
- 보안 경고 시: 시스템 환경설정 → 보안 및 개인정보 보호 → "실행 허용"

---

## 🔧 문제 해결

### 빌드 실패 시
1. `Actions` 탭에서 실패한 빌드 클릭
2. 빨간색 X 표시된 단계 클릭
3. 오류 로그 확인
4. 일반적인 문제:
   - `requirements.txt` 파일 누락
   - `zones.json`, `names.json` 파일 누락
   - `.spec` 파일 오류

### 다운로드 안될 때
- 빌드가 완전히 완료될 때까지 기다리기 (초록색 체크마크 확인)
- 페이지 새로고침 후 다시 시도

### 실행 안될 때
**윈도우**:
- VC++ 재배포 패키지 설치 필요시: Microsoft 공식 사이트에서 다운로드

**맥**:
- `chmod +x CleaningAssign_mac` 명령어로 실행 권한 부여
- Gatekeeper 보안 설정에서 허용

---

## 🚀 활용 팁

### 코드 수정 시
1. GitHub에서 파일 직접 수정하거나 새로 업로드
2. 수정 후 자동으로 새 빌드 시작
3. 10분 후 새 실행파일 다운로드 가능

### 버전 관리
- 각 빌드마다 고유한 번호 부여
- 릴리즈 태그 생성하여 버전별 관리 가능

### 무료 사용량
- GitHub Actions: 월 2,000분 무료
- 프로젝트 빌드: 약 10분/회
- **월 200회** 정도 빌드 가능 (충분!)

---

## ✅ 체크리스트

빌드 전 확인사항:
- [ ] 모든 파일이 GitHub에 업로드됨
- [ ] `.github/workflows/build.yml` 생성됨
- [ ] `requirements.txt` 포함됨
- [ ] `zones.json`, `names.json`, `exclusions.json` 포함됨
- [ ] `windows.spec`, `mac.spec` 포함됨

빌드 후 확인사항:
- [ ] Actions 탭에서 성공 확인
- [ ] Artifacts에서 두 파일 모두 다운로드됨
- [ ] 각 플랫폼에서 실행 테스트 완료

---

🎯 **이제 따라해보세요!** 
각 단계별로 천천히 진행하시면, 약 30분 내에 양쪽 플랫폼 실행파일을 모두 얻을 수 있습니다! 🚀 