# Pixela CLI Tracker

Pixela CLI Tracker is a command-line (CLI) application that helps users track daily habits using the **[Pixela API](https://pixe.la/)**.

The app allows users to:
- Register a new Pixela account
- Log in using a token
- Create graphs to record data
- Post daily pixels to log progress

---

## 🚀 Features

| Function | Description |
|-----------|-------------|
| 🧑‍💻 Sign up | Create a new Pixela user account and save the token |
| 🔐 Sign in | Authenticate an existing user locally |
| 📊 Create graph | Register a new graph for tracking on Pixela |
| 🟩 Post pixel | Record a new daily habit pixel |
| 💾 Save data | All user and graph data are stored in the `data/` folder |

---

## 🧱 Project Structure

```
project/
│
├── controller.py     # Main CLI program controlling the app flow
├── graph.py          # Graph class: handles graph creation and pixel posting
├── user.py           # User class: stores user info and graph relationships
├── model.py          # Data manager for user.csv, graph.csv, and config
├── utils.py          # Helper functions: load/save/call_api
│
├── config.json       # API configuration for Pixela endpoints
└── data/
    ├── user.csv      # Stored users (username, token)
    └── graph.csv     # Stored graph info (username, graph_id)
```

---

## ⚙️ Requirements

- Python >= 3.10  
- Libraries:
  ```bash
  pip install pandas pyinputplus requests
  ```

---

## 🔧 Configuration

`config.json` contains all Pixela API endpoint definitions and request templates.  
Example:

```json
{
  "pixela_api": {
    "create_user": {
      "method": "POST",
      "endpoint": "https://pixe.la/v1/users",
      "request_body": {
        "token": "",
        "username": "",
        "agreeTermsOfService": "yes",
        "notMinor": "yes"
      }
    },
    "create_graph": {
      "method": "POST",
      "endpoint": "https://pixe.la/v1/users/<username>/graphs",
      "request_header": {
        "Content-Type": "application/json",
        "X-USER-TOKEN": ""
      },
      "request_body": {
        "id": "",
        "name": "",
        "unit": "",
        "type": "",
        "color": ""
      }
    },
    "post_pixel": {
      "method": "POST",
      "endpoint": "https://pixe.la/v1/users/<username>/graphs/<graphID>",
      "request_header": {
        "Content-Type": "application/json",
        "X-USER-TOKEN": ""
      },
      "request_body": {
        "date": "",
        "quantity": ""
      }
    }
  }
}
```

---

## 🖥️ How to Run

### 1️⃣ Clone the project
```bash
git clone https://github.com/<your-repo>/pixela-cli-tracker.git
cd pixela-cli-tracker
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
*(or manually: `pip install pandas pyinputplus requests`)*

### 3️⃣ Create data directory
```bash
mkdir -p data
touch data/user.csv data/graph.csv
```

### 4️⃣ Run the program
```bash
python controller.py
```

---

## 🧩 Usage

When running, you’ll see a CLI menu:

```
Please choose one option below:
1. Sign in
2. Sign up
0. Sign out
```

### ▶️ Sign Up
Enter username, token, and agreement options.  
The app will automatically register your account on Pixela.

### ▶️ Sign In
Enter your username and token to authenticate and select a graph.

### ▶️ Create Graph
After login, choose “Create a graph” to make a new tracking chart.

### ▶️ Post Pixel
Choose “Post a pixel”, input the date and quantity, and the app will post to Pixela API.

---

## 📂 Local Data Storage

| File | Description |
|------|--------------|
| `data/user.csv` | List of users: username, token |
| `data/graph.csv` | Graphs associated with each user |
| `config.json` | Pixela API endpoints and templates |

---

## 🧠 Technical Notes

- The app **never overwrites** the JSON config file.
- User input validation is handled by **pyinputplus**.
- Data persistence uses **CSV** for easy inspection and portability.
- No passwords are stored — only Pixela API tokens.

---

## 🧾 License

MIT License © 2025

---

## 👨‍💻 Author

**Đào An Sơn**  
Educational project for learning API integration and CLI development using Python.
