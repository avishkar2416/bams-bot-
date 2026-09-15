import streamlit as st
from google import genai
from google.genai import types
import json
import time
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AyurVeda AI | BAMS Study Studio",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PREMIUM APP CSS
# =========================================================

st.markdown(
    """
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Mukta:wght@400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap'
);


/* ======================================================
   GLOBAL
   ====================================================== */

html,
body,
.stApp {

    background:
        radial-gradient(
            circle at 50% 0%,
            #fffdf5 0%,
            #fff7df 25%,
            #fffaf0 55%,
            #f7faf7 100%
        ) !important;

    font-family:
        'Mukta',
        sans-serif !important;

    color:
        #172554 !important;

    overflow-x:
        hidden;
}


.stApp * {

    font-family:
        'Mukta',
        sans-serif;
}


/* ======================================================
   HIDE STREAMLIT DEFAULT
   ====================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background:
        transparent !important;
}


/* ======================================================
   TOP BRAND
   ====================================================== */

.premium-navbar {

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    gap:
        15px;

    padding:
        15px 20px;

    margin-bottom:
        20px;

    border:
        1px solid
        rgba(217,119,6,.22);

    border-radius:
        22px;

    background:
        rgba(255,255,255,.82);

    backdrop-filter:
        blur(18px);

    box-shadow:
        0 12px 35px
        rgba(146,64,14,.10);
}


.brand-left {

    display:
        flex;

    align-items:
        center;

    gap:
        12px;
}


.brand-icon {

    width:
        48px;

    height:
        48px;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    border-radius:
        15px;

    background:
        linear-gradient(
            135deg,
            #fff7ed,
            #fef3c7
        );

    border:
        1px solid
        #fcd34d;

    font-size:
        26px;

    box-shadow:
        0 6px 18px
        rgba(245,158,11,.16);
}


.brand-title {

    font-size:
        22px;

    font-weight:
        900;

    line-height:
        1.1;

    color:
        #92400e !important;
}


.brand-sub {

    margin-top:
        3px;

    font-size:
        11px;

    font-weight:
        700;

    letter-spacing:
        .4px;

    color:
        #b45309 !important;
}


.creator-pill {

    padding:
        8px 14px;

    border-radius:
        30px;

    background:
        #fff7ed;

    border:
        1px solid
        #fed7aa;

    color:
        #92400e !important;

    font-size:
        12px;

    font-weight:
        800;
}


/* ======================================================
   HERO
   ====================================================== */

.hero {

    position:
        relative;

    overflow:
        hidden;

    padding:
        27px 25px;

    margin-bottom:
        22px;

    border-radius:
        24px;

    color:
        white !important;

    background:
        linear-gradient(
            135deg,
            #7c2d12 0%,
            #c2410c 45%,
            #b45309 100%
        );

    border:
        1px solid
        rgba(254,240,138,.75);

    box-shadow:
        0 20px 45px
        rgba(154,52,18,.28);
}


.hero:after {

    content:
        "✦";

    position:
        absolute;

    right:
        30px;

    top:
        8px;

    font-size:
        75px;

    opacity:
        .12;
}


.hero * {
    color:
        white !important;
}


.hero-kicker {

    display:
        inline-block;

    padding:
        5px 12px;

    border-radius:
        30px;

    background:
        rgba(255,255,255,.15);

    border:
        1px solid
        rgba(255,255,255,.30);

    font-size:
        11px;

    font-weight:
        800;

    letter-spacing:
        .7px;

    margin-bottom:
        9px;
}


.hero h2 {

    margin:
        0 0 6px 0;

    font-size:
        27px;

    font-weight:
        900;
}


.hero p {

    margin:
        0;

    font-size:
        14px;

    line-height:
        1.6;

    opacity:
        .94;
}


/* ======================================================
   TABS
   ====================================================== */

.stTabs [data-baseweb="tab-list"] {

    gap:
        10px;

    margin-bottom:
        20px;
}


.stTabs [data-baseweb="tab"] {

    border:
        1px solid
        #fed7aa;

    border-radius:
        14px;

    padding:
        10px 18px;

    background:
        rgba(255,255,255,.75);

    font-weight:
        800;

    color:
        #78350f !important;
}


.stTabs [aria-selected="true"] {

    color:
        white !important;

    background:
        linear-gradient(
            135deg,
            #b45309,
            #ea580c
        ) !important;

    border-color:
        #ea580c !important;

    box-shadow:
        0 8px 20px
        rgba(234,88,12,.20);
}


/* ======================================================
   INPUTS
   ====================================================== */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {

    background:
        rgba(255,255,255,.92) !important;

    border:
        1.5px solid
        #fed7aa !important;

    border-radius:
        14px !important;

    box-shadow:
        0 3px 10px
        rgba(146,64,14,.05) !important;
}


div[data-baseweb="select"] > div:focus-within,
div[data-baseweb="input"] > div:focus-within {

    border-color:
        #f59e0b !important;

    box-shadow:
        0 0 0 3px
        rgba(245,158,11,.12) !important;
}


/* ======================================================
   LABELS
   ====================================================== */

.stSelectbox label,
.stTextInput label,
.stRadio label {

    color:
        #713f12 !important;

    font-weight:
        800 !important;

    font-size:
        13px !important;
}


/* ======================================================
   GENERATE BUTTON
   ====================================================== */

div.stButton > button {

    min-height:
        50px;

    border:
        0 !important;

    border-radius:
        16px !important;

    color:
        white !important;

    background:
        linear-gradient(
            135deg,
            #b45309 0%,
            #ea580c 50%,
            #c2410c 100%
        ) !important;

    font-size:
        16px !important;

    font-weight:
        900 !important;

    box-shadow:
        0 12px 28px
        rgba(194,65,12,.25) !important;

    transition:
        all .22s ease !important;
}


div.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 17px 34px
        rgba(194,65,12,.35) !important;
}


/* ======================================================
   INFO CARD
   ====================================================== */

.setup-card {

    padding:
        16px 18px;

    border-radius:
        18px;

    background:
        rgba(255,255,255,.72);

    border:
        1px solid
        #fde68a;

    margin-bottom:
        18px;

    box-shadow:
        0 7px 22px
        rgba(146,64,14,.06);
}


.setup-title {

    color:
        #92400e !important;

    font-size:
        17px;

    font-weight:
        900;

    margin-bottom:
        5px;
}


/* ======================================================
   FOOTER
   ====================================================== */

.app-footer {

    margin-top:
        40px;

    padding:
        25px 10px;

    text-align:
        center;

    color:
        #92400e !important;

    font-size:
        13px;

    font-weight:
        700;

    border-top:
        1px solid
        #fde68a;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# API KEY
# =========================================================

api_key = st.secrets.get(
    "GEMINI_API_KEY",
    ""
)

if not api_key:

    st.error(
        "⚠️ GEMINI_API_KEY सापडली नाही. "
        "Streamlit Secrets मध्ये GEMINI_API_KEY add करा."
    )

    st.stop()


client = genai.Client(
    api_key=api_key
)


# =========================================================
# GEMINI CALL
# =========================================================

@st.cache_data(
    show_spinner=False,
    ttl=86400
)
def ask_gemini(
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
                "RESOURCE_EXHAUSTED"
                in error_text
            ):

                time.sleep(16)

            else:

                time.sleep(3)

    raise RuntimeError(
        f"Gemini API Error: {last_error}"
    )


# =========================================================
# SAFE HTML HELPERS
# =========================================================

def escape_text(value):

    if value is None:
        return ""

    return html.escape(
        str(value)
    )


def safe_ai_html(value):

    """
    AI ने दिलेले highlight spans ठेवतो,
    बाकी HTML escape करतो.
    """

    if value is None:
        return ""

    text = str(value)

    text = text.replace(
        "<span class='hl-red'>",
        "___START_HIGHLIGHT___"
    )

    text = text.replace(
        '<span class="hl-red">',
        "___START_HIGHLIGHT___"
    )

    text = text.replace(
        "</span>",
        "___END_HIGHLIGHT___"
    )

    text = html.escape(text)

    text = text.replace(
        "___START_HIGHLIGHT___",
        '<span class="hl-red">'
    )

    text = text.replace(
        "___END_HIGHLIGHT___",
        "</span>"
    )

    return text


# =========================================================
# A4 SHEET HTML
# =========================================================

def create_a4_handwritten_sheet(
    data,
    subject_name,
    topic_name,
    is_marathi=True
):

    if is_marathi:

        definition_label = "व्याख्या (Definition)"

        points1_label = (
            "परीक्षेसाठी महत्त्वाचे मुद्दे"
        )

        points2_label = (
            "लक्षणे व चिकित्सा"
        )

        key1_label = (
            "★ मुख्य संकल्पना"
        )

        key2_label = (
            "★ परीक्षेसाठी महत्त्वाचा मुद्दा"
        )

        flow_label = (
            "संप्राप्ती (Pathogenesis)"
        )

        table_label = (
            "★ परीक्षा तुलनात्मक तक्ता"
        )

        punch_label = (
            "✍️ परीक्षेसाठी मुख्य सूत्र"
        )

    else:

        definition_label = "Definition"

        points1_label = (
            "High-Yield Exam Points"
        )

        points2_label = (
            "Clinical Features & Treatment"
        )

        key1_label = (
            "★ Key Exam Concept"
        )

        key2_label = (
            "★ Important Exam Point"
        )

        flow_label = (
            "Pathogenesis / Flowchart"
        )

        table_label = (
            "★ Quick Exam Comparison"
        )

        punch_label = (
            "✍️ Exam Punch Line"
        )


    marks = data.get(
        "exam_marks",
        "१० गुण - दीर्घोत्तरी (LAQ)"
        if is_marathi
        else
        "10 Marks - LAQ"
    )


    title = data.get(
        "main_heading",
        topic_name
    )


    e1 = data.get(
        "entity_1",
        {}
    )


    e2 = data.get(
        "entity_2",
        {}
    )


    # -----------------------------------------------------
    # POINTS
    # -----------------------------------------------------

    points1_html = ""

    for point in e1.get(
        "key_points",
        []
    ):

        points1_html += (
            "<li>"
            + safe_ai_html(point)
            + "</li>"
        )


    points2_html = ""

    for point in e2.get(
        "key_points",
        []
    ):

        points2_html += (
            "<li>"
            + safe_ai_html(point)
            + "</li>"
        )


    # -----------------------------------------------------
    # FLOWCHART
    # -----------------------------------------------------

    flow_html = ""

    flow_steps = data.get(
        "flowchart_steps",
        []
    )


    if (
        data.get(
            "include_flowchart",
            False
        )
        and
        flow_steps
    ):

        flow_html += """
        <div class="flow-section">

            <div class="flow-title">
                FLOW_LABEL
            </div>
        """

        limited_steps = flow_steps[:4]

        for index, step in enumerate(
            limited_steps
        ):

            if index == len(
                limited_steps
            ) - 1:

                flow_html += (
                    '<div class="flow-final">'
                    +
                    safe_ai_html(step)
                    +
                    '</div>'
                )

            else:

                flow_html += (
                    '<div class="flow-box">'
                    +
                    safe_ai_html(step)
                    +
                    '</div>'
                )

                flow_html += (
                    '<div class="flow-arrow">'
                    '↓'
                    '</div>'
                )


        flow_html += """
        </div>
        """


    # -----------------------------------------------------
    # COMPARISON TABLE
    # -----------------------------------------------------

    table_html = ""

    comparison = data.get(
        "comparison_table",
        []
    )


    if comparison:

        table_html = """
        <div class="table-heading">
            TABLE_LABEL
        </div>

        <table>

            <thead>

                <tr>

                    <th>
                        Feature
                    </th>

                    <th>
                        E1_TITLE
                    </th>

                    <th>
                        E2_TITLE
                    </th>

                </tr>

            </thead>

            <tbody>
        """


        for row in comparison[:3]:

            table_html += """

                <tr>

                    <td>
                        <b>
                            ROW_FEATURE
                        </b>
                    </td>

                    <td>
                        ROW_POINT1
                    </td>

                    <td>
                        ROW_POINT2
                    </td>

                </tr>

            """


            table_html = table_html.replace(
                "ROW_FEATURE",
                safe_ai_html(
                    row.get(
                        "feature",
                        ""
                    )
                ),
                1
            )


            table_html = table_html.replace(
                "ROW_POINT1",
                safe_ai_html(
                    row.get(
                        "point_1",
                        ""
                    )
                ),
                1
            )


            table_html = table_html.replace(
                "ROW_POINT2",
                safe_ai_html(
                    row.get(
                        "point_2",
                        ""
                    )
                ),
                1
            )


        table_html += """
            </tbody>

        </table>
        """


    # -----------------------------------------------------
    # HTML TEMPLATE
    #
    # IMPORTANT:
    # NOT AN F-STRING.
    # Therefore CSS { } will never cause SyntaxError.
    # -----------------------------------------------------

    document = """
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<script src="
https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js
"></script>


<style>

@import url(
'https://fonts.googleapis.com/css2?family=Kalam:wght@400;700&family=Mukta:wght@400;500;600;700;800&display=swap'
);


* {
    box-sizing: border-box;
}


body {

    margin: 0;

    padding: 14px;

    background:
        #e9eef4;

    display:
        flex;

    flex-direction:
        column;

    align-items:
        center;

    font-family:
        'Kalam',
        'Mukta',
        cursive;
}


/* ======================================================
   ACTION BUTTONS
   ====================================================== */

.action-bar {

    display:
        flex;

    gap:
        10px;

    margin-bottom:
        15px;

    font-family:
        Arial,
        sans-serif;
}


.action-btn {

    border:
        none;

    border-radius:
        12px;

    padding:
        11px 18px;

    color:
        white;

    font-weight:
        800;

    cursor:
        pointer;

    background:
        linear-gradient(
            135deg,
            #075985,
            #0284c7
        );

    box-shadow:
        0 7px 18px
        rgba(2,132,199,.25);
}


.action-btn.green {

    background:
        linear-gradient(
            135deg,
            #047857,
            #059669
        );
}


/* ======================================================
   A4 PAPER
   ====================================================== */

.a4 {

    width:
        794px;

    height:
        1123px;

    position:
        relative;

    overflow:
        hidden;

    padding:
        24px 28px 20px;

    background:
        #fffefa;

    border:
        2px solid
        #19376d;

    color:
        #173b7a;

    box-shadow:
        0 18px 45px
        rgba(0,0,0,.18);

    font-size:
        15px;

    line-height:
        1.34;
}


/* subtle paper lines */

.a4:before {

    content:
        "";

    position:
        absolute;

    inset:
        0;

    pointer-events:
        none;

    opacity:
        .10;

    background:
        repeating-linear-gradient(
            to bottom,
            transparent 0px,
            transparent 27px,
            #6d8bb8 28px
        );
}


/* ======================================================
   HEADER
   ====================================================== */

.header {

    position:
        relative;

    z-index:
        3;

    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    gap:
        12px;

    padding-bottom:
        9px;

    margin-bottom:
        11px;

    border-bottom:
        2px solid
        #19376d;
}


.title-box {

    width:
        68%;

    padding:
        7px 12px;

    border:
        2px solid
        #19376d;

    border-radius:
        11px;

    background:
        rgba(255,255,255,.96);

    text-align:
        center;

    font-size:
        21px;

    font-weight:
        700;
}


.title-box span {

    border-bottom:
        2px double
        #19376d;
}


.marks-box {

    width:
        28%;

    padding:
        5px 7px;

    border:
        2px solid
        #19376d;

    border-radius:
        9px;

    text-align:
        center;

    background:
        rgba(255,255,255,.96);

    font-size:
        12px;

    font-weight:
        700;
}


/* ======================================================
   HIGHLIGHT
   ====================================================== */

.hl-red {

    display:
        inline;

    padding:
        0 4px;

    border-radius:
        4px;

    background:
        #ffdce3;

    color:
        #a91d32;

    font-weight:
        700;
}


/* ======================================================
   TWO COLUMN
   ====================================================== */

.main-grid {

    position:
        relative;

    z-index:
        2;

    display:
        grid;

    grid-template-columns:
        1fr 1fr;

    gap:
        18px;
}


.left-column {

    padding-right:
        13px;

    border-right:
        1.5px dashed
        #19376d;
}


.right-column {

    padding-left:
        2px;
}


/* ======================================================
   CONCEPT HEADING
   ====================================================== */

.concept-heading {

    display:
        inline-block;

    padding:
        3px 10px;

    margin:
        1px 0 5px;

    border:
        1.6px solid
        #19376d;

    border-radius:
        15px;

    background:
        rgba(255,255,255,.96);

    font-size:
        15px;

    font-weight:
        700;
}


/* ======================================================
   DEFINITION
   ====================================================== */

.definition {

    font-size:
        13.2px;

    margin:
        2px 0 6px;
}


/* ======================================================
   SECTION HEADING
   ====================================================== */

.section-heading {

    margin:
        5px 0 3px;

    font-size:
        15px;

    font-weight:
        700;

    text-decoration:
        underline;

    text-decoration-color:
        #df5268;

    text-decoration-thickness:
        2px;

    text-underline-offset:
        3px;
}


/* ======================================================
   LIST
   ====================================================== */

ul {

    margin:
        2px 0 7px;

    padding-left:
        18px;
}


li {

    margin-bottom:
        3px;

    font-size:
        13.2px;
}


/* ======================================================
   KEY BOX
   ====================================================== */

.key-box {

    padding:
        6px 9px;

    margin:
        7px 0;

    border:
        1.5px dashed
        #19376d;

    border-radius:
        9px;

    background:
        rgba(255,255,255,.91);

    font-size:
        12.2px;

    line-height:
        1.35;
}


/* ======================================================
   FLOWCHART
   ====================================================== */

.flow-section {

    text-align:
        center;

    margin:
        8px 0 10px;
}


.flow-title {

    display:
        inline-block;

    padding:
        2px 11px;

    margin-bottom:
        5px;

    border:
        1.5px solid
        #19376d;

    border-radius:
        12px;

    font-weight:
        700;

    font-size:
        13.5px;

    background:
        white;
}


.flow-box {

    width:
        82%;

    margin:
        0 auto;

    padding:
        4px 7px;

    border:
        1.5px solid
        #19376d;

    border-radius:
        8px;

    background:
        rgba(255,255,255,.95);

    font-size:
        12.5px;
}


.flow-arrow {

    height:
        17px;

    line-height:
        17px;

    font-size:
        17px;

    font-weight:
        700;
}


.flow-final {

    width:
        88%;

    margin:
        0 auto;

    padding:
        5px 8px;

    border:
        2px dashed
        #19376d;

    border-radius:
        13px;

    background:
        #fff0f3;

    font-size:
        12.5px;

    font-weight:
        700;
}


/* ======================================================
   TABLE
   ====================================================== */

.table-heading {

    position:
        relative;

    z-index:
        2;

    margin:
        7px 0 3px;

    font-size:
        14px;

    font-weight:
        700;

    text-decoration:
        underline;
}


table {

    position:
        relative;

    z-index:
        2;

    width:
        100%;

    border-collapse:
        collapse;

    background:
        rgba(255,255,255,.95);

    font-size:
        11.3px;
}


th,
td {

    border:
        1.2px solid
        #19376d;

    padding:
        4px 5px;

    text-align:
        left;

    vertical-align:
        top;
}


th {

    background:
        #fff4df;

    font-weight:
        700;
}


/* ======================================================
   PUNCH LINE
   ====================================================== */

.punch {

    position:
        absolute;

    z-index:
        5;

    left:
        28px;

    right:
        28px;

    bottom:
        48px;

    padding:
        8px 12px;

    border-top:
        2px solid
        #19376d;

    background:
        rgba(255,255,255,.88);

    font-size:
        13.5px;

    font-weight:
        700;
}


.punch-text {

    margin-top:
        3px;

    text-decoration:
        underline;

    text-decoration-color:
        #df5268;

    text-decoration-thickness:
        1.5px;
}


/* ======================================================
   FOOTER
   ====================================================== */

.paper-footer {

    position:
        absolute;

    z-index:
        5;

    right:
        20px;

    bottom:
        14px;

    font-family:
        Arial,
        sans-serif;

    font-size:
        9px;

    color:
        #31558e;

    opacity:
        .9;
}


/* ======================================================
   PRINT
   ====================================================== */

@media print {

    body {

        padding:
            0;

        background:
            white;
    }

    .action-bar {

        display:
            none !important;
    }

    .a4 {

        border:
            none;

        box-shadow:
            none;
    }
}

</style>

</head>


<body>


<div class="action-bar">

<button
class="action-btn"
onclick="downloadPNG()">

📸 Save A4 PNG

</button>


<button
class="action-btn green"
onclick="window.print()">

📄 Print / Save PDF

</button>

</div>


<div
class="a4"
id="a4Canvas">


<!-- =====================================================
     HEADER
     ===================================================== -->

<div class="header">


<div class="title-box">

<span>
TITLE
</span>

</div>


<div class="marks-box">

SUBJECT

<br>

<span class="hl-red">
🎯 MARKS
</span>

</div>


</div>


<!-- =====================================================
     MAIN GRID
     ===================================================== -->

<div class="main-grid">


<!-- LEFT -->

<div class="left-column">


<div class="concept-heading">

① E1_TITLE

</div>


<div class="definition">

<b>
DEFINITION_LABEL:
</b>

E1_DEFINITION

</div>


<div class="section-heading">

POINTS1_LABEL

</div>


<ul>

E1_POINTS

</ul>


<div class="key-box">

<b>
KEY1_LABEL
</b>

<br>

E1_KEY

</div>


</div>


<!-- RIGHT -->

<div class="right-column">


<div class="concept-heading">

② E2_TITLE

</div>


<div class="definition">

<b>
DEFINITION_LABEL:
</b>

E2_DEFINITION

</div>


<div class="section-heading">

POINTS2_LABEL

</div>


<ul>

E2_POINTS

</ul>


<div class="key-box">

<b>
KEY2_LABEL
</b>

<br>

E2_KEY

</div>


FLOWCHART


</div>


</div>


TABLE


<!-- =====================================================
     EXAM PUNCH
     ===================================================== -->

<div class="punch">

PUNCH_LABEL →

<div class="punch-text">

"EXAM_PUNCH"

</div>

</div>


<div class="paper-footer">

🌿 AyurVeda AI
&nbsp;•&nbsp;
BAMS Study Studio
&nbsp;•&nbsp;
By Avishkar Alase

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
            scale: 2.5,

            useCORS: true,

            backgroundColor:
                "#fffefa",

            logging: false
        }
    ).then(
        function(canvas) {

            const link =
                document.createElement(
                    "a"
                );

            link.download =
                "AyurVeda_AI_A4_Notes.png";

            link.href =
                canvas.toDataURL(
                    "image/png"
                );

            link.click();

        }
    );

}

