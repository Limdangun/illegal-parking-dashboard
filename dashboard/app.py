import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler

# ── 페이지 설정 ─────────────────────────────────────────────────
st.set_page_config(
    page_title="화성시 불법주정차 민원 최소화 정책 지원",
    page_icon="🚔",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 경로 설정 ────────────────────────────────────────────────────
_BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_NEW = os.path.join(_BASE, "data", "전처리_신규")
DATA_OLD = os.path.join(_BASE, "data", "전처리_기존")

# ── 연도별 단속 원데이터 ─────────────────────────────────────────
RAW = {
    "동부출장소\n교통건설과": {
        2021: [1095,1501,1614,1423,1632,1553,1564,1621,1371,1768,1802,1888],
        2022: [1511,1412,1549,1779,1705,1499,2178,1928,2237,2049,2332,1649],
        2023: [1764,1919,2064,1911,1932,1984,2007,1699,1436,1946,2513,1888],
        2024: [2294,1388,1466,2139,2231,2301,2062,1963,1857,2284,2237,2465],
    },
    "주차교통과": {
        2021: [5090,5598,8486,8282,8230,8842,7868,7854,8615,9078,8997,9026],
        2022: [7650,6211,7651,8415,8592,7853,7759,8722,7695,7996,7959,8083],
        2023: [7027,6562,7592,6948,5257,6200,6763,7371,7104,7811,7907,7903],
        2024: [7735,5224,8005,8555,7930,7070,7304,7793,7183,9502,8840,9364],
    },
    "동탄출장소\n교통건설과": {
        2021: [7645,9322,11709,10037,9576,9968,9489,9153,8355,8346,8949,7887],
        2022: [6734,6288,7199,7489,8781,9066,9280,8664,9423,8532,9322,7813],
        2023: [7962,8778,11015,9260,9701,10283,9451,9095,8907,8660,10170,8362],
        2024: [9697,7266,9453,11371,11119,10266,11230,9938,9421,10410,8091,6539],
    },
}
YEAR_TOTALS = {2021: 225234, 2022: 215005, 2023: 219152, 2024: 233993}

# ── 행정동 좌표 ──────────────────────────────────────────────────
COORD = {
    "향남읍": (37.1472, 126.8812), "봉담읍": (37.2042, 126.9238),
    "석우동": (37.1910, 127.0850), "영천동": (37.2080, 127.0670),
    "남양읍": (37.2025, 126.7153), "진안동": (37.1823, 126.8045),
    "오산동": (37.2150, 127.0720), "반송동": (37.1850, 127.0780),
    "산척동": (37.2190, 127.0610), "우정읍": (37.0892, 126.8245),
    "서신면": (37.1600, 126.7800), "팔탄면": (37.1853, 126.9142),
    "송산면": (37.0800, 126.8700), "마도면": (37.1100, 126.8100),
    "비봉면": (37.2650, 126.9500), "정남면": (37.1685, 127.0162),
    "양감면": (37.1350, 126.9500), "매송면": (37.2423, 126.8934),
    "방교동": (37.2110, 126.8900), "병점동": (37.2056, 126.8765),
    "새솔동": (37.2245, 127.0523), "기배동": (37.1820, 126.8234),
    "반월동": (37.1934, 126.8312), "장안면": (37.1236, 126.8953),
    "송산동": (37.2010, 127.0540), "장지동": (37.2100, 127.0900),
    "송동":   (37.1950, 127.0480), "능동":   (37.2060, 127.0590),
    "신동":   (37.1980, 127.0440), "청계동": (37.2140, 127.0800),
    "기안동": (37.2000, 127.0630), "목동":   (37.2070, 127.0560),
    "안녕동": (37.1760, 126.8100), "배양동": (37.1890, 126.8200),
    "반정동": (37.1970, 126.8350), "금곡동": (37.2220, 126.8650),
}
_DEFAULT_COORD = (37.1995, 126.8600)

# ── 데이터 로더 ──────────────────────────────────────────────────
@st.cache_data
def build_monthly_df():
    rows = []
    for dept, years in RAW.items():
        for year, months in years.items():
            for m, val in enumerate(months, 1):
                rows.append({"부서": dept, "연도": year, "월": m, "건수": val})
    return pd.DataFrame(rows)

@st.cache_data(ttl=60)
def load_pivot():
    df = pd.read_csv(os.path.join(DATA_NEW, "시간대별_단속피벗.csv"), encoding="utf-8-sig")
    df = df.set_index("요일명")
    df.columns = [int(c) for c in df.columns]
    return df.reindex(["월","화","수","목","금","토","일"])

@st.cache_data(ttl=60)
def load_vtype():
    return pd.read_csv(os.path.join(DATA_NEW, "행정동별_위반유형집계.csv"), encoding="utf-8-sig")

@st.cache_data(ttl=60)
def load_risk():
    return pd.read_csv(os.path.join(DATA_NEW, "행정동별_실단속위험도.csv"), encoding="utf-8-sig")

@st.cache_data(ttl=60)
def load_cctv():
    return pd.read_csv(os.path.join(DATA_NEW, "CCTV공백지수.csv"), encoding="utf-8-sig")

@st.cache_data(ttl=60)
def load_dong_heat():
    df = pd.read_csv(os.path.join(DATA_NEW, "법정동별_시간대집계.csv"), encoding="utf-8-sig")
    return df

@st.cache_data
def load_monthly_model_data():
    return pd.read_csv(os.path.join(DATA_OLD, "월별통합데이터_전처리_v2.csv"), encoding="utf-8-sig")

@st.cache_data
def train_ensemble_and_predict(n_future: int = 6):
    """Prophet + SARIMA 가중 앙상블 예측"""
    import datetime
    import warnings
    from prophet import Prophet
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    raw = load_monthly_model_data()
    ts = raw[["연도", "월", "단속건수"]].copy()
    ts["날짜"] = pd.to_datetime({"year": ts["연도"], "month": ts["월"], "day": 1})
    ts = ts.sort_values("날짜").reset_index(drop=True)
    y = ts["단속건수"].values

    train_mask = ts["연도"] <= 2024
    test_mask  = ts["연도"] >= 2025
    y_train = y[train_mask]
    y_test  = y[test_mask]
    n_test  = len(y_test)

    # ── 타겟 윈도우: 오늘 기준 다음달부터 n_future개월 ───────────────
    today         = datetime.date.today()
    win_month     = today.month % 12 + 1
    win_year      = today.year + today.month // 12
    win_start_abs = win_year * 12 + win_month
    last_year     = int(ts["연도"].iloc[-1])
    last_month    = int(ts["월"].iloc[-1])
    last_abs      = last_year * 12 + last_month
    total_ahead   = max(win_start_abs - last_abs + n_future - 1, n_future)

    # future 날짜 목록 (전체 → 슬라이스)
    future_dates_all = pd.date_range(
        start=ts["날짜"].iloc[-1] + pd.DateOffset(months=1),
        periods=total_ahead, freq="MS")
    future_info_all = [
        {"연도": int(d.year), "월": int(d.month)} for d in future_dates_all
    ]

    # ── Model 1: Prophet ──────────────────────────────────────────
    prophet_ok = False
    pred_p_te     = np.zeros(n_test)
    pred_p_fu_all = np.zeros(total_ahead)
    mae_p = None
    prophet_components = None
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            # 검증용: 훈련 데이터만으로 out-of-sample MAE 산출
            prophet_train_df = pd.DataFrame({
                "ds": ts[train_mask]["날짜"].values,
                "y":  y_train.astype(float)
            })
            m_prophet = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                seasonality_mode="multiplicative",
                changepoint_prior_scale=0.05,
            )
            m_prophet.fit(prophet_train_df)

            if n_test > 0:
                val_future = m_prophet.make_future_dataframe(
                    periods=n_test + total_ahead, freq="MS")
                val_fc    = m_prophet.predict(val_future)
                all_pred  = val_fc["yhat"].values
                pred_p_te     = all_pred[:n_test]
                pred_p_fu_all = all_pred[n_test: n_test + total_ahead]
                mae_p = float(np.mean(np.abs(y_test - pred_p_te)))
            else:
                val_future = m_prophet.make_future_dataframe(
                    periods=total_ahead, freq="MS")
                pred_p_fu_all = m_prophet.predict(val_future)["yhat"].values[-total_ahead:]

            # 컴포넌트 추출: 전체 데이터로 재학습 → 더 정확한 추세 시각화
            m_full = Prophet(
                yearly_seasonality=True, weekly_seasonality=False,
                daily_seasonality=False, seasonality_mode="multiplicative",
                changepoint_prior_scale=0.05,
            )
            m_full.fit(pd.DataFrame({
                "ds": ts["날짜"], "y": ts["단속건수"].astype(float)
            }))
            full_fc = m_full.predict(
                m_full.make_future_dataframe(periods=total_ahead, freq="MS"))
            prophet_components = full_fc[["ds", "trend", "yearly"]].copy()
            prophet_ok = True
    except Exception:
        pass

    # ── Model 2: SARIMA ───────────────────────────────────────────
    # 1차: (1,1,1)(1,0,1,12) D=0 (계절 차분 생략)
    # 폴백: (1,1,1)(1,1,0,12) — D=0 발산 시 D=1로 안전 복구
    sarima_ok = False
    pred_s_te     = np.zeros(n_test)
    pred_s_fu_all = np.zeros(total_ahead)
    mae_s = None
    for _s_order in [(1,0,1,12), (1,1,0,12)]:
        try:
            sarima_fit = SARIMAX(
                y_train, order=(1,1,1), seasonal_order=_s_order,
                enforce_stationarity=False, enforce_invertibility=False
            ).fit(disp=False)
            sarima_all = sarima_fit.forecast(n_test + total_ahead)
            if (np.any(~np.isfinite(sarima_all)) or
                    np.any(sarima_all < 0) or np.any(sarima_all > 5e5)):
                raise ValueError("SARIMA forecast out of bounds")
            pred_s_te     = sarima_all[:n_test]
            pred_s_fu_all = sarima_all[n_test:].astype(float)
            mae_s = float(np.mean(np.abs(y_test - pred_s_te))) if n_test > 0 else None
            sarima_ok = True
            break
        except Exception:
            continue

    # ── 가중 앙상블 (MAE 역수 가중) ──────────────────────────────────
    # 검증 MAE 기반 가중치 계산 (둘 다 실패 시 단순 평균)
    def _weights(mp, ms):
        if mp and ms:
            wp = 1.0 / mp
            ws = 1.0 / ms
            total = wp + ws
            return wp / total, ws / total
        if mp:  return 1.0, 0.0
        if ms:  return 0.0, 1.0
        return 0.5, 0.5

    w_p, w_s = _weights(mae_p, mae_s)

    # 검증 구간 앙상블
    n_align = min(len(pred_p_te), len(pred_s_te), n_test)
    ens_te = w_p * pred_p_te[-n_align:] + w_s * pred_s_te[-n_align:]
    mae_e  = float(np.mean(np.abs(y_test[-n_align:] - ens_te))) if n_align > 0 else None

    # 미래 앙상블 (전체)
    pred_e_fu_all = (w_p * pred_p_fu_all + w_s * pred_s_fu_all).astype(int)

    # ── 타겟 윈도우 슬라이스 ──────────────────────────────────────────
    tgt_idx = [i for i, fi in enumerate(future_info_all)
               if win_start_abs <= fi["연도"] * 12 + fi["월"] < win_start_abs + n_future]
    future_info   = [future_info_all[i] for i in tgt_idx]
    pred_p_fu     = pred_p_fu_all[tgt_idx].astype(int)
    pred_s_fu     = pred_s_fu_all[tgt_idx].astype(int)
    pred_e_fu     = pred_e_fu_all[tgt_idx]

    return dict(
        ts=ts, train_mask=train_mask, test_mask=test_mask,
        y_train=y_train, y_test=y_test,
        pred_p_te=pred_p_te, pred_s_te=pred_s_te, ens_te=ens_te,
        mae_p=mae_p, mae_s=mae_s, mae_e=mae_e,
        future_info=future_info,
        pred_p_fu=pred_p_fu, pred_s_fu=pred_s_fu, pred_e_fu=pred_e_fu,
        prophet_ok=prophet_ok, sarima_ok=sarima_ok, n_align=n_align,
        prophet_components=prophet_components,
        w_p=w_p, w_s=w_s,
    )

