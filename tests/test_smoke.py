from streamlit.testing.v1 import AppTest


def test_smoke():
    paths = [
        "apps/2_streamlit_chat/main.py",
        "apps/4_streamlit_chat_history/main.py",
        "apps/5_streamlit_query_chat_history/main.py",
        # "apps/7_streamlit_chat_rag/main.py",
        "apps/8_streamlit_azure_openai_batch/main.py",
        # "apps/9_streamlit_azure_document_intelligence/main.py",
        "apps/10_streamlit_batch_transcription/main.py",
        "apps/99_streamlit_examples/main.py",
        "apps/99_streamlit_examples/pages/1_File_Q&A.py",
        "apps/99_streamlit_examples/pages/2_Image_Q&A.py",
        "apps/99_streamlit_examples/pages/3_Camera_Q&A.py",
        "apps/99_streamlit_examples/pages/4_Translate_text.py",
        "apps/99_streamlit_examples/pages/5_Explain_data.py",
        "apps/99_streamlit_examples/pages/6_Speech_to_text.py",
        "apps/99_streamlit_examples/pages/7_Text_to_speech.py",
        "apps/99_streamlit_examples/pages/8_Create_image.py",
        "apps/99_streamlit_examples/pages/9_Visualize_location.py",
        # fixme: disabled due to flaky test
        # "apps/99_streamlit_examples/pages/10_Object_detection.py",
        # "apps/99_streamlit_examples/pages/11_Pose_estimation.py",
        "apps/99_streamlit_examples/pages/12_Video_processing.py",
    ]
    for path in paths:
        at = AppTest(
            script_path=path,
            default_timeout=60,
        )
        at.run()
        assert not at.exception
