# Sanskrit Multilingual Chatbot — CI with Docker & Jenkins

A simple English + Sanskrit computational chatbot built with **Flask**, packaged with **Docker**, and continuously integrated with **Jenkins** — using **`uv`** as the Python package manager.

**Pipeline:** `GitHub → Jenkins → Checkout → uv sync → py_compile → docker build → ✅ SUCCESS`

---

## Project Structure

```
sanskrit-multilingual-chatbot/
├── app.py                 # Flask backend (chat + calculator logic)
├── pyproject.toml         # uv project config + deps
├── uv.lock                # pinned dependency versions (commit this!)
├── Dockerfile             # uv-based container image
├── Jenkinsfile            # CI pipeline definition
├── .gitignore
├── README.md
└── templates/
    └── index.html         # Chat UI
```

---

## 1 — Install the tools (all free)

### a) Git for Windows
Download: https://git-scm.com/download/win → install with defaults.

Verify:
```powershell
git --version
```

### b) uv (Python package manager)
Open **PowerShell** and run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Close and reopen PowerShell, then verify:
```powershell
uv --version
```
uv will auto-download Python 3.11 when needed — you do **not** need to install Python separately.

### c) Docker Desktop
Download: https://www.docker.com/products/docker-desktop/ → install → launch Docker Desktop → wait for the whale icon to say *"Docker Desktop is running"*.

Verify:
```powershell
docker --version
docker run hello-world
```

### d) Jenkins (free, LTS)
Download the Windows installer: https://www.jenkins.io/download/ → *Long-Term Support (LTS)* → *Windows*.

During install:
- Keep the default service account (or choose *Run service as LocalSystem*).
- Default port **8080**.

After install, Jenkins opens at **http://localhost:8080**.
- Unlock using the password at:
  `C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword`
- Choose **Install suggested plugins**.
- Create your admin user.

> **Important:** so Jenkins can call `uv`, `docker`, and `git`, add these to the **system PATH** (not just your user PATH), then restart the Jenkins service:
> - `C:\Users\<you>\.local\bin` (uv)
> - `C:\Program Files\Docker\Docker\resources\bin`
> - `C:\Program Files\Git\cmd`
>
> Restart Jenkins: *Services → Jenkins → Restart*.

---

## 2 — Push the project to GitHub

1. Go to https://github.com/new → create a repo named `sanskrit-multilingual-chatbot` → **Public** → do NOT add README/.gitignore (we have our own).
2. In the project folder:
   ```powershell
   cd path\to\sanskrit-multilingual-chatbot
   git init
   git add .
   git commit -m "Initial multilingual Sanskrit chatbot"
   git branch -M main
   git remote add origin https://github.com/<your-username>/sanskrit-multilingual-chatbot.git
   git push -u origin main
   ```
3. Edit **`Jenkinsfile`** — replace `<your-username>` with your actual GitHub username. Commit and push.

---

## 3 — Run locally (optional sanity check)

```powershell
uv sync
uv run python app.py
```
Open http://127.0.0.1:5000 — try `hello`, `calculate 10-2`, `who are you`.

---

## 4 — Build the Docker image manually (optional)

```powershell
docker build -t sanskrit-chatbot:latest .
docker run -p 5000:5000 sanskrit-chatbot:latest
```
Visit http://127.0.0.1:5000 — the containerized app works identically.

List the image:
```powershell
docker images sanskrit-chatbot
```

---

## 5 — Create the Jenkins pipeline

1. Open **http://localhost:8080** → **New Item**.
2. Name: **`Sanskrit-Chatbot-CI`** → choose **Pipeline** → **OK**.
3. On the config page:
   - **Pipeline → Definition:** `Pipeline script from SCM`
   - **SCM:** `Git`
   - **Repository URL:** `https://github.com/<your-username>/sanskrit-multilingual-chatbot.git`
   - **Branch:** `*/main`
   - **Script Path:** `Jenkinsfile`
4. **Save** → **Build Now**.

You'll see the five stages run: `Checkout → Setup uv → Install Dependencies → Validate → Docker Build`.

### Alternatively — inline script

If you prefer the inline *Pipeline script* style shown in the lab PDF, paste this instead of the SCM option:

```groovy
pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/<your-username>/sanskrit-multilingual-chatbot.git'
            }
        }
        stage('Build') {
            steps {
                echo 'Building Sanskrit Multilingual Chatbot...'
                bat 'uv --version'
                bat 'uv sync'
            }
        }
        stage('Test') {
            steps {
                echo 'Validating app.py...'
                bat 'uv run python -m py_compile app.py'
            }
        }
        stage('Docker Build') {
            steps {
                bat 'docker build -t sanskrit-chatbot:jenkins .'
                bat 'docker images sanskrit-chatbot'
            }
        }
    }
    post {
        success { echo 'Pipeline completed successfully!' }
    }
}
```

---

## 6 — Trigger on every GitHub commit (bonus)

In the job config:
- Enable **Build Triggers → Poll SCM** with schedule `H/2 * * * *` (every ~2 min), or
- Set up a GitHub webhook pointing to `http://<your-public-ip>:8080/github-webhook/` (needs public access — skip if local-only).

Then edit a line in `app.py`, commit & push — Jenkins picks it up and reruns the whole pipeline. Matches the "Change commit → pipeline re-runs" screenshot in the lab doc.

---

## 7 — Why `uv` instead of `pip`

| Thing              | pip                        | uv                              |
|--------------------|----------------------------|---------------------------------|
| Install speed      | slow                       | **10–100× faster**              |
| Lockfile           | needs extra tooling        | **built-in `uv.lock`**          |
| Python management  | separate (pyenv, etc.)     | **built-in**                    |
| Reproducibility    | manual pinning             | **`uv sync --frozen`**          |
| Virtualenv         | manual (`python -m venv`)  | **auto `.venv/`**               |

Everything in this project is free and open-source. No cloud account, no paid plan.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `uv: command not found` in Jenkins | uv is on your user PATH only. Add `C:\Users\<you>\.local\bin` to **System PATH**, restart Jenkins service. |
| `docker: command not found` in Jenkins | Add `C:\Program Files\Docker\Docker\resources\bin` to **System PATH**, restart Jenkins. |
| Jenkins can't talk to Docker | Make sure Docker Desktop is running *before* starting a build. |
| Port 5000 already in use | `docker run -p 5050:5000 sanskrit-chatbot:latest` and visit http://127.0.0.1:5050 |
| `uv sync` fails with lockfile mismatch | Delete `uv.lock` and run `uv lock` to regenerate, then commit. |

---

**Author:** Eshaan · 23MIS1149
**Course:** Agile Development Process and DevOps Lab (ISWE406P) — L9 + L10
