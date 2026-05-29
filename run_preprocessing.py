import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

print("=" * 55)
print("  신규 전처리 시작")
print("=" * 55)

XLSX_PATH = 'data/원본/화성시 불법주정차 단속현황 자료.xlsx'
OUT_DIR   = 'data/전처리_신규/'

# ── 2. 데이터 로드 ────────────────────────────────────────────────
print("\n[1/8] xlsx 로드 중... (217,682건, 잠시 대기)")
sheets = pd.read_excel(XLSX_PATH, sheet_name=None)
df = pd.concat(sheets.values(), ignore_index=True)

df['단속일시'] = pd.to_datetime(df['단속일시'])
df['연도'] = df['단속일시'].dt.year
df['월']   = df['단속일시'].dt.month
df['요일']  = df['단속일시'].dt.dayofweek
df['시간']  = df['단속일시'].dt.hour

print(f"  전체 레코드: {len(df):,}건")
print(f"  기간: {df['단속일시'].min()} ~ {df['단속일시'].max()}")

# ── 3. 행정동 파싱 ────────────────────────────────────────────────
print("\n[2/8] 행정동 파싱 중...")

DONG_ALIAS = {
    '향남': '향남읍', '남양': '남양읍', '봉담': '봉담읍', '우정': '우정읍',
    '마도': '마도면', '송산': '송산면', '서신': '서신면', '팔탄': '팔탄면',
    '양감': '양감면', '정남': '정남면', '비봉': '비봉면', '장안': '장안면',
    '새솔': '새솔동',  # 동탄2신도시 새솔수노을중앙로광장 등
}

TYPO_FIX = {'향납읍': '향남읍'}  # 원본 데이터 오타 교정

def extract_dong(loc):
    if pd.isna(loc):
        return None
    tokens = loc.split()
    for t in tokens[:3]:
        t_clean = re.sub(r'^[^가-힣]+', '', t)
        if re.search(r'(동|읍|면)$', t_clean):
            return TYPO_FIX.get(t_clean, t_clean)
    first = re.sub(r'^[^가-힣]+', '', tokens[0]) if tokens else ''
    # 정확히 일치 먼저
    if first in DONG_ALIAS:
        return DONG_ALIAS[first]
    # 접두어 매칭 (예: '남양굿메이트빌딩앞' → '남양' 접두어)
    for alias, dong_name in DONG_ALIAS.items():
        if first.startswith(alias):
            return dong_name
    return None

df['행정동'] = df['단속장소'].apply(extract_dong)
miss = df['행정동'].isna().sum()
print(f"  추출 완료 | 미추출: {miss}건 ({miss/len(df)*100:.1f}%)")

# ── 4. 위반유형 파싱 ──────────────────────────────────────────────
print("\n[3/8] 위반유형 파싱 중...")
df['위반유형_raw'] = df['단속장소'].str.extract(r'\(([^)]+)\)')
df.loc[df['위반유형_raw'].str.match(r'^\d+$', na=False), '위반유형_raw'] = None

VTYPE_MAP = {
    '횡단보도':      ('횡단보도',      2.0),
    '소화전':        ('소화전',        2.0),
    '버스정류소':    ('버스정류',      2.0),
    '인도':          ('인도',          1.5),
    '도로가장자리':  ('도로가장자리',  1.5),
    '모퉁이·교차로': ('모퉁이|교차로', 1.2),
}

def classify_vtype(raw):
    if pd.isna(raw):
        return ('기타', 1.0)
    for label, (pattern, weight) in VTYPE_MAP.items():
        if re.search(pattern, raw):
            return (label, weight)
    return ('기타', 1.0)

df[['위반유형', '통행불편가중치']] = df['위반유형_raw'].apply(
    lambda x: pd.Series(classify_vtype(x))
)
print("  위반유형 분포:")
for vt, cnt in df['위반유형'].value_counts().items():
    print(f"    {vt:<12} {cnt:>7,}건")

# ── 5. 시간대 피처 ────────────────────────────────────────────────
print("\n[4/8] 시간대 피처 생성 중...")

def time_band(h):
    if 7 <= h < 12:  return '오전피크'
    if 12 <= h < 15: return '점심'
    if 15 <= h < 19: return '오후피크'
    if 19 <= h < 22: return '저녁'
    return '야간'

df['시간대구간'] = df['시간'].apply(time_band)
df['평일여부']   = df['요일'].apply(lambda d: '평일' if d < 5 else '주말')
df['요일명']     = df['요일'].map({0:'월',1:'화',2:'수',3:'목',4:'금',5:'토',6:'일'})
print("  시간대구간 분포:")
for band, cnt in df['시간대구간'].value_counts().items():
    print(f"    {band:<8} {cnt:>7,}건")

