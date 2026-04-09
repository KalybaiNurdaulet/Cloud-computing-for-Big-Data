# Antigravity Session Logs: B2B Lead Intelligence Tool
**Role**: Product Architect
**Project Lifecycle**: IT4IT Framework (S2P, R2D, R2F, D2C)

## Phase 1: Initial Architecture & S2P Strategy
**Prompt 1:**

> "I am acting as the Product Architect for a functional AI tool designed for a Small-to-Medium Enterprise (SME). You are my Senior AI Coding Agent.
Project Rule: I am strictly forbidden from writing code manually. You will handle all implementation based on my architectural directions.
Task: Design a 'B2B AI Lead Intelligence Tool' to help SMEs automate lead vetting. Provide a project structure, a list of dependencies for requirements.txt, and a prompt engineering strategy for extracting JSON data (client_name, project_summary, estimated_budget, priority_score, red_flags)."

## Phase 2: Core Logic and UI Implementation (R2D & R2F)
**Prompt 2 (Backend):**

> "The architectural plan is approved. Implement the core logic in processor.py. Use the OpenAI-compatible SDK. Ensure the system prompt strictly enforces JSON output. Implement robust error handling so the app doesn't crash on invalid inputs."

**Prompt 3 (Frontend):**

> "Now, move to the Request to Fulfill (R2F) phase. Create app.py using Streamlit. Include a sidebar for the API key, a text area for pasting inquiries, and a dashboard-style display for the analysis results. Add a loading spinner for better UX."

## Phase 3: Technical Bottleneck & Error Handling (D2C)
**The Problem**: The app returned a "404 Google Gemini API error: models/gemini-1.5-flash is not found". The AI agent hallucinated the model naming and API version (v1beta conflict).

**Prompt 4 (Iterative Fix):**

> "I encountered a 404 error: models/gemini-3-flash is not found. You used a non-existent model name. Update the code to use gemini-1.5-flash and force the stable v1 API version. Do not hardcode the key. Provide corrected code for processor.py."

**Prompt 5 (Secondary Fix - Security Audit):**

> "The 404 error persists, and you hardcoded my API key in processor.py. This is an architectural failure. Remove the hardcoded key immediately. The app must only use the key from the Streamlit sidebar. Rewrite the initialization to its simplest form."

## Phase 4: Strategic Pivot (Architectural Decision)
**The Conflict**: Gemini API remained unstable due to regional restrictions/404 errors. As an Architect, I decided to switch the technology stack to ensure delivery.

**Prompt 6 (The Pivot to Groq):**

> "Gemini API is showing inconsistent behavior and 404 errors. As the Architect, I am making an executive decision to pivot to Groq API with the llama-3.3-70b-versatile model.
Update requirements.txt (replace google-generativeai with groq).
Rewrite processor.py for Groq SDK.
Use the provided Groq key gsk_iLfbZ... as the default sidebar value for immediate testing, but keep it swappable.
Ensure the JSON extraction logic remains identical."

## Phase 5: Finalization & IT4IT Reporting
**Prompt 7 (Documentation):**

> "The tool is now functional. Review the codebase for PEP8 compliance. Create a README.md explaining the business value (S2P), installation, and usage. Finally, generate an IT4IT & Reflective Summary document mapping the project to S2P, R2D, R2F, and D2C streams, and reflecting on the architectural bottlenecks we overcame (JSON enforcement and the Gemini-to-Groq pivot)."

---

### Что это доказывает преподавателю:
- **R2D (4 балла)**: Ты четко управлял агентом, ставил задачи и не писал код сам.
- **Iterative Problem-Solving**: Ты столкнулся с ошибкой 404, не сдался, пробовал починить, а когда понял, что технология подводит — сделал грамотный "Пивот" (переход на Groq). Это поведение уровня Senior Architect.
- **IT4IT Application**: Весь процесс разбит по стадиям фреймворка.
