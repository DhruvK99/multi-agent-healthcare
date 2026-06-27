# Intelligent Multi-Agent Healthcare Platform 🏥🕵️‍♂️

A collaborative Multi-Agent System (MAS) built using CrewAI and Groq (Llama-3.1). The application orchestrates isolated, role-specific agents to manage healthcare workflows, while seamlessly grounding their logic with an integrated local database and a document serialization engine.

## 🚀 Overview
This repository charts the architectural development from foundational single-agent prompt execution to a complex, multi-agent enterprise simulator. The production build features a clinical workspace that registers patients, queries transactional state, runs safe triage classification via an open-source LLM, and writes historical records directly back into disk storage.

## 🧠 Architecture & Features
*   **Sequential Agent Orchestration:** Leverages CrewAI’s `Process.sequential` runner to transition system states across four dedicated sub-agents:
    *   `Symptom Analyzer`: Evaluates patient severity against unstructured text prompts.
    *   `Doctor Recommender`: Determines medical specializations required for allocation.
    *   `Medical Advisor`: Supplies targeted lifestyle precautions and triage workflows.
    *   `Report Generator`: Compiles context pieces into uniform clinical evaluations.
*   **Relational Context Grounding:** Integrates an active SQLite3 layer to fetch historical visit data for returning patients and inject past symptoms directly into agent reasoning tokens to avoid context fragmentation.
*   **Deterministic Report Serialization:** Binds native execution scripts to the FPDF library to automatically compile unstructured agent outputs into structural, downloadable PDF summaries.
*   **Advanced Terminal Telemetry:** Implements structural tables, panel dividers, and colored workflow logging natively in the terminal workspace via `Rich`.

## 🛠️ Tech Stack
*   **Multi-Agent Framework:** CrewAI 
*   **LLM Orchestration:** LangChain-Groq API
*   **Foundation Model:** Llama-3.1-8b-Instant (Groq)
*   **Data Tier:** SQLite3
*   **Document Tier:** FPDF
*   **Interface Layer:** Rich Console Engine
*   **Language:** Python 3.x

## 💻 Quick Start
1. Clone this repository and configure your `.env` workspace:
   ```bash
   GROQ_API_KEY="your_actual_groq_api_key_here"