</script>


</body>

</html>
"""


    # =====================================================
    # REPLACE CONTENT
    # =====================================================

    replacements = {

        "TITLE":
            escape_text(title),

        "SUBJECT":
            escape_text(subject_name),

        "MARKS":
            escape_text(marks),

        "E1_TITLE":
            safe_ai_html(
                e1.get(
                    "title",
                    "Core Concept"
                )
            ),

        "E2_TITLE":
            safe_ai_html(
                e2.get(
                    "title",
                    "Clinical Features"
                )
            ),

        "DEFINITION_LABEL":
            definition_label,

        "E1_DEFINITION":
            safe_ai_html(
                e1.get(
                    "definition",
                    ""
                )
            ),

        "E2_DEFINITION":
            safe_ai_html(
                e2.get(
                    "definition",
                    ""
                )
            ),

        "POINTS1_LABEL":
            points1_label,

        "POINTS2_LABEL":
            points2_label,

        "E1_POINTS":
            points1_html,

        "E2_POINTS":
            points2_html,

        "KEY1_LABEL":
            key1_label,

        "KEY2_LABEL":
            key2_label,

        "E1_KEY":
            safe_ai_html(
                e1.get(
                    "exam_key",
                    ""
                )
            ),

        "E2_KEY":
            safe_ai_html(
                e2.get(
                    "exam_key",
                    ""
                )
            ),

        "FLOWCHART":
            flow_html,

        "TABLE":
            table_html,

        "TABLE_LABEL":
            table_label,

        "PUNCH_LABEL":
            punch_label,

        "EXAM_PUNCH":
            safe_ai_html(
                data.get(
                    "exam_punch_line",
                    ""
                )
            )
    }


    for key, value in replacements.items():

        document = document.replace(
            key,
            value
        )


    return document


# =========================================================
# TOP NAVBAR
# =========================================================

st.markdown(
    """
