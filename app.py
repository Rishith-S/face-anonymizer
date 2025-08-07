import base64
import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---- Face Blur ----
def blur_faces(image, detection_result) -> np.ndarray:
    annotated_image = image.copy()
    h, w, _ = annotated_image.shape

    for detection in detection_result.detections:
        bbox = detection.bounding_box
        x1 = max(bbox.origin_x, 0)
        y1 = max(bbox.origin_y - 8, 0)
        x2 = min(x1 + bbox.width, w)
        y2 = min(y1 + bbox.height, h)

        face_region = annotated_image[y1:y2, x1:x2]
        if face_region.size == 0:
            continue
        blurred = cv2.GaussianBlur(face_region, (99, 99), 30)
        annotated_image[y1:y2, x1:x2] = blurred

    return annotated_image

# ---- Eye Cover ----
def draw_scribbled_eye_lines(image, facemesh_result) -> np.ndarray:
    scribbled_image = image.copy()
    h, w, _ = scribbled_image.shape

    LEFT_EYE = 33
    RIGHT_EYE = 263

    if facemesh_result.multi_face_landmarks:
        for face_landmarks in facemesh_result.multi_face_landmarks:
            x1 = int(face_landmarks.landmark[LEFT_EYE].x * w) - 10
            y1 = int(face_landmarks.landmark[LEFT_EYE].y * h)
            x2 = int(face_landmarks.landmark[RIGHT_EYE].x * w) + 10
            y2 = int(face_landmarks.landmark[RIGHT_EYE].y * h)
            cv2.line(scribbled_image, (x1, y1), (x2, y2), (0, 0, 255), 10 if x2 - x1 < 100 else 25)

    return scribbled_image

# ---- Utility: Encode image to base64 ----
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64 = base64.b64encode(img_file.read()).decode()
    return f"data:image/png;base64,{b64}"

# ---- Load MediaPipe Models ----
base_options = python.BaseOptions(model_asset_path="blaze_face_short_range.tflite")
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=20,
    refine_landmarks=True,
    min_detection_confidence=0.5
)

# ---- Streamlit UI ----
st.set_page_config(page_title="Red Eye Line - MediaPipe Tasks", layout="wide")
st.title("Face Anonymization Using MediaPipe FaceDetector")

anonymization_type = st.radio(
    "Select the type of anonymization",
    ["Face-Blur", "Cover-Eyes"]
)

# ---- Inject responsive CSS ----
st.markdown("""
    <style>
    @media only screen and (max-width: 768px) {
        .hide-on-mobile {
            display: none !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# ---- Static Image Grid (hidden on mobile) ----
st.markdown('<div class="hide-on-mobile">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    img1_data = get_base64_image("assets/Humans.png")
    st.markdown(
        f"""
        <div style="height: 25vh; display: flex; justify-content: center; align-items: center;">
            <img src="{img1_data}" style="max-height: 100%; max-width: 100%;">
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    img2_data = get_base64_image("assets/image.png")
    st.markdown(
        f"""
        <div style="height: 25vh; display: flex; justify-content: center; align-items: center;">
          <div style="height: 12vh; display: flex; justify-content: center; align-items: center;">
            <img src="{img2_data}" style="max-height: 100%; max-width: 100%;">
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    output_image_path = 'assets/Humans-Face-Blur.png' if anonymization_type == "Face-Blur" else 'assets/Humans-Cover-Eyes.png'
    img3_data = get_base64_image(output_image_path)
    st.markdown(
        f"""
        <div style="height: 25vh; display: flex; justify-content: center; align-items: center;">
            <img src="{img3_data}" style="max-height: 100%; max-width: 100%;">
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---- Image Uploader and Processing ----
uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded:
    file_name = uploaded.name.split('.')[0]
    file_type = uploaded.type
    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
    image_bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if anonymization_type == "Face-Blur":
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
        detection_result = detector.detect(mp_image)
        annotated_image = blur_faces(image_bgr, detection_result)
    else:
        facemesh_results = face_mesh.process(cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB))
        annotated_image = draw_scribbled_eye_lines(image_bgr, facemesh_results)

    annotated_rgb = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)

    st.image(annotated_rgb, caption="Anonymized Image")

    ext = ".png" if file_type == "image/png" else ".jpg"
    success, buffer = cv2.imencode(ext, cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR))
    if success:
        st.download_button(
            label="Download Image",
            data=buffer.tobytes(),
            file_name=f'{file_name}-{anonymization_type}{ext}',
            mime=file_type
        )
