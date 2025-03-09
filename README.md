# GUARDRAILS MODERATOR

Guardrails Moderator is a **SaaS solution** designed to **moderate user inputs**, ensuring compliance and security by filtering **PII (Personally Identifiable Information) and unwanted words** using **AI and Regex**.

### FEATURE

**Censor inappropriate words** with customizable filters  
**Detect and mask PII** 
**Choose between Regex-based filtering (fast) or AI-powered moderation (context-aware)**  
**REST API for seamless integration** into any application  
**Real-time text validation** with flexible moderation settings  

---

### INSTALLATION GUIDE

```sh
# Install dependencies
pip install -r requirements.txt
```
### **Example API Request**
Send a **POST** request to validate text:

```sh
curl -X POST "http://localhost:8000/validate/" -H "Content-Type: application/json" -d '{"text": "My email is test@example.com", "use_ai": false}'
```

### **Example Response**
```json
{
  "original": "My email is test@example.com",
  "censored": "My email is ****"
}
```

---

### LICENSE

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

### CONTRIBUTING
Pull requests are welcome! Feel free to open an issue or suggest improvements.