<div class="premium-navbar">

    <div class="brand-left">

        <div class="brand-icon">
            🌿
        </div>

        <div>

            <div class="brand-title">
                AyurVeda AI
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
""",
    unsafe_allow_html=True
)


# =========================================================
# TABS
# =========================================================

tab1, tab2 = st.tabs(
    [
        "📚 BAMS Study Studio",
        "🧪 Medicine & Manufacturing"
    ]
)


# =========================================================
# TAB 1
# =========================================================

with tab1:


    st.markdown(
        """
<div class="hero">

    <div class="hero-kicker">
        🌺 ॥ श्री गणेशाय नमः ॥ • SMART BAMS ASSISTANT
    </div>

    <h2>
        🎯 A4 Handwritten Exam Notes
    </h2>

    <p>
        University-focused Ayurveda notes with
        clean exam hierarchy, high-yield points,
        flowcharts, important keywords and
        premium handwritten A4 output.
    </p>

</div>
""",
        unsafe_allow_html=True
    )


    st.markdown(
        """
<div class="setup-card">

    <div class="setup-title">
        🎓 Academic Setup
    </div>

    <div>
        तुमचे BAMS year, subject, language आणि
        question/topic निवडा. AI फक्त examination
        मध्ये लागणारा आवश्यक content तयार करेल.
    </div>

