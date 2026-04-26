# 🛠️ Unix Engine: Remote C/C++ Build Factory

[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)](https://www.docker.com/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### The Backstory: Goodbye "VM Crashed" 😤
In college, we all suffered through **Network Programming** using heavy Virtual Machines. You’d be in the middle of a task, and the VM would suddenly crash, taking all your unsaved progress with it. 

I built this project to kill that problem. Instead of running a whole OS just to compile a simple C file, **Unix Engine** provides a containerized "Remote Factory." It ensures that everyone has the same dependencies, follows the "It works on my machine" philosophy, and stays lightweight by running only what's necessary.



---

## 🚀 How It Works (The Brain)
The project acts as a **Build-as-a-Service**. You write your code on Windows, and the engine compiles it in a clean Ubuntu environment inside Docker.

1.  **Zip & Ship:** A PowerShell script (`deploy.ps1`) packages your code. It’s smart enough to filter out "trash" folders like `.vscode` (which can be huge) and `.git` caches.
2.  **The API:** An Nginx reverse proxy hands the request to a Flask app.
3.  **Smart Build:** * If you have a **Makefile**, the engine uses it.
    * If not, it automatically "scouts" all `.c` files in your directory and links them with GCC.
4.  **Auto-Cleanup:** After the build, the engine renames the binary to match your project name and **wipes the workspace clean**, leaving only the final `.out` binary.

---

## 📦 Prerequisites
* **Docker Desktop** (Essential: The engine runs inside a container).
* **PowerShell Core** (To run the deployment script).

---

## 🛠️ Installation & Setup

1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/your-username/unix-engine.git](https://github.com/your-username/unix-engine.git)
   cd unix-engine
   ```

2. **Build the Image:**
   ```bash
   docker build -t unix-compiler .
   ```

3. **Start the Engine:**
   ```bash
   docker run -d -p 8050:80 --name brave_snyder unix-compiler
   ```

---

## 💻 Usage

1.  Copy `deploy.ps1` into your C/C++ project folder.
2.  Run the script:
    ```powershell
    ./deploy.ps1
    ```
3.  The engine will return a compiled Linux binary (e.g., `MyProject.out`) directly to your Windows folder.



---

## 📂 The Workspace
The internal container directory is `/workspace`.
* **Build Site:** Where compilation happens.
* **Final Destination:** Once the build is done, the source code is purged, and the binary is the only thing left.
* **Manual Testing:** To run the app inside the Linux environment:
  ```bash
  docker exec -it brave_snyder bash
  cd /workspace
  ./YourProject.out
  ```

---

## 🛡️ License
This project is open-source under the MIT License.

---
