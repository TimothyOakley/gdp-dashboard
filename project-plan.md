# AI Investment Platform Project Plan

## Objective
Build a Streamlit-based AI platform that helps global investors discover and analyze Australian investment opportunities using AI models, document search, and structured data.

---

# 1. Inventory Existing Repository

Current repository files:

- streamlit_app.py
- requirements.txt
- README.md
- data/

Tasks:

- confirm main app entry file
- clean template/demo code
- document repository structure
- verify dependencies

Target structure:

---

# 2. AI Model Providers

Evaluate major LLM providers.

Providers:

- OpenAI
- Anthropic
- Google Gemini

Evaluation criteria:

- cost
- reliability
- reasoning capability
- document understanding
- structured output
- context length

Likely use model:

Chat & analysis → OpenAI  
Long document reasoning → Anthropic  
Multimodal tasks → Gemini

---

# 3. Retrieval and Vector Database

Goal: enable document search and contextual AI responses.

Components:

- embeddings
- vector database
- retrieval system

Vector database options:

- Chroma
- FAISS
- Pinecone
- Weaviate
- Qdrant

Recommended MVP:

- Chroma
- provider embeddings
- semantic retrieval

Pipeline:

documents  
→ chunk text  
→ create embeddings  
→ store vectors  
→ retrieve relevant chunks  
→ send context to AI model

---

# 4. Data Ingestion Pipeline

Potential data sources:

- PDFs
- financial reports
- company announcements
- spreadsheets
- public datasets
- websites

Processing pipeline:

collect data  
→ extract text  
→ clean text  
→ chunk content  
→ add metadata  
→ generate embeddings  
→ store in vector database

---

# 5. AI Routing Layer

Create a routing system to send tasks to the most appropriate model.

Example routing:

simple questions → fast model  
long reports → large context model  
structured extraction → structured-output model

Router responsibilities:

- select model
- retry on failure
- track costs
- maintain logs

---

# 6. Streamlit App Architecture

One app with multiple pages.

Pages:

Dashboard
- overview of market data

Document Search
- upload documents
- search stored knowledge

AI Analysis
- ask questions
- generate summaries
- compare opportunities

Admin
- ingestion status
- logs
- usage monitoring

---

# 7. Deployment Strategy

MVP deployment:

- GitHub repository
- Streamlit Community Cloud
- requirements.txt for dependencies

Future options:

- Docker deployment
- cloud hosting (AWS / Azure / GCP)
- background ingestion workers

---

# 8. Cost Planning

Cost sources:

- LLM API calls
- embeddings
- vector database hosting
- OCR processing
- storage

Cost tiers:

Prototype → minimal usage  
Pilot → moderate document volume  
Production → full infrastructure

---

# 9. Development Roadmap

Phase 1
Deploy working Streamlit application.

Phase 2
Add document upload and storage.

Phase 3
Add AI analysis capability.

Phase 4
Add embeddings and vector search.

Phase 5
Add multi-model routing and advanced features.

---

# 10. Immediate Next Steps

1. Save this project plan to repository
2. Run Streamlit application locally
3. Add document upload
4. Integrate AI model API
5. Implement retrieval pipeline

---

# Success Criteria

Users can:

- open the Streamlit application
- upload investment documents
- search document content
- ask AI questions about data
- receive grounded AI-generated analysis
