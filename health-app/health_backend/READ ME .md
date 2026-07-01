# HealthAI Backend Implementation Plan

This backend provides a specialized AI assistant for General Health diagnosis support and connects patients with real-life doctors.

## Key Features
 **Specialized AI (General Health)**: Uses a custom knowledge base and system prompting to provide advice on various common diseases, drugs, and measures.


## Project Structure
- `app/main.py`: Entry point and API routes.
- `app/models.py`: Database schema (Users, Messages).
- `app/ai_service.py`: The "Specialized LLM" logic (OpenAI integration with General Health context).
- `app/auth.py`: Security and JWT handling.
- `app/database.py`: SQLite connection setup.

## How to Run
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Environment Setup**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```
3. **Start the Server**:
      Select backend 
      ""cd health-app/health_backend""
     
     and run 
      "".\.venv\Scripts\uvicorn app.main:app --reload""


   **API KEY**
   OPENAI_API_KEY=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
   
   **LINK FOR GETING API**
   (https://platform.openai.com/api-keys)

## Frontend Integration Guide
To connect your frontend (Flutter, React, etc.) to this backend:

### 1. Authentication
- **Register**: `POST /register` with `email`, `full_name`, `password`, and `role` ("patient" or "doctor").
- **Login**: `POST /login` to get a JWT token.
- **Headers**: Include `Authorization: Bearer <your_token>` in all subsequent requests.

### 2. Chatting with AI
- **Endpoint**: `POST /chat`
- **Body**: `{"message": "I have a high fever and chills"}`
- **Response**: The AI will analyze symptoms against its General Health knowledge base.

### 3. Finding Doctors
- **Endpoint**: `GET /doctors/online`
- **Action**: Display this list in a "Contact a Doctor" section.

### 4. Doctor Dashboard
- **Endpoint**: `POST /doctors/status`
- **Body**: `{"is_online": true}`
- **Action**: Use this when the doctor logs in or toggles a switch to be "On Standby".

## Specialized LLM "Training"
Instead of raw training (which requires massive compute), we use **System Prompting** and **Knowledge Injection**. This ensures the AI stays within the bounds of health-related advice and always refers users to the real-life doctors in the system.
