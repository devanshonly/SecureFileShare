# Secure File Share – FastAPI Backend

A secure file-sharing platform built with FastAPI, supporting two user types: **Ops User** (file uploader/admin) and **Client User** (file downloader/customer).

---

## 🖼️ Swagger UI Preview

Here’s what the API documentation looks like:
![Screenshot (87)](https://github.com/user-attachments/assets/3d3c37a5-3cc8-4324-8ef8-ac32110cbe9c)
![Screenshot (88)](https://github.com/user-attachments/assets/e9b7bbbf-40cc-43f9-8823-f75aae2d041b)
![Screenshot (86)](https://github.com/user-attachments/assets/0642755f-0081-42b2-a3fb-ad9f146e961d)



## 🚀 Features

- **User Registration & Login** (JWT Auth, hashed passwords)
- **Email Verification** (simulated via console print)
- **File Upload** (Ops only, supports `.pptx`, `.docx`, `.xlsx`)
- **Client File Listing & Download** (via encrypted links)
- **SQLite + SQLAlchemy ORM**
- **Swagger API Docs** (`/docs`)
- **Industry-standard project structure**

---

## 🗂️ Project Structure

```
secure_file_share/
  ├── auth.py
  ├── database.py
  ├── main.py
  ├── models.py
  ├── requirements.txt
  ├── SecureFileShare.postman_collection.json
  ├── routes/
  │     ├── ops.py
  │     └── client.py
  ├── utils/
  │     ├── encryptor.py
  │     └── email.py
  └── uploads/
```

---

## ⚡ Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd secure_file_share
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the server

```bash
uvicorn secure_file_share.main:app --reload
```

- The API will be available at: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 API Testing with Postman

- Import the provided `SecureFileShare.postman_collection.json` into Postman.
- The collection includes all main flows for both Ops and Client users, with example payloads and instructions.
- **Email verification tokens** are printed to the server console (simulated).

### **Typical Workflow:**
1. Register (Ops or Client)
2. Check the server console for the verification token
3. Verify email
4. Log in to get a JWT token
5. Use the token for protected endpoints (upload, list, download)

---

## 📄 Notes

- All passwords are securely hashed.
- JWT tokens are required for protected endpoints (see Postman collection).
- File uploads are stored in the `uploads/` directory.
- Only Ops users can upload files; only Clients can download.

---

## 📦 Submission

- **Code:** All project files in this repository.
- **Postman Dump:** `SecureFileShare.postman_collection.json` (included).

---

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Postman](https://www.postman.com/)

---

**Good luck with your placement! If you have any questions, feel free to reach out.**
