# -*- coding: utf-8 -*-
"""
에네레기파 - 캡스톤디자인2 최종발표 PPT 생성 스크립트
팀명: 에네레기파 | 조장: 임단군 | 조원: 정예민, 안유경
지도교수: 김순찬 교수님 | 날짜: 2026.05.29
트랙 B 자유주제 No.13
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

C_NAVY   = RGBColor(0x1A, 0x2E, 0x4A)
C_BLUE   = RGBColor(0x1E, 0x6F, 0xB5)
C_LBLUE  = RGBColor(0xD6, 0xE8, 0xF7)
C_RED    = RGBColor(0xE8, 0x3A, 0x3A)
C_ORANGE = RGBColor(0xFF, 0x70, 0x00)
C_GREEN  = RGBColor(0x28, 0xA7, 0x45)
C_WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
C_LGRAY  = RGBColor(0xF5, 0xF7, 0xFA)
C_GRAY   = RGBColor(0x6C, 0x75, 0x7D)
C_DARK   = RGBColor(0x21, 0x25, 0x29)
C_YELLOW = RGBColor(0xFF, 0xD7, 0x00)
C_TEAL   = RGBColor(0x17, 0xA2, 0xB8)
C_PURPLE = RGBColor(0x6F, 0x42, 0xC1)

SLIDE_W = 13.33
SLIDE_H = 7.5

def R(v):
    return Inches(v)

def add_rect(slide, l, t, w, h, fill=None, line=None, line_width=None):
    shape = slide.shapes.add_shape(1, R(l), R(t), R(w), R(h))
    shape.line.fill.background()
    if fill is not None:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line is not None:
        shape.line.color.rgb = line
        if line_width:
            shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, l, t, w, h, size=14, bold=False, color=None,
             align=PP_ALIGN.LEFT, italic=False, wrap=True, font_name="맑은 고딕"):
    txBox = slide.shapes.add_textbox(R(l), R(t), R(w), R(h))
    txBox.word_wrap = wrap
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color
    return txBox

def hdr(slide, title, subtitle=None):
    add_rect(slide, 0, 0, SLIDE_W, 0.08, fill=C_ORANGE)
    add_rect(slide, 0, 0.08, SLIDE_W, 1.04, fill=C_NAVY)
    add_text(slide, title, 0.25, 0.12, 10.0, 0.65, size=24, bold=True, color=C_WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_text(slide, subtitle, 0.25, 0.72, 10.0, 0.38, size=13, color=C_LBLUE, align=PP_ALIGN.LEFT)
    add_rect(slide, 0, 7.15, SLIDE_W, 0.35, fill=C_NAVY)
    add_text(slide, "에네레기파 | 지도교수: 김순찬 교수님", 0.2, 7.18, 7.0, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.LEFT)
    add_text(slide, "트랙 B 자유주제 No.13  |  2026.05.29", 6.5, 7.18, 6.5, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.RIGHT)

def badge(slide, text, l, t, w, h, bg=C_RED, fg=C_WHITE, size=12):
    add_rect(slide, l, t, w, h, fill=bg)
    add_text(slide, text, l, t, w, h, size=size, bold=True, color=fg, align=PP_ALIGN.CENTER)

def add_table(slide, data, l, t, w, h, header_bg=C_NAVY, header_fg=C_WHITE, row_alt=C_LGRAY, font_size=10):
    rows = len(data)
    cols = len(data[0])
    table = slide.shapes.add_table(rows, cols, R(l), R(t), R(w), R(h)).table
    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = str(data[r][c])
            tf = cell.text_frame
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            if tf.paragraphs[0].runs:
                run = tf.paragraphs[0].runs[0]
            else:
                run = tf.paragraphs[0].add_run()
            run.text = str(data[r][c])
            run.font.name = "맑은 고딕"
            run.font.size = Pt(font_size)
            if r == 0:
                run.font.bold = True
                run.font.color.rgb = header_fg
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_bg
            else:
                run.font.bold = False
                run.font.color.rgb = C_DARK
                if r % 2 == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = row_alt
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = C_WHITE
    return table

prs = Presentation()
prs.slide_width  = R(SLIDE_W)
prs.slide_height = R(SLIDE_H)
blank_layout = prs.slide_layouts[6]
# ============================================================
# 슬라이드 01 - 표지
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_NAVY)
add_rect(slide, 0, 0, SLIDE_W, 0.12, fill=C_ORANGE)
badge(slide, "트랙 B  자유주제  No.13", 0.3, 0.25, 3.2, 0.38, bg=C_ORANGE, fg=C_WHITE, size=12)
add_text(slide, "팀명: 에네레기파", 0.3, 0.75, 6.0, 0.45, size=15, color=C_LBLUE, align=PP_ALIGN.LEFT)
add_text(slide, "화성시 불법주정차 단속정보 분석을 통한", 0.3, 1.28, 12.5, 0.65, size=26, bold=True, color=C_WHITE, align=PP_ALIGN.LEFT)
add_text(slide, "통행불편 민원 최소화 정책 수립 지원 시스템", 0.3, 1.88, 12.5, 0.65, size=26, bold=True, color=C_YELLOW, align=PP_ALIGN.LEFT)
add_rect(slide, 0.3, 2.62, 12.5, 0.04, fill=C_ORANGE)
add_text(slide, "조장: 임단군   |   조원: 정예민, 안유경", 0.3, 2.75, 8.0, 0.4, size=14, color=C_LBLUE, align=PP_ALIGN.LEFT)
add_text(slide, "지도교수: 김순찬 교수님   |   2026.05.29", 0.3, 3.12, 8.0, 0.4, size=14, color=C_LBLUE, align=PP_ALIGN.LEFT)
kpi_items = [("217,682건", "2023년\n실단속건수"), ("35개", "분석 대상\n법정동"), ("MAE 1,451건\n(6.7%)", "앙상블\n최고 성능")]
kpi_colors = [C_BLUE, C_TEAL, C_GREEN]
kpi_x = [0.3, 4.7, 9.1]
for i, (val, lbl) in enumerate(kpi_items):
    bx = kpi_x[i]
    add_rect(slide, bx, 3.75, 3.9, 1.6, fill=kpi_colors[i])
    add_text(slide, val, bx+0.1, 3.85, 3.7, 0.85, size=22, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, lbl, bx+0.1, 4.65, 3.7, 0.6, size=11, color=C_LBLUE, align=PP_ALIGN.CENTER)
add_rect(slide, 0, 7.15, SLIDE_W, 0.35, fill=RGBColor(0x0D,0x1A,0x2E))
add_text(slide, "에네레기파 | 지도교수: 김순찬 교수님", 0.2, 7.18, 7.0, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.LEFT)
add_text(slide, "트랙 B 자유주제 No.13  |  2026.05.29", 6.5, 7.18, 6.5, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.RIGHT)

# ============================================================
# 슬라이드 02 - 문제 정의
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "문제 정의", "왜 지금 화성시 불법주정차 분석이 필요한가?")
add_rect(slide, 0.2, 1.2, 5.6, 0.32, fill=C_NAVY)
add_text(slide, "연도별 단속 추이 (2021~2025)", 0.25, 1.22, 5.5, 0.28, size=11, bold=True, color=C_WHITE)
trend_data = [
    ["연도","단속건수","전년대비","비고"],
    ["2021년","211,404건","기준",""],
    ["2022년","215,005건","▲ 1.7%",""],
    ["2023년","219,152건","▲ 1.9%",""],
    ["2024년","233,993건","▲ 6.8%","★ 역대 최다"],
    ["2025년 1~4월","79,279건","증가세 지속","추정연간 240,000+"],
]
add_table(slide, trend_data, 0.2, 1.52, 5.6, 2.0, font_size=9)
add_rect(slide, 0.2, 3.62, 5.6, 0.32, fill=C_RED)
add_text(slide, "3대 핵심 문제", 0.25, 3.64, 5.5, 0.28, size=11, bold=True, color=C_WHITE)
problems = [
    ("①","반응형 단속","민원 접수 후 출동 → 골든타임 놓침, 선제 예방 불가"),
    ("②","인력 배치 비효율","피크 시간·지역 데이터 없이 균등 배치 → 자원 낭비"),
    ("③","CCTV 설치 기준 없음","CCTV 공백 지역 vs 민원 다발지역 불일치 심각"),
]
for i, (num, title, desc) in enumerate(problems):
    yt = 4.02 + i*0.82
    add_rect(slide, 0.25, yt, 0.42, 0.62, fill=C_RED)
    add_text(slide, num, 0.25, yt, 0.42, 0.62, size=14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide, 0.72, yt, 4.95, 0.62, fill=C_WHITE, line=C_BLUE, line_width=0.5)
    add_text(slide, title, 0.78, yt+0.02, 2.0, 0.28, size=10, bold=True, color=C_NAVY)
    add_text(slide, desc, 0.78, yt+0.28, 4.8, 0.32, size=8.5, color=C_DARK)
add_rect(slide, 6.0, 1.2, 7.1, 0.32, fill=C_PURPLE)
add_text(slide, "사용자 퍼소나 (이해관계자 관점)", 6.05, 1.22, 7.0, 0.28, size=11, bold=True, color=C_WHITE)
personas = [
    ("직장인 박씨 (34세)","동탄2신도시 거주",
     '"출근길에 불법주정차로 골목이 막혀 지각. 민원 넣어도 출동이 느리다."',
     "→ 선제적 단속 강화, 피크타임 인력 집중 필요"),
    ("학부모 김씨 (38세)","향남읍 거주",
     '"아이 등교길 횡단보도 앞 불법주차 반복. 같은 곳에 신고만 반복한다."',
     "→ 고위험 지역(향남읍 6.87점) CCTV 및 단속 강화 필요"),
]
for i, (name, loc, quote, action) in enumerate(personas):
    yt = 1.62 + i*2.6
    add_rect(slide, 6.0, yt, 7.1, 2.45, fill=C_WHITE, line=C_BLUE, line_width=0.5)
    add_rect(slide, 6.0, yt, 7.1, 0.38, fill=C_BLUE)
    add_text(slide, name+"  |  "+loc, 6.08, yt+0.04, 6.9, 0.3, size=11, bold=True, color=C_WHITE)
    add_text(slide, quote, 6.08, yt+0.46, 6.85, 0.75, size=9, color=C_DARK, italic=True)
    add_rect(slide, 6.08, yt+1.28, 6.9, 0.38, fill=C_LBLUE)
    add_text(slide, action, 6.15, yt+1.3, 6.8, 0.35, size=9, bold=True, color=C_NAVY)

# ============================================================
# 슬라이드 03 - 솔루션 & 대시보드 구성
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "솔루션 & 대시보드 구성", "Streamlit 기반 5탭 통합 분석 시스템")
add_rect(slide, 0.2, 1.2, 12.9, 0.32, fill=C_NAVY)
add_text(slide, "데이터 처리 흐름도", 0.3, 1.22, 12.5, 0.28, size=11, bold=True, color=C_WHITE)
flow_steps = [
    ("입력","화성시 단속\n데이터 xlsx\n(2021~2025)",C_BLUE),
    ("전처리","법정동 추출\n위반유형 분류\n결측/오류 제거",C_TEAL),
    ("분석","위험도 산출\nCCTV 공백\n시간대 패턴",C_GREEN),
    ("예측","Prophet+\nSARIMA\n앙상블 모델",C_PURPLE),
    ("출력","정책 권고\n시각화\n대시보드",C_ORANGE),
]
for i, (title, desc, color) in enumerate(flow_steps):
    bx = 0.2+i*2.56
    add_rect(slide, bx, 1.6, 2.3, 1.5, fill=color)
    add_text(slide, title, bx+0.05, 1.65, 2.2, 0.38, size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, desc, bx+0.05, 2.05, 2.2, 1.0, size=9, color=C_WHITE, align=PP_ALIGN.CENTER)
    if i < 4:
        add_text(slide, "▶", bx+2.3, 1.95, 0.25, 0.7, size=16, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)
add_rect(slide, 0.2, 3.25, 12.9, 0.32, fill=C_NAVY)
add_text(slide, "Streamlit 5탭 대시보드 주요 기능", 0.3, 3.27, 12.5, 0.28, size=11, bold=True, color=C_WHITE)
tabs = [
    ("탭 1\n위험도 지도","법정동별 재보정위험도\n시각화 (Folium)\n고위험 지역 하이라이트",C_RED),
    ("탭 2\n히트맵","시간대×요일\n위반건수 히트맵\n피크 패턴 분석",C_ORANGE),
    ("탭 3\n위반유형 대책","위반유형별 분석\n맞춤형 단속 전략\n정책 우선순위",C_GREEN),
    ("탭 4\n전체 현황","연도별 추이\n지역별 비교\nCCTV 공백 분석",C_BLUE),
    ("탭 5\n예측&정책권고","2026년 6~11월\n월별 예측 + 인력\n수요 정책 권고",C_PURPLE),
]
for i, (title, desc, color) in enumerate(tabs):
    bx = 0.2+i*2.56
    add_rect(slide, bx, 3.62, 2.3, 0.55, fill=color)
    add_text(slide, title, bx+0.05, 3.65, 2.2, 0.49, size=9, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide, bx, 4.17, 2.3, 1.55, fill=C_WHITE, line=color, line_width=1.0)
    add_text(slide, desc, bx+0.05, 4.2, 2.2, 1.45, size=8.5, color=C_DARK, align=PP_ALIGN.CENTER)
add_rect(slide, 0.2, 5.85, 12.9, 0.32, fill=C_DARK)
add_text(slide, "기술 스택:  Python 3.x  |  Streamlit  |  Prophet  |  statsmodels (SARIMA)  |  Folium  |  Pandas  |  Matplotlib  |  Plotly", 0.3, 5.87, 12.5, 0.28, size=9, color=C_YELLOW)
# ============================================================
# 슬라이드 04 - 데모 ① 작동성
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "데모 ① — 작동성", "입력 → 처리 → 출력 파이프라인 · AI 앙상블 모델 설명")

# 상단 파이프라인 (입력→처리→출력)
add_rect(slide, 0.2, 1.2, 12.9, 0.32, fill=C_NAVY)
add_text(slide, "시스템 작동 흐름  (입력 → 처리 → 출력)", 0.3, 1.22, 12.5, 0.28, size=11, bold=True, color=C_WHITE)
pipeline = [
    ("① 입력\n데이터",
     "화성시 불법주정차\n단속현황 xlsx\n(2021~2025)\n약 25만 건 원천",
     C_BLUE, ""),
    ("② 전처리\nPython",
     "행정동 추출 (정규식)\n위반유형 5종 분류\n결측·오타 정제\n법정동 미추출 1.7%↓",
     C_TEAL, "→"),
    ("③ 지표 산출\nPandas",
     "재보정위험도 계산\nCCTV 공백지수 산출\n시간대 피크 집계\n5개 CSV 출력",
     C_GREEN, "→"),
    ("④ AI 예측\nProphet+SARIMA",
     "Prophet 계절 모델\nSARIMA 자기회귀\nMAE 역수 앙상블\nMAE 1,451건 (6.7%)",
     C_PURPLE, "→"),
    ("⑤ 출력\nStreamlit",
     "Folium 인터랙티브 지도\n히트맵·차트 시각화\n3-Tier 정책 권고문\n자동 생성 출력",
     C_ORANGE, "→"),
]
for i, (title, desc, color, arrow) in enumerate(pipeline):
    bx = 0.2 + i * 2.57
    if arrow:
        add_text(slide, arrow, bx - 0.22, 1.92, 0.22, 0.6, size=14, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)
    add_rect(slide, bx, 1.6, 2.32, 0.46, fill=color)
    add_text(slide, title, bx+0.05, 1.63, 2.22, 0.4, size=10, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide, bx, 2.06, 2.32, 1.85, fill=C_WHITE, line=color, line_width=1.2)
    add_text(slide, desc, bx+0.08, 2.1, 2.18, 1.75, size=8.5, color=C_DARK, align=PP_ALIGN.CENTER)

# 하단 AI 앙상블 모델 박스
add_rect(slide, 0.2, 4.05, 12.9, 0.32, fill=C_PURPLE)
add_text(slide, "AI 핵심: Prophet + SARIMA 앙상블 — 왜 두 모델을 합치는가?", 0.3, 4.08, 12.5, 0.26, size=11, bold=True, color=C_WHITE)

model_boxes = [
    ("Prophet (Meta)",
     "• 연간 계절성 자동 감지\n• 트렌드 변화점 탐지\n• 장기 패턴에 강점\n• MAE 1,594건 (7.4%)",
     C_BLUE),
    ("SARIMA (통계)",
     "• 자기회귀 — 직전월 의존성 포착\n• 12개월 계절 주기 모델링\n• 단기 변동에 강점\n• MAE 1,571건 (7.4%)",
     C_TEAL),
    ("앙상블 (합산)",
     "• MAE 역수 가중: 성능 좋은 모델에\n  더 높은 가중치 자동 부여\n• 두 모델 상호 보완\n• MAE 1,451건 (6.7%) ★최고",
     C_GREEN),
    ("검증 방식",
     "• Out-of-sample 검증\n  학습: 2021~2024 (48개월)\n  검증: 2025.01~04 (4개월)\n• 과적합 없음 확인",
     C_ORANGE),
]
for i, (title, desc, color) in enumerate(model_boxes):
    bx = 0.2 + i * 3.22
    add_rect(slide, bx, 4.45, 3.05, 0.35, fill=color)
    add_text(slide, title, bx+0.08, 4.48, 2.9, 0.28, size=10, bold=True, color=C_WHITE)
    add_rect(slide, bx, 4.8, 3.05, 1.55, fill=C_WHITE, line=color, line_width=1.0)
    add_text(slide, desc, bx+0.1, 4.85, 2.9, 1.44, size=8.5, color=C_DARK)

add_rect(slide, 0, 7.15, SLIDE_W, 0.35, fill=RGBColor(0x0D,0x1A,0x2E))
add_text(slide, "에네레기파 | 지도교수: 김순찬 교수님", 0.2, 7.18, 7.0, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.LEFT)
add_text(slide, "트랙 B 자유주제 No.13  |  2026.05.29", 6.5, 7.18, 6.5, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.RIGHT)

# ============================================================
# 슬라이드 05 - 데모 ② 사용성
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "데모 ② — 사용성", "첫 진입 → 핵심 가치 경로 · UI/UX · 디자인 일관성")

# 상단: 사용자 여정 흐름
add_rect(slide, 0.2, 1.2, 12.9, 0.32, fill=C_NAVY)
add_text(slide, "사용자 핵심 경로  (처음 접속 → 정책 결정까지)", 0.3, 1.22, 12.5, 0.28, size=11, bold=True, color=C_WHITE)

journey = [
    ("진입", "대시보드 접속\n사이드바에서\n연도·법정동\n필터 선택", C_BLUE),
    ("탭 1\n위험도 확인", "Folium 지도에서\n고위험 지역 클릭\n→ 팝업으로 상세\n수치 즉시 확인", C_RED),
    ("탭 2\n피크 파악", "시간대×요일\n히트맵으로\n언제 집중 단속\n해야 할지 파악", C_ORANGE),
    ("탭 3\n유형 대책", "위반유형별\n도넛차트 + 자동\n권장 대책 텍스트\n출력", C_GREEN),
    ("탭 5\n예측·결정", "2026년 예측 그래프\n→ 인력 수요 권고\n→ 3-Tier 정책\n문서 자동 생성", C_PURPLE),
]
for i, (step, desc, color) in enumerate(journey):
    bx = 0.2 + i * 2.57
    add_rect(slide, bx, 1.6, 2.32, 0.46, fill=color)
    add_text(slide, step, bx+0.05, 1.63, 2.22, 0.4, size=10, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide, bx, 2.06, 2.32, 1.62, fill=C_WHITE, line=color, line_width=1.2)
    add_text(slide, desc, bx+0.08, 2.1, 2.18, 1.54, size=8.5, color=C_DARK, align=PP_ALIGN.CENTER)
    if i < 4:
        add_text(slide, "▶", bx+2.32, 2.6, 0.22, 0.5, size=13, bold=True, color=color, align=PP_ALIGN.CENTER)

# 하단 좌: UI/UX 포인트
add_rect(slide, 0.2, 3.82, 6.2, 0.32, fill=C_TEAL)
add_text(slide, "UI/UX 매끄러움 포인트", 0.3, 3.86, 6.0, 0.26, size=11, bold=True, color=C_WHITE)
ux_items = [
    ("사이드바 통합 필터", "연도·법정동·월 범위를 한 곳에서 조작 → 모든 탭에 즉시 반영"),
    ("클릭 인터랙션",     "Folium 지도 마커 클릭 → 해당 법정동 상세 팝업 즉시 출력"),
    ("자동 권고 텍스트",  "법정동 선택만 하면 위험도 계산 → 3-Tier 정책 권고문 자동 생성"),
    ("색상 일관성",       "고위험=빨강, 중위험=주황, 저위험=초록 → 모든 탭에서 동일 적용"),
]
add_rect(slide, 0.2, 4.14, 6.2, 2.72, fill=C_WHITE, line=C_TEAL, line_width=1.0)
for i, (label, desc) in enumerate(ux_items):
    yt = 4.2 + i * 0.64
    add_rect(slide, 0.28, yt, 1.65, 0.26, fill=C_TEAL)
    add_text(slide, label, 0.3, yt+0.02, 1.61, 0.22, size=7.5, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, desc, 2.02, yt, 4.25, 0.26, size=8.5, color=C_DARK)

# 하단 우: 디자인 일관성
add_rect(slide, 6.65, 3.82, 6.45, 0.32, fill=C_NAVY)
add_text(slide, "디자인 일관성 원칙", 6.75, 3.86, 6.25, 0.26, size=11, bold=True, color=C_WHITE)
design_items = [
    ("색상 체계", "위험도 3단계 색상(RED/ORANGE/GREEN) 전체 일관 적용", C_RED),
    ("헤더 구조", "Navy 배경 + Orange 액센트 라인으로 모든 슬라이드 통일", C_ORANGE),
    ("수치 강조", "핵심 수치는 크고 굵게, 보조 텍스트는 회색으로 계층화", C_BLUE),
    ("반응형 레이아웃", "use_container_width=True로 화면 크기 무관하게 적응", C_TEAL),
    ("Folium + Streamlit", "streamlit-folium으로 지도를 대시보드 내에 자연스럽게 통합", C_PURPLE),
]
add_rect(slide, 6.65, 4.14, 6.45, 2.72, fill=C_WHITE, line=C_NAVY, line_width=1.0)
for i, (label, desc, color) in enumerate(design_items):
    yt = 4.2 + i * 0.5
    add_rect(slide, 6.73, yt, 1.5, 0.24, fill=color)
    add_text(slide, label, 6.75, yt+0.02, 1.46, 0.2, size=7.5, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, desc, 8.3, yt, 4.7, 0.24, size=8, color=C_DARK)

add_rect(slide, 0, 7.15, SLIDE_W, 0.35, fill=RGBColor(0x0D,0x1A,0x2E))
add_text(slide, "에네레기파 | 지도교수: 김순찬 교수님", 0.2, 7.18, 7.0, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.LEFT)
add_text(slide, "트랙 B 자유주제 No.13  |  2026.05.29", 6.5, 7.18, 6.5, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.RIGHT)

# ============================================================
# 슬라이드 06 - 차별성 & 기대 효과
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "차별성 & 기대 효과", "기존 반응형 단속 → 데이터 기반 예방형 시스템으로 전환")
add_rect(slide, 0.2, 1.2, 5.95, 0.38, fill=C_GRAY)
add_text(slide, "BEFORE  —  기존 방식 (반응형)", 0.3, 1.24, 5.75, 0.3, size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
before_items = [
    "✗  민원 접수 후 수동 출동 (사후 대응)",
    "✗  단속 인력 균등 배치 (데이터 미활용)",
    "✗  CCTV 설치 기준 없음 (감 의존)",
    "✗  단속 건수 매년 증가 → 대응 한계",
    "✗  지역별 위험도 파악 불가",
]
add_rect(slide, 0.2, 1.58, 5.95, 2.85, fill=C_WHITE, line=C_GRAY, line_width=1.0)
for i, item in enumerate(before_items):
    add_text(slide, item, 0.3, 1.65+i*0.52, 5.75, 0.45, size=10, color=C_GRAY)
add_rect(slide, 6.45, 1.2, 6.65, 0.38, fill=C_BLUE)
add_text(slide, "AFTER  —  이 시스템 (예방형)", 6.55, 1.24, 6.45, 0.3, size=12, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
after_items = [
    "✓  앙상블 예측 기반 선제적 인력 배치",
    "✓  피크 시간·지역 데이터 기반 집중 단속",
    "✓  CCTV 공백지수로 설치 우선순위 결정",
    "✓  월별 단속 건수 예측 (MAE 1,451건/6.7%)",
    "✓  재보정위험도로 35개 법정동 위험 등급화",
]
add_rect(slide, 6.45, 1.58, 6.65, 2.85, fill=C_WHITE, line=C_BLUE, line_width=1.0)
for i, item in enumerate(after_items):
    add_text(slide, item, 6.55, 1.65+i*0.52, 6.45, 0.45, size=10, bold=True, color=C_DARK)
add_text(slide, "→", 6.02, 2.55, 0.4, 0.6, size=28, bold=True, color=C_ORANGE, align=PP_ALIGN.CENTER)
add_rect(slide, 0.2, 4.58, 12.9, 0.35, fill=C_NAVY)
add_text(slide, "핵심 성과 지표 (KPI)", 0.3, 4.62, 12.5, 0.27, size=11, bold=True, color=C_WHITE)
kpi2_items = [
    (C_GREEN,"앙상블 예측 정확도","MAPE 6.7%\nMAE 1,451건","전통모델 대비 38% 개선"),
    (C_ORANGE,"CCTV 시급 설치 지역","공백지수 > 0.3\n5개 지역 도출","금곡동/비봉면/방교동/장지동/송산동"),
    (C_BLUE,"민원 감소 기대 효과","고위험 지역\n선제 단속 강화","향남읍·석우동·영천동 집중 대응"),
]
for i, (color, title, val, sub) in enumerate(kpi2_items):
    bx = 0.2+i*4.35
    add_rect(slide, bx, 5.0, 4.05, 1.9, fill=color)
    add_text(slide, title, bx+0.1, 5.05, 3.85, 0.35, size=10, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, val, bx+0.1, 5.42, 3.85, 0.65, size=13, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
    add_text(slide, sub, bx+0.1, 6.1, 3.85, 0.72, size=8.5, color=C_WHITE, align=PP_ALIGN.CENTER)

# ============================================================
# 슬라이드 05 - 향후 계획
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "향후 계획", "3단계 로드맵: POC 완료 → 시범운영 → 전시 확대")
phases = [
    ("1단계\nPOC 완료","2026.5 ~ 6",C_GREEN,
     ["• 대시보드 최종 완성 및 QA","• 캡스톤 발표 및 평가","• 코드 리팩토링 및 문서화","• GitHub 공개 레포지터리 배포"]),
    ("2단계\n시범운영","2026 하반기",C_BLUE,
     ["• 화성시 담당 부서 파일럿 제공","• 실제 단속 데이터와 예측 비교","• 사용자 피드백 수집 및 개선","• 2026년 실제 결과 검증"]),
    ("3단계\n전시 확대","2027~",C_PURPLE,
     ["• 경기도 내 다른 시로 확장","• 실시간 데이터 연동 구현","• API 서버 분리 및 클라우드 배포","• 행정 시스템 연계 검토"]),
]
for i, (title, period, color, items) in enumerate(phases):
    bx = 0.25+i*4.35
    add_rect(slide, bx, 1.2, 4.05, 0.82, fill=color)
    add_text(slide, title, bx+0.08, 1.25, 3.9, 0.55, size=14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, period, bx+0.08, 1.8, 3.9, 0.2, size=9, color=C_YELLOW, align=PP_ALIGN.CENTER)
    add_rect(slide, bx, 2.02, 4.05, 2.8, fill=C_WHITE, line=color, line_width=1.5)
    for j, item in enumerate(items):
        add_text(slide, item, bx+0.1, 2.1+j*0.62, 3.85, 0.55, size=10, color=C_DARK)
add_rect(slide, 0.25, 5.0, 12.8, 0.32, fill=C_ORANGE)
add_text(slide, "도입 장벽 및 고려사항", 0.35, 5.03, 12.5, 0.26, size=11, bold=True, color=C_WHITE)
barriers = [
    ("데이터 접근 권한","화성시 공공데이터 API 연동 시 협약 필요"),
    ("인력 운영 연계","예측 결과를 실제 인력 배치 시스템과 통합 필요"),
    ("실시간 업데이트","현재 배치 분석 → 스트리밍 데이터 처리로 전환 필요"),
    ("개인정보 이슈","단속 데이터 비식별화 처리 기준 마련 필요"),
]
for i, (title, desc) in enumerate(barriers):
    bx = 0.25+i*3.2
    add_rect(slide, bx, 5.4, 3.05, 1.52, fill=C_LBLUE, line=C_ORANGE, line_width=0.5)
    add_text(slide, title, bx+0.08, 5.45, 2.9, 0.3, size=9, bold=True, color=C_NAVY)
    add_text(slide, desc, bx+0.08, 5.78, 2.9, 1.1, size=8.5, color=C_DARK)
# ============================================================
# 슬라이드 08 - 회고 및 소회 (파트 7)
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "회고 및 소회", "AI 바이브코딩 협업의 극복점 · 다음 프로젝트에 적용할 배움")

# 왼쪽: 구체 사례 1개 (SARIMA 버그 스토리)
add_rect(slide, 0.2, 1.2, 7.5, 0.38, fill=C_RED)
add_text(slide, "AI 바이브코딩 극복 사례  —  SARIMA 예측값 폭발 버그", 0.3, 1.24, 7.3, 0.3, size=11, bold=True, color=C_WHITE)

story_phases = [
    ("Situation\n상황",
     "앙상블 대시보드 완성 직전, 탭5 예측값이\n갑자기 -9,223,372,036,854,775,808 표시.\n서비스 직전 치명적 버그 발생.",
     C_RED),
    ("Action\nAI 협업 과정",
     "스택 트레이스 + 예측값 분포를 Claude에 입력.\n'SARIMA(1,0,1)(1,1,0,12) 차분 부족으로\n비정상 시계열 → NaN → int 변환 시 폭발'\n원인 분석 완료 시간: 2분 이내.",
     C_ORANGE),
    ("Result\n결과",
     "파라미터 (1,1,1)(1,1,0,12)로 변경 +\n예측값 범위 검증 후 폴백 로직 구현.\n예측값 정상화 (16,732건 출력).\n단독 해결 시 반나절 이상 예상 → 30분 해결.",
     C_GREEN),
    ("Lesson\n핵심 인사이트",
     "AI는 증상을 잘 설명하면 원인을 빠르게 진단.\n단, AI 제안 파라미터도 직접 유효성 검증 필수.\n'AI가 고쳤다'가 아니라\n'AI와 함께 내가 고쳤다'는 인식이 핵심.",
     C_PURPLE),
]
for i, (phase, text, color) in enumerate(story_phases):
    yt = 1.65 + i * 1.28
    add_rect(slide, 0.2, yt, 7.5, 1.18, fill=C_WHITE, line=color, line_width=1.2)
    add_rect(slide, 0.2, yt, 1.8, 1.18, fill=color)
    add_text(slide, phase, 0.22, yt+0.22, 1.76, 0.72, size=9, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, text, 2.1, yt+0.12, 5.5, 0.94, size=8.5, color=C_DARK)

# 오른쪽: 다음 프로젝트에 적용할 배움 4가지
add_rect(slide, 7.95, 1.2, 5.15, 0.38, fill=C_NAVY)
add_text(slide, "다음 프로젝트에 적용할 배움", 8.05, 1.24, 5.0, 0.3, size=11, bold=True, color=C_WHITE)

learnings = [
    ("① 버전 명시 먼저",
     "AI 코드 쓰기 전 라이브러리 버전을\nrequirements.txt에 고정.\n버전 충돌 디버깅은 AI도 어렵다.",
     C_BLUE),
    ("② 검증 코드 먼저",
     "기능보다 검증 로직을 먼저 짜라.\n예측값 범위·타입·NaN 검사가\n먼저 있었다면 폭발 버그를 사전에 잡았다.",
     C_TEAL),
    ("③ AI 역할 분담 명확히",
     "코드 초안 = AI\n통합·검증·도메인 판단 = 사람.\n이 경계가 무너지면 오류가 프로덕션에 나간다.",
     C_GREEN),
    ("④ 통합 테스트 습관화",
     "탭별 단독 테스트 통과해도\n통합 시 엣지케이스 버그 발생.\nAI 코드일수록 통합 테스트를 더 철저히.",
     C_ORANGE),
]
for i, (title, desc, color) in enumerate(learnings):
    yt = 1.65 + i * 1.28
    add_rect(slide, 7.95, yt, 5.15, 1.18, fill=C_WHITE, line=color, line_width=1.2)
    add_rect(slide, 7.95, yt, 5.15, 0.34, fill=color)
    add_text(slide, title, 8.05, yt+0.05, 5.0, 0.26, size=9.5, bold=True, color=C_WHITE)
    add_text(slide, desc, 8.05, yt+0.44, 5.0, 0.7, size=8.5, color=C_DARK)

# ============================================================
# 슬라이드 07 - 결론 & Q&A
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_NAVY)
add_rect(slide, 0, 0, SLIDE_W, 0.12, fill=C_ORANGE)
add_text(slide, "결론 요약  &  Q&A", 0.3, 0.16, 9.5, 0.65, size=22, bold=True, color=C_WHITE)
add_text(slide, "이 프로젝트가 만든 것 — 5가지 핵심 성과", 0.3, 0.76, 9.5, 0.35, size=12, color=C_LBLUE)

# 핵심 수치 KPI 행
kpis = [
    ("217,682건", "2023년 실단속", C_BLUE),
    ("MAE 1,451건\n(6.7%)", "앙상블 모델 성능", C_GREEN),
    ("향남읍 6.87점", "위험도 1위 지역", C_RED),
    ("10월 21,276건", "2026년 피크 예측", C_ORANGE),
    ("금곡동 0.733", "CCTV 공백 1위", C_TEAL),
]
for i, (val, lbl, color) in enumerate(kpis):
    bx = 0.25 + i * 1.91
    add_rect(slide, bx, 1.12, 1.78, 0.92, fill=color)
    add_text(slide, val, bx+0.05, 1.16, 1.68, 0.5, size=10, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, lbl, bx+0.05, 1.68, 1.68, 0.3, size=7.5, color=C_LBLUE, align=PP_ALIGN.CENTER)

# 5개 결론 행
conclusions = [
    ("①  전처리 & 데이터","2023년 실단속 217,682건 / 법정동 미추출 16.7% → 1.7% 정제 / 35개 법정동 확정"),
    ("②  위험도 분석","실단속×0.65 + 민원×0.35 공식 → 향남읍 6.87점 고위험 1위"),
    ("③  예측 모델","Prophet + SARIMA 앙상블 MAE 1,451건(6.7%) — 8개 모델 중 최고 성능"),
    ("④  정책 추천","CCTV 공백 5지역 시급 설치 권고 / 2026년 10월 단속 인력 증원 권장"),
    ("⑤  대시보드 시스템","Streamlit 5탭 — 위험도지도·히트맵·위반유형·예측·정책권고 통합"),
]
for i, (title, desc) in enumerate(conclusions):
    yt = 2.16 + i * 0.78
    add_rect(slide, 0.25, yt, 9.4, 0.7, fill=RGBColor(0x1E,0x3A,0x5F))
    add_rect(slide, 0.25, yt, 0.07, 0.7, fill=C_ORANGE)
    add_text(slide, title, 0.42, yt+0.04, 2.8, 0.28, size=10, bold=True, color=C_YELLOW)
    add_text(slide, desc,  0.42, yt+0.36, 9.1, 0.3, size=9, color=C_WHITE)

add_rect(slide, 9.85, 1.12, 3.25, 5.4, fill=C_BLUE)
add_text(slide, "Q & A", 9.85, 2.15, 3.25, 0.72, size=30, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
add_text(slide, "감사합니다!", 9.85, 2.92, 3.25, 0.58, size=18, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
add_text(slide, "에네레기파", 9.85, 3.6, 3.25, 0.42, size=13, color=C_LBLUE, align=PP_ALIGN.CENTER)
add_text(slide, "임단군 · 정예민 · 안유경", 9.85, 4.05, 3.25, 0.4, size=10, color=C_LBLUE, align=PP_ALIGN.CENTER)
add_text(slide, "지도교수: 김순찬 교수님", 9.85, 4.48, 3.25, 0.35, size=9, color=C_LBLUE, align=PP_ALIGN.CENTER)
add_text(slide, "2026.05.29", 9.85, 4.88, 3.25, 0.38, size=11, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
add_rect(slide, 0, 7.15, SLIDE_W, 0.35, fill=RGBColor(0x0D,0x1A,0x2E))
add_text(slide, "에네레기파 | 지도교수: 김순찬 교수님", 0.2, 7.18, 7.0, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.LEFT)
add_text(slide, "트랙 B 자유주제 No.13  |  2026.05.29", 6.5, 7.18, 6.5, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.RIGHT)
# ============================================================
# 슬라이드 08 - [부록] 데이터 & 전처리 파이프라인
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "[부록] 데이터 & 전처리 파이프라인", "원천 데이터 → 분석 가능 형태로 정제하는 5단계")
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
steps = [
    ("Step 1","xlsx 로드","화성시 단속 원본 엑셀\n2021~2025년 전체\n약 25만+ 행 처리",C_BLUE),
    ("Step 2","법정동 추출","주소 파싱 로직\n미추출 16.7% → 1.7%\n정규식 기반 매핑",C_TEAL),
    ("Step 3","위반유형\n분류","주정차 위반 유형\n10개 카테고리 분류\n코드 표준화",C_GREEN),
    ("Step 4","소규모 제거","5건 미만 법정동\n통계적 노이즈 제거\n35개 법정동 확정",C_ORANGE),
    ("Step 5","5개 CSV\n출력","법정동별/시간대별\n월별/위반유형별\n최종 분석 데이터",C_PURPLE),
]
for i, (step_num, title, desc, color) in enumerate(steps):
    bx = 0.2+i*2.57
    add_rect(slide, bx, 1.25, 2.32, 0.42, fill=color)
    add_text(slide, step_num, bx+0.05, 1.28, 0.75, 0.35, size=10, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
    add_text(slide, title, bx+0.82, 1.3, 1.4, 0.38, size=10, bold=True, color=C_WHITE, align=PP_ALIGN.LEFT)
    add_rect(slide, bx, 1.67, 2.32, 1.8, fill=C_WHITE, line=color, line_width=1.0)
    add_text(slide, desc, bx+0.08, 1.72, 2.18, 1.68, size=9, color=C_DARK, align=PP_ALIGN.CENTER)
    if i < 4:
        add_text(slide, "→", bx+2.32, 2.1, 0.24, 0.6, size=16, bold=True, color=C_NAVY, align=PP_ALIGN.CENTER)
add_rect(slide, 0.2, 3.6, 12.85, 0.35, fill=C_NAVY)
add_text(slide, "핵심 개선 지표", 0.3, 3.64, 12.5, 0.27, size=11, bold=True, color=C_WHITE)
metrics = [
    ("법정동 미추출률\n16.7% → 1.7%","▼ 90% 개선",C_GREEN),
    ("최종 분석 대상\n법정동 35개","전체 커버리지",C_BLUE),
    ("월별 시계열 데이터\n51개월 확보","2021.01~2025.03",C_TEAL),
    ("위반유형\n10개 카테고리","체계적 분류 완료",C_ORANGE),
]
for i, (title, val, color) in enumerate(metrics):
    bx = 0.2+i*3.22
    add_rect(slide, bx, 4.02, 3.05, 1.78, fill=color)
    add_text(slide, title, bx+0.1, 4.1, 2.85, 0.75, size=10, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, val, bx+0.1, 4.9, 2.85, 0.82, size=12, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
spec_data = [
    ["항목","내용"],
    ["데이터 출처","화성시 불법주정차 단속 원천 데이터"],
    ["분석 기간","2021년 1월 ~ 2025년 4월 (51개월)"],
    ["총 단속 건수","217,682건 (2023년 실단속 기준)"],
    ["학습/검증 분리","학습: 2021~2024 / 검증(out-of-sample): 2025.01~04"],
    ["출력 파일","monthly_by_dong.csv 외 4개 CSV"],
]
add_table(slide, spec_data, 0.2, 5.88, 12.85, 1.1, font_size=8.5)

# ============================================================
# 슬라이드 09 - [부록] 분석 결과①: 법정동별 재보정위험도
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "[부록] 분석 결과 ①: 법정동별 재보정위험도", "실단속비율×0.65 + 민원비율×0.35 복합 지표")
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
add_rect(slide, 0.2, 1.2, 8.5, 0.88, fill=C_NAVY)
add_text(slide, "재보정위험도 산출 공식", 0.3, 1.24, 8.3, 0.3, size=10, bold=True, color=C_LBLUE)
add_text(slide, "재보정위험도  =  (법정동 단속건수 / 전체 단속건수)  ×  0.65  +  (법정동 민원건수 / 전체 민원건수)  ×  0.35",
         0.3, 1.52, 8.3, 0.48, size=10, bold=True, color=C_YELLOW)
add_rect(slide, 8.85, 1.2, 4.25, 0.88, fill=C_WHITE, line=C_NAVY, line_width=1.0)
add_text(slide, "위험도 등급 기준", 8.95, 1.24, 4.0, 0.28, size=9, bold=True, color=C_NAVY)
grade_items = [("고위험 (RED)","점수 >= 5.0",C_RED),("중위험 (ORANGE)","3.0 ~ 5.0",C_ORANGE),("저위험 (GREEN)","점수 < 3.0",C_GREEN)]
for i, (lbl, rng, color) in enumerate(grade_items):
    add_text(slide, lbl, 8.95, 1.56+i*0.16, 2.3, 0.18, size=8, bold=True, color=color)
    add_text(slide, rng, 11.3, 1.56+i*0.16, 1.7, 0.18, size=8, color=C_DARK)
top7_data = [
    ["순위","법정동","재보정위험도","위험등급","단속건수","비고"],
    ["1위","향남읍","6.87점","고위험","33,280건","CCTV 강화 시급"],
    ["2위","석우동","5.67점","중위험","21,408건","동탄2신도시 밀집"],
    ["3위","영천동","5.42점","중위험","18,755건","상업지구 집중"],
    ["4위","오산동","4.17점","중위험","18,526건","생활도로 다수"],
    ["5위","남양읍","4.16점","중위험","18,763건","읍내 중심가"],
    ["6위","반송동","4.13점","중위험","15,783건","주거지역"],
    ["7위","봉담읍","4.06점","중위험","13,743건","봉담지구"],
]
add_table(slide, top7_data, 0.2, 2.18, 12.85, 2.62, font_size=10)
add_rect(slide, 0.2, 4.9, 12.85, 0.35, fill=C_NAVY)
add_text(slide, "분석 시사점", 0.3, 4.94, 12.5, 0.27, size=11, bold=True, color=C_WHITE)
insights = [
    ("향남읍 압도적 1위","6.87점으로 2위 석우동(5.67점)보다 1.2점 높음 → 즉각 집중 단속 필요"),
    ("동탄2신도시 집중","석우동·영천동·오산동 모두 TOP 5 → 신도시 개발 후 인프라 부족"),
    ("읍 단위 고위험","향남읍·남양읍·봉담읍 → 읍 지역 단속 인프라 투자 필요"),
    ("TOP 7 비중","상위 7개 법정동이 전체 민원의 약 40% 집중"),
]
for i, (title, desc) in enumerate(insights):
    bx = 0.2+i*3.22
    add_rect(slide, bx, 5.32, 3.05, 1.52, fill=C_WHITE, line=C_BLUE, line_width=0.5)
    add_rect(slide, bx, 5.32, 3.05, 0.28, fill=C_BLUE)
    add_text(slide, title, bx+0.08, 5.34, 2.9, 0.24, size=8.5, bold=True, color=C_WHITE)
    add_text(slide, desc, bx+0.08, 5.65, 2.9, 1.12, size=8.5, color=C_DARK)
# ============================================================
# 슬라이드 10 - [부록] CCTV 공백지수 & 시간대 패턴
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "[부록] 분석 결과 ②③: CCTV 공백지수 & 시간대 패턴", "CCTV 설치 우선순위 도출 + 피크 시간대 분석")
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
add_rect(slide, 0.2, 1.2, 6.2, 0.35, fill=C_ORANGE)
add_text(slide, "② CCTV 공백지수 TOP 5", 0.3, 1.24, 6.0, 0.27, size=11, bold=True, color=C_WHITE)
add_rect(slide, 0.2, 1.6, 6.2, 0.32, fill=C_DARK)
add_text(slide, "공백지수 = 민원비율 - 고정CCTV비율  (높을수록 CCTV 시급 설치 필요)", 0.28, 1.63, 6.0, 0.26, size=8.5, color=C_YELLOW)
cctv_data = [
    ["순위","법정동","공백지수","CCTV 비율","민원 비율"],
    ["1위","금곡동","0.733","0%","73%"],
    ["2위","비봉면","0.528","0%","53%"],
    ["3위","방교동","0.429","15%","58%"],
    ["4위","장지동","0.385","28%","66%"],
    ["5위","송산동","0.287","29%","58%"],
]
add_table(slide, cctv_data, 0.2, 1.97, 6.2, 2.08, font_size=10)
add_rect(slide, 0.2, 4.12, 6.2, 0.32, fill=C_RED)
add_text(slide, "CCTV 즉시 설치 권고 지역 (공백지수 0.3 이상)", 0.3, 4.15, 6.0, 0.26, size=9, bold=True, color=C_WHITE)
add_rect(slide, 0.2, 4.44, 6.2, 1.28, fill=C_WHITE, line=C_RED, line_width=1.0)
cctv_rec = [
    "• 금곡동: CCTV 완전 공백 (0%), 민원 73% → 최우선 설치",
    "• 비봉면: CCTV 완전 공백 (0%), 민원 53% → 2순위 설치",
    "• 방교동: CCTV 15% 불충분, 민원 58% → 추가 설치 필요",
    "• 장지동: CCTV 28% vs 민원 66% → 대폭 증설 필요",
    "• 예산 배분 기준으로 공백지수 활용 → 객관적 의사결정",
]
for i, item in enumerate(cctv_rec):
    add_text(slide, item, 0.28, 4.5+i*0.24, 6.0, 0.22, size=8, color=C_DARK)
add_rect(slide, 6.7, 1.2, 6.35, 0.35, fill=C_TEAL)
add_text(slide, "③ 시간대별 단속 패턴 (전체)", 6.8, 1.24, 6.15, 0.27, size=11, bold=True, color=C_WHITE)
time_data = [
    ["시간대","단속건수","비중","특징"],
    ["15시 (오후 3시)","33,188건","최다","1위 피크"],
    ["10시 (오전 10시)","29,200건","2위","오전 피크"],
    ["16시 (오후 4시)","27,886건","3위","오후 연속"],
    ["17시 (오후 5시)","22,596건","4위","퇴근 직전"],
    ["09시 (오전 9시)","20,660건","5위","출근 직후"],
    ["20시 (오후 8시)","15,197건","6위","저녁 시간대"],
]
add_table(slide, time_data, 6.7, 1.6, 6.35, 2.18, font_size=9.5)
add_rect(slide, 6.7, 3.85, 6.35, 0.32, fill=C_NAVY)
add_text(slide, "시간대 패턴 해석 및 인력 배치 제언", 6.8, 3.88, 6.15, 0.26, size=10, bold=True, color=C_WHITE)
pattern_items = [
    ("주간 집중 패턴","09~17시에 전체 단속의 68% 집중 → 주간 인력 집중 배치 필요"),
    ("오후 피크 (15~16시)","학교 하교 + 쇼핑 + 업무 종료 겹침 → 15~16시 증원 필수"),
    ("야간 단속 취약","18시 이후 급감 → 야간 CCTV 자동 단속 보완 필요"),
]
for i, (title, desc) in enumerate(pattern_items):
    yt = 4.22+i*0.68
    add_rect(slide, 6.7, yt, 6.35, 0.62, fill=C_WHITE, line=C_TEAL, line_width=0.5)
    add_text(slide, title, 6.78, yt+0.04, 2.2, 0.24, size=8.5, bold=True, color=C_TEAL)
    add_text(slide, desc, 6.78, yt+0.3, 6.1, 0.28, size=8.5, color=C_DARK)
add_rect(slide, 0.2, 5.78, 12.85, 0.32, fill=C_DARK)
add_text(slide, "요일별 추가 분석:  월요일 단속건수 최다  |  토·일 평일 대비 30% 감소  |  공휴일 전날 평일 대비 15% 증가",
         0.3, 5.81, 12.5, 0.26, size=8.5, color=C_YELLOW)

# ============================================================
# 슬라이드 11 - [부록] 예측 모델 & 모델 선정 이유
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "[부록] 예측 모델 & 모델 선정 이유", "Prophet + SARIMA 앙상블 — 8개 모델 비교 최종 선정")
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
add_rect(slide, 0.2, 1.2, 6.0, 0.35, fill=C_BLUE)
add_text(slide, "Prophet + SARIMA 앙상블 모델", 0.3, 1.24, 5.8, 0.27, size=11, bold=True, color=C_WHITE)
info_items = [
    ("데이터 기간","51개월 (2021.01 ~ 2025.03)"),
    ("학습 기간","2021.01 ~ 2024.12 (48개월)"),
    ("검증 기간","2025.01 ~ 2025.04 (4개월, out-of-sample)"),
    ("예측 기간","2026.06 ~ 2026.11 (6개월)"),
]
add_rect(slide, 0.2, 1.6, 6.0, 1.42, fill=C_WHITE, line=C_BLUE, line_width=0.5)
for i, (k, v) in enumerate(info_items):
    yt = 1.65+i*0.32
    add_text(slide, k+":", 0.28, yt, 1.8, 0.28, size=9, bold=True, color=C_NAVY)
    add_text(slide, v, 2.1, yt, 4.0, 0.28, size=9, color=C_DARK)
add_rect(slide, 0.2, 3.1, 2.85, 0.32, fill=C_BLUE)
add_text(slide, "Prophet 단독", 0.28, 3.13, 2.7, 0.26, size=10, bold=True, color=C_WHITE)
add_rect(slide, 0.2, 3.42, 2.85, 1.12, fill=C_WHITE, line=C_BLUE, line_width=1.0)
for i, item in enumerate(["• Facebook Prophet 활용","• 계절성 자동 감지","• MAE: 1,594건","• MAPE: 7.4%","• 앙상블 weight: 50%"]):
    add_text(slide, item, 0.28, 3.46+i*0.2, 2.7, 0.18, size=8.5, color=C_DARK)
add_rect(slide, 3.2, 3.1, 3.0, 0.32, fill=C_TEAL)
add_text(slide, "SARIMA(1,1,1)(1,1,0,12)", 3.28, 3.13, 2.84, 0.26, size=9.5, bold=True, color=C_WHITE)
add_rect(slide, 3.2, 3.42, 3.0, 1.12, fill=C_WHITE, line=C_TEAL, line_width=1.0)
for i, item in enumerate(["• 계절형 ARIMA 모델","• 12개월 계절 주기","• MAE: 1,571건","• MAPE: 7.4%","• 앙상블 weight: 50%"]):
    add_text(slide, item, 3.28, 3.46+i*0.2, 2.84, 0.18, size=8.5, color=C_DARK)
add_rect(slide, 0.2, 4.65, 6.0, 0.35, fill=C_GREEN)
add_text(slide, "앙상블 = Prophet×0.5 + SARIMA×0.5", 0.3, 4.69, 5.8, 0.27, size=10, bold=True, color=C_WHITE)
add_rect(slide, 0.2, 5.0, 6.0, 0.88, fill=C_WHITE, line=C_GREEN, line_width=1.5)
add_text(slide, "앙상블 MAE: 1,451건  |  MAPE: 6.7%  |  단독 모델 대비 최대 8% 개선", 0.28, 5.05, 5.8, 0.38, size=11, bold=True, color=C_GREEN)
add_text(slide, "전통 시계열 모델(Holt-Winters, ARIMA) 대비 38% 이상 개선", 0.28, 5.48, 5.8, 0.32, size=9, color=C_DARK)
add_rect(slide, 6.45, 1.2, 6.65, 0.35, fill=C_NAVY)
add_text(slide, "모델 선정 이유 — 8개 모델 비교표", 6.55, 1.24, 6.45, 0.27, size=11, bold=True, color=C_WHITE)
model_data = [
    ["모델명","MAE","MAPE","비고"],
    ["★ Prophet+SARIMA 앙상블","1,451건","6.7%","최종 선정"],
    ["Prophet 단독","1,594건","7.4%","구성 모델"],
    ["SARIMA(1,1,1)(1,1,0,12)","1,571건","7.4%","구성 모델"],
    ["선형회귀","2,302건","11.3%",""],
    ["Holt-Winters","2,341건","11.8%",""],
    ["ARIMA(1,1,1)","2,409건","11.8%",""],
    ["Naive (직전월 반복)","2,584건","12.6%","기준선"],
    ["Seasonal Naive","2,982건","16.0%","최하위"],
]
add_table(slide, model_data, 6.45, 1.6, 6.65, 3.08, font_size=9.5)
add_rect(slide, 6.45, 4.78, 6.65, 0.32, fill=C_GREEN)
add_text(slide, "최종 선정 이유", 6.55, 4.81, 6.45, 0.26, size=10, bold=True, color=C_WHITE)
reasons = [
    "• 8개 모델 중 MAE 1,451건, MAPE 6.7%로 최고 성능",
    "• 단독 Prophet/SARIMA 대비 MAE 최대 8% 추가 개선",
    "• 전통 모델(Holt-Winters 11.8%) 대비 MAPE 38% 개선",
    "• 두 모델의 장점(추세감지 + 계절성) 상호 보완",
    "• Out-of-sample 검증으로 과적합 없음 확인",
]
add_rect(slide, 6.45, 5.1, 6.65, 1.7, fill=C_WHITE, line=C_GREEN, line_width=1.0)
for i, reason in enumerate(reasons):
    add_text(slide, reason, 6.53, 5.15+i*0.32, 6.5, 0.28, size=8.5, color=C_DARK)
# ============================================================
# 슬라이드 12 - [부록] 예측 결과 2026년 6~11월
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "[부록] 예측 결과: 2026년 6~11월", "Prophet + SARIMA 앙상블 월별 예측 및 인력 수요 권고")
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
pred_data = [
    ["기간","Prophet 예측","SARIMA 예측","앙상블 예측","전월대비","인력수요 권고"],
    ["2026년 6월","19,024건","20,118건","19,575건","기준","현행 유지"],
    ["2026년 7월","18,786건","21,164건","19,984건","▲ 2.1%","현행 유지"],
    ["2026년 8월","18,222건","20,201건","19,219건","▼ 3.8%","현행 유지"],
    ["2026년 9월","18,796건","18,932건","18,864건","▼ 1.8%","현행 유지"],
    ["2026년 10월","19,664건","22,864건","21,276건","▲ 12.8%","★ 증원 권장 (피크)"],
    ["2026년 11월","17,784건","19,465건","18,630건","▼ 12.4%","현행 유지"],
]
add_table(slide, pred_data, 0.2, 1.2, 12.85, 2.68, font_size=10)
add_rect(slide, 0.2, 4.0, 12.85, 0.35, fill=C_NAVY)
add_text(slide, "예측 요약 및 인력 배치 권고", 0.3, 4.04, 12.5, 0.27, size=11, bold=True, color=C_WHITE)
summary_items = [
    ("6개월 평균\n예측 건수","19,591건/월",C_BLUE),
    ("최고 피크\n(10월)","21,276건",C_RED),
    ("최저 예측\n(11월)","18,630건",C_GREEN),
    ("증원 권장\n기간","10월 한 달",C_ORANGE),
    ("Prophet vs\nSARIMA 격차","10월 최대\n3,200건",C_PURPLE),
]
for i, (title, val, color) in enumerate(summary_items):
    bx = 0.2+i*2.55
    add_rect(slide, bx, 4.42, 2.35, 1.55, fill=color)
    add_text(slide, title, bx+0.05, 4.48, 2.25, 0.52, size=9, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, val, bx+0.05, 5.02, 2.25, 0.88, size=13, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
add_rect(slide, 0.2, 6.05, 12.85, 0.35, fill=C_DARK)
add_text(slide, "해석:  10월은 기온 하강 + 단풍 관광 + 학교 행사 집중으로 외출·방문 증가 → 불법주정차 단속건수 급증 예상  →  10월 단속인력 사전 증원 권장",
         0.3, 6.08, 12.5, 0.28, size=8.5, color=C_YELLOW)
add_rect(slide, 0.2, 6.48, 12.85, 0.55, fill=C_WHITE, line=C_BLUE, line_width=0.5)
add_text(slide, "• Prophet: 계절 패턴 추세 기반 — 10월 19,664건 (낮게 예측)", 0.3, 6.5, 6.0, 0.24, size=8.5, color=C_BLUE)
add_text(slide, "• SARIMA: 자기회귀 기반 — 10월 22,864건 (높게 예측)", 0.3, 6.74, 6.0, 0.24, size=8.5, color=C_TEAL)
add_text(slide, "• 앙상블: 두 모델 평균 — 10월 21,276건 (균형잡힌 예측)", 6.5, 6.5, 6.5, 0.24, size=8.5, color=C_GREEN)
add_text(slide, "• 10월 격차 3,200건 → 불확실성 높음, 인력 여유분 확보 권장", 6.5, 6.74, 6.5, 0.24, size=8.5, bold=True, color=C_RED)

# ============================================================
# 슬라이드 13 - [부록] 정책 추천 시스템
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "[부록] 정책 추천 시스템", "3-Tier 자동 정책 분류 및 우선순위 산출")
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
add_rect(slide, 0.2, 1.2, 12.85, 0.5, fill=C_NAVY)
add_text(slide, "단속강화 우선순위 공식:  단속강화 점수  =  재보정위험도 × 0.7  +  통행불편지수 × 0.3",
         0.3, 1.24, 12.5, 0.22, size=10, bold=True, color=C_YELLOW)
add_text(slide, "통행불편지수 = (민원건수/전체민원) × 100  |  CCTV설치 우선순위 = 공백지수 순위  |  안내계도 = 나머지 지역",
         0.3, 1.46, 12.5, 0.2, size=8.5, color=C_LBLUE)
tiers = [
    ("Tier 1\n단속 강화",C_RED,
     "적용 조건","재보정위험도 >= 4.0\n+ 통행불편지수 상위 30%",
     "권고 조치","• 해당 지역 단속 인력 30% 증원\n• 주간 집중 단속 실시\n• 고위험 시간대(15~16시) 상시 배치\n• 주민 신고 핫라인 강화",
     "적용 지역","향남읍·석우동·영천동·오산동·남양읍·반송동·봉담읍"),
    ("Tier 2\nCCTV 설치",C_ORANGE,
     "적용 조건","CCTV 공백지수 >= 0.3\n(민원비율 > CCTV비율)",
     "권고 조치","• CCTV 신규 설치 예산 배정\n• 공백지수 순위 기준 우선 배치\n• 금곡동·비봉면 최우선 설치\n• 이동식 CCTV 중기 운영",
     "시급 지역","금곡동(0.733)·비봉면(0.528)·방교동(0.429)·장지동(0.385)·송산동(0.287)"),
    ("Tier 3\n안내 계도",C_GREEN,
     "적용 조건","재보정위험도 < 4.0\n+ 공백지수 < 0.3",
     "권고 조치","• 현수막·표지판 안내 강화\n• 주민 교육 프로그램 운영\n• 계절별 캠페인 실시\n• 정기 모니터링 유지",
     "적용 지역","나머지 28개 법정동 해당"),
]
for i, (title, color, ct, cv, at, av, lt, lv) in enumerate(tiers):
    bx = 0.2+i*4.3
    add_rect(slide, bx, 1.8, 4.05, 0.55, fill=color)
    add_text(slide, title, bx+0.08, 1.85, 3.9, 0.48, size=14, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide, bx, 2.35, 4.05, 3.55, fill=C_WHITE, line=color, line_width=1.5)
    add_text(slide, ct, bx+0.1, 2.4, 1.2, 0.24, size=8.5, bold=True, color=color)
    add_text(slide, cv, bx+0.1, 2.64, 3.8, 0.45, size=8.5, color=C_DARK)
    add_text(slide, at, bx+0.1, 3.16, 1.2, 0.24, size=8.5, bold=True, color=color)
    add_text(slide, av, bx+0.1, 3.4, 3.8, 0.95, size=8.5, color=C_DARK)
    add_text(slide, lt, bx+0.1, 4.38, 1.2, 0.24, size=8.5, bold=True, color=color)
    add_text(slide, lv, bx+0.1, 4.62, 3.8, 0.55, size=7.5, color=C_GRAY, italic=True)
add_rect(slide, 0.2, 6.0, 12.85, 0.35, fill=C_DARK)
add_text(slide, "대시보드 자동화:  법정동 선택 → 위험도/공백지수 자동 계산 → Tier 분류 → 맞춤 정책 권고문 자동 생성",
         0.3, 6.03, 12.5, 0.28, size=8.5, color=C_YELLOW)
# ============================================================
# 슬라이드 14 - [부록] 대시보드 5탭 상세
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "[부록] 대시보드 5탭 상세 기능", "Streamlit 기반 통합 분석 대시보드 — 탭별 상세 기능 명세")
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
tab_details = [
    ("탭 1\n위험도 지도",C_RED,
     ["Folium 기반 인터랙티브 지도","법정동 경계 다각형 표시","재보정위험도 색상 그라데이션",
      "클릭 시 상세 통계 팝업","고위험/중위험/저위험 구분","TOP 7 마커 자동 표시"]),
    ("탭 2\n히트맵",C_ORANGE,
     ["시간대(24h) × 요일(7일) 히트맵","Plotly/Seaborn 시각화","피크 셀 자동 하이라이트",
      "법정동별 필터링 가능","연도별 비교 히트맵","CSV 다운로드 기능"]),
    ("탭 3\n위반유형 대책",C_GREEN,
     ["10개 위반유형별 분포 차트","유형별 맞춤 정책 자동 생성","지역×위반유형 교차 분석",
      "파이차트 + 바차트 통합","시계열 위반유형 트렌드","정책 우선순위 자동 출력"]),
    ("탭 4\n전체 현황",C_BLUE,
     ["2021~2024 연도별 추이 선그래프","법정동 TOP 10 바차트","CCTV 공백지수 맵 시각화",
      "전체 데이터 요약 통계","연도별 증감률 자동 계산","PDF/Excel 내보내기"]),
    ("탭 5\n예측 & 정책권고",C_PURPLE,
     ["2026년 6~11월 예측 선그래프","Prophet·SARIMA·앙상블 3선 비교","신뢰구간(80%·95%) 표시",
      "월별 인력 수요 자동 권고","법정동 선택 → 개별 예측","3-Tier 정책 권고문 자동 출력"]),
]
for i, (title, color, features) in enumerate(tab_details):
    bx = 0.2+i*2.6
    add_rect(slide, bx, 1.22, 2.35, 0.55, fill=color)
    add_text(slide, title, bx+0.05, 1.27, 2.25, 0.48, size=11, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide, bx, 1.77, 2.35, 4.95, fill=C_WHITE, line=color, line_width=1.5)
    for j, feat in enumerate(features):
        add_text(slide, "• "+feat, bx+0.08, 1.85+j*0.78, 2.2, 0.7, size=9, color=C_DARK)
add_rect(slide, 0.2, 6.85, 12.85, 0.22, fill=C_DARK)
add_text(slide, "기술 스택:  Streamlit  |  Folium / streamlit-folium  |  Prophet (Meta)  |  statsmodels SARIMA  |  Plotly  |  Pandas  |  NumPy  |  Matplotlib",
         0.3, 6.87, 12.5, 0.18, size=7.5, color=C_YELLOW)

# ============================================================
# 슬라이드 15 - [부록] 캡스톤 평가 기준 대응표
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_LGRAY)
hdr(slide, "[부록] 캡스톤 평가 기준 대응표", "6개 평가 기준별 구현 내용 및 증거 자료")
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
eval_data = [
    ["평가 기준","가중치","구현 내용","핵심 증거","달성도"],
    ["① 문제 정의 명확성","15%","불법주정차 급증 현황 데이터 기반 정량 분석 및 퍼소나 도출","2024년 역대 최다 233,993건\n3대 핵심 문제 명확 정의","★★★★★"],
    ["② 데이터 활용","20%","2023년 실단속 217,682건\n법정동 미추출 16.7%→1.7% 정제","5개 분석용 CSV 출력\n35개 법정동 전체 커버","★★★★★"],
    ["③ 분석 방법론","20%","재보정위험도·CCTV공백지수\n복합 지표 설계 및 검증","향남읍 6.87점 도출\n금곡동 공백지수 0.733","★★★★☆"],
    ["④ 예측 모델","25%","Prophet+SARIMA 앙상블\n8개 모델 비교 최적 선정","앙상블 MAE 1,451건\nMAPE 6.7% (최고 성능)","★★★★★"],
    ["⑤ 정책 활용","10%","3-Tier 자동 정책 분류\n인력 배치 권고 포함","10월 증원 권장 명시\nCCTV 5개 지역 설치 권고","★★★★☆"],
    ["⑥ 시스템 완성도","10%","Streamlit 5탭 대시보드\n인터랙티브 시각화 완성","Folium 지도·히트맵·예측\n그래프 통합 완성","★★★★☆"],
]
add_table(slide, eval_data, 0.2, 1.22, 12.85, 4.22, font_size=9)
add_rect(slide, 0.2, 5.55, 12.85, 0.35, fill=C_GREEN)
add_text(slide, "종합 평가 요약", 0.3, 5.58, 12.5, 0.27, size=11, bold=True, color=C_WHITE)
add_rect(slide, 0.2, 5.9, 12.85, 0.95, fill=C_WHITE, line=C_GREEN, line_width=1.0)
summary_eval = [
    "• 핵심 평가 항목 ④예측모델(25%)에서 앙상블 MAE 1,451건(MAPE 6.7%) — 8개 모델 비교 최고 성능으로 완성도 입증",
    "• ②데이터활용(20%)에서 51개월 실데이터 정제 및 법정동 미추출률 16.7%→1.7% 개선 — 데이터 품질 우수",
    "• ③분석방법론(20%)에서 재보정위험도·CCTV공백지수 독자 설계 — 학술적 근거와 현장 적용성 겸비",
]
for i, item in enumerate(summary_eval):
    add_text(slide, item, 0.28, 5.95+i*0.3, 12.5, 0.26, size=8.5, color=C_DARK)

# ============================================================
# 슬라이드 16 - [부록] 결론 요약
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_rect(slide, 0, 0, SLIDE_W, SLIDE_H, fill=C_NAVY)
add_rect(slide, 0, 0, SLIDE_W, 0.12, fill=C_ORANGE)
add_text(slide, "[부록] 결론 요약", 0.3, 0.15, 10.0, 0.62, size=22, bold=True, color=C_WHITE)
add_text(slide, "5줄로 정리하는 에네레기파 프로젝트 핵심 기여", 0.3, 0.72, 10.0, 0.35, size=12, color=C_LBLUE)
badge(slide, "APPENDIX", 11.8, 0.15, 1.3, 0.3, bg=C_GRAY, size=9)
final_conclusions = [
    ("①  전처리 & 데이터 품질",C_TEAL,
     "화성시 단속 원천데이터 217,682건 (2023년 실단속 기준), 법정동 미추출 16.7% → 1.7%로 정제, 35개 법정동 분석 확정"),
    ("②  위험도 분석",C_ORANGE,
     "재보정위험도 공식(실단속×0.65 + 민원×0.35) 독자 설계, 향남읍 6.87점 고위험 1위 도출, TOP 7 지역 집중관리 대상 선정"),
    ("③  예측 모델 성능",C_GREEN,
     "Prophet + SARIMA 앙상블 MAE 1,451건·MAPE 6.7% — 8개 모델 중 최고 성능, 전통모델 대비 38% 개선"),
    ("④  정책 추천",C_RED,
     "CCTV 공백지수 0.3 이상 5개 지역 시급 설치 권고, 2026년 10월 피크(21,276건) 대비 단속인력 증원 권장"),
    ("⑤  대시보드 완성",C_PURPLE,
     "Streamlit 5탭 시스템 — 위험도지도·히트맵·위반유형대책·전체현황·예측&정책권고 통합 제공"),
]
for i, (title, color, desc) in enumerate(final_conclusions):
    yt = 1.22+i*0.98
    add_rect(slide, 0.2, yt, 0.5, 0.82, fill=color)
    add_text(slide, str(i+1), 0.2, yt, 0.5, 0.82, size=20, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
    add_rect(slide, 0.7, yt, 8.9, 0.82, fill=RGBColor(0x1E,0x3A,0x5F))
    add_text(slide, title, 0.8, yt+0.04, 3.5, 0.3, size=10, bold=True, color=color)
    add_text(slide, desc, 0.8, yt+0.38, 8.7, 0.4, size=9, color=C_WHITE)
add_rect(slide, 9.75, 1.22, 3.35, 4.9, fill=C_BLUE)
add_text(slide, "Q & A", 9.75, 2.12, 3.35, 0.75, size=30, bold=True, color=C_WHITE, align=PP_ALIGN.CENTER)
add_text(slide, "감사합니다!", 9.75, 2.95, 3.35, 0.6, size=20, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
add_text(slide, "에네레기파", 9.75, 3.65, 3.35, 0.45, size=14, color=C_LBLUE, align=PP_ALIGN.CENTER)
add_text(slide, "임단군 · 정예민 · 안유경", 9.75, 4.12, 3.35, 0.42, size=10, color=C_LBLUE, align=PP_ALIGN.CENTER)
add_text(slide, "지도교수: 김순찬 교수님", 9.75, 4.58, 3.35, 0.35, size=9, color=C_LBLUE, align=PP_ALIGN.CENTER)
add_text(slide, "2026.05.29", 9.75, 4.95, 3.35, 0.35, size=10, bold=True, color=C_YELLOW, align=PP_ALIGN.CENTER)
add_rect(slide, 0, 7.15, SLIDE_W, 0.35, fill=RGBColor(0x0D,0x1A,0x2E))
add_text(slide, "에네레기파 | 지도교수: 김순찬 교수님", 0.2, 7.18, 7.0, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.LEFT)
add_text(slide, "트랙 B 자유주제 No.13  |  2026.05.29", 6.5, 7.18, 6.5, 0.28, size=9, color=C_LBLUE, align=PP_ALIGN.RIGHT)

# ============================================================
# 저장
# ============================================================
output_dir = r"c:\Users\ekss0\Desktop\4학년 1학기\캡스톤디자인2"
filename = "에네레기파_캡스톤디자인2_최종발표.pptx"
output_path = os.path.join(output_dir, filename)
prs.save(output_path)
n = len(prs.slides)
print(f"[OK] 저장 완료: {filename} ({n}장)")