df_valid = df[df['행정동'].notna()].copy()

# 50건 미만 행정동 제외 (통계 신뢰성 확보)
dong_counts = df_valid['행정동'].value_counts()
exclude_dongs = dong_counts[dong_counts < 50].index.tolist()
if exclude_dongs:
    print(f"\n  [필터] 50건 미만 행정동 제외: {exclude_dongs}")
df_valid = df_valid[~df_valid['행정동'].isin(exclude_dongs)].copy()

print(f"\n  [필터] 유효 행정동 레코드: {len(df_valid):,}건 | 행정동 수: {df_valid['행정동'].nunique()}")
print("  상위 10 행정동:")
for name, cnt in df_valid['행정동'].value_counts().head(10).items():
    print(f"    {name:<10} {cnt:>7,}건")

# ── 6. OUTPUT 1 — 행정동별 실단속 위험도 ─────────────────────────
print("\n[5/8] 행정동별_실단속위험도.csv 생성 중...")

dong_total = df_valid.groupby('행정동').size().reset_index(name='실단속건수')
dong_민원  = df_valid[df_valid['단속구분'] == '민원(공익제보)'].groupby('행정동').size().reset_index(name='민원건수')
dong_cctv  = df_valid[df_valid['단속구분'].str.contains('CCTV', na=False)].groupby('행정동').size().reset_index(name='CCTV건수')

dong = dong_total.merge(dong_민원, on='행정동', how='left')
dong = dong.merge(dong_cctv,  on='행정동', how='left').fillna(0)

dong['민원비율']          = (dong['민원건수'] / dong['실단속건수']).round(4)
dong['CCTV비율']         = (dong['CCTV건수']  / dong['실단속건수']).round(4)
dong['실단속비율_정규화'] = (dong['실단속건수'] / dong['실단속건수'].sum()).round(6)

scaler = MinMaxScaler(feature_range=(0, 10))
dong['실단속비율_점수'] = scaler.fit_transform(dong[['실단속비율_정규화']]).round(2)
dong['민원비율_점수']   = scaler.fit_transform(dong[['민원비율']]).round(2)

# 공식: 실단속비율×0.65 + 민원비율×0.35
# 상권위험도는 43개 행정동 중 26개(60%)가 결측→0 처리로 왜곡 발생하여 제외
dong['재보정위험도점수'] = (
    dong['실단속비율_점수'] * 0.65 +
    dong['민원비율_점수']   * 0.35
).round(2)

dong['위험등급'] = pd.cut(
    dong['재보정위험도점수'],
    bins=[0, 3, 6, 10],
    labels=['저위험', '중위험', '고위험'],
    include_lowest=True
)
dong = dong.sort_values('재보정위험도점수', ascending=False).reset_index(drop=True)

print("  재보정 위험도 상위 10:")
for _, r in dong.head(10).iterrows():
    print(f"    {r['행정동']:<10} {r['재보정위험도점수']:>5.2f}점  {r['위험등급']}  (실단속 {r['실단속건수']:,.0f}건)")

dong.to_csv(OUT_DIR + '행정동별_실단속위험도.csv', index=False, encoding='utf-8-sig')
print("  → 저장 완료")

# ── 7. OUTPUT 2 — 위반유형 집계 ──────────────────────────────────
print("\n[6/8] 행정동별_위반유형집계.csv 생성 중...")

# CCTV 적발은 위반유형 정보가 없으므로 민원(공익제보) 건만 위반유형 집계
df_민원 = df_valid[df_valid['단속구분'] == '민원(공익제보)'].copy()
민원_유효 = df_민원[df_민원['위반유형'] != '기타']
print(f"  민원 전체: {len(df_민원):,}건  |  유형 명시: {len(민원_유효):,}건  |  CCTV 미기재 제외: {len(df_valid)-len(df_민원):,}건")