</div>
""",
        unsafe_allow_html=True
    )


    # -----------------------------------------------------
    # YEAR / SUBJECT
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # MODE / LANGUAGE
    # -----------------------------------------------------

    col3, col4 = st.columns(
        [1.2, 1]
    )


    with col3:

        study_mode = st.selectbox(
            "🎯 अभ्यासाचा प्रकार / Study Mode",
            [
                "📋 A4 Blue Ballpen Handwritten Sheet",
                "📖 Comprehensive Notes",
                "📜 Only Shlokas & Meanings",
                "📝 10-Mark LAQ Answer",
                "⚡ Quick Revision / Viva"
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


    # -----------------------------------------------------
    # TOPIC
    # -----------------------------------------------------

    topic = st.text_input(
        "🔍 अभ्यासाचा विषय / प्रश्न",
        placeholder=
        "उदा. Pitta Dosha, Garavisha vs Dooshivisha, Ashwagandha"
    )


    # -----------------------------------------------------
    # BUTTON
    # -----------------------------------------------------

    generate_button = st.button(
        "🚀 Exam Notes तयार करा",
        key="generate_a4",
        use_container_width=True
    )


    # =====================================================
    # GENERATE
    # =====================================================

    if generate_button:

        if not topic.strip():

            st.warning(
                "⚠️ कृपया अभ्यासाचा विषय टाका."
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

                    language_rule = """
