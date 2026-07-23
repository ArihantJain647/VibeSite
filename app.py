import streamlit as st
import streamlit.components.v1 as components

from website_agent import generate_website, edit_website

st.set_page_config(
    page_title="VibeSite",
    page_icon="✨",
    layout="wide"
)

st.title("✨ VibeSite")
st.caption("Turn your ideas into websites with AI.")

# Keep generated website in memory
if "website_code" not in st.session_state:
    st.session_state.website_code = ""

if "history" not in st.session_state:
    st.session_state.history = []

# User prompt
user_prompt = st.text_area(
    "Describe the website you want",
    placeholder="Example: Create a modern portfolio website for a photographer with a dark theme...",
    height=120
)

if st.button("✨ Generate Website", type="primary"):

    if not user_prompt.strip():
        st.warning("Please describe the website you want.")

    else:
        try:
            with st.spinner("VibeSite is building your website..."):
                code = generate_website(user_prompt)
                st.session_state.website_code = code

        except Exception as e:
            st.error(f"Generation failed: {e}")


# Show result
if st.session_state.website_code:

    st.subheader("✨ Refine with AI")

    edit_request = st.text_input(
        "What would you like to change?",
        placeholder="Example: Make the theme blue and add a pricing section"
    )

    if st.button("✨ Apply Changes"):

        if not edit_request.strip():
            st.warning("Describe what you want to change.")

        else:
            try:
                with st.spinner("VibeSite is updating your website..."):

                    # Save current version before editing
                    st.session_state.history.append(
                        st.session_state.website_code
                    )

                    updated_code = edit_website(
                        st.session_state.website_code,
                        edit_request
                    )

                    st.session_state.website_code = updated_code
                    st.rerun()

            except Exception as e:
                st.error(f"Editing failed: {e}")

    # Undo previous AI edit
    if st.session_state.history:
        if st.button("↩️ Undo Last Change"):
            st.session_state.website_code = st.session_state.history.pop()
            st.rerun()

    st.divider()

    preview_tab, code_tab = st.tabs([
        "🌐 Live Preview",
        "💻 Code"
    ])

    with preview_tab:
        components.html(
            st.session_state.website_code,
            height=700,
            scrolling=True
        )

    with code_tab:
        st.code(
            st.session_state.website_code,
            language="html"
        )

        st.download_button(
            "⬇️ Download Website",
            data=st.session_state.website_code,
            file_name="index.html",
            mime="text/html"
        )