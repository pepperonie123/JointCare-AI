import streamlit as st

st.set_page_config(
    page_title="JointCare AI",
    page_icon="🦵",
    layout="centered"
)

# -----------------------------
# TITLE
# -----------------------------

st.title("🦵 JointCare AI")
st.subheader("AI-Assisted Osteoarthritis Screening")

st.write(
    "A preliminary screening system designed to "
    "assist healthcare workers in identifying "
    "individuals who may require further clinical evaluation."
)

st.divider()

# -----------------------------
# PATIENT INFORMATION
# -----------------------------

st.header("👤 Patient Information")

patient_id = st.text_input("Patient ID")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=40
)

sex = st.selectbox(
    "Sex",
    ["Female", "Male", "Other"]
)

occupation = st.selectbox(
    "Occupation",
    [
        "Farmer",
        "Manual Labour",
        "Office Work",
        "Student",
        "Other"
    ]
)

st.divider()

# -----------------------------
# SYMPTOMS
# -----------------------------

st.header("🦵 Joint Symptoms")

pain = st.slider(
    "Knee pain level (0–10)",
    0,
    10,
    0
)

stiffness = st.radio(
    "Morning stiffness?",
    ["Yes", "No"]
)

previous_injury = st.radio(
    "Previous knee injury?",
    ["Yes", "No"]
)

walking_difficulty = st.radio(
    "Difficulty while walking?",
    ["Yes", "No"]
)

stairs = st.radio(
    "Difficulty climbing stairs?",
    ["Yes", "No"]
)

st.divider()

# -----------------------------
# MOVEMENT ASSESSMENT
# -----------------------------

st.header("🚶 Movement Assessment")

st.write(
    "Ask the patient to walk approximately "
    "5 metres in front of the camera."
)

walking_video = st.file_uploader(
    "📹 Upload Walking Video",
    type=["mp4", "mov", "avi"]
)

if walking_video is not None:

    st.success("Walking video uploaded successfully!")

    st.video(walking_video)

    st.divider()

    if st.button(
        "🧠 Analyse Movement",
        type="primary"
    ):

        st.info(
            "Movement analysis module will process "
            "the video here."
        )

        st.write("Patient ID:", patient_id)
        st.write("Age:", age)
        st.write("Pain Score:", pain)

        st.success(
            "Video received successfully. "
            "AI analysis module is ready for the next stage."
        )