LANGUAGE:
- Simple natural Maharashtra Marathi.
- Use authentic Sanskrit Ayurveda terminology.
- Give English term in brackets only when useful.
- Avoid difficult literary Marathi.
- Write like a BAMS student writes exam answers.
"""

                    marks_example = (
                        "१० गुण - दीर्घोत्तरी (LAQ)"
                    )

                else:

                    language_rule = """
LANGUAGE:
- 100% English + Roman Sanskrit.
- ABSOLUTELY NO Marathi.
- ABSOLUTELY NO Devanagari.
- Sanskrit terms must be Roman transliteration.
- Example: Pitta Dosha, Ushna, Tikshna, Virechana.
"""

                    marks_example = (
                        "10 Marks - LAQ"
                    )


                # =============================================
                # MASTER A4 PROMPT
                # =============================================

                prompt = f"""
You are a senior BAMS Ayurveda Professor,
University Paper Setter and examination mentor.

ACADEMIC YEAR:
{bams_year}

SUBJECT:
{subject}

TOPIC:
{topic}

SELECTED MODE:
{study_mode}

LANGUAGE:
{language_preference}

{language_rule}


=========================================================
MOST IMPORTANT INSTRUCTION
=========================================================

Create ONE SINGLE A4 PAGE of handwritten-style
UNIVERSITY EXAM NOTES.

