import streamlit as st
from backend.rag.rag import RAG

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="🤖",
    layout="wide",
)

if "rag" not in st.session_state:
    st.session_state.rag = RAG()

st.title("🤖 DocuMind AI")
st.caption("Documentation Question Answering using RAG + ChromaDB + Qwen")

st.divider()

col1, col2 = st.columns([3, 1])

with col1:

    question = st.text_input(
        "Ask a question",
        placeholder="Example: How do I install Python?"
    )

with col2:

    st.write("")
    st.write("")

    ask = st.button(
        "🚀 Ask",
        use_container_width=True
    )

st.divider()

with st.expander("Example Questions", expanded=True):

    c1, c2 = st.columns(2)

    with c1:

        if st.button("How do I install Python?"):
            question = "How do I install Python?"

        if st.button("What is pip?"):
            question = "What is pip?"

    with c2:

        if st.button("How to create virtualenv?"):
            question = "How to create virtualenv?"

        if st.button("What is list comprehension?"):
            question = "What is list comprehension?"

if ask or question:

    if question.strip():

        with st.spinner("Searching documentation..."):

            result = st.session_state.rag.ask(question)

        st.success("Answer")

        st.markdown(result["answer"])

        if result["sources"]:

            st.divider()

            st.subheader("📚 Sources")

            shown = set()

            for source in result["sources"]:

                url = source["url"]

                if url not in shown:
                    shown.add(url)

                    st.markdown(f"- {url}")