# 🤖 Customer Support Agent Workflow

## Simple customer support agent using Agentic-AI approach.

### 📜 Description

This utility implements a modular, agentic workflow using **LangGraph** to automate the intake, evaluation, and logging of client support inquiries. It helps users get clear, policy-based answers to their queries by passing the request through a sequence of specialized agents.

The core architecture is structured into independent Python classes, designed for eventual deployment as scalable microservices (e.g., in Kubernetes).

## ✨ Features

* **Modular Agent Design:** Each workflow step is a distinct Python class, ready for individual containerization and scaling.
* **AI-Powered Evaluation:** Uses the Gemini API (via the OpenAI compatibility layer) to dynamically approve or deny requests based on policy and request details.
* **Structured State Management:** Utilizes the central `InquiryState` dataclass to pass data seamlessly and safely between agents (Nodes).

## 📐 Workflow Diagram

The workflow follows a sequential path managed by the LangGraph orchestrator:

1.  **IntakeAgent:** Logs the request and initializes the state.
2.  **EvaluationAgent:** Calls the Gemini model to decide approval/denial.
3.  **SchedulingAgent:** Schedules a follow-up if the request is approved.
4.  **CRMUpdateAgent:** Logs the final status to a simulated CRM system.



## 🚀 Getting Started

### Dependencies

* Python version **3.8** or higher.
* The required libraries are listed in `setup.py`.

### 1. Prerequisites and Configuration

You must have a **Gemini API Key** to run the `EvaluationAgent`.

1.  **Create a `.env` file** in the project's root directory (`customer_support/`).
2.  Add your API key:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

### 2. Installing

**It is highly recommended to use a Python virtual environment to isolate project dependencies.**

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/customer-support-agent.git](https://github.com/your-username/customer-support-agent.git)
    cd customer_support
    ```
2.  **Create and Activate Virtual Environment:**
    ```bash
    # Create the environment
    python -m venv venv 
    
    # Activate the environment (Windows)
    .\venv\Scripts\activate
    
    # Activate the environment (macOS/Linux)
    source venv/bin/activate
    ```
3.  **Install the package:**
    Install the package in editable mode (`-e`) using `pip`:
    ```bash
    pip install -e .
    ```

## 🖥️ Usage

The package exposes a console script named `run-support` defined in `setup.py`.

### Run the Workflow Demo

Execute the full workflow demo, which runs two predefined scenarios: a quota request (approved) and a sensitive access request (denied).

```bash
run-support