The student does NOT want textbook notes.

The student wants ONLY the answer content
which is actually required to score marks.

Keep the content SHORT, HIGH-YIELD and
EXAM-ORIENTED.


=========================================================
CONTENT RULE
=========================================================

If the topic is generally asked for 5 marks:

Use:
- Definition
- 4 to 6 important points
- Important Lakshana
- Essential Chikitsa
- One conclusion

If the topic is generally asked for 10 marks:

Use:
- Definition
- Nidana
- Samprapti if applicable
- Lakshana
- Types/classification if important
- Chikitsa
- Important drugs if relevant
- Flowchart if genuinely useful
- Exam conclusion


DO NOT add:

- Long introduction
- History
- Unnecessary explanation
- Repeated points
- Very long paragraphs
- Irrelevant modern medicine
- Extra textbook content


=========================================================
A4 SPACE LIMIT
=========================================================

The final answer MUST comfortably fit on ONE A4 PAGE.

Maximum:
- 6 points in entity_1
- 6 points in entity_2
- 4 flowchart steps
- 3 comparison rows

Every point should be useful for examination.


=========================================================
HIGHLIGHT RULE
=========================================================

Highlight only the most important keywords.

Use exactly:

<span class="hl-red">KEYWORD</span>

Do NOT highlight complete paragraphs.

