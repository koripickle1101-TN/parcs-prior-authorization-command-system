import streamlit as st
import pandas as pd
import altair as alt
from datetime import date, timedelta

st.set_page_config(
    page_title="PARCS | Prior Authorization Command System",
    page_icon="📋",
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
    ["PARCS-001","MRI","Commercial","Pending","Authorization submitted too close to service date","Complete","Strong","Yes","Routine","No","Moderate",2.5,"Authorization Submission","Submit authorization earlier and monitor pending cases 72 hours before service"],
    ["PARCS-002","Specialist Visit","Medicaid","Not Started","Authorization requirement was not identified","Partial","Weak","Yes","Routine","Yes","High",5.0,"Authorization Requirement Check","Add payer-specific authorization requirement checklist during scheduling"],
    ["PARCS-003","Outpatient Procedure","Medicare Advantage","Denied","Medical necessity support was insufficient","Complete","Weak","Yes","Urgent","Yes","High",6.5,"Medical Necessity Review","Strengthen documentation review before authorization submission"],
    ["PARCS-004","Physical Therapy","Commercial","Approved","No major issue identified","Complete","Strong","Yes","Routine","No","Low",0.5,"Controlled Workflow","Continue standard eligibility and authorization verification process"],
    ["PARCS-005","Diagnostic Imaging","Commercial","Pending","Payer requested additional documentation","Partial","Moderate","Yes","Routine","No","Moderate",3.0,"Documentation Readiness","Create pre-submission documentation completeness checkpoint"],
    ["PARCS-006","Surgery Consult","Medicaid","Not Started","Insurance eligibility was not verified before authorization review","Incomplete","Missing","No","Routine","Yes","Critical",8.0,"Eligibility Verification","Verify eligibility before scheduling authorization-dependent services"],
    ["PARCS-007","Infusion Therapy","Medicare Advantage","Pending","Authorization delayed due to missing clinical notes","Incomplete","Weak","Yes","Urgent","Yes","Critical",7.5,"Documentation Readiness","Require complete clinical support before submitting authorization"],
    ["PARCS-008","CT Scan","Commercial","Denied","Authorization submitted after service was performed","Complete","Moderate","Yes","Urgent","Yes","Critical",9.0,"Service Clearance","Stop service from proceeding until authorization status is confirmed"],
    ["PARCS-009","Cardiology Test","Medicare Advantage","Pending","Payer follow-up overdue","Complete","Strong","Yes","Routine","No","Moderate",2.0,"Payer Follow-Up","Add daily aging report for pending authorizations"],
    ["PARCS-010","Orthopedic Procedure","Commercial","Pending","Authorization still unresolved within 48 hours of service","Complete","Moderate","Yes","Urgent","Yes","High",4.5,"Authorization Tracking","Escalate pending authorizations within 72 hours of service date"],
    ["PARCS-011","Neurology Visit","Medicaid","Denied","Referral and authorization requirements were both missed","Partial","Weak","No","Routine","Yes","Critical",8.5,"Scheduling Intake","Add referral and authorization requirement validation at intake"],
    ["PARCS-012","Behavioral Health Visit","Commercial","Approved","Eligibility and authorization were confirmed correctly","Complete","Strong","Yes","Routine","No","Low",0.5,"Controlled Workflow","Maintain current pre-service verification workflow"],
    ["PARCS-013","Sleep Study","Medicare Advantage","Denied","Documentation did not clearly support medical necessity","Partial","Weak","Yes","Routine","Yes","High",6.0,"Medical Necessity Review","Use payer medical necessity checklist before submission"],
    ["PARCS-014","Wound Care","Medicaid","Pending","Eligibility verified too early and not rechecked","Complete","Moderate","Late","Urgent","No","Moderate",3.5,"Eligibility Reverification","Recheck eligibility 48 to 72 hours before service"],
    ["PARCS-015","Outpatient Surgery","Commercial","Not Started","Authorization queue backlog caused missed submission","Complete","Strong","Yes","Urgent","Yes","Critical",9.5,"Authorization Queue Management","Create backlog dashboard with aging and urgency filters"],
    ["PARCS-016","Endoscopy","Medicare Advantage","Pending","Payer requested corrected procedure information","Partial","Moderate","Yes","Routine","No","Moderate",3.0,"Order Review","Confirm service codes and order details before authorization submission"],
    ["PARCS-017","Pain Management Procedure","Commercial","Denied","Prior conservative treatment documentation was missing","Incomplete","Weak","Yes","Routine","Yes","High",7.0,"Documentation Readiness","Add supporting-treatment documentation checklist"],
    ["PARCS-018","Specialist Follow-Up","Medicaid","Approved","Authorization approved after manual follow-up","Complete","Moderate","Yes","Routine","No","Moderate",1.5,"Payer Follow-Up","Track payer follow-up attempts and response deadlines"],
    ["PARCS-019","Diagnostic Ultrasound","Commercial","Approved","No authorization required after payer review","Complete","Strong","Yes","Routine","No","Low",0.5,"Authorization Requirement Check","Document no-authorization-required confirmation clearly"],
    ["PARCS-020","Rehabilitation Services","Medicare Advantage","Pending","Visit limit verification incomplete","Partial","Moderate","Late","Routine","No","Moderate",2.5,"Benefit Verification","Verify visit limits and remaining benefits before service"],
    ["PARCS-021","Ambulatory Procedure","Commercial","Denied","Authorization was approved for wrong service type","Complete","Moderate","Yes","Urgent","Yes","Critical",8.0,"Order and Authorization Match","Match authorization approval details to scheduled service before clearance"],
    ["PARCS-022","Oncology Infusion","Medicare Advantage","Pending","High-cost service requires additional payer review","Complete","Strong","Yes","Urgent","No","High",4.0,"Payer Follow-Up","Escalate high-cost pending cases earlier in the workflow"],
    ["PARCS-023","ENT Procedure","Medicaid","Not Started","Patient coverage inactive at time of verification","Incomplete","Missing","No","Routine","Yes","Critical",7.5,"Eligibility Verification","Resolve coverage status before authorization submission"],
    ["PARCS-024","Advanced Imaging","Commercial","Denied","Peer-to-peer review was not completed before deadline","Complete","Moderate","Yes","Urgent","Yes","High",6.5,"Clinical Escalation","Track peer-to-peer deadlines and escalation ownership"],
    ["PARCS-025","Specialty Medication","Medicare Advantage","Pending","Medication authorization requires missing dosage clarification","Partial","Weak","Yes","Urgent","No","High",5.5,"Documentation and Order Review","Clarify dosage and supporting documentation before payer submission"],
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
        @import url('https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; color: {BLACK}; background: {WHITE}; }}
        .block-container {{ padding-top: 2.5rem; padding-bottom: 3rem; max-width: 1220px; }}
        .hero {{ background: linear-gradient(135deg,#FFFFFF 0%,#FFFFFF 65%,#FFF4EA 100%); border:1px solid {LINE_GRAY}; border-radius:30px; padding:48px 50px; box-shadow:0 14px 40px rgba(0,0,0,.04); }}
        .eyebrow {{ color:{TENNESSEE_ORANGE}; letter-spacing:.14em; text-transform:uppercase; font-weight:700; font-size:.78rem; margin-bottom:14px; }}
        .hero h1, .section-title {{ font-family:'Newsreader',Georgia,serif; }}
        .hero h1 {{ font-size:clamp(3rem,6vw,5.8rem); line-height:.92; letter-spacing:-.035em; margin:0 0 20px; max-width:900px; }}
        .hero p {{ max-width:860px; font-size:1.05rem; line-height:1.72; color:{DARK_GRAY}; }}
        .tag-row {{ display:flex; flex-wrap:wrap; gap:9px; margin-top:24px; }}
        .tag {{ border:1px solid rgba(255,130,0,.42); border-radius:999px; padding:7px 12px; font-size:.77rem; font-weight:600; background:rgba(255,130,0,.07); }}
        .section-title {{ font-size:2.35rem; font-weight:600; margin-top:42px; margin-bottom:4px; letter-spacing:-.02em; }}
        .section-rule {{ width:78px; height:3px; background:{TENNESSEE_ORANGE}; border-radius:999px; margin-bottom:20px; }}
        .integrity, .insight-box {{ background:{WARM_GRAY}; border-left:5px solid {TENNESSEE_ORANGE}; border-radius:0 20px 20px 0; padding:22px 26px; line-height:1.7; margin:18px 0 28px; }}
        .metric-card {{ border:1px solid {LINE_GRAY}; border-radius:22px; padding:23px; min-height:138px; background:{WHITE}; }}
        .metric-label {{ font-size:.75rem; font-weight:700; text-transform:uppercase; letter-spacing:.10em; color:{DARK_GRAY}; }}
        .metric-value {{ font-family:'Newsreader',Georgia,serif; font-size:3.15rem; font-weight:600; line-height:1; margin-top:12px; }}
        .metric-note {{ font-size:.84rem; line-height:1.45; margin-top:9px; color:#5a514b; }}
        .node-grid {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:16px; margin-top:16px; }}
        .node {{ border:1px solid {LINE_GRAY}; border-radius:20px; padding:20px; background:{WHITE}; min-height:135px; }}
        .node h4 {{ margin:0 0 8px; font-size:.95rem; }}
        .node p {{ margin:0; font-size:.84rem; line-height:1.55; color:#5a514b; }}
        .footer {{ margin-top:54px; padding:36px 24px; border-top:1px dashed rgba(255,130,0,.65); text-align:center; background:linear-gradient(180deg,#FFFFFF 0%,#FFF9F3 100%); border-radius:26px; }}
        .footer a {{ color:{BLACK}; font-weight:600; }}
        @media (max-width:900px) {{ .hero {{ padding:34px 24px; }} .node-grid {{ grid-template-columns:1fr; }} }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">Healthcare Operations Intelligence Engine™ · Student Portfolio</div>
        <h1>PARCS — Prior Authorization Command System</h1>
        <p>I built PARCS to study what happens when a prior authorization looks like one task, but the real problem started earlier somewhere else in the workflow.</p>
        <p>As I work toward my Bachelor's of Science degree in Healthcare Administration, I use this synthetic case set to practice prior authorization workflow analysis, documentation readiness, ownership, escalation, patient-access thinking, and denial-prevention reasoning without presenting student work as professional healthcare employment.</p>
        <div class="tag-row">
            <span class="tag">Prior Authorization</span><span class="tag">Patient Access</span><span class="tag">Documentation Readiness</span><span class="tag">Workflow Analysis</span><span class="tag">Denial Prevention</span><span class="tag">Synthetic Data</span>
        </div>
    </div>
    <div class="integrity"><strong>Student-developed · simulated · no PHI.</strong> No real patient, payer, employer, claim, EHR, or authorization data is used. This dashboard does not make clinical, coding, coverage, medical-necessity, or payer decisions.</div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Why I Built PARCS</div><div class="section-rule"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="insight-box">
        From the patient side, a prior authorization problem may simply feel like waiting, uncertainty, another phone call, or a changed appointment. Inside the workflow, that same problem may involve eligibility, documentation, payer follow-up, aging, ownership, or service clearance. I built PARCS to practice connecting those two views and asking: <strong>Where did the authorization workflow first lose control?</strong>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Synthetic Case Set</div><div class="section-rule"></div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
metrics = [
    ("Total Cases", len(df), "Fictional cases in this learning dataset"),
    ("Retro-Auth Review", len(retro_cases), "Synthetic cases marked for retro-authorization review"),
    ("High / Critical Risk", len(high_critical), "Cases I would prioritize for human review"),
    ("Avg. Modeled Rework", f"{df['Estimated Rework Hours'].mean():.1f} hrs", "Educational estimate per case"),
]
for col, (label, value, note) in zip([c1, c2, c3, c4], metrics):
    with col:
        st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

st.caption("All counts and modeled rework values come only from this synthetic dataset. They are not healthcare benchmarks or real-world performance results.")

st.markdown('<div class="section-title">How I Think About the Workflow</div><div class="section-rule"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="node-grid">
        <div class="node"><h4>1. Scheduling / Intake</h4><p>Identify the service, payer, referral needs, and authorization requirement before the case moves forward.</p></div>
        <div class="node"><h4>2. Eligibility</h4><p>Check whether coverage information is current enough to support the next step.</p></div>
        <div class="node"><h4>3. Documentation</h4><p>Review whether the order, notes, and supporting information are ready for submission.</p></div>
        <div class="node"><h4>4. Submission</h4><p>Track whether the authorization has actually been started and whether required information was sent.</p></div>
        <div class="node"><h4>5. Payer Follow-Up</h4><p>Watch aging, additional-information requests, response deadlines, and unresolved status.</p></div>
        <div class="node"><h4>6. Escalation</h4><p>Make ownership and the next action visible when a case is approaching risk.</p></div>
        <div class="node"><h4>7. Service Clearance</h4><p>Review unresolved or mismatched authorization issues before the scheduled service.</p></div>
        <div class="node"><h4>8. Downstream Readiness</h4><p>Connect authorization status to claim-readiness and denial-prevention thinking.</p></div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Risk Review</div><div class="section-rule"></div>', unsafe_allow_html=True)
left, right = st.columns([1.08, .92])
with left:
    risk_counts = df["Denial Risk Level"].value_counts().rename_axis("Risk Level").reset_index(name="Cases")
    risk_counts["Risk Sort"] = risk_counts["Risk Level"].map(risk_order)
    risk_counts = risk_counts.sort_values("Risk Sort")
    chart = alt.Chart(risk_counts).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
        x=alt.X("Risk Level:N", sort=["Low", "Moderate", "High", "Critical"], title=None),
        y=alt.Y("Cases:Q", title="Synthetic cases"),
        tooltip=["Risk Level", "Cases"],
        color=alt.value(TENNESSEE_ORANGE),
    ).properties(height=320)
    st.altair_chart(chart, use_container_width=True)
with right:
    st.markdown("### What I look for")
    st.write("I use the High and Critical categories to practice deciding which synthetic cases deserve attention first. The risk label is a learning aid, not a payer or clinical determination.")
    st.metric("Modeled Rework Hours", f"{df['Estimated Rework Hours'].sum():.1f}")
    st.metric("Documentation Gap Cases", len(doc_gap_cases))
    st.metric("Eligibility Issue Cases", len(eligibility_issues))

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("#### Workflow failure points")
    failure_counts = df["Workflow Failure Point"].value_counts().rename_axis("Failure Point").reset_index(name="Cases")
    st.dataframe(failure_counts, use_container_width=True, hide_index=True)
with col_b:
    st.markdown("#### High / Critical cases by payer type")
    payer_risk = high_critical.groupby("Payer Type").size().reset_index(name="High/Critical Cases").sort_values("High/Critical Cases", ascending=False)
    st.dataframe(payer_risk, use_container_width=True, hide_index=True)

st.markdown('<div class="section-title">Case Explorer</div><div class="section-rule"></div>', unsafe_allow_html=True)
st.write("I use these filters to practice narrowing a workqueue and reviewing the reason a case became at risk.")
risk_filter = st.multiselect("Filter by modeled denial-risk level", ["Low", "Moderate", "High", "Critical"], default=["High", "Critical"])
status_filter = st.multiselect("Filter by authorization status", sorted(df["Authorization Status"].unique()), default=sorted(df["Authorization Status"].unique()))
filtered = df[df["Denial Risk Level"].isin(risk_filter) & df["Authorization Status"].isin(status_filter)]
st.dataframe(filtered.drop(columns=["Risk Rank"]), use_container_width=True, hide_index=True)

st.markdown('<div class="section-title">Possible Workflow Controls</div><div class="section-rule"></div>', unsafe_allow_html=True)
st.write("These are student-developed responses to patterns in the synthetic cases. They are not organization-specific recommendations or validated interventions.")
fixes = high_critical[["Workflow Failure Point", "Recommended Fix"]].drop_duplicates().sort_values("Workflow Failure Point")
st.dataframe(fixes, use_container_width=True, hide_index=True)

st.markdown('<div class="section-title">Pre-Service vs. Post-Service Authorization Exception Review™</div><div class="section-rule"></div>', unsafe_allow_html=True)
st.write(
    "This interactive workbench practices what happens when a pre-service authorization control is incomplete and the case must move through an evidence-based exception workflow. It does not determine whether a real payer permits retroactive or retrospective authorization."
)

st.markdown(
    """
    <div class="insight-box">
        <strong>Operational distinctions</strong><br>
        Retro request submitted ≠ authorization resolved.<br>
        Missing prior authorization ≠ automatic eligibility for post-service review.<br>
        Technically open ≠ actively moving.<br>
        Submission ≠ closure.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("Open Authorization Exception Workbench", expanded=True):
    left, right = st.columns(2)

    with left:
        authorization_required = st.checkbox("Authorization requirement identified", key="retro_requirement")
        payer_source_reviewed = st.checkbox("Applicable payer / program source reviewed", key="retro_source")
        service_performed = st.checkbox("Service already performed", value=True, key="retro_service")
        pre_service_complete = st.checkbox("Pre-service authorization completed", key="retro_precomplete")
        miss_reason = st.selectbox(
            "Reason pre-service authorization was not completed",
            [
                "Not established / needs review",
                "Requirement not identified before service",
                "Documentation not ready",
                "Ownership / handoff gap",
                "Submission not completed",
                "Service / date / provider / location mismatch",
                "Emergency or other exception scenario requires qualified review",
            ],
            key="retro_reason",
        )
        retro_path = st.selectbox(
            "Post-service / retrospective review pathway",
            [
                "Not established — source review required",
                "Potentially available in this synthetic scenario",
                "Not supported by the reviewed synthetic rule path",
                "Qualified specialist review required",
            ],
            key="retro_path",
        )

    with right:
        documentation_requirements = st.checkbox("Documentation requirements identified", key="retro_docreq")
        documentation_ready = st.checkbox("Required documentation ready", key="retro_docready")
        service_alignment = st.checkbox("Service / date / provider / location alignment reviewed", key="retro_alignment")
        qualified_review = st.checkbox("Qualified review routed when needed", key="retro_qualified")
        owner = st.selectbox(
            "Current owner",
            [
                "Unassigned",
                "Prior Authorization Support",
                "Patient Access",
                "Documentation / Clinical Support",
                "Payer Follow-Up",
                "Claims / A/R Follow-Up",
                "Qualified Specialist Review",
            ],
            key="retro_owner",
        )
        case_status = st.selectbox(
            "Case status",
            ["Needs Rule Review", "Pending Evidence", "Submitted / Follow-Up Due", "Specialist Review", "Closed"],
            key="retro_status",
        )

    st.markdown("#### Active-Movement Control™")
    m1, m2, m3 = st.columns(3)
    with m1:
        last_action = st.date_input("Last meaningful action", value=date.today(), key="retro_last_action")
    with m2:
        next_due = st.date_input("Next-action due date", value=date.today() + timedelta(days=2), key="retro_due")
    with m3:
        escalation = st.selectbox(
            "Escalation threshold",
            ["Not reached", "Approaching threshold", "Reached — escalation required"],
            key="retro_escalation",
        )

    next_action = st.selectbox(
        "Next required action",
        [
            "Review applicable payer / program source",
            "Confirm missing authorization condition",
            "Identify documentation requirements",
            "Route for qualified review",
            "Submit post-service review request",
            "Confirm payer receipt / status",
            "Follow up with payer",
            "Route downstream claim action",
            "Document closure evidence",
        ],
        key="retro_next_action",
    )
    evidence_note = st.text_area(
        "Evidence / documentation note",
        placeholder="Synthetic example: current payer source reviewed; service details compared; missing document identified; qualified review routed.",
        key="retro_evidence_note",
    )

    days_since_action = max(0, (date.today() - last_action).days)
    st.caption(
        f"Active-movement view: {days_since_action} day(s) since last meaningful action · Owner: {owner} · "
        f"Next action due: {next_due.isoformat()} · Escalation: {escalation}"
    )

    st.markdown("#### Submission, Determination, and Closure")
    c1, c2, c3 = st.columns(3)
    with c1:
        request_submitted = st.checkbox("Request submitted", key="retro_submitted")
        submission_evidence = st.checkbox("Submission evidence documented", key="retro_submission_evidence")
    with c2:
        receipt_confirmed = st.checkbox("Receipt / status confirmed", key="retro_receipt")
        final_determination = st.checkbox("Final determination received", key="retro_determination")
    with c3:
        downstream_action = st.checkbox("Required downstream account action completed", key="retro_downstream")
        closure_verified = st.checkbox("Closure evidence verified", key="retro_closure")

    closure_evidence = st.text_area(
        "Closure evidence",
        placeholder="Synthetic example: final determination documented, downstream action completed, no required follow-up remains, and closure verified.",
        key="retro_closure_note",
    )

    patient_effect = st.selectbox(
        "Potential patient-facing effect",
        [
            "Coverage uncertainty",
            "Unexpected bill / balance concern",
            "Additional phone calls",
            "Post-service administrative delay",
            "Claim uncertainty",
            "No modeled patient-facing effect identified",
        ],
        key="retro_patient_effect",
    )

    st.markdown("#### PARCS Control Gate")
    if not service_performed and not pre_service_complete:
        st.warning("Pre-service control remains open. The simulated case should not be treated as cleared while required authorization review remains unresolved.")
    elif service_performed and (not authorization_required or not payer_source_reviewed):
        st.warning("Post-service pathway not established. Requirement identification and current payer/program source review are still needed.")
    elif service_performed and retro_path == "Not established — source review required":
        st.warning("Exception path still unresolved. A post-service request should not be treated as the default response.")
    elif service_performed and retro_path in ["Not supported by the reviewed synthetic rule path", "Qualified specialist review required"]:
        st.info("Route to qualified review or another revenue-cycle workflow. PARCS does not independently decide the payer or contractual outcome.")
    elif service_performed and (not documentation_requirements or not service_alignment or owner == "Unassigned"):
        st.warning("Exception pathway identified, but control is incomplete. Documentation requirements, service alignment, and ownership are not fully established.")
    elif service_performed and (not request_submitted or not submission_evidence or not receipt_confirmed):
        st.info("Post-service review is active but not resolved. Submission evidence and receipt/status confirmation remain open.")
    elif service_performed and (not final_determination or not downstream_action or not closure_verified or not closure_evidence.strip()):
        st.info("Determination or closure work remains. A submitted request is not closure.")
    else:
        st.success("Modeled closure verified. The synthetic case has the required evidence trail for closure within this educational workflow.")

    st.markdown(
        """
        <div class="insight-box">
            <strong>Control question:</strong><br>
            If a service has already occurred without completed authorization, what evidence should determine whether the case enters an allowable post-service review path, escalates for specialist review, or moves to another revenue-cycle workflow?
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "**Patient-to-professional perspective:** The patient experiences the uncertainty after the service. "
        "The operations team has to reconstruct whether the required control happened before service, what exception path is available now, "
        "what evidence is required, who owns resolution, and what proves closure."
    )
    st.caption(
        "Educational boundary: PARCS does not determine medical necessity, coverage, coding accuracy, payer liability, contractual rights, legal obligations, "
        "or whether a real payer must permit retroactive or retrospective authorization."
    )

st.markdown('<div class="section-title">What I Learned</div><div class="section-rule"></div>', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="insight-box">
        This simulated dashboard contains <strong>{len(df)} cases</strong>, including <strong>{len(retro_cases)} retro-authorization review cases</strong> and <strong>{len(high_critical)} High or Critical risk cases</strong>. What matters more to me than the counts is the pattern behind them: a late authorization problem can be the visible end of an earlier eligibility, documentation, requirement, follow-up, or ownership breakdown.<br><br>
        The patient usually does not see those internal labels. The patient sees whether care moves forward, whether another call is needed, or whether the plan changes. PARCS is how I practice tracing that visible experience back through the workflow without pretending a synthetic model proves real-world outcomes.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="footer">
        <strong>PARCS — Prior Authorization Command System</strong><br><br>
        Created by Kori Pickle<br>
        Student-developed portfolio project · Synthetic data only · No PHI<br>
        Not formal healthcare employment · Not clinical, coding, coverage, medical-necessity, or payer decision-making.<br><br>
        <a href="https://healthcare-operations-portfolio-hub.vercel.app/" target="_blank">Portfolio Hub</a> ·
        <a href="https://www.linkedin.com/in/kori-pickle" target="_blank">LinkedIn</a> ·
        <a href="https://github.com/koripickle1101-TN/parcs-prior-authorization-command-system" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True,
)
