# macOS 전용 설정
import os
import sys

# macOS GUI 환경 강제 설정
if sys.platform == "darwin":
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    # GUI 모드 강제 설정
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'

# 맥용 폰트 설정
FONT_FAMILY = "SF Pro Display"  # macOS 시스템 폰트
FONT_SIZE = 12

# 메인 앱 import 및 실행
if __name__ == "__main__":
    # 현재 디렉터리를 실행 파일 위치로 변경
    if hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    
    from CleaningAssign import CleaningAssignApp
    
    try:
        app = CleaningAssignApp()
        app.mainloop()
    except Exception as e:
        # GUI 실패시 터미널에 오류 메시지 출력
        print(f"GUI 실행 중 오류가 발생했습니다: {e}")
        print("터미널에서 다음 명령어로 다시 시도해보세요:")
        print("export DISPLAY=:0 && ./CleaningAssign_mac &")
        input("아무 키나 누르면 종료됩니다...") 