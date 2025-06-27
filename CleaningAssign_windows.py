# 윈도우용 설정
import os
import sys
from pathlib import Path

# 윈도우용 폰트 설정
FONT_REGULAR = ("Malgun Gothic", 13)
FONT_BOLD = ("Malgun Gothic", 13, "bold")
FONT_TITLE = ("Malgun Gothic", 13, "bold")
FONT_SMALL = ("Malgun Gothic", 11)

# 데이터 파일 경로 (윈도우용)
DATA_DIR = str(Path.home() / "AppData" / "Local" / "CleaningAssign")
os.makedirs(DATA_DIR, exist_ok=True)

# 메인 앱 코드 import 전에 설정 적용
import CleaningAssign

# 플랫폼별 설정 적용
CleaningAssign.FONT_REGULAR = FONT_REGULAR
CleaningAssign.FONT_BOLD = FONT_BOLD
CleaningAssign.FONT_TITLE = FONT_TITLE
CleaningAssign.FONT_SMALL = FONT_SMALL
CleaningAssign.DATA_DIR = DATA_DIR

# 데이터 파일 경로 업데이트
CleaningAssign.ZONES_FILE = os.path.join(DATA_DIR, 'zones.json')
CleaningAssign.NAMES_FILE = os.path.join(DATA_DIR, 'names.json')
CleaningAssign.SETTINGS_DIR = os.path.join(DATA_DIR, 'settings')
CleaningAssign.EXCLUSION_FILE = os.path.join(DATA_DIR, 'exclusions.json')
os.makedirs(CleaningAssign.SETTINGS_DIR, exist_ok=True)

# 앱 실행
if __name__ == "__main__":
    # 배정 제외 설정 로드
    CleaningAssign.load_exclusions()
    
    # 앱 시작
    app = CleaningAssign.CleaningAssignApp()
    app.mainloop() 