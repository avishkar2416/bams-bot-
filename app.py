import streamlit as st
from google import genai
from google.genai import types
import json
import time
import html


# ============================================================
# 🌿 AYURVEDA AI — PREMIUM BAMS STUDY STUDIO
# ============================================================

st.set_page_config(
    page_title="AyurVeda AI | BAMS Study Studio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 🎨 PREMIUM APP DESIGN
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Mukta:wght@400;500;600;700;800;900&display=swap');

:root {
    --orange: #ea580c;
    --saffron: #d97706;
    --gold: #f59e0b;
    --deep: #7c2d12;
    --cream: #fffaf0;
    --paper: #fffdf7;
    --ink: #172033;
}


/* ============================================================
   APP BACKGROUND
   ============================================================ */

html,
body,
.stApp {

    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(251,191,36,.18),
            transparent 25%
        ),
        radial-gradient(
            circle at 95% 5%,
            rgba(234,88,12,.12),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #fffaf0 0%,
            #fffdf9 45%,
            #fff7ed 100%
        ) !important;

    font-family:
        'Mukta',
        'Plus Jakarta Sans',
        sans-serif !important;

    color:
        var(--ink) !important;
}


/* ============================================================
   STREAMLIT CLEAN
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {

    max-width: 1380px;

    padding-top:
        1rem !important;

    padding-bottom:
        3rem !important;
}


/* ============================================================
   NAVBAR
   ============================================================ */

.premium-nav {

    position: relative;

    overflow: hidden;

    display: flex;

    align-items: center;

    justify-content: space-between;

    gap: 15px;

    padding: 13px 16px;

    margin-bottom: 20px;

    border-radius: 23px;

    border:
        1px solid
        rgba(217,119,6,.25);

    background:
        rgba(255,255,255,.78);

    backdrop-filter:
        blur(20px);

    box-shadow:
        0 14px 40px
        rgba(120,53,15,.08);
}


.premium-nav::after {

    content: "ॐ";

    position: absolute;

    right: 22px;

    top: -35px;

    font-size: 110px;

    color: #d97706;

    opacity: .045;
}


.brand {

    display: flex;

    align-items: center;

    gap: 11px;

    position: relative;

    z-index: 2;
}


.brand-mark {

    width: 46px;

    height: 46px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            #fff9df,
            #fef3c7
        );

    border:
        1px solid
        #f2cf72;

    box-shadow:
        0 7px 18px
        rgba(180,83,9,.12);

    font-size: 24px;
}