# ── 정책 추천 엔진 ───────────────────────────────────────────────
def build_policy_table(risk_df: pd.DataFrame, cctv_df: pd.DataFrame,
                        vtype_df: pd.DataFrame) -> pd.DataFrame:
    """법정동별 개입 방식 추천 — 단속강화 / CCTV설치 우선순위 분리"""
    merged = risk_df.merge(
        cctv_df[["행정동","CCTV공백지수","CCTV설치우선순위","고정CCTV비율"]],
        on="행정동", how="left"
    ).merge(
        vtype_df[["행정동","통행불편지수"]],
        on="행정동", how="left"
    )
    merged["CCTV공백지수"] = merged["CCTV공백지수"].fillna(0)
    merged["통행불편지수"] = merged["통행불편지수"].fillna(0)

    # 통행불편지수 0~10 정규화 (재보정위험도점수와 스케일 통일)
    # 미기재(0) 제외하고 실제 값만으로 min/max 계산
    _vt_nonzero = merged.loc[merged["통행불편지수"] > 0, "통행불편지수"]
    if len(_vt_nonzero) > 1:
        _vt_min = _vt_nonzero.min()
        _vt_max = _vt_nonzero.max()
        merged["통행불편지수_정규화"] = merged["통행불편지수"].apply(
            lambda x: round(((x - _vt_min) / (_vt_max - _vt_min)) * 10, 3) if x > 0 else 0
        )
    else:
        merged["통행불편지수_정규화"] = merged["통행불편지수"]

    # 단속 강화 우선순위
    # 통행불편지수 미기재: 재보정위험도 단일 기준
    # 통행불편지수 있음: 재보정위험도×0.7 + 통행불편지수(정규화)×0.3
    def calc_enforcement(row):
        if row["통행불편지수"] == 0:
            return round(row["재보정위험도점수"], 3)
        return round(row["재보정위험도점수"] * 0.7 + row["통행불편지수_정규화"] * 0.3, 3)

    merged["단속강화_우선순위"] = merged.apply(calc_enforcement, axis=1)

    # CCTV 설치 우선순위: 공백지수 중심 (실단속 50건↑ & 공백>0 필터)
    cctv_mask = (merged["실단속건수"] >= 50) & (merged["CCTV공백지수"] > 0)
    merged["CCTV설치_우선순위"] = (
        merged["CCTV공백지수"]     * 0.8 +
        merged["재보정위험도점수"] * 0.2
    ).where(cctv_mask, 0).round(3)

    def recommend(row):
        if row["CCTV설치_우선순위"] > 0:
            return "📷 CCTV 설치"
        if row["단속강화_우선순위"] >= 3.5:
            return "🚔 단속 강화"
        if row["통행불편지수"] >= 1.4:
            return "🪧 안내·계도"
        return "✅ 현행 유지"

    merged["추천 개입"] = merged.apply(recommend, axis=1)
    merged["통행불편지수_표시"] = merged["통행불편지수"].apply(
        lambda x: "미기재" if x == 0 else f"{x:.4f}"
    )
    return merged.reset_index(drop=True)

