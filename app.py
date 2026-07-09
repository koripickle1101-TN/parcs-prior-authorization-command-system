import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Prior Authorization Failure Intelligence System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

TENNESSEE_ORANGE = "#FF8200"
BLACK = "#000000"
WHITE = "#FFFFFF"
WARM_GRAY = "#F7F3EE"
LINE_GRAY = "#E8DED2"
DARK_GRAY = "#2A2623"

DATA = [
    ["PAFI-001","MRI","Commercial","Pending","Authorization submitted too close to service date","Complete","Strong","Yes","Routine","No","Moderate",2.5,"Authorization Submission","Submit authorization earlier and monitor pending cases 72 hours before service"],
    ["PAFI-002","Specialist Visit","Medicaid","Not Started","Authorization requirement was not identified","Partial","Weak","Yes","Routine","Yes","High",5.0,"Authorization Requirement Check","Add payer-specific authorization requirement checklist during scheduling"],
    ["PAFI-003","Outpatient Procedure","Medicare Advantage","Denied","Medical necessity support was insufficient","Complete","Weak","Yes","Urgent","Yes","High",6.5,"Medical Necessity Review","Strengthen documentation review before authorization submission"],
    ["PAFI-004","Physical Therapy","Commercial","Approved","No major issue identified","Complete","Strong","Yes","Routine","No","Low",0.5,"Controlled Workflow","Continue standard eligibility and authorization verification process"],
    ["PAFI-005","Diagnostic Imaging","Commercial","Pending","Payer requested additional documentation","Partial","Moderate","Yes","Routine","No","Moderate",3.0,"Documentation Readiness","Create pre-submission documentation completeness checkpoint"],
    ["PAFI-006","Surgery Consult","Medicaid","Not Started","Insurance eligibility was not verified before authorization review","Incomplete","Missing","No","Routine","Yes","Critical",8.0,"Eligibility Verification","Verify eligibility before scheduling authorization-dependent services"],
    ["PAFI-007","Infusion Therapy","Medicare Advantage","Pending","Authorization delayed due to missing clinical notes","Incomplete","Weak","Yes","Urgent","Yes","Critical",7.5,"Documentation Readiness","Require complete clinical support before submitting authorization"],
    ["PAFI-008","CT Scan","Commercial","Denied","Authorization submitted after service was performed","Complete","Moderate","Yes","Urgent","Yes","Critical",9.0,"Service Clearance","Stop service from proceeding until authorization status is confirmed"],
    ["PAFI-009","Cardiology Test","Medicare Advantage","Pending","Payer follow-up overdue","Complete","Strong","Yes","Routine","No","Moderate",2.0,"Payer Follow-Up","Add daily aging report for pending authorizations"],
    ["PAFI-010","Orthopedic Procedure","Commercial","Pending","Authorization still unresolved within 48 hours of service","Complete","Moderate","Yes","Urgent","Yes","High",4.5,"Authorization Tracking","Escalate pending authorizations within 72 hours of service date"],
    ["PAFI-011","Neurology Visit","Medicaid","Denied","Referral and authorization requirements were both missed","Partial","Weak","No","Routine","Yes","Critical",8.5,"Scheduling Intake","Add referral and authorization requirement validation at intake"],
    ["PAFI-012","Behavioral Health Visit","Commercial","Approved","Eligibility and authorization were confirmed correctly","Complete","Strong","Yes","Routine","No","Low",0.5,"Controlled Workflow","Maintain current pre-service verification workflow"],
    ["PAFI-013","Sleep Study","Medicare Advantage","Denied","Documentation did not clearly support medical necessity","Partial","Weak","Yes","Routine","Yes","High",6.0,"Medical Necessity Review","Use payer medical necessity checklist before submission"],
    ["PAFI-014","Wound Care","Medicaid","Pending","Eligibility verified too early and not rechecked","Complete","Moderate","Late","Urgent","No","Moderate",3.5,"Eligibility Reverification","Recheck eligibility 48 to 72 hours before service"],
    ["PAFI-015","Outpatient Surgery","Commercial","Not Started","Authorization queue backlog caused missed submission","Complete","Strong","Yes","Urgent","Yes","Critical",9.5,"Authorization Queue Management","Create backlog dashboard with aging and urgency filters"],
    ["PAFI-016","Endoscopy","Medicare Advantage","Pending","Payer requested corrected procedure information","Partial","Moderate","Yes","Routine","No","Moderate",3.0,"Order Review","Confirm service codes and order details before authorization submission"],
    ["PAFI-017","Pain Management Procedure","Commercial","Denied","Prior conservative treatment documentation was missing","Incomplete","Weak","Yes","Routine","Yes","High",7.0,"Documentation Readiness","Add supporting-treatment documentation checklist"],
    ["PAFI-018","Specialist Follow-Up","Medicaid","Approved","Authorization approved after manual follow-up","Complete","Moderate","Yes","Routine","No","Moderate",1.5,"Payer Follow-Up","Track payer follow-up attempts and response deadlines"],
    ["PAFI-019","Diagnostic Ultrasound","Commercial","Approved","No authorization required after payer review","Complete","Strong","Yes","Routine","No","Low",0.5,"Authorization Requirement Check","Document no-authorization-required confirmation clearly"],
    ["PAFI-020","Rehabilitation Services","Medicare Advantage","Pending","Visit limit verification incomplete","Partial","Moderate","Late","Routine","No","Moderate",2.5,"Benefit Verification","Verify visit limits and remaining benefits before service"],
    ["PAFI-021","Ambulatory Procedure","Commercial","Denied","Authorization was approved for wrong service type","Complete","Moderate","Yes","Urgent","Yes","Critical",8.0,"Order and Authorization Match","Match authorization approval details to scheduled service before clearance"],
    ["PAFI-022","Oncology Infusion","Medicare Advantage","Pending","High-cost service requires additional payer review","Complete","Strong","Yes","Urgent","No","High",4.0,"Payer Follow-Up","Escalate high-cost pending cases earlier in the workflow"],
    ["PAFI-023","ENT Procedure","Medicaid","Not Started","Patient coverage inactive at time of verification","Incomplete","Missing","No","Routine","Yes","Critical",7.5,"Eligibility Verification","Resolve coverage status before authorization submission"],
    ["PAFI-024","Advanced Imaging","Commercial","Denied","Peer-to-peer review was not completed before deadline","Complete","Moderate","Yes","Urgent","Yes","High",6.5,"Clinical Escalation","Track peer-to-peer deadlines and escalation ownership"],
    ["PAFI-025","Specialty Medication","Medicare Advantage","Pending","Medication authorization requires missing dosage clarification","Partial","Weak","Yes","Urgent","No","High",5.5,"Documentation and Order Review","Clarify dosage and supporting documentation before payer submission"],
]

