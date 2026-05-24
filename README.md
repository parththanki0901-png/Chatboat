# Chatboard API

AI chatbot backend built using FastAPI and Groq API.

---

## Features

- FastAPI backend
- Groq LLM integration
- Multi-turn conversation support
- REST API
- CORS enabled
- Environment variable support

---

## Tech Stack

- Python
- FastAPI
- Groq API
- Uvicorn
- Pydantic

---

## Installation

Clone the repository:

```bash
git clone https://github.com/parththanki0901-png/chatboard.git
```

Move into project folder:

```bash
cd chatboard
```

Create virtual environment:

```bash
python -m venv myenv
```

Activate virtual environment:

### Windows

```bash
myenv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file and add:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run Server

```bash
uvicorn main:app --reload
```

---

## API Endpoint

### POST `/chat`

Request:

```json
{
  "session_id": "abc123",
  "message": "Hello"
}
```

Response:

```json
{
  "reply": "Hello! How can I help you?"
}
```

---

## Future Improvements

- Database integration
- JWT authentication
- Chat history storage
- Deployment
- Docker support

---

## Author

Parth Thanki