# 청소구역 배정 프로그램 빌드 가이드

## 🔧 빌드 환경 설정

### 공통 요구사항
```bash
pip install -r requirements.txt
```

## 🏗️ 빌드 방법

### 윈도우용 빌드
```bash
pyinstaller windows.spec --clean --noconfirm
```
- 결과물: `dist/CleaningAssign_windows.exe`

### 맥용 빌드
```bash
pyinstaller mac.spec --clean --noconfirm
```
- 결과물: `dist/CleaningAssign_mac` (실행파일)

## 📦 배포 파일 구성

### 간단 배포 (권장)
**실행파일만 배포하면 됩니다!**
- 윈도우: `CleaningAssign_windows.exe`
- 맥: `CleaningAssign_mac`

### 왜 실행파일만으로 충분한가요?
PyInstaller가 다음 파일들을 자동으로 실행파일에 포함합니다:
- `zones.json` (구역 목록)
- `names.json` (담당자 목록)  
- `exclusions.json` (배정 제외 설정)
- `settings/` 폴더 (저장된 설정들)
- `CleaningAssign.py` (메인 코드)

### 완전 배포 패키지 (선택사항)
개발자나 고급 사용자를 위한 전체 소스코드 포함:
```
CleaningAssign/
├── CleaningAssign_windows.exe    # 윈도우용 실행파일
├── CleaningAssign_mac            # 맥용 실행파일
├── CleaningAssign.py             # 메인 소스코드
├── CleaningAssign_windows.py     # 윈도우용 설정
├── CleaningAssign_mac.py         # 맥용 설정
├── requirements.txt              # 의존성 목록
├── zones.json                    # 기본 구역 목록
├── names.json                    # 기본 담당자 목록
├── exclusions.json               # 기본 제외 설정
├── settings/                     # 설정 폴더
├── windows.spec                  # 윈도우 빌드 설정
├── mac.spec                      # 맥 빌드 설정
└── README_배포.md               # 사용법 안내
```

## 💡 사용자 안내사항

### 첫 실행 시
1. 실행파일을 더블클릭하여 실행
2. 구역과 담당자를 추가
3. Dooray 웹훅 URL 설정
4. 배정 실행

### 데이터 저장 위치
- **윈도우**: `%USERPROFILE%\AppData\Local\CleaningAssign\`
- **맥**: `~/Library/Application Support/CleaningAssign/`

### 주요 기능
- F1: 구역 배정 제외 설정
- F2: 담당자 매칭 제한 설정  
- F3: 현재 제한사항 확인
- 설정 저장/불러오기 지원
- Dooray 메신저 자동 전송

## 🔍 문제 해결

### 실행 안됨 (윈도우)
- Windows Defender에서 차단된 경우: "추가 정보" → "실행" 클릭
- VC++ 재배포 패키지 설치: `vc_redist.x64.exe` 실행

### 실행 안됨 (맥)
- 개발자 미확인 앱 경고: System Preferences → Security & Privacy → "실행 허용" 클릭
- 권한 문제: `chmod +x CleaningAssign_mac` 실행

## 📝 버전 정보
- 버전: v2.0
- 최종 업데이트: 2025-06-27
- 지원 플랫폼: Windows 10/11, macOS 10.14+ 