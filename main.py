import streamlit as st
from sentence_transformers import SentenceTransformer
import chromadb
from pypdf import PdfReader
import ollama
from PIL import Image

st.set_page_config(page_title="AI Study Planner", page_icon="📚")
st.title("📚 AI Study Planner")
st.write("Create a personalized study plan with AI.")

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()
collection = client.get_or_create_collection("study_material")

name = st.text_input("Student Name")
subjects = st.text_area("Enter Subjects (one per line)")
hours = st.number_input("Study Hours Per Day", 1, 12, 3)
days = st.number_input("Number of Days", 1, 30, 7)

uploaded = st.file_uploader("Upload Study PDF", type=["pdf"])

if uploaded:
    reader = PdfReader(uploaded)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    embedding = model.encode(text).tolist()
    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=["study_pdf"]
    )
    st.success("PDF uploaded successfully!")

if st.button("Generate Study Plan"):
    if not name or not subjects:
        st.warning("Please enter your name and subjects.")
    else:
        prompt = f"""
        Create a {days}-day study plan for a B.Tech student.
        Student: {name}
        Subjects: {subjects}
        Available study hours per day: {hours}
        Make the plan practical, balanced and exam-oriented.
        Include daily subjects, topics, study hours and revision.
        """
        try:
            response = ollama.chat(
                model="llama3.2",
                messages=[{"role": "user", "content": prompt}]
            )
            st.subheader("📅 Your AI Study Plan")
            st.markdown(response["message"]["content"])
        except Exception as e:
            st.error("Please make sure Ollama is installed and the llama3.2 model is available.")

st.divider()
st.subheader("🔎 Study Material Search")

query = st.text_input("Search your uploaded PDF")
if st.button("Search") and query:
    result = collection.query(
        query_embeddings=[model.encode(query).tolist()],
        n_results=1
    )
    if result["documents"]:
        st.write(result["documents"][0][0][:2000])
    else:
        st.info("No matching material found.")