# ── 유틸리티 ─────────────────────────────────────────────────────
def risk_color(score, low_t, high_t):
    if score >= high_t: return "#FF3B30"
    if score >= low_t:  return "#FF9500"
    return "#34C759"

def risk_label(color):
    return {"#FF3B30":"🔴 고위험","#FF9500":"🟠 중위험","#34C759":"🟢 저위험"}[color]

# ── 데이터 로드 ──────────────────────────────────────────────────
try:
    pivot_df      = load_pivot()
    vtype_df      = load_vtype()
    risk_df       = load_risk()
    cctv_df       = load_cctv()
    dong_heat_df  = load_dong_heat()
    # 재보정위험도 재계산: 상권위험도 제거, 실단속비율×0.65 + 민원비율×0.35
    if not risk_df.empty and "실단속비율_점수" in risk_df.columns and "민원비율_점수" in risk_df.columns:
        from sklearn.preprocessing import MinMaxScaler as _MMS
        _s = _MMS(feature_range=(0, 10))
        risk_df["실단속비율_점수"] = _s.fit_transform(risk_df[["실단속비율_정규화"]]).round(2)
        risk_df["민원비율_점수"]   = _s.fit_transform(risk_df[["민원비율"]]).round(2)
        risk_df["재보정위험도점수"] = (
            risk_df["실단속비율_점수"] * 0.65 +
            risk_df["민원비율_점수"]   * 0.35
        ).round(2)
        risk_df["위험등급"] = pd.cut(
            risk_df["재보정위험도점수"],
            bins=[0, 3, 6, 10], labels=["저위험","중위험","고위험"], include_lowest=True
        ).astype(str)
        risk_df = risk_df.sort_values("재보정위험도점수", ascending=False).reset_index(drop=True)
    _data_ok = True
except Exception as e:
    st.error(f"데이터 파일 로드 실패: {e}")
    _data_ok = False
    pivot_df = vtype_df = risk_df = cctv_df = dong_heat_df = pd.DataFrame()

# ── 지도용 데이터 구성 ───────────────────────────────────────────
if _data_ok and not risk_df.empty:
    risk_scores = {r["행정동"]: r["재보정위험도점수"] for _, r in risk_df.iterrows()}
    cctv_gaps   = {r["행정동"]: r["CCTV공백지수"] for _, r in cctv_df.iterrows()} if not cctv_df.empty else {}
    AREAS = [(d, *COORD.get(d, _DEFAULT_COORD), s) for d, s in risk_scores.items()]
    counts_all  = [a[3] for a in AREAS]
    HIGH_THRESH = np.percentile(counts_all, 70)
    LOW_THRESH  = np.percentile(counts_all, 30)
else:
    AREAS = [("데이터없음", 37.1995, 126.8600, 0)]
    cctv_gaps = {}
    HIGH_THRESH, LOW_THRESH = 5.0, 2.0

# ── 사이드바 ─────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 대시보드 필터")

    st.markdown("**📅 기간**")
    selected_year = st.selectbox("연도", [2024, 2023, 2022, 2021], label_visibility="collapsed")
    month_range   = st.slider("월 범위", 1, 12, (1, 12))
    mo_label = f"{month_range[0]}월" if month_range[0] == month_range[1] else f"{month_range[0]}월 ~ {month_range[1]}월"
    st.caption(f"선택 기간: {selected_year}년 {mo_label}")

    st.divider()
    st.markdown("**🚗 위반 유형** (탭3 반영)")
    viol_all    = st.checkbox("전체 선택", value=True, key="viol_all")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        viol_cross  = st.checkbox("횡단보도",      value=True, disabled=viol_all)
        viol_fire   = st.checkbox("소화전",        value=True, disabled=viol_all)
        viol_corner = st.checkbox("모퉁이·교차로", value=True, disabled=viol_all)
    with col_v2:
        viol_walk   = st.checkbox("인도",          value=True, disabled=viol_all)
        viol_bus    = st.checkbox("버스정류소",    value=True, disabled=viol_all)

    st.divider()
    st.markdown("**🗺️ 지도 설정**")
    map_layer   = st.radio("표시 기준", ["위험도 점수", "CCTV 공백지수"], horizontal=True)
    show_labels = st.toggle("지역명 표시", value=True)
    map_tile    = st.radio("지도 스타일", ["밝은 배경", "어두운 배경"], horizontal=True)
    tile_map = {"밝은 배경": "CartoDB positron", "어두운 배경": "CartoDB dark_matter"}[map_tile]

    st.divider()
    # 현재 활성 필터 요약
    import datetime as _dt
    _today = _dt.date.today()
    _today_day = ["월","화","수","목","금","토","일"][_today.weekday()]
    st.caption(f"📅 오늘: {_today.strftime('%Y.%m.%d')} ({_today_day}요일)")
    st.caption("📊 2023년 단속현황 217,682건 기반")
    st.caption("ℹ️ 분석 법정동: 35개 (50건 미만 7개 동 제외)")

VTYPE_MAP = {"횡단보도": viol_cross, "인도": viol_walk, "소화전": viol_fire,
             "버스정류소": viol_bus, "모퉁이·교차로": viol_corner}
selected_vtypes = list(VTYPE_MAP.keys()) if viol_all else [k for k, v in VTYPE_MAP.items() if v]

# ── 헤더 ─────────────────────────────────────────────────────────
st.title("🚔 화성시 불법주정차 통행불편 민원 최소화 정책 지원")
st.caption("단속 현황 분석 → 개입 방식 추천 → 민원 감소 효과 예측 | 2023년 실단속 217,682건 기반")

# ── KPI 카드 ─────────────────────────────────────────────────────
_df_kpi = build_monthly_df()
_kpi_now  = _df_kpi[(_df_kpi["연도"] == selected_year) &
                     (_df_kpi["월"] >= month_range[0]) & (_df_kpi["월"] <= month_range[1])]
_kpi_prev = _df_kpi[(_df_kpi["연도"] == selected_year - 1) &
                     (_df_kpi["월"] >= month_range[0]) & (_df_kpi["월"] <= month_range[1])]
total_now  = int(_kpi_now["건수"].sum())
total_prev = int(_kpi_prev["건수"].sum()) if len(_kpi_prev) > 0 else total_now
delta_pct  = (total_now - total_prev) / total_prev * 100 if total_prev > 0 else 0

if _data_ok and not risk_df.empty and not cctv_df.empty:
    top_risk = risk_df.iloc[0]
    need_cctv = (cctv_df["CCTV설치우선순위"] == "높음").sum()
    high_complaint = int((risk_df["민원건수"] / risk_df["실단속건수"] >= 0.3).sum())
else:
    top_risk = pd.Series({"행정동": "–", "실단속건수": 0})
    need_cctv = high_complaint = 0

c1, c2, c3, c4 = st.columns(4)
c1.metric(f"📋 단속 건수 ({mo_label})", f"{total_now:,}건",     f"{delta_pct:+.1f}% vs 전년 동기")
c2.metric("🚔 단속 강화 1순위",    top_risk["행정동"],        f"위험도 {top_risk.get('재보정위험도점수', 0):.2f}점")
c3.metric("📷 CCTV 설치 필요 지역", f"{need_cctv}개 지역",    "공백지수 기준")
c4.metric("⚠️ 민원 집중 지역",      f"{high_complaint}개 지역","민원비율 30% 이상")

st.divider()

# ── 지도 + 우측 패널 ─────────────────────────────────────────────
map_col, side_col = st.columns([3, 2])

