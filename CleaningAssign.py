import customtkinter as ctk
import os
import json
import datetime
import requests
from tkinter import messagebox
import random
import tkinter as tk
import tkinter.ttk as ttk

# 데이터 파일 경로
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
ZONES_FILE = os.path.join(DATA_DIR, 'zones.json')
NAMES_FILE = os.path.join(DATA_DIR, 'names.json')
SETTINGS_DIR = os.path.join(DATA_DIR, 'settings')
os.makedirs(SETTINGS_DIR, exist_ok=True)

# 배정 제외 및 매칭 제한 설정
EXCLUSION_SETTINGS = {
    "zone_exclusions": {},  # 담당자: [제외할 구역들]
    "pair_exclusions": {}   # 담당자: [매칭 제외할 담당자들]
}

# 설정 파일 경로
EXCLUSION_FILE = os.path.join(DATA_DIR, 'exclusions.json')

# 데이터 불러오기/저장 함수
def load_json(file_path, default=None):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default if default is not None else []

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# customtkinter 기본 설정
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
 
# 폰트 설정
FONT_REGULAR = ("Pretendard", 13)
FONT_BOLD = ("Pretendard", 13, "bold")
FONT_TITLE = ("Pretendard", 13, "bold")
FONT_SMALL = ("Pretendard", 11)

# 스타일 상수
INPUT_HEIGHT = 32  # 입력 요소 높이
BORDER_COLOR = "#E5E5E5"
HOVER_COLOR = "#F8F9FA"
SELECT_COLOR = "#EBF6FF"

# 높이 상수 (행 개수 기준)
SETTING_ROWS = 2     # 설정 목록 표시 행 수
ASSIGN_ROWS = 3      # 배정 목록 표시 행 수
LIST_ROWS = 3       # 일반 목록 표시 행 수

# 상수 추가
MAX_TEXT_LENGTH = 15  # 최대 표시 글자 수

def truncate_text(text, max_length=MAX_TEXT_LENGTH):
    """텍스트가 최대 길이를 초과하면 말줄임표를 추가합니다."""
    return text if len(text) <= max_length else text[:max_length-2] + "..."

# 설정 저장/로드 함수
def save_exclusions():
    save_json(EXCLUSION_FILE, EXCLUSION_SETTINGS)

def load_exclusions():
    global EXCLUSION_SETTINGS
    if os.path.exists(EXCLUSION_FILE):
        EXCLUSION_SETTINGS = load_json(EXCLUSION_FILE)