vtype_pivot = (
    민원_유효.groupby(['행정동', '위반유형'])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

WEIGHT = {
    '횡단보도': 2.0, '소화전': 2.0, '버스정류소': 2.0,
    '인도': 1.5, '도로가장자리': 1.5, '모퉁이·교차로': 1.2,
}

def calc_idx(row):
    total = sum(row.get(k, 0) * w for k, w in WEIGHT.items())
    cnt   = sum(row.get(k, 0) for k in WEIGHT)
    return round(total / cnt, 4) if cnt > 0 else 0

vtype_pivot['통행불편지수'] = vtype_pivot.apply(calc_idx, axis=1)
# 민원 건수 합계 추가 (행정동별)
민원_cnt = 민원_유효.groupby('행정동').size().reset_index(name='민원_위반유형_건수')
vtype_pivot = vtype_pivot.merge(민원_cnt, on='행정동', how='left').fillna(0)
vtype_pivot = vtype_pivot.merge(
    dong[['행정동', '실단속건수', '재보정위험도점수', '위험등급']],
    on='행정동', how='left'
).sort_values('통행불편지수', ascending=False).reset_index(drop=True)

print("  통행불편지수 상위 10:")
cols = ['행정동','통행불편지수','실단속건수']
for _, r in vtype_pivot[cols].head(10).iterrows():
    print(f"    {r['행정동']:<10} 불편지수 {r['통행불편지수']:.4f}  ({r['실단속건수']:,.0f}건)")

vtype_pivot.to_csv(OUT_DIR + '행정동별_위반유형집계.csv', index=False, encoding='utf-8-sig')
print("  → 저장 완료")

# ── 8. OUTPUT 3 — 시간대별 집계 ──────────────────────────────────
print("\n[7/8] 시간대별_단속집계.csv 생성 중...")

heat = df.groupby(['요일명','시간']).size().reset_index(name='단속건수')
heat_pivot = heat.pivot(index='요일명', columns='시간', values='단속건수').fillna(0).astype(int)
heat_pivot = heat_pivot.reindex(['월','화','수','목','금','토','일'])

print("  요일×피크시간 단속건수 (9시/15시/20시):")
for day in ['월','화','수','목','금','토','일']:
    row = heat_pivot.loc[day]
    print(f"    {day}요일  9시:{row.get(9,0):>5,}  15시:{row.get(15,0):>5,}  20시:{row.get(20,0):>5,}")

heat.to_csv(OUT_DIR + '시간대별_단속집계.csv', index=False, encoding='utf-8-sig')
heat_pivot.reset_index().to_csv(OUT_DIR + '시간대별_단속피벗.csv', index=False, encoding='utf-8-sig')
print("  → 저장 완료")

# ── OUTPUT 3b — 법정동별 시간대 집계 (탭1·2 법정동 필터용) ───────────
dong_heat = df_valid.groupby(['행정동','요일명','시간']).size().reset_index(name='단속건수')
dong_heat.to_csv(OUT_DIR + '법정동별_시간대집계.csv', index=False, encoding='utf-8-sig')
print(f"  법정동별_시간대집계.csv 저장 완료 ({len(dong_heat):,}행)")

# ── 9. OUTPUT 4 — CCTV 공백 지수 ─────────────────────────────────
print("\n[8/8] CCTV공백지수.csv 생성 중...")

cctv_df = dong[['행정동','실단속건수','민원비율','CCTV비율','재보정위험도점수','위험등급']].copy()

fixed = df_valid[df_valid['단속구분'] == '고정형CCTV'].groupby('행정동').size().reset_index(name='고정CCTV건수')
cctv_df = cctv_df.merge(fixed, on='행정동', how='left').fillna({'고정CCTV건수': 0})
cctv_df['고정CCTV비율'] = (cctv_df['고정CCTV건수'] / cctv_df['실단속건수']).round(4)
cctv_df['CCTV공백지수'] = (cctv_df['민원비율'] - cctv_df['고정CCTV비율']).round(4)
cctv_df['CCTV설치우선순위'] = pd.cut(
    cctv_df['CCTV공백지수'], bins=[-1, 0, 0.1, 1],
    labels=['낮음','보통','높음'], include_lowest=True
)
cctv_df = cctv_df.sort_values('CCTV공백지수', ascending=False).reset_index(drop=True)

print("  CCTV 공백 지수 상위 10:")
for _, r in cctv_df.head(10).iterrows():
    print(f"    {r['행정동']:<10} 공백지수 {r['CCTV공백지수']:>6.4f}  우선순위:{r['CCTV설치우선순위']}")

cctv_df.to_csv(OUT_DIR + 'CCTV공백지수.csv', index=False, encoding='utf-8-sig')
print("  → 저장 완료")

# ── 최종 확인 ────────────────────────────────────────────────────
import os
print("\n" + "=" * 55)
print("  전처리 완료! data/전처리_신규/ 생성 파일:")
print("=" * 55)
for f in sorted(os.listdir(OUT_DIR)):
    size = os.path.getsize(OUT_DIR + f)
    print(f"  {f:<45} {size:>10,} bytes")