Examples:

<span class="hl-red">Ushna</span>

<span class="hl-red">Virechana</span>

<span class="hl-red">Daha</span>


=========================================================
FLOWCHART
=========================================================

Use flowchart ONLY if the topic genuinely involves:

- Samprapti
- Pathogenesis
- Stages
- Mechanism
- Sequence

Maximum 4 steps.

Otherwise:

include_flowchart = false

flowchart_steps = []


=========================================================
COMPARISON TABLE
=========================================================

Use comparison_table ONLY if comparison
is genuinely useful.

Maximum 3 rows.

Otherwise return:

comparison_table = []


=========================================================
JSON ONLY
=========================================================

Return ONLY valid JSON.

NO markdown.

NO ```json.

NO explanation outside JSON.

Schema:

{{
    "exam_marks": "{marks_example}",

    "main_heading": "Short Topic Heading",

    "include_flowchart": false,

    "flowchart_steps": [],

    "entity_1": {{

        "title": "Core Concept",

        "definition": "Short 1-2 line exam definition",

        "key_points": [

            "Important exam point",

            "Important exam point",

            "Important exam point",

            "Important exam point",

            "Important exam point"

        ],

        "exam_key":
        "One highly important exam concept."
    }},

    "entity_2": {{

        "title":
        "Lakshana & Chikitsa",

        "definition":
        "Short definition if required",

        "key_points": [

            "Important Lakshana",

            "Important Lakshana",

            "Important Chikitsa",

            "Important treatment",

            "Important drug"

        ],

        "exam_key":
        "One important exam point."
    }},

    "comparison_table": [],

    "exam_punch_line":
    "One memorable sentence which summarizes the answer."
}}

FINAL RULE:

LESS CONTENT + MORE MARKS.

Make it look like a topper's
last-minute university revision sheet.
"""


                # =============================================
                # API
                # =============================================

                with st.spinner(
                    "✍️ Premium A4 handwritten exam sheet तयार होत आहे..."
                ):

                    try:

                        raw = ask_gemini(
                            prompt,
                            as_json=True
                        )


                        clean = raw.strip()


                        if clean.startswith(
                            "```json"
                        ):

                            clean = clean[
                                7:
                            ]


                        if clean.startswith(
                            "```"
                        ):

                            clean = clean[
                                3:
                            ]


                        if clean.endswith(
                            "```"
                        ):

                            clean = clean[
                                :-3
                            ]


                        data = json.loads(
                            clean.strip()
                        )


                        # =====================================
                        # CREATE SHEET
                        # =====================================

                        sheet = (
                            create_a4_handwritten_sheet(
                                data,
                                subject,
                                topic,
                                is_marathi
                            )
                        )


                        st.success(
                            "✅ Premium A4 Exam Sheet तयार झाली!"
                        )


                        st.components.v1.html(
                            sheet,
                            height=1190,
                            scrolling=True
                        )


                    except Exception as error:

                        st.error(
                            f"❌ Error: {error}"
                        )


            # =================================================
            # OTHER STUDY MODES
            # =================================================

            else:


                if is_marathi:

                    language_instruction = """
Write in simple Maharashtra Marathi.
Use Sanskrit Ayurveda terms naturally.
Add English terminology in brackets where useful.
"""

                else:

                    language_instruction = """
Write 100% English.
Use Roman Sanskrit transliteration.
Do not use Devanagari.
Do not use Marathi.
"""


                normal_prompt = f"""

You are a senior BAMS Ayurveda Professor.

Academic Year:
{bams_year}

Subject:
{subject}

Topic:
{topic}

Study Mode:
{study_mode}

Language:
{language_preference}


{language_instruction}


Create high-yield BAMS examination material.

STRICTLY follow the selected study mode.

If this is a 10-mark answer:

- Definition
- Nidana
- Samprapti
- Lakshana
- Types
- Chikitsa
- Important drugs
- Conclusion

If this is Quick Revision:

Use very short bullet points.

If this is Only Shlokas:

Give authentic Sanskrit shloka,
then Anvaya,
then simple meaning.

Use:

**bold**

for important terms.

Do not unnecessarily repeat information.
"""


                with st.spinner(
                    "⚡ AI BAMS notes तयार करत आहे..."
                ):

                    try:

                        result = ask_gemini(
                            normal_prompt,
                            as_json=False
                        )


                        st.success(
                            "✅ Notes तयार झाल्या!"
                        )


                        st.markdown(
                            result
                        )


                    except Exception as error:

                        st.error(
                            f"❌ Error: {error}"
                        )


