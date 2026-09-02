import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import tempfile
import math

# -----------------------------
# PAGE SETTINGS
# -----------------------------

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
    "A preliminary screening system designed to assist "
    "healthcare workers in identifying individuals who "
    "may require further clinical evaluation."
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

# -----------------------------
# KNEE ANGLE FUNCTION
# -----------------------------

def calculate_angle(a, b, c):

    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(
        c[1] - b[1],
        c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1],
        a[0] - b[0]
    )

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


# -----------------------------
# VIDEO ANALYSIS
# -----------------------------

if walking_video is not None:

    st.success("Walking video uploaded successfully!")

    st.video(walking_video)

    st.divider()

    if st.button(
        "🧠 Analyse Movement",
        type="primary"
    ):

        st.info("Analysing movement... Please wait.")

        # Save uploaded video temporarily
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp4"
        )

        temp_file.write(
            walking_video.read()
        )

        temp_file.close()

        # MediaPipe setup
        mp_pose = mp.solutions.pose

        pose = mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        cap = cv2.VideoCapture(
            temp_file.name
        )

        left_angles = []
        right_angles = []

        frame_count = 0

        while cap.isOpened():

            success, frame = cap.read()

            if not success:
                break

            frame_count += 1

            # Convert BGR → RGB
            image = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            results = pose.process(image)

            if results.pose_landmarks:

                landmarks = results.pose_landmarks.landmark

                # Left leg
                left_hip = landmarks[
                    mp_pose.PoseLandmark.LEFT_HIP
                ]

                left_knee = landmarks[
                    mp_pose.PoseLandmark.LEFT_KNEE
                ]

                left_ankle = landmarks[
                    mp_pose.PoseLandmark.LEFT_ANKLE
                ]

                # Right leg
                right_hip = landmarks[
                    mp_pose.PoseLandmark.RIGHT_HIP
                ]

                right_knee = landmarks[
                    mp_pose.PoseLandmark.RIGHT_KNEE
                ]

                right_ankle = landmarks[
                    mp_pose.PoseLandmark.RIGHT_ANKLE
                ]

                # Calculate left knee angle
                left_angle = calculate_angle(
                    [left_hip.x, left_hip.y],
                    [left_knee.x, left_knee.y],
                    [left_ankle.x, left_ankle.y]
                )

                # Calculate right knee angle
                right_angle = calculate_angle(
                    [right_hip.x, right_hip.y],
                    [right_knee.x, right_knee.y],
                    [right_ankle.x, right_ankle.y]
                )

                left_angles.append(left_angle)
                right_angles.append(right_angle)

        cap.release()
        pose.close()

        # -----------------------------
        # RESULTS
        # -----------------------------

        st.success("Movement analysis completed!")

        if len(left_angles) > 0:

            left_average = np.mean(left_angles)
            right_average = np.mean(right_angles)

            left_rom = (
                max(left_angles)
                - min(left_angles)
            )

            right_rom = (
                max(right_angles)
                - min(right_angles)
            )

            st.subheader("📊 Movement Results")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Left Knee ROM",
                    f"{left_rom:.1f}°"
                )

            with col2:
                st.metric(
                    "Right Knee ROM",
                    f"{right_rom:.1f}°"
                )

            st.write(
                f"Average Left Knee Angle: "
                f"**{left_average:.1f}°**"
            )

            st.write(
                f"Average Right Knee Angle: "
                f"**{right_average:.1f}°**"
            )

            st.divider()

            st.info(
                "These movement measurements are preliminary "
                "screening indicators and are NOT a medical diagnosis."
            )

        else:

            st.error(
                "No human body landmarks could be detected "
                "in the uploaded video. Please try a clearer "
                "video with the full body visible."
            )


