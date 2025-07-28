# GUARDRAILS MODERATOR  

Guardrails Moderator is a robust, extensible API service for real-time text moderation. It leverages both traditional regex-based filtering and advanced AI-powered moderation to detect and mask inappropriate language and personally identifiable information (PII) in user input. Designed for seamless integration, it provides RESTful endpoints for both manual and AI-driven moderation workflows.

---

### **FEATURE**

- **Customizable word filtering**: Easily extend the prohibited word list via a simple text file.
- **Regex-based fast moderation**: Efficiently censors unwanted words using regular expressions and a customizable filter list.
- **AI-powered moderation**: Uses OpenAI's model for context-aware detection and masking of offensive language and PII.
- **REST API**: Simple, stateless endpoints for integration into any application stack.
- **Environment-based configuration**: Securely manage API keys and settings with environment variables.

---

### **INSTALLATION**

```sh
pip install -r requirements.txt
```
     
```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=sqlite:///./moderator.db
```

```sh
uvicorn src.app:app --reload
```

---

### **API ENDPOINTS**

#### 1. Manual Moderation

- **Endpoint:** `POST /manualmoderate`
- **Description:** Censors words found in the customizable filter list using regex.
- **Request Body:**
  ```json
  {
    "text_input": "string"
  }
  ```
- **Response:**
  ```json
  {
    "original": "string",
    "moderated": "string"
  }
  ```

#### 2. AI Moderation

- **Endpoint:** `POST /aimoderate`
- **Description:** Uses OpenAI to mask offensive language and PII contextually.
- **Request Body:**
  ```json
  {
    "text_input": "string"
  }
  ```
- **Response:**
  ```json
  {
    "original": "string",
    "moderated": "string"
  }
  ```

---

### **CUSTOM WORD FILTER**

- Edit `src/template/word_filter.txt` to add or remove prohibited words.
- The list is loaded at server startup.

---

### **CURL USAGE**

**Manual Moderation**

```sh
curl -X POST "http://localhost:8000/manualmoderate" -H "Content-Type: application/json" -d '{"text_input": "This is a badword"}'
```

**AI Moderation**

```sh
curl -X POST "http://localhost:8000/aimoderate" -H "Content-Type: application/json" -d '{"text_input": "My email is test@example.com"}'
```

### **AUTHORS**

[Enzo Hashinokuti](https://github.com/EnzoHashinokutiXavier) | [Giovane Iwamoto](https://github.com/GiovaneIwamoto)

We are always open to receiving constructive criticism and suggestions for improving our developed code. We believe that feedback is essential for learning and growth, and we are eager to learn from others to make our code the best it can be. Whether it's a minor tweak or a major overhaul, we are willing to consider all suggestions and implement changes that will benefit our code and its users.