# =========================================================
# TAB 2
# =========================================================

with tab2:


    st.markdown(
        """
<div class="hero"
style="
background:
linear-gradient(
135deg,
#064e3b,
#0f766e,
#0d9488
);
border-color:#5eead4;
">

    <div class="hero-kicker">
        🌿 RASASHASTRA • BHAISHAJYA KALPANA
    </div>

    <h2>
        🧪 Medicine & Manufacturing Studio
    </h2>

    <p>
        Ayurvedic formulations, ingredients,
        Shodhana and manufacturing steps
        in simple BAMS examination language.
    </p>

</div>
""",
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(
        [1.2, 1]
    )


    with col1:

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


    with col2:

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
        placeholder=
        "उदा. Arogyavardhini Vati / Chandraprabha Vati"
    )


    medicine_button = st.button(
        "🔬 औषध घटक व निर्माण विधी तयार करा",
        key="medicine_button",
        use_container_width=True
    )


    if medicine_button:


        if not medicine_name.strip():

            st.warning(
                "⚠️ कृपया औषधाचे नाव टाका."
            )


        else:


            medicine_prompt = f"""

You are a senior BAMS Ayurveda Professor
specialized in Rasashastra and Bhaishajya Kalpana.

Medicine:
{medicine_name}

Dosage Form:
{dosage_form}

Language:
{medicine_language}


Explain this formulation for BAMS examination.

Include:

1. Introduction
2. Ingredients
3. Quantity if standard and confidently known
4. Shodhana / purification if applicable
5. Bhavana if applicable
6. Manufacturing procedure
7. Important precautions
8. Storage
9. Dose only when appropriate
10. Important exam points


IMPORTANT:

Do NOT invent classical quantities.

If there are multiple classical references,
clearly mention that the formulation may vary
according to reference.

For potentially hazardous mineral/metal preparations,
do NOT provide unsafe experimental instructions.
Keep the explanation academic and reference-oriented.

Use tables where useful.

Keep language simple and examination-friendly.
"""


            with st.spinner(
                f"🔬 {medicine_name} ची माहिती तयार होत आहे..."
            ):

                try:

                    medicine_result = ask_gemini(
                        medicine_prompt,
                        as_json=False
                    )


                    st.success(
                        "✅ Medicine information तयार झाली!"
                    )


                    st.markdown(
                        medicine_result
                    )


                except Exception as error:

                    st.error(
                        f"❌ Error: {error}"
                    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="app-footer">

    🌺 ॥ गणपती बाप्पा मोरया ॥ 🌺

    <br>

    🌿 <strong>AyurVeda AI</strong>
    • BAMS Study Studio

    <br>

    ✦ Developed by
    <strong>Avishkar Alase</strong>

</div>
""",
    unsafe_allow_html=True
)
