# 청소구역 배정 프로그램 v2.0

## 개요
Dooray! 웹훅을 통해 청소구역을 자동으로 배정하고 알림을 전송하는 프로그램입니다.

## 배포 구조

### 윈도우용 (Windows)
- **위치**: `windows_dist/dist/CleaningAssign_windows.exe`
- **폰트**: Malgun Gothic
- **데이터 저장 위치**: `%LOCALAPPDATA%\CleaningAssign`

### 맥용 (macOS)
- **위치**: `mac_dist/dist/CleaningAssign_mac.app` (맥 환경에서 빌드 필요)
- **폰트**: AppleGothic  
- **데이터 저장 위치**: `~/Library/Application Support/CleaningAssign`

## 주요 기능

### 기본 기능
- 구역 및 담당자 관리
- 자동 배정 및 Dooray! 전송
- 설정 저장/불러오기

### 특별 기능 (백도어)
- **F1**: 구역 배정 제외 설정
- **F2**: 매칭 제한 설정  
- **F3**: 현재 설정된 제한사항 보기

## 맥용 빌드 방법 (맥 환경에서)

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 빌드 실행:
```bash
cd mac_dist
pyinstaller build_mac.spec
```

3. 빌드된 파일은 `mac_dist/dist/CleaningAssign_mac.app`에 생성됩니다.

## 시스템 요구사항

### 윈도우
- Windows 10 이상
- Visual C++ 재배포 가능 패키지 (자동 설치됨)

### 맥
- macOS 10.14 이상
- Python 3.8 이상 (빌드 시에만 필요)

## 사용법

1. 프로그램 실행
2. 구역과 담당자 등록
3. Dooray! 웹훅 URL 입력
4. "배정 시작 및 Dooray 전송" 버튼 클릭

## 데이터 백업

각 운영체제별 데이터 저장 위치에서 다음 파일들을 백업할 수 있습니다:
- `zones.json`: 구역 정보
- `names.json`: 담당자 정보
- `exclusions.json`: 제외/제한 설정
- `settings/`: 저장된 설정 파일들 