COLUMNS = [
    "Case ID", "Service Type", "Payer Type", "Authorization Status", "Authorization Issue",
    "Documentation Status", "Medical Necessity Support", "Eligibility Verified", "Service Urgency",
    "Retro Authorization Needed", "Denial Risk Level", "Estimated Rework Hours", "Workflow Failure Point",
    "Recommended Fix"
]

df = pd.DataFrame(DATA, columns=COLUMNS)

risk_order = {"Low": 1, "Moderate": 2, "High": 3, "Critical": 4}
df["Risk Rank"] = df["Denial Risk Level"].map(risk_order)
high_critical = df[df["Denial Risk Level"].isin(["High", "Critical"])]
retro_cases = df[df["Retro Authorization Needed"] == "Yes"]
doc_gap_cases = df[df["Documentation Status"].isin(["Partial", "Incomplete"])]
eligibility_issues = df[df["Eligibility Verified"].isin(["No", "Late"])]

st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&family=Great+Vibes&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
            color: {BLACK};
            background: {WHITE};
        }}

        .block-container {{
            padding-top: 3.25rem;
            padding-bottom: 3rem;
            max-width: 1220px;
        }}

        .hero {{
            background: linear-gradient(135deg, #FFFFFF 0%, #FFFFFF 58%, #FFF4EA 100%);
            border: 1px solid {LINE_GRAY};
            border-radius: 34px;
            padding: 56px 58px 48px 58px;
            position: relative;
            overflow: hidden;
            box-shadow: 0 18px 50px rgba(0,0,0,0.045);
        }}

        .hero:before {{
            content: '';
            position: absolute;
            right: -90px;
            top: -90px;
            width: 310px;
            height: 310px;
            border: 2px solid rgba(255,130,0,.32);
            border-radius: 50%;
            box-shadow: 0 0 55px rgba(255,130,0,.18);
        }}

        .hero:after {{
            content: '';
            position: absolute;
            right: 84px;
            top: 78px;
            width: 118px;
            height: 118px;
            border: 2px solid {TENNESSEE_ORANGE};
            outline: 10px solid rgba(255,130,0,.08);
            border-radius: 50%;
            box-shadow: 0 0 34px rgba(255,130,0,.25);
        }}

        .eyebrow {{
            color: {TENNESSEE_ORANGE};
            letter-spacing: .16em;
            text-transform: uppercase;
            font-weight: 800;
            font-size: .78rem;
            margin-bottom: 16px;
        }}

        .hero h1 {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-weight: 700;
            font-size: clamp(3rem, 7vw, 6.4rem);
            line-height: .86;
            letter-spacing: -.045em;
            max-width: 850px;
            margin: 0 0 22px 0;
            color: {BLACK};
        }}

        .hero p {{
            font-size: 1.05rem;
            line-height: 1.75;
            max-width: 760px;
            color: {DARK_GRAY};
        }}

        .tag-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 28px;
        }}

        .tag {{
            border: 1px solid rgba(255,130,0,.42);
            border-radius: 999px;
            padding: 8px 13px;
            font-size: .78rem;
            font-weight: 700;
            background: rgba(255,130,0,.07);
        }}

        .section-title {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-weight: 700;
            font-size: 2.4rem;
            letter-spacing: -.03em;
            margin-top: 42px;
            margin-bottom: 4px;
        }}

        .section-rule {{
            width: 82px;
            height: 3px;
            background: {TENNESSEE_ORANGE};
            border-radius: 999px;
            margin-bottom: 22px;
        }}

        .metric-card {{
            border: 1px solid {LINE_GRAY};
            border-radius: 24px;
            padding: 26px 26px 22px 26px;
            min-height: 145px;
            background: {WHITE};
            box-shadow: 0 14px 38px rgba(0,0,0,0.035);
            position: relative;
        }}

        .metric-card:before {{
            content: '';
            position: absolute;
            top: 18px;
            right: 18px;
            width: 28px;
            height: 28px;
            border: 2px solid {TENNESSEE_ORANGE};
            outline: 6px solid rgba(255,130,0,.09);
            border-radius: 50%;
        }}

        .metric-label {{
            font-size: .76rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .11em;
            color: {DARK_GRAY};
        }}

        .metric-value {{
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 3.35rem;
            font-weight: 700;
            line-height: 1;
            margin-top: 14px;
            color: {BLACK};
        }}

        .metric-note {{
            font-size: .86rem;
            line-height: 1.45;
            margin-top: 10px;
            color: #5a514b;
        }}

        .insight-box {{
            background: {WARM_GRAY};
            border-left: 5px solid {TENNESSEE_ORANGE};
            border-radius: 0 22px 22px 0;
            padding: 25px 30px;
            line-height: 1.72;
            margin: 18px 0 30px 0;
        }}

        .node-grid {{
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 18px;
            margin-top: 18px;
        }}

        .node {{
            border: 1px solid {LINE_GRAY};
            border-radius: 22px;
            padding: 22px;
            background: {WHITE};
            min-height: 135px;
            position: relative;
        }}

        .node:before {{
            content: '';
            width: 34px;
            height: 34px;
            border: 2px solid {TENNESSEE_ORANGE};
            outline: 7px solid rgba(255,130,0,.10);
            border-radius: 50%;
            display: block;
            margin-bottom: 18px;
            box-shadow: 0 0 26px rgba(255,130,0,.20);
        }}

        .node h4 {{
            font-size: .95rem;
            margin: 0 0 8px 0;
            font-weight: 800;
        }}

        .node p {{
            font-size: .84rem;
            color: #5a514b;
            line-height: 1.55;
            margin: 0;
        }}

        .footer {{
            margin-top: 58px;
            padding: 44px 20px 34px 20px;
            border-top: 1px dashed rgba(255,130,0,.65);
            text-align: center;
            background: linear-gradient(180deg, #FFFFFF 0%, #FFF9F3 100%);
            border-radius: 28px;
        }}

        .created {{
            font-size: .92rem;
            font-weight: 700;
            letter-spacing: .06em;
            text-transform: uppercase;
        }}

        .signature {{
            font-family: 'Great Vibes', 'Brush Script MT', cursive;
            font-size: 3.1rem;
            color: #1c1a18;
            transform: rotate(-1.2deg);
            margin: 8px 0 8px 0;
            letter-spacing: .02em;
            text-shadow: .35px .35px 0 rgba(0,0,0,.18);
        }}

        .socials {{
            display: flex;
            justify-content: center;
            gap: 18px;
            margin-top: 12px;
        }}

        .social-icon {{
            width: 38px;
            height: 38px;
            border: 1px solid {LINE_GRAY};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            color: {BLACK};
            background: {WHITE};
        }}

        div[data-testid="stMetric"] {{
            background: #FFFFFF;
            border: 1px solid {LINE_GRAY};
            padding: 16px 18px;
            border-radius: 20px;
        }}

        @media (max-width: 900px) {{
            .hero {{ padding: 40px 28px; }}
            .node-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Simulated Healthcare Operations Dashboard · No PHI · Student Portfolio Project</div>
        <h1>Prior Authorization Failure Intelligence System</h1>
        <p>
            A premium branded portfolio dashboard that examines where prior authorization workflows lose control before
            retro authorization, denial exposure, staff rework, A/R delays, or patient access friction appears downstream.
        </p>
        <div class="tag-row">
            <span class="tag">Prior Authorization</span>
            <span class="tag">Retro Authorization</span>
            <span class="tag">Patient Access</span>
            <span class="tag">Denial Prevention</span>
            <span class="tag">Revenue Cycle Workflow</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Executive Signal</div><div class="section-rule"></div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("Total Cases", len(df), "Simulated cases reviewed"),
    ("Retro Auth Cases", len(retro_cases), "Cases needing retro authorization review"),
    ("High/Critical Risk", len(high_critical), "Cases with elevated denial exposure"),
    ("Avg. Rework Hours", f"{df['Estimated Rework Hours'].mean():.1f}", "Estimated per case burden"),
]
for col, (label, value, note) in zip([c1, c2, c3, c4], metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div class="insight-box">
        <strong>Portfolio finding:</strong> In this simulated dataset, prior authorization risk is not only a billing event.
        It appears earlier across eligibility verification, documentation readiness, medical necessity support, payer follow-up,
        authorization tracking, and service clearance. The dashboard is designed to answer one operating question:
        <strong>Where did the workflow lose control before the denial or retro authorization happened?</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Workflow Control Map</div><div class="section-rule"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="node-grid">
        <div class="node"><h4>1. Scheduling Intake</h4><p>Confirm service type, payer, referral, and authorization requirement before the case moves forward.</p></div>
        <div class="node"><h4>2. Eligibility Verification</h4><p>Detect inactive, late, or outdated coverage checks before auth work begins.</p></div>
        <div class="node"><h4>3. Documentation Readiness</h4><p>Review order details, supporting notes, and medical necessity support before submission.</p></div>
        <div class="node"><h4>4. Authorization Tracking</h4><p>Monitor pending, denied, not-started, and at-risk cases before service clearance.</p></div>
        <div class="node"><h4>5. Payer Follow-Up</h4><p>Track additional information requests, aging, deadline risk, and manual follow-up burden.</p></div>
        <div class="node"><h4>6. Service Clearance</h4><p>Stop unresolved or mismatched authorization cases before care is performed at risk.</p></div>
        <div class="node"><h4>7. Denial Prevention</h4><p>Identify retro authorization, appeal, claim hold, and A/R delay exposure earlier.</p></div>
        <div class="node"><h4>8. Operational Fix</h4><p>Translate risk patterns into practical checkpoints, escalation ownership, and workflow controls.</p></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Risk Intelligence Views</div><div class="section-rule"></div>', unsafe_allow_html=True)

left, right = st.columns([1.08, .92])

with left:
    risk_counts = df["Denial Risk Level"].value_counts().rename_axis("Risk Level").reset_index(name="Cases")
    risk_counts["Risk Sort"] = risk_counts["Risk Level"].map(risk_order)
    risk_counts = risk_counts.sort_values("Risk Sort")
    chart = (
        alt.Chart(risk_counts)
        .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
        .encode(
            x=alt.X("Risk Level:N", sort=["Low", "Moderate", "High", "Critical"], title=None),
            y=alt.Y("Cases:Q", title="Cases"),
            tooltip=["Risk Level", "Cases"],
            color=alt.value(TENNESSEE_ORANGE),
        )
        .properties(height=320)
    )
    st.altair_chart(chart, use_container_width=True)

with right:
    st.markdown("### Dashboard Interpretation")
    st.write(
        "High and Critical cases represent simulated authorization workflows where human review should occur before the issue becomes a retro authorization, denial, appeal, A/R delay, or patient access disruption."
    )
    st.metric("Total Estimated Rework Hours", f"{df['Estimated Rework Hours'].sum():.1f}")
    st.metric("Documentation Gap Cases", len(doc_gap_cases))
    st.metric("Eligibility Issue Cases", len(eligibility_issues))

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("#### Workflow Failure Point Breakdown")
    failure_counts = df["Workflow Failure Point"].value_counts().rename_axis("Failure Point").reset_index(name="Cases")
    st.dataframe(failure_counts, use_container_width=True, hide_index=True)

with col_b:
    st.markdown("#### Payer Type by High/Critical Risk")
    payer_risk = high_critical.groupby("Payer Type").size().reset_index(name="High/Critical Cases").sort_values("High/Critical Cases", ascending=False)
    st.dataframe(payer_risk, use_container_width=True, hide_index=True)

st.markdown('<div class="section-title">Prior Authorization Failure Table</div><div class="section-rule"></div>', unsafe_allow_html=True)

risk_filter = st.multiselect(
    "Filter by denial risk level",
    options=["Low", "Moderate", "High", "Critical"],
    default=["High", "Critical"],
)
status_filter = st.multiselect(
    "Filter by authorization status",
    options=sorted(df["Authorization Status"].unique()),
    default=sorted(df["Authorization Status"].unique()),
)
filtered = df[df["Denial Risk Level"].isin(risk_filter) & df["Authorization Status"].isin(status_filter)]
st.dataframe(
    filtered.drop(columns=["Risk Rank"]),
    use_container_width=True,
    hide_index=True,
)

st.markdown('<div class="section-title">Recommended Operational Fixes</div><div class="section-rule"></div>', unsafe_allow_html=True)

fixes = (
    high_critical[["Workflow Failure Point", "Recommended Fix"]]
    .drop_duplicates()
    .sort_values("Workflow Failure Point")
)
st.dataframe(fixes, use_container_width=True, hide_index=True)

st.markdown('<div class="section-title">Executive Summary</div><div class="section-rule"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="insight-box">
        This simulated dashboard reviews <strong>{len(df)} no-PHI prior authorization workflow cases</strong>.
        The dataset contains <strong>{len(retro_cases)} retro authorization review cases</strong> and
        <strong>{len(high_critical)} high or critical denial-risk cases</strong>. The total simulated rework burden is
        <strong>{df['Estimated Rework Hours'].sum():.1f} hours</strong>, with an average of
        <strong>{df['Estimated Rework Hours'].mean():.1f} hours per case</strong>.
        <br><br>
        The strongest operational lesson is that retro authorization and denial risk often become visible late, but the
        workflow usually begins losing control earlier. This portfolio project demonstrates student-level healthcare operations
        reasoning across eligibility, prior authorization, documentation readiness, payer follow-up, service clearance, patient access,
        and denial prevention.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer">
        <div class="created">Created by Kori Pickle</div>
        <div class="signature">Kori Pickle</div>
        <div class="socials">
            <div class="social-icon">in</div>
            <div class="social-icon">GH</div>
        </div>
        <p style="max-width:760px;margin:18px auto 0 auto;line-height:1.65;color:#5a514b;font-size:.9rem;">
            Simulated Healthcare Operations Dashboard · No PHI · BSHA Student Portfolio Project · Not employer experience · Not clinical, coding, payer, or medical decision-making.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
