import streamlit as st
from PIL import Image
import tempfile
import os

from modules.detector import detect_weeds
from modules.target import get_targets
from modules.modes import get_mode_result


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Agri Vision",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🌱 Agri Vision")
st.caption("AI-Based Weed Detection System")


# =========================================================
# CONTROLS
# =========================================================

col1, col2, col3 = st.columns([5, 2, 2])

with col2:
    crop = st.selectbox(
        "Select Crop",
        [
            "Cotton",
            "Tomato",
            "Chilli",
            "Maize"
        ]
    )

with col3:
    work = st.selectbox(
        "Select Work",
        [
            "Weed Removal",
            "Weed Spraying",
            "Sowing"
        ]
    )


st.divider()


# =========================================================
# IMAGE UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload Crop / Field Image",
    type=["jpg", "jpeg", "png"]
)


# =========================================================
# PROCESS IMAGE
# =========================================================

if uploaded_file is not None:

    # -----------------------------------------------------
    # Create temporary directory
    # -----------------------------------------------------

    temp_dir = tempfile.mkdtemp()

    input_path = os.path.join(
        temp_dir,
        uploaded_file.name
    )

    # Save uploaded image

    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())


    # -----------------------------------------------------
    # Display input image
    # -----------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("📷 Input Image")

        image = Image.open(input_path)

        st.image(
            image,
            use_container_width=True
        )


    # -----------------------------------------------------
    # Run YOLO detection
    # -----------------------------------------------------

    with st.spinner("🔍 Detecting weeds..."):

        try:

            output_image, detections = detect_weeds(
                image
            )

        except Exception as e:

            st.error("Detection failed.")

            st.code(str(e))

            st.stop()

    


    # -----------------------------------------------------
    # Display detection result
    # -----------------------------------------------------

    with right:

        st.subheader("🎯 Detection Result")

        st.image(
            output_image,
            use_container_width=True
        )


    # =====================================================
    # TARGET CALCULATION
    # =====================================================

    image_width, image_height = image.size

    targets = get_targets(
        detections,
        image_width,
        image_height
    )

    mode_result = get_mode_result(
        work,
        targets
    )


    # =====================================================
    # DETECTION INFORMATION
    # =====================================================

    st.divider()

    st.subheader("📊 Detection Information")
    st.subheader(f"⚙️ {work} Mode")

    mode_col1, mode_col2 = st.columns([1, 3])

    with mode_col1:

        if mode_result["status"] == "TARGET READY":
            st.success(mode_result["status"])

        elif mode_result["status"] == "SPRAY TARGET READY":
            st.success(mode_result["status"])

        elif mode_result["status"] == "POSITION DETECTED":
            st.info(mode_result["status"])

        else:
            st.warning(mode_result["status"])


    with mode_col2:

        st.write(mode_result["message"])


    info1, info2, info3, info4 = st.columns(4)


    with info1:

        st.metric(
            "Selected Crop",
            crop
        )


    with info2:

        st.metric(
            "Work",
            work
        )


    with info3:

        st.metric(
            "Weeds Detected",
            len(targets)
        )


    with info4:

        if targets:

            st.metric(
                "Status",
                "Weed Detected"
            )

        else:

            st.metric(
                "Status",
                "No Weed"
            )


    # =====================================================
    # TARGET POSITIONS
    # =====================================================

    st.divider()

    st.subheader("🎯 Weed Target Positions")


    if targets:

        camera_center_x = image_width / 2
        camera_center_y = image_height / 2


        st.write(
            f"**Image Size:** "
            f"{image_width} × {image_height} pixels"
        )

        st.write(
            f"**Camera Center:** "
            f"({camera_center_x:.1f}, "
            f"{camera_center_y:.1f})"
        )


        # -------------------------------------------------
        # Display every detected weed
        # -------------------------------------------------

        for target in targets:

            st.markdown(
                f"### 🌿 Weed #{target['weed']}"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Confidence",
                    f"{target['confidence'] * 100:.1f}%"
                )


            with col2:

                st.metric(
                    "Weed Center",
                    f"({target['cx']}, {target['cy']})"
                )


            with col3:

                st.metric(
                    "Target Offset",
                    f"({target['offset_x']}, "
                    f"{target['offset_y']})"
                )


            st.write(
                f"**Direction:** "
                f"{target['horizontal']} + "
                f"{target['vertical']}"
            )


    else:

        st.info(
            "No weed targets detected in this image."
        )


else:

    # =====================================================
    # INITIAL STATE
    # =====================================================

    st.info(
        "Upload an image to start weed detection."
    )