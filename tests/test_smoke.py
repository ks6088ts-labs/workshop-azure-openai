from streamlit.testing.v1 import AppTest


def test_smoke():
    paths = [
        "apps/2_streamlit_chat/main.py",
        "apps/4_streamlit_chat_history/main.py",
        "apps/5_streamlit_query_chat_history/main.py",
        # "apps/7_streamlit_chat_rag/main.py",
        "apps/8_streamlit_azure_openai_batch/main.py",
        "apps/99_streamlit_examples/main.py",
    ]
    for path in paths:
        at = AppTest(
            script_path=path,
            default_timeout=60,
        )
        at.run()
        assert not at.exception