# 설정 다이얼로그 클래스 추가
class ExclusionDialog(ctk.CTkToplevel):
    def __init__(self, parent, names, zones, mode="zone"):
        super().__init__(parent)
        self.result = None
        self.mode = mode
        
        # 창 설정
        self.title("배정 제외 설정" if mode == "zone" else "매칭 제한 설정")
        self.geometry("500x800")  # 창 크기 증가
        self.resizable(False, False)
        
        # 모달 설정
        self.transient(parent)
        self.grab_set()
        
        # 메인 프레임
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        if mode == "zone":
            # 구역 배정 제외 설정
            ctk.CTkLabel(main_frame, text="담당자 선택:", font=FONT_BOLD).pack(pady=(0, 5))
            self.name_combobox = ctk.CTkComboBox(main_frame, values=names, font=FONT_REGULAR)
            self.name_combobox.pack(fill="x", pady=(0, 15))
            
            ctk.CTkLabel(main_frame, text="제외할 구역 선택:", font=FONT_BOLD).pack(pady=(0, 5))
            self.zone_listbox = tk.Listbox(main_frame, font=FONT_REGULAR, selectmode="multiple", height=15)
            self.zone_listbox.pack(fill="both", expand=True, pady=(0, 15))
            
            # 현재 선택된 구역 표시
            ctk.CTkLabel(main_frame, text="현재 선택된 제외 설정:", font=FONT_BOLD).pack(pady=(0, 5))
            self.current_exclusions = ctk.CTkTextbox(main_frame, height=100, font=FONT_REGULAR)
            self.current_exclusions.pack(fill="x", pady=(0, 15))
            self.current_exclusions.configure(state="disabled")
            
            # 구역 목록 채우기
            for zone in zones:
                self.zone_listbox.insert(tk.END, zone["name"])
                
            # 기존 설정 선택
            if self.name_combobox.get() in EXCLUSION_SETTINGS["zone_exclusions"]:
                excluded_zones = EXCLUSION_SETTINGS["zone_exclusions"][self.name_combobox.get()]
                for i in range(self.zone_listbox.size()):
                    if self.zone_listbox.get(i) in excluded_zones:
                        self.zone_listbox.selection_set(i)
            
        else:
            # 매칭 제한 설정
            ctk.CTkLabel(main_frame, text="기준 담당자:", font=FONT_BOLD).pack(pady=(0, 5))
            self.name1_combobox = ctk.CTkComboBox(main_frame, values=names, font=FONT_REGULAR)
            self.name1_combobox.pack(fill="x", pady=(0, 15))
            
            ctk.CTkLabel(main_frame, text="매칭 제외할 담당자들:", font=FONT_BOLD).pack(pady=(0, 5))
            self.name2_listbox = tk.Listbox(main_frame, font=FONT_REGULAR, selectmode="multiple", height=15)
            self.name2_listbox.pack(fill="both", expand=True, pady=(0, 15))
            
            # 현재 선택된 매칭 표시
            ctk.CTkLabel(main_frame, text="현재 선택된 매칭 제한:", font=FONT_BOLD).pack(pady=(0, 5))
            self.current_exclusions = ctk.CTkTextbox(main_frame, height=100, font=FONT_REGULAR)
            self.current_exclusions.pack(fill="x", pady=(0, 15))
            self.current_exclusions.configure(state="disabled")
            
            # 담당자 목록 채우기
            for name in names:
                self.name2_listbox.insert(tk.END, name)
                
            # 기존 설정 선택
            if self.name1_combobox.get() in EXCLUSION_SETTINGS["pair_exclusions"]:
                excluded_names = EXCLUSION_SETTINGS["pair_exclusions"][self.name1_combobox.get()]
                for i in range(self.name2_listbox.size()):
                    if self.name2_listbox.get(i) in excluded_names:
                        self.name2_listbox.selection_set(i)
        
        # 버튼 프레임
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(15, 0))
        
        # 버튼 크기 증가
        ctk.CTkButton(btn_frame, text="설정 저장", command=self.save_clicked, 
                     font=FONT_REGULAR, width=150, height=32).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btn_frame, text="취소", command=self.cancel_clicked, 
                     font=FONT_REGULAR, width=150, height=32).pack(side="right", expand=True, padx=5)
        
        # 선택 변경 시 이벤트 바인딩
        if mode == "zone":
            self.zone_listbox.bind('<<ListboxSelect>>', self.update_current_exclusions)
            self.name_combobox.configure(command=self.update_current_exclusions)
        else:
            self.name2_listbox.bind('<<ListboxSelect>>', self.update_current_exclusions)
            self.name1_combobox.configure(command=self.update_current_exclusions)
        
        # 초기 선택 상태 표시
        self.update_current_exclusions()

    def update_current_exclusions(self, event=None):
        """현재 선택된 제외 설정을 표시"""
        self.current_exclusions.configure(state="normal")
        self.current_exclusions.delete("1.0", tk.END)
        
        if self.mode == "zone":
            name = self.name_combobox.get()
            selected_indices = self.zone_listbox.curselection()
            zones = [self.zone_listbox.get(i) for i in selected_indices]
            
            if zones:
                self.current_exclusions.insert("1.0", f"'{name}'의 제외 구역:\n{', '.join(zones)}")
            else:
                self.current_exclusions.insert("1.0", "제외할 구역을 선택하세요.")
        else:
            name1 = self.name1_combobox.get()
            selected_indices = self.name2_listbox.curselection()
            names = [self.name2_listbox.get(i) for i in selected_indices]
            
            if names:
                self.current_exclusions.insert("1.0", f"'{name1}'의 매칭 제외:\n{', '.join(names)}")
            else:
                self.current_exclusions.insert("1.0", "매칭 제외할 담당자를 선택하세요.")
        
        self.current_exclusions.configure(state="disabled")
    
    def save_clicked(self):
        """설정을 저장하고 적용"""
        if not self.validate_selection():
            return
            
        name, items = self.get_selection()
        
        if self.mode == "zone":
            # 구역 배정 제외 설정
            if items:  # 선택된 구역이 있는 경우
                EXCLUSION_SETTINGS["zone_exclusions"][name] = items
            elif name in EXCLUSION_SETTINGS["zone_exclusions"]:  # 선택된 구역이 없는 경우 설정 제거
                del EXCLUSION_SETTINGS["zone_exclusions"][name]
        else:
            # 매칭 제한 설정
            if items:  # 선택된 담당자가 있는 경우
                EXCLUSION_SETTINGS["pair_exclusions"][name] = items
            elif name in EXCLUSION_SETTINGS["pair_exclusions"]:  # 선택된 담당자가 없는 경우 설정 제거
                del EXCLUSION_SETTINGS["pair_exclusions"][name]
        
        # 설정 파일에 저장
        save_exclusions()
        
        # 설정 적용 메시지
        if self.mode == "zone":
            if items:
                messagebox.showinfo("알림", f"{name}의 제외 구역이 설정되었습니다.")
            else:
                messagebox.showinfo("알림", f"{name}의 모든 제외 설정이 해제되었습니다.")
        else:
            if items:
                messagebox.showinfo("알림", f"{name}의 매칭 제한이 설정되었습니다.")
            else:
                messagebox.showinfo("알림", f"{name}의 모든 매칭 제한이 해제되었습니다.")
        
        self.destroy()
    
    def validate_selection(self):
        """선택 유효성 검사"""
        if self.mode == "zone":
            name = self.name_combobox.get()
            selected_indices = self.zone_listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("경고", "제외할 구역을 선택해주세요.")
                return False
        else:
            name1 = self.name1_combobox.get()
            selected_indices = self.name2_listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("경고", "매칭 제외할 담당자를 선택해주세요.")
                return False
            if name1 in [self.name2_listbox.get(i) for i in selected_indices]:
                messagebox.showwarning("경고", "자기 자신은 매칭 제외 대상이 될 수 없습니다.")
                return False
        return True
    
    def get_selection(self):
        """현재 선택 상태 반환"""
        if self.mode == "zone":
            name = self.name_combobox.get()
            selected_indices = self.zone_listbox.curselection()
            zones = [self.zone_listbox.get(i) for i in selected_indices]
            return (name, zones)
        else:
            name1 = self.name1_combobox.get()
            selected_indices = self.name2_listbox.curselection()
            excluded_names = [self.name2_listbox.get(i) for i in selected_indices]
            return (name1, excluded_names)
    
    def cancel_clicked(self):
        self.destroy()

class CleaningAssignApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("청소구역 배정 프로그램 v2.0")
        self.geometry("1000x1200")
        self.resizable(True, True)
        
        # 선택된 항목 관리
        self.selected_zone = None
        self.selected_assign_zone = None
        self.selected_name = None
        self.selected_setting = None
        self.selected_setting_file = None
        
        # 키 바인딩 추가
        self.bind('<F1>', self.toggle_zone_exclusion)  # F1: 구역 배정 제외
        self.bind('<F2>', self.toggle_pair_exclusion)  # F2: 페어 매칭 제한
        self.bind('<F3>', self.show_current_exclusions)  # F3: 현재 설정된 제한사항 보기

        self.create_widgets()

    def create_widgets(self):
        # 데이터 로드
        self.zones = load_json(ZONES_FILE, default=[])
        self.names = load_json(NAMES_FILE, default=[])

        # 전체 프레임
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.main_frame.pack(fill="both", expand=True, padx=16, pady=16)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # 1:1:1 비율로 설정
        self.main_frame.grid_columnconfigure(0, weight=10)  # 좌측 프레임
        self.main_frame.grid_columnconfigure(1, weight=0)  # 구분선
        self.main_frame.grid_columnconfigure(2, weight=10)  # 중앙 프레임
        self.main_frame.grid_columnconfigure(3, weight=0)  # 구분선
        self.main_frame.grid_columnconfigure(4, weight=1)  # 우측 프레임

        # 좌: 구역 관리
        self.left_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=0)

        # 제목: 구역 관리
        title_zone = ctk.CTkFrame(self.left_frame, fg_color="#f5f6fa")
        title_zone.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(title_zone, text="구역 관리", font=FONT_TITLE, fg_color="#f5f6fa", anchor="w").pack(fill="x", padx=10, pady=10)

        # 입력 영역
        entry_frame = ctk.CTkFrame(self.left_frame, fg_color="#ffffff")
        entry_frame.pack(fill="x", pady=(0, 10), padx=5)
        self.zone_entry = ctk.CTkEntry(entry_frame, placeholder_text="구역명 입력", 
                                     font=FONT_REGULAR, height=INPUT_HEIGHT)
        self.zone_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.zone_count_var = ctk.StringVar(value="1")
        self.zone_count_menu = ctk.CTkOptionMenu(entry_frame, variable=self.zone_count_var, 
                                                values=[str(i) for i in range(1, 11)], 
                                                font=FONT_REGULAR, width=60, height=INPUT_HEIGHT)
        self.zone_count_menu.pack(side="left", padx=(0, 5))
        self.zone_add_btn = ctk.CTkButton(entry_frame, text="+", command=self.add_zone, 
                                         font=FONT_REGULAR, width=INPUT_HEIGHT, height=INPUT_HEIGHT)
        self.zone_add_btn.pack(side="left")

        # 전체 구역 목록 제목
        title_zone_list = ctk.CTkFrame(self.left_frame, fg_color="#f5f6fa")
        title_zone_list.pack(fill="x", pady=(0, 5))
        title_frame = ctk.CTkFrame(title_zone_list, fg_color="#f5f6fa")
        title_frame.pack(fill="x", padx=10, pady=7)
        ctk.CTkLabel(title_frame, text="전체 구역 목록", font=FONT_BOLD, 
                    fg_color="#f5f6fa", anchor="w").pack(side="left")
        assign_all_zones_btn = ctk.CTkButton(title_frame, text="전체 배정", width=70, height=24,
                                           command=self.assign_all_zones, font=FONT_SMALL)
        assign_all_zones_btn.pack(side="right")

        # 구역 목록 스크롤 프레임
        zone_list_frame = ctk.CTkFrame(self.left_frame, fg_color="#ffffff",
                                     border_width=1, border_color=BORDER_COLOR)
        zone_list_frame.pack(fill="both", expand=True, padx=5)
        
        self.zone_scroll_frame = ctk.CTkScrollableFrame(zone_list_frame, fg_color="#ffffff")
        self.zone_scroll_frame.pack(fill="both", expand=True)
        
        # 최소 높이 설정
        min_height = LIST_ROWS * (INPUT_HEIGHT + 10)  # 행 높이 + 여백
        zone_list_frame.configure(height=min_height)
        zone_list_frame.pack_propagate(False)

        # 중앙: 배정에 사용할 구역
        self.center_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff")
        self.center_frame.grid(row=0, column=2, sticky="nsew", padx=8, pady=0)

        # 제목: 배정에 사용할 구역
        title_assign = ctk.CTkFrame(self.center_frame, fg_color="#f5f6fa")
        title_assign.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(title_assign, text="배정에 사용할 구역", font=FONT_BOLD, 
                    fg_color="#f5f6fa", anchor="w").pack(fill="x", padx=10, pady=7)

        # 배정 구역 스크롤 프레임
        zone_assign_frame = ctk.CTkFrame(self.center_frame, fg_color="#ffffff",
                                       border_width=1, border_color=BORDER_COLOR)
        zone_assign_frame.pack(fill="both", expand=True, padx=5)
        
        self.zone_assign_scroll_frame = ctk.CTkScrollableFrame(zone_assign_frame, fg_color="#ffffff")
        self.zone_assign_scroll_frame.pack(fill="both", expand=True)
        
        # 최소 높이 설정
        min_height = LIST_ROWS * (INPUT_HEIGHT + 10)
        zone_assign_frame.configure(height=min_height)
        zone_assign_frame.pack_propagate(False)

        # 우: 담당자 관리
        self.right_frame = ctk.CTkFrame(self.main_frame, fg_color="#ffffff")
        self.right_frame.grid(row=0, column=4, sticky="nsew", padx=(8, 0), pady=0)

        # 제목: 담당자 관리
        title_name = ctk.CTkFrame(self.right_frame, fg_color="#f5f6fa")
        title_name.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(title_name, text="담당자 관리", font=FONT_TITLE, 
                    fg_color="#f5f6fa", anchor="w").pack(fill="x", padx=10, pady=10)

        # 입력 영역
        name_entry_frame = ctk.CTkFrame(self.right_frame, fg_color="#ffffff", 
                                      border_width=1, border_color=BORDER_COLOR)
        name_entry_frame.pack(fill="x", pady=(0, 10), padx=5)
        self.name_entry = ctk.CTkEntry(name_entry_frame, placeholder_text="담당자명 입력", 
                                     font=FONT_REGULAR, height=INPUT_HEIGHT)
        self.name_entry.pack(side="left", fill="x", expand=True, padx=(5, 5), pady=5)
        self.name_add_btn = ctk.CTkButton(name_entry_frame, text="+", command=self.add_name, 
                                         font=FONT_REGULAR, width=INPUT_HEIGHT, height=INPUT_HEIGHT)
        self.name_add_btn.pack(side="left", padx=(0, 5), pady=5)

        # 전체 담당자 목록 제목
        title_name_list = ctk.CTkFrame(self.right_frame, fg_color="#f5f6fa")
        title_name_list.pack(fill="x", pady=(0, 5))
        title_frame = ctk.CTkFrame(title_name_list, fg_color="#f5f6fa")
        title_frame.pack(fill="x", padx=10, pady=7)
        ctk.CTkLabel(title_frame, text="전체 담당자 목록", font=FONT_BOLD, 
                    fg_color="#f5f6fa", anchor="w").pack(side="left")
        assign_all_names_btn = ctk.CTkButton(title_frame, text="전체 배정", width=70, height=24,
                                           command=self.assign_all_names, font=FONT_SMALL)
        assign_all_names_btn.pack(side="right")

        # 담당자 목록 스크롤 프레임
        name_list_frame = ctk.CTkFrame(self.right_frame, fg_color="#ffffff",
                                     border_width=1, border_color=BORDER_COLOR)
        name_list_frame.pack(fill="both", expand=True, pady=(0, 10), padx=5)
        
        self.name_scroll_frame = ctk.CTkScrollableFrame(name_list_frame, fg_color="#ffffff")
        self.name_scroll_frame.pack(fill="both", expand=True)
        
        # 최소 높이 설정
        min_height = LIST_ROWS * (INPUT_HEIGHT + 10)
        name_list_frame.configure(height=min_height)
        name_list_frame.pack_propagate(False)

        # 배정에 사용할 담당자 제목
        title_assign_name = ctk.CTkFrame(self.right_frame, fg_color="#f5f6fa")
        title_assign_name.pack(fill="x", pady=(0, 5))
        ctk.CTkLabel(title_assign_name, text="배정에 사용할 담당자", font=FONT_BOLD, 
                    fg_color="#f5f6fa", anchor="w").pack(fill="x", padx=10, pady=7)

        # 담당자 배정 스크롤 프레임
        name_assign_frame = ctk.CTkFrame(self.right_frame, fg_color="#ffffff",
                                       border_width=1, border_color=BORDER_COLOR)
        name_assign_frame.pack(fill="both", expand=True, padx=5)
        
        self.name_assign_scroll_frame = ctk.CTkScrollableFrame(name_assign_frame, fg_color="#ffffff")
        self.name_assign_scroll_frame.pack(fill="both", expand=True)
        
        # 최소 높이 설정
        min_height = ASSIGN_ROWS * (INPUT_HEIGHT + 10)
        name_assign_frame.configure(height=min_height)
        name_assign_frame.pack_propagate(False)

        # 담당자 배정 리스트박스
        self.name_assign_listbox = tk.Listbox(self.name_assign_scroll_frame, height=7, 
                                            font=FONT_REGULAR, 
                                            selectbackground='#3399ff', 
                                            selectforeground='white', 
                                            borderwidth=0, 
                                            highlightthickness=0)
        self.name_assign_listbox.pack(fill="both", expand=True, padx=5, pady=5)

        # 구분선
        self.sep1 = ttk.Separator(self.main_frame, orient="vertical")
        self.sep1.grid(row=0, column=1, sticky="ns")
        self.sep2 = ttk.Separator(self.main_frame, orient="vertical")
        self.sep2.grid(row=0, column=3, sticky="ns")

        # 하단: 설정/전송
        self.bottom_frame = ctk.CTkFrame(self, fg_color="#ffffff")
        self.bottom_frame.pack(fill="x", padx=16, pady=(0, 16))
        
        title_bottom = ctk.CTkFrame(self.bottom_frame, fg_color="#f5f6fa")
        title_bottom.pack(fill="x", pady=(0, 10))
        ctk.CTkLabel(title_bottom, text="설정 저장/불러오기 및 Dooray 전송", 
                    font=FONT_TITLE, fg_color="#f5f6fa").pack(pady=10)

        self.webhook_entry = ctk.CTkEntry(self.bottom_frame, 
                                        placeholder_text="Dooray 웹훅 URL 입력", 
                                        font=FONT_REGULAR)
        self.webhook_entry.pack(fill="x", padx=10, pady=5)

        now_str = datetime.datetime.now().strftime("%Y-%m-%d_")
        self.setting_name_entry = ctk.CTkEntry(self.bottom_frame, 
                                             placeholder_text="설정 이름 입력", 
                                             font=FONT_REGULAR)
        self.setting_name_entry.insert(0, now_str)
        self.setting_name_entry.pack(fill="x", padx=10, pady=5)

        self.save_setting_btn = ctk.CTkButton(self.bottom_frame, 
                                            text="현재 설정 저장", 
                                            command=self.save_setting, 
                                            font=FONT_REGULAR)
        self.save_setting_btn.pack(fill="x", padx=10, pady=5)

        # 저장된 설정 목록 제목
        title_setting_list = ctk.CTkFrame(self.bottom_frame, fg_color="#f5f6fa")
        title_setting_list.pack(fill="x", pady=(10, 5))
        ctk.CTkLabel(title_setting_list, text="저장된 설정 목록", 
                    font=FONT_BOLD, fg_color="#f5f6fa").pack(pady=7)

        # 설정 목록 스크롤 프레임
        setting_frame = ctk.CTkFrame(self.bottom_frame, fg_color="#ffffff",
                                   border_width=1, border_color=BORDER_COLOR)
        setting_frame.pack(fill="x", padx=10, pady=5)
        
        self.setting_scroll_frame = ctk.CTkScrollableFrame(setting_frame, fg_color="#ffffff")
        self.setting_scroll_frame.pack(fill="both", expand=True)
        
        # 최소 높이 설정
        min_height = SETTING_ROWS * (INPUT_HEIGHT + 10)
        setting_frame.configure(height=min_height)
        setting_frame.pack_propagate(False)

        # 설정 관련 버튼 프레임
        setting_btn_frame = ctk.CTkFrame(self.bottom_frame, fg_color="#ffffff")
        setting_btn_frame.pack(fill="x", padx=10, pady=5)

        self.load_setting_btn = ctk.CTkButton(setting_btn_frame, 
                                            text="선택 설정 불러오기", 
                                            command=self.load_setting, 
                                            font=FONT_REGULAR)
        self.load_setting_btn.pack(side="left", fill="x", expand=True, padx=(0, 2))

        self.delete_setting_btn = ctk.CTkButton(setting_btn_frame, 
                                              text="선택 설정 삭제", 
                                              command=self.delete_setting,
                                              font=FONT_REGULAR)
        self.delete_setting_btn.pack(side="right", fill="x", expand=True, padx=(2, 0))

        self.assign_btn = ctk.CTkButton(self.bottom_frame, 
                                      text="배정 시작 및 Dooray 전송", 
                                      command=self.assign_and_send, 
                                      font=FONT_TITLE)
        self.assign_btn.pack(fill="x", padx=10, pady=10)

        # 초기화
        self.zone_assign_list = []
        self.name_assign_list = []
        self.refresh_zone_list()
        self.refresh_zone_assign_list()
        self.refresh_name_list()
        self.refresh_name_assign_list()
        self.refresh_setting_list()

        # 설정 불러오기
        load_exclusions()

    def add_zone(self):
        name = self.zone_entry.get().strip()
        count = int(self.zone_count_var.get())
        if name:
            self.zones.append({"name": name, "count": count})
            save_json(ZONES_FILE, self.zones)
            self.zone_entry.delete(0, ctk.END)
            self.refresh_zone_list()
            self.refresh_zone_assign_list()
            self.refresh_name_assign_list()

    def refresh_zone_list(self):
        for widget in self.zone_scroll_frame.winfo_children():
            widget.destroy()
        for idx, z in enumerate(self.zones):
            row = ctk.CTkFrame(self.zone_scroll_frame, fg_color="#ffffff")
            row.pack(fill="x", pady=2, padx=5)
            
            content_frame = ctk.CTkFrame(row, fg_color="#ffffff")
            content_frame.pack(fill="x", expand=True, padx=5, pady=5)
            
            # 레이블 텍스트에 말줄임표 적용
            display_text = truncate_text(z['name'])
            label = ctk.CTkLabel(content_frame, text=f"{display_text} (인원: {z['count']})", 
                               font=FONT_REGULAR, anchor="w")
            label.pack(side="left", fill="x", expand=True)
            
            # 버튼 프레임
            btn_frame = ctk.CTkFrame(content_frame, fg_color="#ffffff")
            btn_frame.pack(side="right")
            
            # -/+ 버튼
            minus_btn = ctk.CTkButton(btn_frame, text="-", width=INPUT_HEIGHT, height=INPUT_HEIGHT,
                                    command=lambda i=idx: self.decrease_zone_count_direct(i), 
                                    font=FONT_REGULAR)
            minus_btn.pack(side="left", padx=2)
            
            plus_btn = ctk.CTkButton(btn_frame, text="+", width=INPUT_HEIGHT, height=INPUT_HEIGHT,
                                   command=lambda i=idx: self.increase_zone_count_direct(i), 
                                   font=FONT_REGULAR)
            plus_btn.pack(side="left", padx=2)
            
            # X 버튼
            delete_btn = ctk.CTkButton(btn_frame, text="✕", width=INPUT_HEIGHT, height=INPUT_HEIGHT,
                                     command=lambda i=idx: self.delete_zone_direct(i), 
                                     font=FONT_REGULAR)
            delete_btn.pack(side="left", padx=(2, 0))

            def on_select(event, current_row=row, zone_idx=idx):
                if self.selected_zone:
                    self.selected_zone.configure(fg_color="#ffffff")
                if self.selected_zone == current_row:
                    self.selected_zone = None
                    current_row.configure(fg_color="#ffffff")
                else:
                    self.selected_zone = current_row
                    current_row.configure(fg_color=SELECT_COLOR)

            def on_double_click(event, zone_idx=idx):
                self.add_zone_to_assign_modern(zone_idx)
                if self.selected_zone:
                    self.selected_zone.configure(fg_color="#ffffff")
                    self.selected_zone = None
            
            # 클릭 효과
            for widget in [row, content_frame, label]:
                widget.bind('<Button-1>', on_select)
                widget.bind('<Double-Button-1>', on_double_click)
                widget.bind('<Enter>', lambda e, r=row: e.widget.configure(fg_color=HOVER_COLOR) 
                          if r != self.selected_zone else None)
                widget.bind('<Leave>', lambda e, r=row: e.widget.configure(fg_color="#ffffff") 
                          if r != self.selected_zone else e.widget.configure(fg_color=SELECT_COLOR))

    def add_zone_to_assign_modern(self, idx):
        zone = self.zones[idx]
        if zone not in self.zone_assign_list:
            self.zone_assign_list.append(zone.copy())
            self.refresh_zone_assign_list()

    def add_name(self):
        name = self.name_entry.get().strip()
        if name and name not in self.names:
            self.names.append(name)
            save_json(NAMES_FILE, self.names)
            self.name_entry.delete(0, ctk.END)
            self.refresh_name_list()
            self.refresh_name_assign_list()

    def refresh_name_list(self):
        for widget in self.name_scroll_frame.winfo_children():
            widget.destroy()
        for idx, n in enumerate(self.names):
            row = ctk.CTkFrame(self.name_scroll_frame, fg_color="#ffffff")
            row.pack(fill="x", pady=2, padx=5)
            
            content_frame = ctk.CTkFrame(row, fg_color="#ffffff")
            content_frame.pack(fill="x", expand=True, padx=5, pady=5)
            
            # 레이블 텍스트에 말줄임표 적용
            display_text = truncate_text(n)
            label = ctk.CTkLabel(content_frame, text=display_text, font=FONT_REGULAR, anchor="w")
            label.pack(side="left", fill="x", expand=True)
            
            delete_btn = ctk.CTkButton(content_frame, text="✕", width=INPUT_HEIGHT, height=INPUT_HEIGHT,
                                     command=lambda i=idx: self.delete_name_direct(i), 
                                     font=FONT_REGULAR)
            delete_btn.pack(side="right")

            def on_select(event, current_row=row, name_idx=idx):
                if self.selected_name:
                    self.selected_name.configure(fg_color="#ffffff")
                if self.selected_name == current_row:
                    self.selected_name = None
                    current_row.configure(fg_color="#ffffff")
                else:
                    self.selected_name = current_row
                    current_row.configure(fg_color=SELECT_COLOR)

            def on_double_click(event, name_idx=idx):
                self.add_name_to_assign_modern(name_idx)
                if self.selected_name:
                    self.selected_name.configure(fg_color="#ffffff")
                    self.selected_name = None
            
            # 클릭 효과
            for widget in [row, content_frame, label]:
                widget.bind('<Button-1>', on_select)
                widget.bind('<Double-Button-1>', on_double_click)
                widget.bind('<Enter>', lambda e, r=row: e.widget.configure(fg_color=HOVER_COLOR) 
                          if r != self.selected_name else None)
                widget.bind('<Leave>', lambda e, r=row: e.widget.configure(fg_color="#ffffff") 
                          if r != self.selected_name else e.widget.configure(fg_color=SELECT_COLOR))

    def add_name_to_assign_modern(self, idx):
        name = self.names[idx]
        if name not in self.name_assign_list:
            self.name_assign_list.append(name)
            self.refresh_name_assign_list()

    def delete_name_direct(self, idx):
        del self.names[idx]
        save_json(NAMES_FILE, self.names)
        self.refresh_name_list()

    def save_setting(self):
        name = self.setting_name_entry.get().strip()
        if not name:
            messagebox.showerror("오류", "설정 이름을 입력하세요.")
            return
        
        # .json 확장자 추가
        if not name.endswith('.json'):
            name += '.json'
        
        setting = {
            "zones": self.zones,
            "names": self.names,
            "webhook": self.webhook_entry.get().strip()
        }
        
        try:
            save_json(os.path.join(SETTINGS_DIR, name), setting)
            self.refresh_setting_list()
            messagebox.showinfo("성공", "설정이 저장되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"설정 저장 중 오류가 발생했습니다: {str(e)}")

    def refresh_setting_list(self):
        for widget in self.setting_scroll_frame.winfo_children():
            widget.destroy()
        
        files = [f for f in os.listdir(SETTINGS_DIR) if f.endswith('.json')]
        for idx, fname in enumerate(sorted(files)):
            row = ctk.CTkFrame(self.setting_scroll_frame, fg_color="#ffffff")
            row.pack(fill="x", pady=2, padx=5)
            
            content_frame = ctk.CTkFrame(row, fg_color="#ffffff")
            content_frame.pack(fill="x", expand=True, padx=5, pady=5)
            
            # 파일명에서 .json 제거하고 말줄임표 적용
            display_name = fname[:-5] if fname.endswith('.json') else fname
            display_text = truncate_text(display_name)
            label = ctk.CTkLabel(content_frame, text=display_text, 
                               font=FONT_REGULAR, anchor="w")
            label.pack(side="left", fill="x", expand=True)

            def on_select(event, current_row=row, file_name=fname):
                if self.selected_setting:
                    self.selected_setting.configure(fg_color="#ffffff")
                if self.selected_setting == current_row:
                    self.selected_setting = None
                    self.selected_setting_file = None
                    current_row.configure(fg_color="#ffffff")
                else:
                    self.selected_setting = current_row
                    self.selected_setting_file = file_name
                    current_row.configure(fg_color=SELECT_COLOR)
            
            # 클릭 효과
            for widget in [row, content_frame, label]:
                widget.bind('<Button-1>', on_select)
                widget.bind('<Enter>', lambda e, r=row: e.widget.configure(fg_color=HOVER_COLOR) 
                          if r != self.selected_setting else None)
                widget.bind('<Leave>', lambda e, r=row: e.widget.configure(fg_color="#ffffff") 
                          if r != self.selected_setting else e.widget.configure(fg_color=SELECT_COLOR))

            # 이전에 선택된 설정이면 선택 상태로 표시
            if fname == self.selected_setting_file:
                row.configure(fg_color=SELECT_COLOR)
                self.selected_setting = row

    def load_setting(self):
        if not self.selected_setting_file:
            messagebox.showwarning("알림", "불러올 설정을 선택하세요.")
            return
        
        setting_path = os.path.join(SETTINGS_DIR, self.selected_setting_file)
        if os.path.exists(setting_path):
            try:
                setting = load_json(setting_path, default={})
                self.zones = setting.get("zones", [])
                self.names = setting.get("names", [])
                self.webhook_entry.delete(0, ctk.END)
                self.webhook_entry.insert(0, setting.get("webhook", ""))
                
                # 기존 배정 목록 초기화
                self.zone_assign_list = []
                self.name_assign_list = []
                
                # 목록 새로고침
                self.refresh_zone_list()
                self.refresh_name_list()
                self.refresh_zone_assign_list()
                self.refresh_name_assign_list()
                
                messagebox.showinfo("성공", "설정을 불러왔습니다.")
            except Exception as e:
                messagebox.showerror("오류", f"설정을 불러오는 중 오류가 발생했습니다: {str(e)}")
        else:
            messagebox.showerror("오류", "설정 파일을 찾을 수 없습니다.")

    def delete_setting(self):
        if not self.selected_setting_file:
            messagebox.showwarning("알림", "삭제할 설정을 선택하세요.")
            return
        
        if messagebox.askyesno("확인", "선택한 설정을 삭제하시겠습니까?"):
            setting_path = os.path.join(SETTINGS_DIR, self.selected_setting_file)
            if os.path.exists(setting_path):
                try:
                    os.remove(setting_path)
                    self.selected_setting = None
                    self.selected_setting_file = None
                    self.refresh_setting_list()
                    messagebox.showinfo("성공", "설정이 삭제되었습니다.")
                except Exception as e:
                    messagebox.showerror("오류", f"설정 삭제 중 오류가 발생했습니다: {str(e)}")
            else:
                messagebox.showerror("오류", "설정 파일을 찾을 수 없습니다.")

    def toggle_zone_exclusion(self, event=None):
        """특정 담당자를 특정 구역에서 제외"""
        dialog = ExclusionDialog(self, self.names, self.zones, mode="zone")
        self.wait_window(dialog)
        
        if dialog.result:
            name, zones, should_save = dialog.result
            if name not in EXCLUSION_SETTINGS["zone_exclusions"]:
                EXCLUSION_SETTINGS["zone_exclusions"][name] = []
            
            for zone in zones:
                if zone in EXCLUSION_SETTINGS["zone_exclusions"][name]:
                    EXCLUSION_SETTINGS["zone_exclusions"][name].remove(zone)
                else:
                    EXCLUSION_SETTINGS["zone_exclusions"][name].append(zone)
            
            if zones:
                if EXCLUSION_SETTINGS["zone_exclusions"][name]:
                    messagebox.showinfo("알림", f"{name}의 제외 구역이 설정되었습니다.")
                else:
                    messagebox.showinfo("알림", f"{name}의 모든 제외 설정이 해제되었습니다.")
                    
            if should_save:
                save_exclusions()

    def toggle_pair_exclusion(self, event=None):
        """특정 담당자들끼리 매칭 제한"""
        dialog = ExclusionDialog(self, self.names, self.zones, mode="pair")
        self.wait_window(dialog)
        
        if dialog.result:
            name1, excluded_names, should_save = dialog.result
            
            if name1 not in EXCLUSION_SETTINGS["pair_exclusions"]:
                EXCLUSION_SETTINGS["pair_exclusions"][name1] = []
                
            # 기존 설정과 비교하여 추가/제거
            for name2 in excluded_names:
                if name2 in EXCLUSION_SETTINGS["pair_exclusions"][name1]:
                    EXCLUSION_SETTINGS["pair_exclusions"][name1].remove(name2)
                else:
                    EXCLUSION_SETTINGS["pair_exclusions"][name1].append(name2)
            
            if not EXCLUSION_SETTINGS["pair_exclusions"][name1]:
                del EXCLUSION_SETTINGS["pair_exclusions"][name1]
                messagebox.showinfo("알림", f"{name1}의 모든 매칭 제한이 해제되었습니다.")
            else:
                excluded_list = ", ".join(EXCLUSION_SETTINGS["pair_exclusions"][name1])
                messagebox.showinfo("알림", f"{name1}와(과) {excluded_list}의 매칭이 제한되었습니다.")
            
            if should_save:
                save_exclusions()

    def show_current_exclusions(self, event=None):
        """현재 설정된 제한사항 확인"""
        message = "현재 설정된 제한사항:\n\n"
        
        if EXCLUSION_SETTINGS["zone_exclusions"]:
            message += "구역 배정 제외:\n"
            for name, zones in EXCLUSION_SETTINGS["zone_exclusions"].items():
                if zones:
                    message += f"- {name}: {', '.join(zones)}\n"
        
        if EXCLUSION_SETTINGS["pair_exclusions"]:
            message += "\n매칭 제한 페어:\n"
            for name, excluded_names in EXCLUSION_SETTINGS["pair_exclusions"].items():
                if excluded_names:
                    excluded_list = ", ".join(excluded_names)
                    message += f"- {name} ↔ {excluded_list}\n"
                
        if not EXCLUSION_SETTINGS["zone_exclusions"] and not EXCLUSION_SETTINGS["pair_exclusions"]:
            message += "설정된 제한사항이 없습니다."
            
        messagebox.showinfo("제한사항 목록", message)

    def assign_and_send(self):
        zones = self.zone_assign_list.copy() if self.zone_assign_list else self.zones.copy()
        names = self.name_assign_list.copy() if self.name_assign_list else self.names.copy()
        webhook_url = self.webhook_entry.get().strip()
        total_needed = sum(int(z['count']) for z in zones)
        
        if not zones or not names or not webhook_url:
            messagebox.showerror("오류", "구역, 담당자, 웹훅을 모두 입력/선택하세요.")
            return
        if total_needed != len(names):
            if total_needed > len(names):
                messagebox.showerror("오류", f"담당자가 {total_needed - len(names)}명 부족합니다.")
            else:
                messagebox.showerror("오류", f"담당자가 {len(names) - total_needed}명 초과입니다.")
            return

        # 배정 로직
        assignments = {}
        available_names = names.copy()
        max_attempts = 100  # 최대 시도 횟수

        for _ in range(max_attempts):
            assignments.clear()
            random.shuffle(available_names)
            name_idx = 0
            valid_assignment = True

            for zone in zones:
                zone_name = zone["name"]
                count = int(zone["count"])
                assigned_names = []

                for _ in range(count):
                    if name_idx >= len(available_names):
                        valid_assignment = False
                        break

                    current_name = available_names[name_idx]
                    
                    # 구역 제외 검사
                    if (current_name in EXCLUSION_SETTINGS["zone_exclusions"] and 
                        zone_name in EXCLUSION_SETTINGS["zone_exclusions"][current_name]):
                        valid_assignment = False
                        break

                    # 매칭 제한 검사
                    excluded = False
                    for assigned_name in assigned_names:
                        if (assigned_name in EXCLUSION_SETTINGS["pair_exclusions"] and 
                            current_name in EXCLUSION_SETTINGS["pair_exclusions"][assigned_name]) or \
                           (current_name in EXCLUSION_SETTINGS["pair_exclusions"] and 
                            assigned_name in EXCLUSION_SETTINGS["pair_exclusions"][current_name]):
                            excluded = True
                            break

                    if excluded:
                        valid_assignment = False
                        break

                    assigned_names.append(current_name)
                    name_idx += 1

                if not valid_assignment:
                    break

                assignments[zone_name] = assigned_names

            if valid_assignment:
                break

        if not valid_assignment:
            messagebox.showerror("오류", "설정된 제한사항으로 인해 배정이 불가능합니다.")
            return

        # 메시지 생성 및 전송
        message = "🧹 **W-DAY 청소구역 배정 결과**\n\n"
        for zone_name, assigned_names in assignments.items():
            message += f"⭐ {zone_name}: {', '.join(assigned_names)}\n"
        message += "\n모두 수고해주세요! 🙏"

        payload = {
            "text": message
        }

        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            messagebox.showinfo("성공", "배정 결과가 전송되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"전송 중 오류가 발생했습니다: {str(e)}")

    def refresh_zone_assign_list(self):
        for widget in self.zone_assign_scroll_frame.winfo_children():
            widget.destroy()
        for idx, z in enumerate(self.zone_assign_list):
            row = ctk.CTkFrame(self.zone_assign_scroll_frame, fg_color="#ffffff")
            row.pack(fill="x", pady=2, padx=5)
            
            content_frame = ctk.CTkFrame(row, fg_color="#ffffff")
            content_frame.pack(fill="x", expand=True, padx=5, pady=5)
            
            # 레이블 텍스트에 말줄임표 적용
            display_text = truncate_text(z['name'])
            label = ctk.CTkLabel(content_frame, text=f"{display_text} (인원: {z['count']})", 
                               font=FONT_REGULAR, anchor="w")
            label.pack(side="left", fill="x", expand=True)
            
            btn_frame = ctk.CTkFrame(content_frame, fg_color="#ffffff")
            btn_frame.pack(side="right")
            
            minus_btn = ctk.CTkButton(btn_frame, text="-", width=INPUT_HEIGHT, height=INPUT_HEIGHT,
                                    command=lambda i=idx: self.decrease_zone_assign_count(i), 
                                    font=FONT_REGULAR)
            minus_btn.pack(side="left", padx=2)
            
            plus_btn = ctk.CTkButton(btn_frame, text="+", width=INPUT_HEIGHT, height=INPUT_HEIGHT,
                                   command=lambda i=idx: self.increase_zone_assign_count(i), 
                                   font=FONT_REGULAR)
            plus_btn.pack(side="left", padx=2)
            
            delete_btn = ctk.CTkButton(btn_frame, text="✕", width=INPUT_HEIGHT, height=INPUT_HEIGHT,
                                     command=lambda i=idx: self.delete_assign_zone(i), 
                                     font=FONT_REGULAR)
            delete_btn.pack(side="left", padx=(2, 0))

            def on_select(event, current_row=row, assign_idx=idx):
                if self.selected_assign_zone:
                    self.selected_assign_zone.configure(fg_color="#ffffff")
                if self.selected_assign_zone == current_row:
                    self.selected_assign_zone = None
                    current_row.configure(fg_color="#ffffff")
                else:
                    self.selected_assign_zone = current_row
                    current_row.configure(fg_color=SELECT_COLOR)
            
            # 클릭 효과
            for widget in [row, content_frame, label]:
                widget.bind('<Button-1>', on_select)
                widget.bind('<Enter>', lambda e, r=row: e.widget.configure(fg_color=HOVER_COLOR) 
                          if r != self.selected_assign_zone else None)
                widget.bind('<Leave>', lambda e, r=row: e.widget.configure(fg_color="#ffffff") 
                          if r != self.selected_assign_zone else e.widget.configure(fg_color=SELECT_COLOR))

    def increase_zone_assign_count(self, idx):
        self.zone_assign_list[idx]['count'] += 1
        self.refresh_zone_assign_list()

    def decrease_zone_assign_count(self, idx):
        if self.zone_assign_list[idx]['count'] > 1:
            self.zone_assign_list[idx]['count'] -= 1
            self.refresh_zone_assign_list()

    def delete_assign_zone(self, idx):
        del self.zone_assign_list[idx]
        self.refresh_zone_assign_list()

    def delete_assign_name(self, idx):
        if 0 <= idx < len(self.name_assign_list):
            del self.name_assign_list[idx]
            self.refresh_name_assign_list()

    def increase_zone_count_direct(self, idx):
        self.zones[idx]['count'] += 1
        save_json(ZONES_FILE, self.zones)
        self.refresh_zone_list()

    def decrease_zone_count_direct(self, idx):
        if self.zones[idx]['count'] > 1:
            self.zones[idx]['count'] -= 1
            save_json(ZONES_FILE, self.zones)
            self.refresh_zone_list()

    def delete_zone_direct(self, idx):
        del self.zones[idx]
        save_json(ZONES_FILE, self.zones)
        self.refresh_zone_list()

    def refresh_name_assign_list(self):
        for widget in self.name_assign_scroll_frame.winfo_children():
            widget.destroy()
        for idx, name in enumerate(self.name_assign_list):
            row = ctk.CTkFrame(self.name_assign_scroll_frame, fg_color="#ffffff")
            row.pack(fill="x", pady=2, padx=5)
            
            content_frame = ctk.CTkFrame(row, fg_color="#ffffff")
            content_frame.pack(fill="x", expand=True, padx=5, pady=5)
            
            # 레이블 텍스트에 말줄임표 적용
            display_text = truncate_text(name)
            label = ctk.CTkLabel(content_frame, text=display_text, font=FONT_REGULAR, anchor="w")
            label.pack(side="left", fill="x", expand=True)
            
            delete_btn = ctk.CTkButton(content_frame, text="✕", width=INPUT_HEIGHT, height=INPUT_HEIGHT,
                                     command=lambda i=idx: self.delete_assign_name(i), 
                                     font=FONT_REGULAR)
            delete_btn.pack(side="right")

            def on_select(event, current_row=row, name_idx=idx):
                if self.selected_assign_name:
                    self.selected_assign_name.configure(fg_color="#ffffff")
                if self.selected_assign_name == current_row:
                    self.selected_assign_name = None
                    current_row.configure(fg_color="#ffffff")
                else:
                    self.selected_assign_name = current_row
                    current_row.configure(fg_color=SELECT_COLOR)
            
            # 클릭 효과
            for widget in [row, content_frame, label]:
                widget.bind('<Button-1>', on_select)
                widget.bind('<Enter>', lambda e, r=row: e.widget.configure(fg_color=HOVER_COLOR) 
                          if r != self.selected_assign_name else None)
                widget.bind('<Leave>', lambda e, r=row: e.widget.configure(fg_color="#ffffff") 
                          if r != self.selected_assign_name else e.widget.configure(fg_color=SELECT_COLOR))

    def highlight_row(self, widget):
        # 클릭된 행의 배경색 변경
        widget.configure(fg_color=SELECT_COLOR)
        widget.selected = True  # 선택 상태 변경

    def assign_all_zones(self):
        """모든 구역을 배정 목록에 추가"""
        self.zone_assign_list = []
        for zone in self.zones:
            if zone not in self.zone_assign_list:
                self.zone_assign_list.append(zone.copy())
        self.refresh_zone_assign_list()

    def assign_all_names(self):
        """모든 담당자를 배정 목록에 추가"""
        self.name_assign_list = []
        for name in self.names:
            if name not in self.name_assign_list:
                self.name_assign_list.append(name)
        self.refresh_name_assign_list()

if __name__ == "__main__":
    app = CleaningAssignApp()
    app.mainloop()