.brand-title {

    font-family:
        'Plus Jakarta Sans',
        sans-serif !important;

    font-size: 19px;

    font-weight: 800;

    margin: 0;

    background:
        linear-gradient(
            90deg,
            #9a3412,
            #d97706,
            #a16207
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


.brand-sub {

    color:
        #9a5a13 !important;

    font-size:
        9px;

    font-weight:
        800;

    letter-spacing:
        .5px;
}


.creator-pill {

    position: relative;

    z-index: 2;

    padding:
        8px 13px;

    border:
        1px solid
        rgba(217,119,6,.25);

    border-radius:
        999px;

    background:
        #fff8e6;

    color:
        #8a4b08 !important;

    font-size:
        11px;

    font-weight:
        800;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    position:
        relative;

    overflow:
        hidden;

    padding:
        29px 30px;

    margin-bottom:
        21px;

    border-radius:
        27px;

    background:
        radial-gradient(
            circle at 88% 8%,
            rgba(255,255,255,.18),
            transparent 22%
        ),
        radial-gradient(
            circle at 0% 100%,
            rgba(251,191,36,.16),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #9a3412,
            #c2410c 50%,
            #7f1d1d
        );

    border:
        1px solid
        rgba(254,240,138,.55);

    box-shadow:
        0 22px 50px
        rgba(127,29,29,.18);
}


.hero::after {

    content:
        "✦";

    position:
        absolute;

    right:
        35px;

    top:
        5px;

    font-size:
        120px;

    color:
        white;

    opacity:
        .07;
}


.hero-kicker {

    display:
        inline-flex;

    padding:
        5px 11px;

    border:
        1px solid
        rgba(255,255,255,.3);

    border-radius:
        999px;

    background:
        rgba(255,255,255,.12);

    color:
        white !important;

    font-size:
        11px;

    font-weight:
        800;

    letter-spacing:
        .4px;
}


.hero-title {

    color:
        white !important;

    font-family:
        'Plus Jakarta Sans',
        sans-serif !important;

    font-size:
        29px;

    font-weight:
        800;

    margin:
        11px 0 6px;
}


.hero-description {

    max-width:
        920px;

    margin:
        0;

    color:
        rgba(255,255,255,.9) !important;

    font-size:
        14px;

    line-height:
        1.6;
}


/* ============================================================
   SECTION TITLE
   ============================================================ */

.section-title {

    display:
        flex;

    align-items:
        center;

    gap:
        9px;

    margin:
        6px 0 11px;

    color:
        #63350f !important;

    font-family:
        'Plus Jakarta Sans',
        sans-serif !important;

    font-size:
        14px;

    font-weight:
        800;
}


.section-title::before {

    content:
        "";

    width:
        4px;

    height:
        18px;

    border-radius:
        20px;

    background:
        linear-gradient(
            #f59e0b,
            #ea580c
        );
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {

    background:
        rgba(255,255,255,.94) !important;

    border:
        1px solid
        #ead8c2 !important;

    border-radius:
        14px !important;

    min-height:
        47px;

    box-shadow:
        0 4px 14px
        rgba(120,53,15,.035) !important;

    transition:
        .2s ease !important;
}


div[data-baseweb="select"] > div:hover,
div[data-baseweb="input"] > div:hover,
div[data-baseweb="textarea"] > div:hover {

    border-color:
        #e5a629 !important;

    box-shadow:
        0 7px 20px
        rgba(217,119,6,.12) !important;
}


input,
textarea {

    color:
        #172033 !important;

    font-weight:
        600 !important;
}


[data-testid="stWidgetLabel"] p {

    color:
        #59320e !important;

    font-size:
        12.5px !important;

    font-weight:
        800 !important;
}


/* ============================================================
   RADIO
   ============================================================ */

div[role="radiogroup"] {

    gap:
        5px !important;
}


div[role="radiogroup"] label {

    background:
        rgba(255,255,255,.72);

    border:
        1px solid
        rgba(180,83,9,.12);

    border-radius:
        11px;

    padding:
        6px 9px;
}


/* ============================================================
   BUTTON
   ============================================================ */

div.stButton > button {

    min-height:
        53px !important;

    border:
        0 !important;

    border-radius:
        16px !important;

    color:
        white !important;

    background:
        linear-gradient(
            135deg,
            #ea580c,
            #d97706 52%,
            #b45309
        ) !important;

    font-family:
        'Plus Jakarta Sans',
        sans-serif !important;

    font-size:
        14px !important;

    font-weight:
        800 !important;

    box-shadow:
        0 12px 28px
        rgba(194,65,12,.25) !important;

    transition:
        .2s ease !important;
}


div.stButton > button:hover {

    transform:
        translateY(-2px) !important;

    box-shadow:
        0 17px 34px
        rgba(194,65,12,.32) !important;
}


/* ============================================================
   TABS
   ============================================================ */

.stTabs [data-baseweb="tab-list"] {

    gap:
        6px;

    padding:
        5px;

    border-radius:
        18px;

    background:
        rgba(255,255,255,.68);

    border:
        1px solid
        rgba(180,83,9,.10);
}


.stTabs [data-baseweb="tab"] {

    height:
        46px;

    padding:
        0 18px !important;

    border-radius:
        12px !important;

    color:
        #71400f !important;

    font-weight:
        800 !important;

    border:
        0 !important;
}


.stTabs [aria-selected="true"] {

    background:
        linear-gradient(
            135deg,
            #fff3cf,
            #ffe4b2
        ) !important;

    color:
        #9a3412 !important;

    box-shadow:
        0 5px 16px
        rgba(217,119,6,.12);
}


.stTabs [aria-selected="true"] * {

    color:
        #9a3412 !important;
}


/* ============================================================
   RESULT CARD
   ============================================================ */

.result-card {

    padding:
        21px 23px;

    border:
        1px solid
        rgba(180,83,9,.12);

    border-radius:
        20px;

    background:
        rgba(255,255,255,.78);

    box-shadow:
        0 13px 36px
        rgba(120,53,15,.06);

    margin-top:
        10px;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {

    text-align:
        center;

    margin-top:
        40px;

    padding:
        20px 10px 4px;

    color:
        #8a5a20 !important;

    font-size:
        12px;

    font-weight:
        700;
}


.footer-line {

    width:
        90px;

    height:
        1px;

    margin:
        0 auto 11px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #d97706,
            transparent
        );
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .block-container {

        padding-left:
            .75rem !important;

        padding-right:
            .75rem !important;
    }


    .premium-nav {

        padding:
            10px 11px;

        border-radius:
            18px;
    }


    .brand-mark {

        width:
            40px;

        height:
            40px;

        font-size:
            21px;
    }


    .brand-title {

        font-size:
            15px;
    }


    .brand-sub {

        font-size:
            7.5px;
    }


    .creator-pill {

        font-size:
            8px;

        padding:
            6px 8px;
    }


    .hero {

        padding:
            23px 18px;

        border-radius:
            21px;
    }


    .hero-title {

        font-size:
            22px;
    }


    .hero-description {

        font-size:
            12px;
    }


    .stTabs [data-baseweb="tab"] {

        padding:
            0 8px !important;

        font-size:
            10.5px !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 🔑 GEMINI API
# ============================================================

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    ""
)

if not api_key:

    st.error(
        "⚠️ Streamlit Secrets मध्ये GEMINI_API_KEY configure करा."
    )

    st.stop()


client = genai.Client(
    api_key=api_key
)


# ============================================================
# 🤖 GEMINI CALL
# ============================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def cached_ask_gemini(
    prompt: str,
    as_json: bool = False
):

    model_name = "gemini-3.6-flash"

    last_error = None

    for attempt in range(3):

        try:

            config = None

            if as_json:

                config = types.GenerateContentConfig(
                    response_mime_type="application/json"
                )

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config
            )

            if response and response.text:

                return response.text

        except Exception as error:

            last_error = error

            error_text = str(error)

            if (
                "429" in error_text
                or
                "RESOURCE_EXHAUSTED" in error_text
            ):

                time.sleep(16)

            else:

                time.sleep(2)

    raise RuntimeError(
        f"तांत्रिक अडचण आली: {last_error}"
    )


# ============================================================
# 📄 A4 HANDWRITTEN SHEET GENERATOR
# ============================================================

def create_a4_handwritten_doc(
    data,
    subject_name,
    topic_name,
    is_marathi=True
):

    # --------------------------------------------------------
    # SAFE DATA
    # --------------------------------------------------------

    marks = str(
        data.get(
            "exam_marks",
            "१० गुण - दीर्घोत्तरी (LAQ)"
            if is_marathi
            else
            "10 Marks - LAQ"
        )
    )

    title = str(
        data.get(
            "main_heading",
            topic_name
        )
    )

    entity1 = data.get(
        "entity_1",
        {}
    )

    entity2 = data.get(
        "entity_2",
        {}
    )

    flow_steps = data.get(
        "flowchart_steps",
        []
    )

    include_flowchart = bool(
        data.get(
            "include_flowchart",
            False
        )
    )

    comparison = data.get(
        "comparison_table",
        []
    )


    # --------------------------------------------------------
    # LABELS
    # --------------------------------------------------------

    if is_marathi:

        label_definition = "व्याख्या"

        label_points_1 = "परीक्षेसाठी महत्त्वाचे मुद्दे"

        label_points_2 = "लक्षणे व चिकित्सा"

        label_key = "★ मुख्य संकल्पना"

        label_modern = "★ परीक्षेसाठी महत्त्वाचा मुद्दा"

        label_flow = "संप्राप्ती / प्रवाह तक्ता"

        label_table = "★ परीक्षा तुलनात्मक तक्ता"

        label_feature = "मुद्दा / लक्षण"

        label_punch = "✍️ परीक्षेसाठी मुख्य सूत्र"

        label_png = "📸 A4 PNG जतन करा"

        label_print = "📄 PDF / PRINT"

    else:

        label_definition = "Definition"

        label_points_1 = "High-Yield Exam Points"

        label_points_2 = "Clinical Features & Treatment"

        label_key = "★ Key Exam Concept"

        label_modern = "★ Important Exam Point"

        label_flow = "Pathogenesis / Flowchart"

        label_table = "★ Quick Exam Comparison"

        label_feature = "Feature"

        label_punch = "✍️ Exam Punch Line"

        label_png = "📸 Save A4 PNG"

        label_print = "📄 PDF / PRINT"


    # --------------------------------------------------------
    # POINT LISTS
    # --------------------------------------------------------

    points1_html = ""

    for point in entity1.get(
        "key_points",
        []
    ):

        points1_html += (
            "<li>"
            + str(point)
            + "</li>"
        )


    points2_html = ""

    for point in entity2.get(
        "key_points",
        []
    ):

        points2_html += (
            "<li>"
            + str(point)
            + "</li>"
        )


    # --------------------------------------------------------
    # FLOWCHART
    # --------------------------------------------------------

    flow_html = ""

    if include_flowchart and flow_steps:

        flow_parts = []

        for index, step in enumerate(
            flow_steps[:4]
        ):

            if index == len(flow_steps[:4]) - 1:

                flow_parts.append(
                    '<div class="flow-final">'
                    + str(step)
                    + '</div>'
                )

            else:

                flow_parts.append(
                    '<div class="flow-step">'
                    + str(step)
                    + '</div>'
                )

                flow_parts.append(
                    '<div class="flow-arrow">↓</div>'
                )


        flow_html = (
            '<div class="flow-section">'
            '<div class="flow-label">'
            + label_flow +
            '</div>'
            '<div class="flow-body">'
            + "".join(flow_parts) +
            '</div>'
            '</div>'
        )


    # --------------------------------------------------------
    # COMPARISON TABLE
    # --------------------------------------------------------

    table_html = ""

    if comparison:

        rows = ""

        for row in comparison[:3]:

            rows += (
                "<tr>"
                "<td><b>"
                + str(
                    row.get(
                        "feature",
                        ""
                    )
                )
                + "</b></td>"
                "<td>"
                + str(
                    row.get(
                        "point_1",
                        ""
                    )
                )
                + "</td>"
                "<td>"
                + str(
                    row.get(
                        "point_2",
                        ""
                    )
                )
                + "</td>"
                "</tr>"
            )


        table_html = (
            '<div class="section-heading">'
            + label_table +
            '</div>'
            '<table class="compare-table">'
            '<thead>'
            '<tr>'
            '<th>'
            + label_feature +
            '</th>'
            '<th>'
            + str(
                entity1.get(
                    "title",
                    "Concept 1"
                )
            )
            + '</th>'
            '<th>'
            + str(
                entity2.get(
                    "title",
                    "Concept 2"
                )
            )
            + '</th>'
            '</tr>'
            '</thead>'
            '<tbody>'
            + rows +
            '</tbody>'
            '</table>'
        )


    # --------------------------------------------------------
    # FONT
    # --------------------------------------------------------

    if is_marathi:

        font_family = "'Mukta', sans-serif"

    else:

        font_family = (
            "'Patrick Hand', "
            "'Caveat', "
            "cursive, sans-serif"
        )


    # ========================================================
    # IMPORTANT:
    #
    # DO NOT MAKE THIS HTML AN F-STRING.
    #
    # CSS contains { }.
    # Normal string avoids the previous
    # "f-string expecting a }" error.
    # ========================================================

    html_doc = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<script
src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js">
</script>

<style>

@import url(
'https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Caveat:wght@600;700&family=Mukta:wght@500;600;700;800;900&display=swap'
);

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    padding: 18px 10px;

    background: #edf1f6;

    display: flex;

    flex-direction: column;

    align-items: center;

    font-family: FONT_FAMILY;
}

.action-bar {

    display: flex;

    gap: 10px;

    margin-bottom: 15px;

    font-family: Arial, sans-serif;
}

.action-button {

    border: 0;

    border-radius: 11px;

    padding: 10px 16px;

    color: white;

    font-weight: 800;

    cursor: pointer;

    background:
        linear-gradient(
            135deg,
            #0369a1,
            #0284c7
        );

    box-shadow:
        0 6px 17px
        rgba(3,105,161,.25);
}

.action-button.green {

    background:
        linear-gradient(
            135deg,
            #047857,
            #059669
        );
}


/* ========================================================
   REAL A4
   ======================================================== */

.a4-paper {

    width: 794px;

    min-height: 1123px;

    position: relative;

    overflow: hidden;

    padding: 25px 28px;

    background: #fffef9;

    border:
        2px solid
        #17325f;

    box-shadow:
        0 17px 45px
        rgba(15,23,42,.18);

    color: #17325f;

    font-size: 15px;

    line-height: 1.40;
}


/* ruled notebook paper */

.a4-paper::before {

    content: "";

    position: absolute;

    inset: 0;

    pointer-events: none;

    opacity: .18;

    background:
        repeating-linear-gradient(
            0deg,
            transparent 0,
            transparent 29px,
            rgba(23,50,95,.10) 30px
        );
}


.a4-paper > * {

    position: relative;

    z-index: 1;
}


/* ========================================================
   HEADER
   ======================================================== */

.header {

    display: flex;

    justify-content: space-between;

    align-items: center;

    gap: 14px;

    padding-bottom: 9px;

    margin-bottom: 10px;

    border-bottom:
        2px solid
        #17325f;
}


.main-title {

    width: 69%;

    padding: 7px 12px;

    border:
        2px solid
        #17325f;

    border-radius: 10px;

    background: white;

    text-align: center;

    font-size: 21px;

    font-weight: 800;
}


.main-title span {

    border-bottom:
        2px double
        #17325f;

    padding-bottom: 1px;
}


.marks-box {

    padding: 5px 9px;

    border:
        2px solid
        #17325f;

    border-radius: 8px;

    background: white;

    text-align: center;

    font-size: 12px;

    font-weight: 800;
}


/* ========================================================
   RED HIGHLIGHT
   ======================================================== */

.hl-red {

    display: inline-block;

    padding:
        0 4px;

    border-radius: 4px;

    background: #ffe0e5;

    color: #b42318;

    border:
        1px solid
        #fecdd3;

    font-weight: 800;
}


/* ========================================================
   FLOWCHART
   ======================================================== */

.flow-section {

    text-align: center;

    margin:
        5px 0 11px;
}


.flow-label {

    display: inline-block;

    padding:
        2px 10px;

    border:
        1.5px solid
        #17325f;

    border-radius:
        999px;

    background:
        white;

    font-size:
        12px;

    font-weight:
        800;
}


.flow-body {

    margin-top:
        5px;
}


.flow-step {

    width:
        78%;

    margin:
        0 auto;

    padding:
        3px 8px;

    border:
        1.4px solid
        #17325f;

    border-radius:
        8px;

    background:
        white;

    font-size:
        12.5px;

    font-weight:
        600;
}


.flow-final {

    width:
        82%;

    margin:
        0 auto;

    padding:
        4px 8px;

    border:
        1.7px dashed
        #17325f;

    border-radius:
        13px;

    background:
        #fffaf3;

    font-size:
        12.5px;

    font-weight:
        800;
}


.flow-arrow {

    font-size:
        13px;

    font-weight:
        900;

    margin:
        0;
}


/* ========================================================
   MAIN TWO COLUMN ANSWER
   ======================================================== */

.answer-columns {

    display:
        flex;

    gap:
        13px;
}


.answer-column {

    flex:
        1;

    padding:
        0 5px;
}


.answer-column:first-child {

    border-right:
        1.4px dashed
        #17325f;
}


/* ========================================================
   BADGE
   ======================================================== */

.concept-badge {

    display:
        inline-block;

    padding:
        2px 10px;

    margin-bottom:
        3px;

    border:
        1.5px solid
        #17325f;

    border-radius:
        999px;

    background:
        white;

    font-size:
        15px;

    font-weight:
        800;
}


/* ========================================================
   DEFINITION
   ======================================================== */

.definition {

    margin:
        2px 0 5px;

    font-size:
        13px;
}


/* ========================================================
   SECTION HEADING
   ======================================================== */

.section-heading {

    margin:
        6px 0 3px;

    font-size:
        14px;

    font-weight:
        800;

    text-decoration:
        underline;
}


/* ========================================================
   LIST
   ======================================================== */

.exam-list {

    margin:
        2px 0 6px;

    padding-left:
        17px;

    font-size:
        13px;
}


.exam-list li {

    margin-bottom:
        3px;
}


/* ========================================================
   KEY BOX
   ======================================================== */

.key-box {

    padding:
        6px 8px;

    margin-top:
        5px;

    border:
        1.4px dashed
        #17325f;

    border-radius:
        8px;

    background:
        #fcfcf8;

    font-size:
        12px;

    line-height:
        1.35;
}


/* ========================================================
   TABLE
   ======================================================== */

.compare-table {

    width:
        100%;

    border-collapse:
        collapse;

    margin:
        3px 0 8px;

    background:
        white;

    font-size:
        12px;
}


.compare-table th,
.compare-table td {

    border:
        1.3px solid
        #17325f;

    padding:
        4px 6px;

    text-align:
        left;
}


.compare-table th {

    background:
        #f8fafc;

    font-weight:
        800;
}


/* ========================================================
   EXAM PUNCH
   ======================================================== */

.exam-punch {

    margin-top:
        8px;

    padding-top:
        7px;

    border-top:
        2px solid
        #17325f;

    font-size:
        13px;

    font-weight:
        800;
}


/* ========================================================
   FOOTER
   ======================================================== */

.paper-footer {

    position:
        absolute;

    right:
        20px;

    bottom:
        7px;

    font-family:
        Arial,
        sans-serif;

    font-size:
        9px;

    opacity:
        .55;
}


/* ========================================================
   PRINT
   ======================================================== */

@media print {

    body {

        padding:
            0;

        background:
            white;
    }

    .action-bar {

        display:
            none;
    }

    .a4-paper {

        border:
            0;

        box-shadow:
            none;
    }
}

</style>

</head>


<body>


<div class="action-bar">

<button
class="action-button"
onclick="downloadPNG()">
PNG_BUTTON
</button>


<button
class="action-button green"
onclick="window.print()">
PRINT_BUTTON
</button>

</div>


<div
class="a4-paper"
id="a4Canvas">


<!-- HEADER -->

<div class="header">

<div class="main-title">

<span>
TITLE_TEXT
</span>

</div>


<div class="marks-box">

<b>
SUBJECT_TEXT
</b>

<br>

<span class="hl-red">
🎯 MARKS_TEXT
</span>

</div>

</div>


FLOW_HTML


<!-- ANSWER -->

<div class="answer-columns">


<!-- LEFT -->

<div class="answer-column">

<div class="concept-badge">

① T1_TITLE

</div>


<div class="definition">

<b>
DEFINITION_TEXT:
</b>

T1_DEFINITION

</div>


<div class="section-heading">

POINTS_1_TITLE

</div>


<ul class="exam-list">

T1_POINTS

</ul>


<div class="key-box">

<b>
KEY_TEXT
</b>

<br>

T1_KEY

</div>

</div>


<!-- RIGHT -->

<div class="answer-column">

<div class="concept-badge">

② T2_TITLE

</div>


<div class="definition">

<b>
DEFINITION_TEXT:
</b>

T2_DEFINITION

</div>


<div class="section-heading">

POINTS_2_TITLE

</div>


<ul class="exam-list">

T2_POINTS

</ul>


<div class="key-box">

<b>
MODERN_TEXT
</b>

<br>

T2_KEY

</div>

</div>


</div>


TABLE_HTML


<!-- PUNCH -->

<div class="exam-punch">

PUNCH_TEXT

→

"EXAM_PUNCH"

</div>


<div class="paper-footer">

🌿 AyurVeda AI • BAMS Study Studio • Avishkar Alase

</div>


</div>


<script>

function downloadPNG() {

    const element =
        document.getElementById(
            "a4Canvas"
        );

    html2canvas(
        element,
        {
            scale: 2.2,
            useCORS: true,
            backgroundColor: "#fffef9"
        }
    ).then(function(canvas) {

        const link =
            document.createElement("a");

        link.download =
            "AyurVeda_AI_A4_Notes.png";

        link.href =
            canvas.toDataURL(
                "image/png"
            );

        link.click();

    });

}

</script>

</body>

</html>
"""


    # ========================================================
    # REPLACE PLACEHOLDERS
    # ========================================================

    replacements = {

        "FONT_FAMILY":
            font_family,

        "PNG_BUTTON":
            label_png,

        "PRINT_BUTTON":
            label_print,

        "TITLE_TEXT":
            title,

        "SUBJECT_TEXT":
            str(subject_name),

        "MARKS_TEXT":
            marks,

        "FLOW_HTML":
            flow_html,

        "T1_TITLE":
            str(
                entity1.get(
                    "title",
                    "Core Concept"
                )
            ),

        "T2_TITLE":
            str(
                entity2.get(
                    "title",
                    "Clinical Features"
                )
            ),

        "DEFINITION_TEXT":
            label_definition,

        "T1_DEFINITION":
            str(
                entity1.get(
                    "definition",
                    ""
                )
            ),

        "T2_DEFINITION":
            str(
                entity2.get(
                    "definition",
                    ""
                )
            ),

        "POINTS_1_TITLE":
            label_points_1,

        "POINTS_2_TITLE":
            label_points_2,

        "T1_POINTS":
            points1_html,

        "T2_POINTS":
            points2_html,

        "KEY_TEXT":
            label_key,

        "MODERN_TEXT":
            label_modern,

        "T1_KEY":
            str(
                entity1.get(
                    "exam_key",
                    ""
                )
            ),

        "T2_KEY":
            str(
                entity2.get(
                    "exam_key",
                    ""
                )
            ),

        "TABLE_HTML":
            table_html,

        "PUNCH_TEXT":
            label_punch,

        "EXAM_PUNCH":
            str(
                data.get(
                    "exam_punch_line",
                    ""
                )
            )
    }


    for key, value in replacements.items():

        html_doc = html_doc.replace(
            key,
            value
        )


    return html_doc


# ============================================================
# 🌿 NAVBAR
# ============================================================

st.html("""
<div class="premium-nav">

    <div class="brand">

        <div class="brand-mark">
            🪔
        </div>

        <div>

            <div class="brand-title">
                🌿 AyurVeda AI
            </div>

            <div class="brand-sub">
                BAMS STUDY STUDIO • FESTIVE PREMIUM EDITION
            </div>

        </div>

    </div>


    <div class="creator-pill">
        ✦ Created by Avishkar Alase
    </div>

</div>
""")


# ============================================================
# 📚 TABS
# ============================================================

tab1, tab2 = st.tabs([
    "📖  BAMS Study Studio",
    "🧪  Medicine & Manufacturing"
])


# ============================================================
# 📖 TAB 1
# ============================================================

with tab1:


    st.html("""
    <div class="hero">

        <span class="hero-kicker">
            🌺 ॥ श्री गणेशाय नमः ॥ • SMART BAMS ASSISTANT
        </span>

        <div class="hero-title">
            🎯 A4 Handwritten Exam Notes
        </div>

        <p class="hero-description">
            फक्त exam मध्ये लिहायला लागेल तेवढेच content.
            Clean headings, important keywords, आवश्यक flowchart
            आणि university-focused answer format.
        </p>

    </div>
    """)


    st.html("""
    <div class="section-title">
        🎓 Academic Setup
    </div>
    """)


    # --------------------------------------------------------
    # ACADEMIC YEAR + SUBJECT
    # --------------------------------------------------------

    col1, col2 = st.columns(
        [1, 1.2]
    )


    with col1:

        bams_year = st.selectbox(

            "🎓 BAMS वर्ष / Academic Year",

            [
                "BAMS 1st Professional (प्रथम वर्ष)",
                "BAMS 2nd Professional (द्वितीय वर्ष)",
                "BAMS 3rd Professional (तृतीय वर्ष)",
                "BAMS Final Professional (अंतिम वर्ष)"
            ]
        )


    with col2:

        subject = st.selectbox(

            "📚 विषय / Subject",

            [
                "Agada Tantra & Vyavahara Ayurveda (अगद तंत्र)",

                "Kriya Sharir (क्रिया शारीर)",

                "Rachana Sharir (रचना शारीर)",

                "Dravyaguna Vijnana (द्रव्यगुण विज्ञान)",

                "Rasashastra & Bhaishajya Kalpana (रसशास्त्र व भैषज्य कल्पना)",

                "Roga Nidan & Vikriti Vigyan (रोगनिदान)",

                "Samhita Siddhant & Charak Samhita (संहिता सिद्धांत)",

                "Kayachikitsa (कायचिकित्सा)",

                "Panchakarma (पंचकर्म)",

                "Shalya Tantra (शल्य तंत्र)",

                "Shalakya Tantra (शालाक्य तंत्र)",

                "Prasuti Tantra & Stri Roga (प्रसूति तंत्र व स्त्रीरोग)",

                "Kaumarbhritya (कौमारभृत्य)"
            ]
        )


    # --------------------------------------------------------
    # MODE + LANGUAGE
    # --------------------------------------------------------

    col3, col4 = st.columns(
        [1.2, 1]
    )


    with col3:

        study_mode = st.selectbox(

            "🎯 Study Mode",

            [
                "📋 A4 Blue Ballpen Handwritten Sheet",

                "📖 Comprehensive Notes",

                "📜 Only Shlokas & Meanings",

                "📝 10-Mark LAQ Answer Format",

                "⚡ Quick Revision / Viva Voce Points"
            ]
        )


    with col4:

        language_preference = st.radio(

            "🌐 माध्यम / Language",

            [
                "मराठी (संस्कृत + सोपा अर्थ + Modern Terms)",

                "Simple Indian English + Sanskrit"
            ],

            horizontal=True
        )


    # --------------------------------------------------------
    # TOPIC
    # --------------------------------------------------------

    topic = st.text_input(

        "🔍 Topic / Question",

        placeholder=(
            "उदा. Pitta Dosha • Garavisha vs Dooshivisha • "
            "Ashwagandha • Pandu Roga"
        )
    )


    generate_btn = st.button(

        "🚀  Generate Exam-Ready Notes",

        key="generate_notes",

        use_container_width=True
    )


    # ========================================================
    # GENERATE NOTES
    # ========================================================

    if generate_btn:


        if not topic.strip():

            st.warning(
                "⚠️ कृपया Topic / Question टाका."
            )


        else:


            is_marathi = (
                "मराठी"
                in language_preference
            )


            # =================================================
            # A4 MODE
            # =================================================

            if "A4 Blue Ballpen" in study_mode:


                if is_marathi:

                    language_instruction = """

LANGUAGE:

Write in simple natural Marathi used by
BAMS students in Maharashtra.

Use Sanskrit Ayurveda terms where appropriate.

Use simple English medical terms in brackets
only when genuinely useful.

Do not use unnecessarily literary Marathi.

"""

                else:

                    language_instruction = """

LANGUAGE:

STRICT ENGLISH + ROMAN SANSKRIT ONLY.

Do NOT use Marathi.

Do NOT use Devanagari.

Examples:

Pitta Dosha
Ushna Guna
Tikshna Guna
Rakta Dhatu
Virechana
Pachaka Pitta

"""


                # =================================================
                # EXAM-ONLY PROMPT
                # =================================================

                prompt = f"""

You are a senior BAMS Ayurveda Professor,
University examiner and question paper setter.

You are preparing ONE handwritten exam sheet.

Academic Year:
{bams_year}

Subject:
{subject}

Topic / Question:
{topic}

{language_instruction}


=========================================================
MOST IMPORTANT OBJECTIVE
=========================================================

CREATE ONLY EXAM-WRITING CONTENT.

The student will use your output directly
to write a university answer.

DO NOT create comprehensive study notes.

DO NOT write a textbook explanation.

DO NOT add unnecessary information.

DO NOT repeat concepts.

DO NOT add motivational content.

DO NOT add long paragraphs.

Every point must help the student score marks.

=========================================================
MARKS
=========================================================

Decide whether the topic should be:

5 Marks - SAQ

OR

10 Marks - LAQ

For short-note topics:
choose 5 Marks.

For topics requiring multiple headings such as
Nidana, Samprapti, Lakshana and Chikitsa:
choose 10 Marks.

=========================================================
5 MARK ANSWER
=========================================================

Target approximately 120-170 words.

Include only:

• Definition
• 4-6 important points
• Essential Lakshana / features
• Essential Chikitsa if applicable
• One short conclusion

=========================================================
10 MARK ANSWER
=========================================================

Target approximately 220-300 words.

Include only relevant sections:

• Definition
• Nidana / Causes
• Samprapti
• Lakshana
• Classification if important
• Chikitsa
• Important drugs / procedures if relevant
• One flowchart OR comparison table if useful
• Conclusion

DO NOT force every section.

=========================================================
FLOWCHART
=========================================================

Use flowchart ONLY if the topic genuinely
has a sequence or Samprapti.

Maximum 4 steps.

Example:

Nidana
↓
Dosha Prakopa
↓
Dushya involvement
↓
Vyadhi manifestation

If not useful:

include_flowchart = false

flowchart_steps = []

=========================================================
COMPARISON TABLE
=========================================================

Use comparison ONLY if the question contains
two entities that students need to differentiate.

Maximum 3 rows.

Otherwise:

comparison_table = []

=========================================================
RED HIGHLIGHT
=========================================================

Highlight only very important exam keywords.

Use exactly:

<span class="hl-red">KEYWORD</span>

Highlight:

• Cardinal symptoms
• Important Dosha
• Important Guna
• Important Nidana
• Important Chikitsa
• Important drugs
• Important classical terms
• Important mechanisms

Do NOT highlight whole sentences.

=========================================================
EXAM STYLE
=========================================================

Write like a BAMS student writing an answer sheet.

Use:

• Short headings
• Numbered points
• Short bullets
• Simple sentences
• Classical terminology
• High-yield facts

Avoid:

• Long explanations
• Repetition
• History
• Research discussion
• Excessive modern correlation
• Unnecessary examples
• Unnecessary references

=========================================================
IMPORTANT
=========================================================

The complete answer MUST comfortably fit
on ONE A4 handwritten sheet.

LESS CONTENT + MORE MARKS.

=========================================================
OUTPUT
=========================================================

Return ONLY valid JSON.

No Markdown.

No explanation outside JSON.

Use exactly:

{{
    "exam_marks": "10 Marks - LAQ",

    "main_heading": "Clean Topic Heading",

    "include_flowchart": false,

    "flowchart_steps": [],

    "entity_1": {{
        "title": "Definition & Core Points",

        "definition": "1-2 line exam-ready definition with <span class='hl-red'>important keyword</span>",

        "key_points": [
            "Important point 1",
            "Important point 2",
            "Important point 3",
            "Important point 4",
            "Important point 5"
        ],

        "exam_key": "One very important exam concept."
    }},

    "entity_2": {{
        "title": "Lakshana & Chikitsa",

        "definition": "",

        "key_points": [
            "Essential Lakshana",
            "Essential Lakshana",
            "Important Chikitsa",
            "Important drug or procedure",
            "Important management point"
        ],

        "exam_key": "One high-yield exam point."
    }},

    "comparison_table": [],

    "exam_punch_line": "One short memorable conclusion."
}}

=========================================================
FINAL CHECK
=========================================================

Before returning JSON silently check:

1. Can this be written in the university exam?
2. Is the content only what is needed for marks?
3. Is it short enough for one A4 sheet?
4. Are unnecessary explanations removed?
5. Are important keywords highlighted?
6. Is the selected 5/10 mark level appropriate?
7. Is the language correct?

Return ONLY JSON.
"""


                with st.spinner(
                    "✍️ Exam-ready A4 handwritten sheet तयार करत आहे..."
                ):


                    try:

                        raw_json = cached_ask_gemini(
                            prompt,
                            as_json=True
                        )


                        clean_json = raw_json.strip()


                        if clean_json.startswith(
                            "```json"
                        ):

                            clean_json = clean_json[7:]


                        if clean_json.startswith(
                            "```"
                        ):

                            clean_json = clean_json[3:]


                        if clean_json.endswith(
                            "```"
                        ):

                            clean_json = clean_json[:-3]


                        sheet_data = json.loads(
                            clean_json.strip()
                        )


                        st.success(
                            "✅ Exam-ready A4 Sheet तयार झाली!"
                        )


                        st.components.v1.html(

                            create_a4_handwritten_doc(

                                sheet_data,

                                subject,

                                topic,

                                is_marathi=is_marathi
                            ),

                            height=1290,

                            scrolling=True
                        )


                    except Exception as error:

                        st.error(
                            f"❌ A4 Sheet तयार करताना त्रुटी: {error}"
                        )


            # =================================================
            # OTHER MODES
            # =================================================

            else:


                normal_prompt = f"""

You are a senior BAMS Ayurveda Professor.

Academic Year:
{bams_year}

Subject:
{subject}

Study Mode:
{study_mode}

Topic:
{topic}

Language:
{language_preference}

Create high-yield BAMS study material.

Strictly follow the selected study mode.

Use:

• Clear headings
• Short paragraphs
• Exam-focused bullets
• Bold important terms
• Sanskrit terminology
• Tables where genuinely useful
• Flowcharts where genuinely useful

If English is selected:
use English + Roman Sanskrit.

Do not add unnecessary information.

Make the answer useful for university examinations.
"""


                with st.spinner(
                    "⚡ AI exam notes तयार करत आहे..."
                ):


                    try:

                        notes = cached_ask_gemini(
                            normal_prompt,
                            as_json=False
                        )


                        st.success(
                            "✅ Notes तयार झाल्या!"
                        )


                        st.markdown(
                            '<div class="result-card">',
                            unsafe_allow_html=True
                        )


                        st.markdown(
                            notes
                        )


                        st.markdown(
                            '</div>',
                            unsafe_allow_html=True
                        )


                    except Exception as error:

                        st.error(
                            f"❌ त्रुटी: {error}"
                        )


# ============================================================
# 🧪 TAB 2 — MEDICINE & MANUFACTURING
# ============================================================

with tab2:


    st.html("""
    <div class="hero"
         style="
         background:
         radial-gradient(
             circle at 88% 8%,
             rgba(255,255,255,.16),
             transparent 22%
         ),
         linear-gradient(
             135deg,
             #075e54,
             #0f766e 55%,
             #115e59
         );
         box-shadow:
         0 22px 50px
         rgba(15,118,110,.18);
         ">

        <span class="hero-kicker">
            🌿 RASAUSHADHI VIDHI • FORMULATION LAB
        </span>

        <div class="hero-title">
            🧪 Medicine & Manufacturing Studio
        </div>

        <p class="hero-description">
            Ayurvedic formulation ingredients, preparation sequence,
            Shodhana concepts, manufacturing steps and
            exam-focused points in a clean format.
        </p>

    </div>
    """)


    st.html("""
    <div class="section-title">
        🧪 Formulation Setup
    </div>
    """)


    med_col1, med_col2 = st.columns(
        [1.2, 1]
    )


    with med_col1:

        dosage_form = st.selectbox(

            "🏺 औषधाचा प्रकार / Dosage Form",

            [
                "Vati / Gutika (गोळी / वटी)",

                "Churna (चूर्ण)",

                "Asava & Arishta (आसव व अरिष्ट)",

                "Taila / Ghrita (सिद्ध तेल व घृत)",

                "Bhasma & Pishti (भस्म व पिष्टी)"
            ]
        )


    with med_col2:

        medicine_language = st.radio(

            "🌐 भाषा / Language",

            [
                "Simple Indian English",
                "मराठी"
            ],

            horizontal=True,

            key="medicine_language"
        )


    medicine_name = st.text_input(

        "💊 औषधाचे नाव / Medicine Name",

        placeholder=(
            "उदा. Arogyavardhini Vati • "
            "Chandraprabha Vati • Triphala Churna"
        )
    )


    medicine_btn = st.button(

        "🔬  Generate Formulation Guide",

        key="medicine_generate",

        use_container_width=True
    )


    if medicine_btn:


        if not medicine_name.strip():

            st.warning(
                "⚠️ कृपया औषधाचे नाव टाका."
            )


        else:


            medicine_prompt = f"""

You are a senior Ayurveda Professor
teaching BAMS students.

Explain this Ayurvedic formulation:

Medicine:
{medicine_name}

Dosage Form:
{dosage_form}

Language:
{medicine_language}

Provide exam-oriented educational information.

Include:

1. Introduction
2. Classical purpose
3. Ingredients
4. Shodhana / purification if applicable
5. Preparation sequence
6. Important manufacturing points
7. Quality-control concepts
8. Important BAMS exam points
9. Classical dose and Anupana as academic information
10. Safety precautions

Keep the explanation clear and structured.

Clearly distinguish classical Ayurvedic
description from modern safety and quality practices.

Do not provide personalized medical advice.
"""


            with st.spinner(
                "🔬 Formulation Guide तयार करत आहे..."
            ):


                try:

                    medicine_result = cached_ask_gemini(

                        medicine_prompt,

                        as_json=False
                    )


                    st.success(
                        "✅ Formulation Guide तयार झाला!"
                    )


                    st.markdown(
                        '<div class="result-card">',
                        unsafe_allow_html=True
                    )


                    st.markdown(
                        medicine_result
                    )


                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )


                except Exception as error:

                    st.error(
                        f"❌ त्रुटी: {error}"
                    )


# ============================================================
# 🌺 FOOTER
# ============================================================

st.html("""
<div class="footer">

    <div class="footer-line"></div>

    🌺 ॥ गणपती बाप्पा मोरया ॥ 🌿

    <br><br>

    <strong>AyurVeda AI</strong>
    • BAMS Study Studio
    • Crafted with ❤️ by
    <strong>Avishkar Alase</strong>

</div>
""")
