import streamlit as st

st.set_page_config(
    page_title="JointCare AI",
    page_icon="🦵",
    layout="centered"
)

st.title("🦵 JointCare AI")
st.subheader("AI-Assisted Osteoarthritis Screening")

st.write(
    "A preliminary screening tool designed to assist "
    "healthcare workers in identifying individuals who "
    "may require further clinical evaluation."
)

st.divider()

st.header("Patient Information")

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

if st.button("Continue to Movement Assessment", type="primary"):

    if patient_id == "":
        st.warning("Please enter a Patient ID.")
    else:
        st.success("Patient information recorded!")
        st.info(
            "Next step: movement and gait assessment."
        )