with map_col:
    layer_title = "CCTV 공백 지수" if map_layer == "CCTV 공백지수" else "재보정 위험도"
    st.subheader(f"📍 행정동별 {layer_title} 지도")
    if map_layer == "CCTV 공백지수":
        st.caption("원 크기 = CCTV공백지수 | 빨강 = CCTV 설치 시급 지역")
    else:
        st.caption("원 크기 = 재보정위험도 | 빨강 = 고위험(단속 강화 필요) | 공식: 실단속비율×0.65 + 민원비율×0.35")

    m = folium.Map(location=[37.1995, 126.8600], zoom_start=11, tiles=tile_map)

    for name, lat, lon, score in AREAS:
        if map_layer == "CCTV 공백지수":
            gap = cctv_gaps.get(name, 0)
            display_val = gap
            if gap >= 0.3:   color = "#FF3B30"
            elif gap >= 0.1: color = "#FF9500"
            else:            color = "#34C759"
            radius = max(300, min(2000, gap * 2000))
            tooltip_txt = f"<b>{name}</b><br>CCTV공백지수: {gap:.3f}"
        else:
            display_val = score
            color  = risk_color(score, LOW_THRESH, HIGH_THRESH)
            radius = max(300, min(2200, score * 250))
            tooltip_txt = f"<b>{name}</b><br>위험도: {score:.2f}점"

        cnt = int(risk_df[risk_df["행정동"] == name]["실단속건수"].values[0]) if (
            _data_ok and name in risk_df["행정동"].values) else 0
        gap_val = cctv_gaps.get(name, 0)
        cctv_priority = cctv_df[cctv_df["행정동"] == name]["CCTV설치우선순위"].values
        cctv_p_str = cctv_priority[0] if len(cctv_priority) > 0 else "–"

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius / 100,
            color=color, weight=2,
            fill=True, fill_color=color, fill_opacity=0.65,
            tooltip=tooltip_txt,
            popup=folium.Popup(
                f"""<div style='font-family:sans-serif;min-width:180px'>
                    <b style='font-size:14px'>{name}</b><hr style='margin:4px 0'>
                    재보정위험도: <b>{score:.2f}점</b> ({risk_label(risk_color(score,LOW_THRESH,HIGH_THRESH))})<br>
                    실단속건수: <b>{cnt:,}건</b><br>
                    CCTV공백지수: <b>{gap_val:.3f}</b><br>
                    CCTV설치우선순위: <b>{cctv_p_str}</b>
                </div>""", max_width=240),
        ).add_to(m)

        if show_labels:
            folium.Marker(
                location=[lat + 0.003, lon],
                icon=folium.DivIcon(
                    html=f'<div style="font-size:10px;font-weight:bold;color:#333;white-space:nowrap">{name}</div>',
                    icon_size=(80, 20), icon_anchor=(40, 0)),
            ).add_to(m)

    if map_layer == "CCTV 공백지수":
        legend_html = """<div style="position:fixed;bottom:30px;right:10px;z-index:9999;
            background:white;color:#222;padding:10px 14px;border-radius:10px;
            box-shadow:0 2px 8px rgba(0,0,0,0.25);font-family:sans-serif;font-size:13px">
            <b style="color:#222">CCTV 공백지수</b><br>
            <span style="color:#FF3B30;font-size:18px">●</span><span style="color:#222"> 설치 시급 (≥0.3)</span><br>
            <span style="color:#FF9500;font-size:18px">●</span><span style="color:#222"> 보통 (0.1~0.3)</span><br>
            <span style="color:#34C759;font-size:18px">●</span><span style="color:#222"> 충분 (&lt;0.1)</span><br>
            <small style="color:#666">공백지수 = 민원비율 − 고정CCTV비율</small></div>"""
    else:
        legend_html = """<div style="position:fixed;bottom:30px;right:10px;z-index:9999;
            background:white;color:#222;padding:10px 14px;border-radius:10px;
            box-shadow:0 2px 8px rgba(0,0,0,0.25);font-family:sans-serif;font-size:13px">
            <b style="color:#222">재보정 위험도</b><br>
            <span style="color:#FF3B30;font-size:18px">●</span><span style="color:#222"> 고위험 (상위 30%)</span><br>
            <span style="color:#FF9500;font-size:18px">●</span><span style="color:#222"> 중위험 (30~70%)</span><br>
            <span style="color:#34C759;font-size:18px">●</span><span style="color:#222"> 저위험 (하위 30%)</span></div>"""
    m.get_root().html.add_child(folium.Element(legend_html))
    st_folium(m, width=720, height=500, returned_objects=[])

