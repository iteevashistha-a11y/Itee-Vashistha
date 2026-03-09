import streamlit as st

st.set_page_config(page_title="CCSCR ", page_icon="", layout="wide")

st.title("🧠 CCSCR -My project")
st.caption("Elite. Refine. Clear instructions.")

st.divider()

# ===============================
# CCSCR INPUT SECTION
# ===============================

st.header("📌 CCSCR Framework Input")

col1, col2 = st.columns(2)
"Create ONE"
with col1:
    context = st.text_area(
        "1️⃣ Context Requirements",
        placeholder="Clear, Crisp, Data Driven...",
        height=140
    )

    constraints = st.text_area(
        "2️⃣ Constraint Specifications",
        placeholder="Policies, tone limits, boundaries...",
        height=140
    )

with col2:
    structure = st.text_area(
        "3️⃣ Structure Mandates",
        placeholder="Organized, formatting, output, Clean style...",
        height=140
    )

    checkpoints = st.text_area(
        "4️⃣ Checkpoint Integration",
        placeholder="Risks, assumptions, confidence...",
        height=140
    )

review = st.text_area(
    "5️⃣ Review Protocols",
    placeholder="Approval of rules & Regulations, revision logic...",
    height=140
)

st.divider()

# ===============================
# DRAFT PROMPT INPUT
# ===============================

st.header("✏️ Your Rough Prompt / Idea")

draft_prompt = st.text_area(
    "Paste your rough prompt or requirement:",
    height=140,
    placeholder="Example: There should be more promote response by customer service.."
)

# ===============================
# ENHANCEMENT ENGINE
# ===============================

def generate_ccscr_prompt(context, constraints, structure, checkpoints, review, draft):
    enhanced_prompt = f"""
You must follow the CCSCR Essential Controls Framework.

CONTEXT REQUIREMENTS:
{context}

CONSTRAINT SPECIFICATIONS:
{constraints}

STRUCTURE MANDATES:
{structure}

CHECKPOINT INTEGRATION:
{checkpoints}

REVIEW PROTOCOLS:
{review}

TASK:
{draft}
"""
    return enhanced_prompt


def analyze_prompt_quality(draft):
    feedback = []

    if len(draft.split()) < 8:
        feedback.append("⚠ Your prompt is very short. Consider adding clarity on goals or outputs.")

    if "report" not in draft.lower():
        feedback.append("💡 Tip: Specify output style (report, table, bullets, strategy doc, etc.).")

    if "analyze" not in draft.lower():
        feedback.append("💡 Tip: Use action verbs (analyze, generate, design, evaluate, compare).")

    if not feedback:
        feedback.append("✅ Prompt looks reasonably structured.")

    return feedback


# ===============================
# BUTTON ACTIONS
# ===============================

colA, colB = st.columns(2)

with colA:
    if st.button("🚀 Generate CCSCR Prompt", use_container_width=True):
        if not draft_prompt.strip():
            st.error("Please enter your rough prompt.")
        else:
            enhanced = generate_ccscr_prompt(
                context,
                constraints,
                structure,
                checkpoints,
                review,
                draft_prompt
            )

            st.success("Structured CCSCR Prompt Generated")

            st.code(enhanced, language="markdown")


with colB:
    if st.button("🔍 Improve My Prompt Thinking", use_container_width=True):
        if not draft_prompt.strip():
            st.error("Please enter your rough prompt.")
        else:
            feedback = analyze_prompt_quality(draft_prompt)

            st.subheader("🧠 Prompt Intelligence Feedback")

            for item in feedback:
                st.write(item)

st.divider()

# ===============================
# PROMPT REFINEMENT ASSISTANT
# ===============================

st.header("🛠 Prompt Refinement Assistant")

if draft_prompt:
    refined_prompt = st.text_area(
        "Refine / Expand Your Prompt:",
        value=draft_prompt,
        height=140
    )

    if st.button("✨ Re-Enhance Using CCSCR"):
        enhanced = generate_ccscr_prompt(
            context,
            constraints,
            structure,
            checkpoints,
            review,
            refined_prompt
        )

        st.success("Enhanced Prompt (Refined Version)")

        st.code(enhanced, language="markdown")

st.divider()

st.caption("Designed for CCSCR-Driven Prompt Engineering & Report Generation")
