# AI Vakeel — Indian Legal Assistant (starter project)

A mobile-friendly legal assistant starter app for citizens, advocates and law students.
Includes an AI Q&A interface, document drafting, case analysis and legal research modes.
English/Hindi response preference is built in. The OpenAI API key stays on the server.

## What is included
- Responsive web interface designed for Android screens
- Backend API using FastAPI
- OpenAI Responses API integration
- Legal answer, document drafting, case analysis and research modes
- India/state jurisdiction field
- Official legal-source shortcuts
- Dockerfile for deployment

## Run locally
1. Install Python 3.11+.
2. Open a terminal in this folder and run:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env`, then set your OpenAI API key in the environment.
   The app does not automatically load `.env`; export the variables before launching:
   ```bash
   export OPENAI_API_KEY="your_key_here"
   export OPENAI_MODEL="gpt-4.1-mini"
   uvicorn app:app --reload
   ```
   On Windows PowerShell:
   ```powershell
   $env:OPENAI_API_KEY="your_key_here"
   $env:OPENAI_MODEL="gpt-4.1-mini"
   uvicorn app:app --reload
   ```
4. Visit `http://127.0.0.1:8000`.

## Security before public launch
This is a starter build, not a production legal-services platform. Before public use:
- Add authentication, authorization, rate limits, abuse prevention and audit controls.
- Add encrypted storage and explicit consent for any uploaded or saved case materials.
- Do not store secrets in frontend code, source control, or Android package.
- Configure HTTPS, monitoring, backups, retention/deletion controls and privacy notices.
- Review applicable Indian privacy, professional conduct, consumer, and platform requirements.
- Have an Indian advocate review legal prompts, templates and safety workflows.
- Add a verified legal corpus and retrieval/citation pipeline before marketing it as comprehensive legal research.
- Test generated documents and any translations. Drafts are not automatically filing-ready.

## Android
This starter is responsive and works in an Android browser. To distribute a native Android app,
wrap the deployed HTTPS web app using a maintained Android WebView/Trusted Web Activity setup
or build a native client that calls this backend. Keep API keys exclusively on the backend.

## Official source starting points
- India Code: https://www.indiacode.nic.in/
- Supreme Court of India: https://www.sci.gov.in/
- eCourts: https://ecourts.gov.in/
- National Legal Services Authority: https://nalsa.gov.in/

## API
- `GET /health` — health check
- `POST /api/assist` — JSON body: `message`, `language`, `mode`, `jurisdiction`, `context`