with side_col:
    if _data_ok and not risk_df.empty and not cctv_df.empty:
        policy_df = build_policy_table(risk_df, cctv_df, vtype_df)

        st.subheader("🚔 단속 강화 TOP 5")
        enf_top = policy_df.sort_values("단속강화_우선순위", ascending=False).head(5)
        max_enf = enf_top["단속강화_우선순위"].max()
        for rank, (_, r) in enumerate(enf_top.iterrows(), 1):
            score = r["재보정위험도점수"]
            color = risk_color(score, LOW_THRESH, HIGH_THRESH)
            bar_w = int(r["단속강화_우선순위"] / max_enf * 100)
            st.markdown(
                f"""<div style='margin-bottom:8px'>
                    <b>{rank}위 {r['행정동']}</b>
                    <span style='float:right;color:{color};font-weight:bold'>{score:.2f}점</span><br>
                    <small style='opacity:0.75'>{r['위험등급']} | 실단속 {int(r['실단속건수']):,}건</small><br>
                    <div style='background:rgba(128,128,128,0.2);border-radius:4px;height:5px;margin-top:3px'>
                      <div style='background:{color};width:{bar_w}%;height:5px;border-radius:4px'></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.divider()
        st.subheader("📷 CCTV 설치 TOP 5")
        cctv_top = policy_df[policy_df["CCTV설치_우선순위"] > 0].sort_values("CCTV설치_우선순위", ascending=False).head(5)
        max_cctv = cctv_top["CCTV설치_우선순위"].max() if not cctv_top.empty else 1
        for rank, (_, r) in enumerate(cctv_top.iterrows(), 1):
            gap = r["CCTV공백지수"]
            bar_w = int(r["CCTV설치_우선순위"] / max_cctv * 100)
            st.markdown(
                f"""<div style='margin-bottom:8px'>
                    <b>{rank}위 {r['행정동']}</b>
                    <span style='float:right;color:#e67e22;font-weight:bold'>공백 {gap:.3f}</span><br>
                    <small style='opacity:0.75'>실단속 {int(r['실단속건수']):,}건 | CCTV공백 {r['CCTV공백지수']:.3f}</small><br>
                    <div style='background:rgba(128,128,128,0.2);border-radius:4px;height:5px;margin-top:3px'>
                      <div style='background:#e67e22;width:{bar_w}%;height:5px;border-radius:4px'></div>
                    </div>
                </div>""", unsafe_allow_html=True)
    else:
        st.warning("데이터를 불러올 수 없습니다.")

    st.divider()
    st.subheader(f"📈 {selected_year}년 월별 추이")
    df_mb = build_monthly_df()
    df_y  = df_mb[df_mb["연도"] == selected_year].groupby("월")["건수"].sum().reset_index()
    # 선택 월 범위 강조
    df_y["선택"] = df_y["월"].between(month_range[0], month_range[1])
    fig_mini = go.Figure()
    fig_mini.add_trace(go.Bar(
        x=df_y["월"], y=df_y["건수"],
        marker_color=["#FF6B6B" if s else "#DDDDDD" for s in df_y["선택"]],
        hovertemplate="%{x}월: %{y:,}건<extra></extra>"))
    fig_mini.update_layout(height=170, margin=dict(t=5,b=5,l=5,r=5),
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            showlegend=False)
    fig_mini.update_xaxes(tickvals=list(range(1,13)), ticktext=[f"{i}월" for i in range(1,13)])
    st.plotly_chart(fig_mini, use_container_width=True)

st.divider()

# ── 탭 ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab_all, tab4 = st.tabs([
    "📅 연도별 추이",
    "🕐 단속 집중 시간대",
    "📊 위반유형별 대책",
    "🗂️ 전체 현황",
    "🔮 예측 모델 & 정책 추천",
])

# ── 탭1: 연도별 비교 ──────────────────────────────────────────────
with tab1:
    df_all = build_monthly_df()
    # month_range 필터 적용
    df_filtered = df_all[(df_all["월"] >= month_range[0]) & (df_all["월"] <= month_range[1])]
    df_total = df_filtered.groupby(["연도","월"])["건수"].sum().reset_index()
    df_total["연도"] = df_total["연도"].astype(str)

    title_str = f"연도별 월간 단속 건수 ({mo_label} 기준, 2021~2024)"
    fig = px.line(df_total, x="월", y="건수", color="연도", markers=True,
                  color_discrete_map={"2021":"#636EFA","2022":"#EF553B","2023":"#00CC96","2024":"#AB63FA"},
                  title=title_str, labels={"건수":"단속 건수 (건)","월":""})
    fig.update_xaxes(tickvals=list(range(month_range[0], month_range[1]+1)),
                     ticktext=[f"{i}월" for i in range(month_range[0], month_range[1]+1)])
    fig.update_layout(height=400, hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # 선택 기간 연도별 합계 비교
    summary_rows = []
    for yr in [2021, 2022, 2023, 2024]:
        total = int(df_filtered[df_filtered["연도"] == yr]["건수"].sum())
        prev  = int(df_filtered[df_filtered["연도"] == yr-1]["건수"].sum()) if yr > 2021 else 0
        yoy   = f"{(total-prev)/prev*100:+.1f}%" if prev > 0 else "–"
        summary_rows.append({"연도": str(yr), f"단속 건수 ({mo_label})": f"{total:,}건", "전년 동기 대비": yoy})
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

# ── 탭2: 단속 집중 시간대 ─────────────────────────────────────────
with tab2:
    if not _data_ok or pivot_df.empty:
        st.error("데이터를 불러올 수 없습니다.")
    else:
        st.markdown("### 🕐 언제 단속해야 통행불편이 줄어드나?")
        st.caption("단속 건수가 많은 시간대 = 불법주정차가 집중되는 시간대 → 이 때 집중 단속하면 통행불편 예방 효과 최대")

        # ── 법정동 선택 ──
        dong_options2 = ["전체 (화성시 합계)"] + (
            risk_df.sort_values("실단속건수", ascending=False)["행정동"].tolist()
            if _data_ok and not risk_df.empty else []
        )
        sel_dong2 = st.selectbox("🔍 법정동 선택 (전체 또는 특정 법정동 히트맵)", dong_options2, key="tab2_dong")

        import datetime as _dt2
        _today_idx = _dt2.date.today().weekday()
        _day_kr = ["월","화","수","목","금","토","일"]
        _today_kr = _day_kr[_today_idx]
        hour_labels = [f"{h:02d}:00" for h in range(24)]

        # 선택에 따라 피벗 생성
        if sel_dong2 == "전체 (화성시 합계)":
            cur_pivot = pivot_df
            heat_title = f"전체 화성시 — 요일×시간대별 단속 건수 (오늘: {_today_kr}요일)"
        else:
            if not dong_heat_df.empty:
                _sub = dong_heat_df[dong_heat_df["행정동"] == sel_dong2]
                cur_pivot = (
                    _sub.groupby(["요일명","시간"])["단속건수"].sum()
                    .unstack(fill_value=0)
                    .reindex(["월","화","수","목","금","토","일"])
                    .fillna(0).astype(int)
                )
            else:
                cur_pivot = pivot_df
            heat_title = f"{sel_dong2} — 요일×시간대별 단속 건수 (오늘: {_today_kr}요일)"

        days   = cur_pivot.index.tolist()
        z_vals = cur_pivot.values.tolist()

        fig_heat = go.Figure(data=go.Heatmap(
            z=z_vals, x=hour_labels, y=days,
            colorscale="RdYlGn_r",
            text=[[f"{v:,}" for v in row] for row in z_vals],
            texttemplate="%{text}",
            colorbar=dict(title="단속건수"),
            hovertemplate="<b>%{y}요일 %{x}</b><br>단속건수: <b>%{z:,}건</b><br>→ 이 시간대 집중 단속 효과 높음<extra></extra>",
        ))
        if _today_kr in days:
            _today_y = days.index(_today_kr)
            fig_heat.add_shape(type="rect",
                x0=-0.5, x1=23.5, y0=_today_y-0.5, y1=_today_y+0.5,
                line=dict(color="#0066FF", width=3), fillcolor="rgba(0,102,255,0)")
            fig_heat.add_annotation(x=23.8, y=_today_y, text="← 오늘",
                showarrow=False, font=dict(color="#0066FF", size=12, family="Arial Black"))
        fig_heat.update_layout(
            title=heat_title,
            height=400, xaxis_title="시간대", yaxis_title="요일", xaxis=dict(tickangle=-45))
        st.plotly_chart(fig_heat, use_container_width=True)

        # 피크 시간대 → 집중 단속 추천
        hourly = cur_pivot.sum(axis=0).sort_values(ascending=False)
        top3h  = hourly.head(3).index.tolist()
        today_peak = cur_pivot.loc[_today_kr].idxmax() if _today_kr in cur_pivot.index else top3h[0]
        st.info(f"**오늘 ({_today_kr}요일) 집중 단속 권장 시간대: {today_peak:02d}:00 ~ {(today_peak+2)%24:02d}:00**  "
                f"— 해당 시간 단속 건수 {int(cur_pivot.loc[_today_kr, today_peak] if _today_kr in cur_pivot.index else 0):,}건")

        col_a, col_b, col_c = st.columns(3)
        for col, h, rank in zip([col_a, col_b, col_c], top3h, ["1순위","2순위","3순위"]):
            col.success(
                f"**{rank} 집중 단속 시간대**\n\n"
                f"**{h:02d}:00 ~ {(h+2)%24:02d}:00**\n\n"
                f"연간 {int(hourly[h]):,}건 단속 집중\n\n"
                f"→ 이 시간 단속 강화 시 통행 방해 예방 효과 최대"
            )

        st.markdown("---")
        # 평일 vs 주말 전략
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("**📅 평일 vs 주말 단속 전략**")
            weekday_h = cur_pivot.loc[["월","화","수","목","금"]].sum(axis=0)
            weekend_h = cur_pivot.loc[["토","일"]].sum(axis=0)
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(x=hour_labels, y=weekday_h.values, name="평일", marker_color="#4C72B0", opacity=0.8))
            fig_comp.add_trace(go.Bar(x=hour_labels, y=weekend_h.values, name="주말", marker_color="#DD8452", opacity=0.8))
            fig_comp.update_layout(height=280, barmode="group", margin=dict(t=10,b=10),
                                    xaxis=dict(tickangle=-45), legend=dict(orientation="h"))
            st.plotly_chart(fig_comp, use_container_width=True)
        with col_r:
            label_str = sel_dong2 if sel_dong2 != "전체 (화성시 합계)" else "화성시 전체"
            st.markdown(f"**💡 [{label_str}] 시간대별 단속 효과 가이드**")

            # 시간대 구간별 단속건수 집계
            BAND_HOURS = {
                "오전 피크": (list(range(7, 12)),  "07:00~12:00"),
                "점심":      (list(range(12, 15)), "12:00~15:00"),
                "오후 피크": (list(range(15, 19)), "15:00~19:00"),
                "저녁":      (list(range(19, 22)), "19:00~22:00"),
                "야간":      (list(range(22, 24)) + list(range(0, 7)), "22:00~07:00"),
            }
            band_totals = {}
            for bname, (bhours, _) in BAND_HOURS.items():
                vcols = [h for h in bhours if h in cur_pivot.columns]
                band_totals[bname] = int(cur_pivot[vcols].values.sum()) if vcols else 0

            total_cnt = sum(band_totals.values()) or 1
            peak_band = max(band_totals, key=band_totals.get)

            # 해당 법정동 위반유형 TOP1 (있는 경우)
            vtype_tip = {}
            if sel_dong2 != "전체 (화성시 합계)" and not vtype_df.empty:
                vrow = vtype_df[vtype_df["행정동"] == sel_dong2]
                if not vrow.empty:
                    vtype_cols = [c for c in ["횡단보도","소화전","버스정류소","인도","도로가장자리","모퉁이·교차로"]
                                  if c in vrow.columns]
                    if vtype_cols:
                        top_vtype = vrow[vtype_cols].iloc[0].idxmax()
                        vtype_tip = {peak_band: f"→ 이 지역 주요 위반: **{top_vtype}** 집중 점검 효과 높음"}

            BAND_BASE_TIP = {
                "오전 피크": "출근·등교 시간대, 횡단보도·버스정류장 위주",
                "점심":      "상업지구 주변, 소화전·인도 침범 주의",
                "오후 피크": "하교·퇴근 시간대, 이중주차·교차로 위주",
                "저녁":      "식당가·상가 주변, 민원신고 집중 시간대",
                "야간":      "단속 효율 낮음, CCTV 모니터링 중심 권장",
            }

            for bname, (_, btime) in BAND_HOURS.items():
                cnt = band_totals[bname]
                pct = cnt / total_cnt * 100
                is_peak = (bname == peak_band)
                tip = vtype_tip.get(bname, BAND_BASE_TIP[bname])
                prefix = "🔴 **최고 집중**" if is_peak else ("🟡" if pct >= 15 else "⚪")
                st.markdown(f"{prefix} **{btime} ({bname})** — {cnt:,}건 ({pct:.0f}%)\n  {tip}")

# ── 탭3: 위반유형별 대책 ──────────────────────────────────────────
with tab3:
    if not _data_ok or vtype_df.empty:
        st.error("데이터를 불러올 수 없습니다.")
    else:
        st.markdown("### 📊 위반유형별 민원 감소 대책")
        st.caption("위반 유형에 따라 효과적인 개입 방식이 다릅니다 — 단속 강화 / CCTV 설치 / 안내·계도 구분")
        st.info("ℹ️ **분석 대상: 횡단보도·소화전·인도·버스정류소·모퉁이·교차로 위반 명시 건 11,222건**\n\n"
                "전체 단속 217,682건 중 CCTV 자동 적발 및 위반유형 미기재 건은 이 분석에서 제외됩니다.\n\n"
                "기타(도로가장자리·주차금지 등) 위반은 범주 분류가 어려워 개입 방식 추천에서 별도 표시하지 않습니다.")

        VTYPE_COLS  = ["횡단보도","인도","소화전","버스정류소","모퉁이·교차로"]
        avail_cols  = [c for c in VTYPE_COLS if c in vtype_df.columns]
        filtered_cols = [c for c in avail_cols if c in selected_vtypes]

        # 위반유형별 권장 대책
        ACTION_MAP = {
            "횡단보도":     ("📷 CCTV 설치",    "#E63946", "보행자 안전 직결, 고정 CCTV 효과 최대"),
            "소화전":       ("📷 CCTV 설치",    "#F4A261", "소방 대응 방해, CCTV 억제 효과 높음"),
            "버스정류소":   ("🚔 단속 강화",    "#2A9D8F", "대중교통 흐름 방해, 이동단속 효과적"),
            "인도":         ("🪧 안내·계도",    "#457B9D", "보행권 침해, 표지판·계도 우선"),
            "모퉁이·교차로":("🚔 단속 강화",    "#6A4C93", "사고위험 높음, 단속 강화 필요"),
        }

        col_a, col_b = st.columns(2)
        with col_a:
            if filtered_cols:
                total_by_type = vtype_df[filtered_cols].sum()
                colors = [ACTION_MAP.get(c, ("", "#999",""))[1] for c in total_by_type.index]
                fig_pie = px.pie(
                    values=total_by_type.values, names=total_by_type.index,
                    title="위반유형 분포 (2023년 전체)",
                    color_discrete_sequence=colors, hole=0.4,
                )
                fig_pie.update_traces(textinfo="label+percent",
                                      hovertemplate="%{label}: %{value:,}건 (%{percent})<extra></extra>")
                fig_pie.update_layout(height=360)
                st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            n_sel = len(selected_vtypes)
            st.markdown(f"**위반유형별 권장 대책** ({n_sel}개 선택)")
            for vtype, (action, color, reason) in ACTION_MAP.items():
                if vtype in avail_cols:
                    is_sel = viol_all or (vtype in selected_vtypes)
                    cnt = int(vtype_df[vtype].sum())
                    bg    = "#f9f9f9" if is_sel else "#f0f0f0"
                    alpha = "1"       if is_sel else "0.4"
                    badge = "" if is_sel else " <span style='color:#aaa;font-size:10px'>(필터 제외)</span>"
                    st.markdown(
                        f"""<div style='margin-bottom:8px;padding:8px;border-left:4px solid {color};
                                background:{bg};border-radius:4px;opacity:{alpha}'>
                            <b>{vtype}</b>{badge} — {action}<br>
                            <small style='color:#555'>{reason}<br>
                            2023년 {cnt:,}건 단속</small>
                        </div>""", unsafe_allow_html=True)


# ── 탭 전체현황: 35개 행정동 마스터 테이블 ──────────────────────────
with tab_all:
    st.markdown("### 🗂️ 전체 법정동 현황 (35개)")
    st.caption("화성시 법정동 전체 지표 — 열 클릭으로 정렬 | 검색으로 특정 동 필터링")
    st.info(
        "ℹ️ **분석 대상: 35개 법정동**\n\n"
        "원본 217,682건 중 법정동 미분류 3,776건(1.7%)은 주소가 랜드마크·도로명으로만 기재되어 법정동 파악 불가로 제외되었습니다.\n\n"
        "또한 **단속건수 50건 미만의 7개 법정동(반정동·배양동·황계동·중동·오목천동·척동·산동)은 "
        "표본 수 부족으로 통계 신뢰성이 낮아 분석에서 제외**하였습니다."
    )

    if not _data_ok or risk_df.empty:
        st.error("데이터를 불러올 수 없습니다.")
    else:
        master = build_policy_table(risk_df, cctv_df, vtype_df)

        # ── 검색 필터 ──
        search = st.text_input("🔍 법정동 검색", placeholder="예: 향남읍, 석우동 …")
        if search:
            master = master[master["행정동"].str.contains(search, na=False)]

        # ── 요약 KPI ──
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("전체 법정동", f"{len(master)}개")
        k2.metric("고위험", f"{(master['위험등급']=='고위험').sum()}개", delta_color="inverse")
        k3.metric("중위험", f"{(master['위험등급']=='중위험').sum()}개")
        k4.metric("저위험", f"{(master['위험등급']=='저위험').sum()}개", delta_color="off")
        k5.metric("총 실단속건수", f"{int(master['실단속건수'].sum()):,}건")

        st.markdown("---")

        # ── 마스터 테이블 ──
        st.markdown("#### 📋 전체 지표 종합표")
        show_master_cols = [
            "행정동", "위험등급", "재보정위험도점수", "실단속건수",
            "민원비율", "CCTV공백지수", "통행불편지수_표시",
            "단속강화_우선순위", "CCTV설치_우선순위", "추천 개입"
        ]
        show_master_cols = [c for c in show_master_cols if c in master.columns]
        tbl_master = master[show_master_cols].sort_values("재보정위험도점수", ascending=False).reset_index(drop=True)
        tbl_master = tbl_master.rename(columns={"통행불편지수_표시": "통행불편지수"})
        tbl_master.index += 1

        # 숫자 포맷
        tbl_master["실단속건수"] = tbl_master["실단속건수"].apply(lambda x: f"{int(x):,}건")
        tbl_master["민원비율"]   = tbl_master["민원비율"].apply(lambda x: f"{x:.1%}")

        def grade_style(val):
            if val == "고위험": return "background-color:#c0392b;color:white;font-weight:bold"
            if val == "중위험": return "background-color:#e67e22;color:white;font-weight:bold"
            if val == "저위험": return "background-color:#27ae60;color:white;font-weight:bold"
            return ""

        def action_style(val):
            if "CCTV"  in str(val): return "background-color:#c0392b;color:white"
            if "단속"  in str(val): return "background-color:#e67e22;color:white"
            if "계도"  in str(val): return "background-color:#2980b9;color:white"
            if "유지"  in str(val): return "background-color:#27ae60;color:white"
            return ""

        styled = (
            tbl_master.style
            .map(grade_style,  subset=["위험등급"])
            .map(action_style, subset=["추천 개입"] if "추천 개입" in tbl_master.columns else [])
            .background_gradient(subset=["재보정위험도점수"], cmap="Reds", vmin=0, vmax=15)
            .background_gradient(subset=["CCTV공백지수"], cmap="Oranges", vmin=0, vmax=2)
            .format({"재보정위험도점수": "{:.2f}", "CCTV공백지수": "{:.4f}",
                     "단속강화_우선순위": "{:.3f}", "CCTV설치_우선순위": "{:.3f}"})
        )
        st.dataframe(styled, use_container_width=True, height=600)

        # ── 다운로드 버튼 ──
        csv_data = master[show_master_cols].sort_values("재보정위험도점수", ascending=False).to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 전체 데이터 CSV 다운로드",
            data=csv_data.encode("utf-8-sig"),
            file_name="화성시_법정동별_전체현황.csv",
            mime="text/csv",
        )

# ── 탭5: 예측 모델 & 정책 권고 ───────────────────────────────────
with tab4:
    st.markdown("### 🔮 향후 6개월 단속 예측 & 정책 권고")
    try:
        res = train_ensemble_and_predict(6)
        ts       = res["ts"]
        month_kn = {1:"1월",2:"2월",3:"3월",4:"4월",5:"5월",6:"6월",
                    7:"7월",8:"8월",9:"9월",10:"10월",11:"11월",12:"12월"}
        _fi0, _fi5 = res["future_info"][0], res["future_info"][-1]
        _period_str = f"{_fi0['연도']}년 {month_kn[_fi0['월']]}~{month_kn[_fi5['월']]}"
        st.caption(f"2021~2024년 단속 실적 기반 Prophet+SARIMA 앙상블 예측 → {_period_str} 인력 배치·CCTV 설치 우선순위 도출")

        # ════════════════════════════════════════════════════════
        # SECTION 1 — 예측 차트 + 6개월 테이블
        # ════════════════════════════════════════════════════════
        st.markdown(f"#### 📈 단속건수 예측 ({_period_str})")

        future_dates = pd.date_range(
            start=pd.Timestamp(year=res["future_info"][0]["연도"], month=res["future_info"][0]["월"], day=1),
            periods=len(res["future_info"]), freq="MS")
        train_dates = ts[res["train_mask"]]["날짜"]
        test_dates  = ts[res["test_mask"]]["날짜"]

        # ── 예측 차트 ──────────────────────────────────────────────
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(
            x=train_dates, y=res["y_train"], mode="lines",
            name="실제 단속건수", line=dict(color="#4C72B0", width=2)))
        if res["n_align"] > 0:
            fig_pred.add_trace(go.Scatter(
                x=test_dates, y=res["y_test"], mode="lines+markers",
                name="실제 (검증)", line=dict(color="#2CA02C", width=2),
                marker=dict(size=7)))
            fig_pred.add_trace(go.Scatter(
                x=test_dates, y=res["ens_te"], mode="lines+markers",
                name="앙상블 예측 (검증)", line=dict(color="#D62728", width=2, dash="dash"),
                marker=dict(symbol="star", size=9)))
        fig_pred.add_trace(go.Scatter(
            x=future_dates, y=res["pred_e_fu"], mode="lines+markers",
            name="앙상블 예측 (향후 6개월)", line=dict(color="#D62728", width=2.5, dash="dot"),
            marker=dict(size=9)))
        if res["mae_e"]:
            fig_pred.add_trace(go.Scatter(
                x=list(future_dates) + list(future_dates[::-1]),
                y=list(res["pred_e_fu"] + res["mae_e"]) + list((res["pred_e_fu"] - res["mae_e"])[::-1]),
                fill="toself", fillcolor="rgba(214,39,40,0.08)",
                line=dict(color="rgba(255,255,255,0)"),
                name=f"오차 범위 (±{res['mae_e']:.0f}건)"))
        fig_pred.update_layout(
            height=380, hovermode="x unified",
            xaxis_title="", yaxis_title="단속 건수 (건)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            margin=dict(t=10, b=10))
        st.plotly_chart(fig_pred, use_container_width=True)

        # ── 6개월 예측 테이블 ──────────────────────────────────────
        pred_rows = []
        for i, (fi, v) in enumerate(zip(res["future_info"], res["pred_e_fu"])):
            yoy = f"{((v - res['pred_e_fu'][i-1]) / res['pred_e_fu'][i-1] * 100):+.1f}%" if i > 0 else "–"
            demand = "↑ 증원 권장" if v > 20000 else ("→ 현행 유지" if v > 17000 else "↓ 여유")
            pred_rows.append({
                "기간": f"{fi['연도']}년 {month_kn[fi['월']]}",
                "앙상블 예측": f"{v:,}건",
                "Prophet": f"{res['pred_p_fu'][i]:,}건",
                "SARIMA":  f"{res['pred_s_fu'][i]:,}건" if res['sarima_ok'] else "–",
                "전월 대비": yoy,
                "전체 인력 수요": demand,
            })
        st.dataframe(pd.DataFrame(pred_rows), use_container_width=True, hide_index=True)

        # ── 모델 상세 접기 ─────────────────────────────────────────
        with st.expander("🔬 모델 상세 (Prophet·SARIMA 개별 예측 & Prophet 계절 분해)", expanded=False):
            mc1, mc2, mc3 = st.columns(3)
            mc1.metric("Prophet MAE",  f"{res['mae_p']:.0f}건" if res['mae_p'] else "–",
                       f"가중치 {res['w_p']:.0%}")
            mc2.metric("SARIMA MAE",   f"{res['mae_s']:.0f}건" if res['mae_s'] else "–",
                       f"가중치 {res['w_s']:.0%}")
            mc3.metric("앙상블 MAE",   f"{res['mae_e']:.0f}건" if res['mae_e'] else "–", "최종")

            st.caption(f"Prophet {'✅' if res['prophet_ok'] else '⚠️ 실패'}  |  "
                       f"SARIMA {'✅' if res['sarima_ok'] else '⚠️ 실패'}  |  "
                       f"앙상블 = Prophet×{res['w_p']:.0%} + SARIMA×{res['w_s']:.0%} (MAE 역수 가중)")

            # Prophet 계절 분해 차트
            if res["prophet_components"] is not None:
                comp = res["prophet_components"]
                fig_comp = go.Figure()
                fig_comp.add_trace(go.Scatter(
                    x=comp["ds"], y=comp["trend"],
                    name="추세 (Trend)", line=dict(color="#4C72B0", width=2)))
                fig_comp.add_trace(go.Scatter(
                    x=comp["ds"], y=comp["yearly"],
                    name="연간 계절성", line=dict(color="#FF7F0E", width=2, dash="dot")))
                fig_comp.update_layout(
                    height=280, hovermode="x unified",
                    title="Prophet 분해: 추세 + 연간 계절성",
                    xaxis_title="", yaxis_title="단속건수 기여분",
                    legend=dict(orientation="h", yanchor="bottom", y=1.02),
                    margin=dict(t=40, b=10))
                st.plotly_chart(fig_comp, use_container_width=True)
                st.caption("추세선이 우상향 → 단속 건수 장기 증가 추세. 계절성 파동이 크면 특정 월에 집중 단속 필요.")

        # ── 타 모델 대비 성능 비교 ────────────────────────────────
        with st.expander("📊 타 모델 대비 성능 비교 (2025년 1~4월 검증 기준)", expanded=False):
            cmp_data = [
                ("Prophet+SARIMA 앙상블 (우리 모델)", 1546, 7.4, True),
                ("Prophet 단독",                      1521, 7.4, False),
                ("SARIMA 단독",                       1571, 7.4, False),
                ("선형회귀 (추세+계절성)",               2302, 11.3, False),
                ("Holt-Winters (3중 지수평활)",         2341, 11.8, False),
                ("ARIMA(1,1,1)",                      2409, 11.8, False),
                ("Naive (직전값 반복)",                 2584, 12.6, False),
                ("Seasonal Naive (전년 동월)",          2982, 16.0, False),
            ]
            cmp_df = pd.DataFrame(cmp_data, columns=["모델", "MAE(건)", "MAPE(%)", "우리모델"])
            cmp_df = cmp_df.sort_values("MAE(건)")

            colors = ["#e74c3c" if r else "#95a5a6" for r in cmp_df["우리모델"]]
            fig_cmp = go.Figure(go.Bar(
                x=cmp_df["MAE(건)"], y=cmp_df["모델"],
                orientation="h",
                marker_color=colors,
                text=cmp_df["MAE(건)"].apply(lambda v: f"{v:,}건"),
                textposition="outside",
            ))
            fig_cmp.update_layout(
                height=380, xaxis_title="MAE (건수 오차)", yaxis_title="",
                title="모델별 MAE 비교 — 낮을수록 우수 (2025년 1~4월 검증)",
                margin=dict(l=10, r=80, t=45, b=10),
                xaxis=dict(range=[0, 3500]),
            )
            st.plotly_chart(fig_cmp, use_container_width=True)

            cc1, cc2, cc3 = st.columns(3)
            cc1.metric("Prophet+SARIMA 앙상블", "MAE 1,546건 (7.4%)", "전체 8개 모델 중 2위")
            cc2.metric("Holt-Winters 대비", "MAE 795건 개선", "↓34% 향상")
            cc3.metric("Naive 대비", "MAE 1,038건 개선", "↓40% 향상")
            st.info(
                "**왜 앙상블이 좋은가?**\n\n"
                "• Prophet은 장기 추세·계절성 포착에 강하지만 단기 급변 대응이 약합니다.\n"
                "• SARIMA는 직전 월 패턴과 잔차를 보완하여 단기 변동을 흡수합니다.\n"
                "• 두 모델의 MAE 역수로 가중치를 산출해 더 잘 맞는 모델에 자동으로 높은 가중치를 부여합니다.\n\n"
                "Prophet 단독이 MAE 기준으로는 25건(1.6%) 더 낮지만, "
                "테스트셋 4개월이라는 소표본에서의 차이로 앙상블 방법론의 강건성을 유지합니다."
            )
            st.caption("검증 기간: 2025년 1~4월 (4개월) · 비교 모델: Naive, Seasonal Naive, 선형회귀, "
                       "Holt-Winters, ARIMA(1,1,1), Prophet 단독, SARIMA 단독, Prophet+SARIMA 앙상블")

        st.divider()

        # ════════════════════════════════════════════════════════
        # SECTION 2 — 2026년 6월~11월 법정동별 정책 권고 (핵심)
        # ════════════════════════════════════════════════════════
        st.markdown(f"#### 📌 {_period_str} 법정동별 정책 권고")
        st.caption("예측 증가 구간 + 현재 위험도·CCTV 공백을 종합한 선제 대응 권고")

        if not cctv_df.empty:
            policy_t = build_policy_table(risk_df, cctv_df, vtype_df)

            def _gc(val):
                if val == "고위험": return "background-color:#c0392b;color:white;font-weight:bold"
                if val == "중위험": return "background-color:#e67e22;color:white;font-weight:bold"
                if val == "저위험": return "background-color:#27ae60;color:white;font-weight:bold"
                return ""

            col_enf, col_cctv = st.columns(2)

            with col_enf:
                st.markdown("##### 🚔 인원 배치 강화 권고 TOP 7")
                st.caption("단속강화 점수 = 재보정위험도 × 0.7 + 통행불편지수 × 0.3 | 통행불편 미기재 지역은 재보정위험도 단일 기준")
                enf7 = policy_t.sort_values("단속강화_우선순위", ascending=False).head(7)[
                    ["행정동","위험등급","재보정위험도점수","통행불편지수_표시","단속강화_우선순위"]
                ].reset_index(drop=True)
                enf7.index += 1
                enf7.columns = ["법정동","위험등급","위험도","통행불편","단속강화점수"]
                st.dataframe(
                    enf7.style
                        .map(_gc, subset=["위험등급"])
                        .background_gradient(subset=["단속강화점수"], cmap="Reds", vmin=0, vmax=15),
                    use_container_width=True)
                st.info("이동단속반·순찰 인원을 이 지역에 우선 배치하세요.\n\n"
                        "위험도·통행불편이 동시에 높아 단속 효과가 가장 큽니다.")

            with col_cctv:
                st.markdown("##### 📷 CCTV 신규 설치 권고 TOP 7")
                st.caption("CCTV 설치 점수 = 공백지수 × 0.8 + 재보정위험도 × 0.2 (실단속 50건↑ 지역만)")
                cctv7 = policy_t[policy_t["CCTV설치_우선순위"] > 0].sort_values(
                    "CCTV설치_우선순위", ascending=False).head(7)[
                    ["행정동","위험등급","CCTV공백지수","고정CCTV비율","CCTV설치_우선순위"]
                ].reset_index(drop=True)
                cctv7.index += 1
                cctv7.columns = ["법정동","위험등급","CCTV공백지수","현재CCTV비율","설치점수"]
                cctv7["현재CCTV비율"] = cctv7["현재CCTV비율"].apply(lambda x: f"{x:.1%}")
                st.dataframe(
                    cctv7.style
                        .map(_gc, subset=["위험등급"])
                        .background_gradient(subset=["CCTV공백지수"], cmap="Oranges", vmin=0, vmax=2),
                    use_container_width=True)
                st.info("민원 비율 대비 고정 CCTV 비율이 낮은 지역입니다.\n\n"
                        "CCTV 1기 설치로 24시간 자동 단속 → 인력 부담 절감 효과가 있습니다.")


    except Exception as e:
        import traceback
        st.error(f"예측 모델 실행 오류: {e}")
        st.code(traceback.format_exc())
