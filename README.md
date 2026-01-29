# Neon Hearts of Kowloon: A Ren'Py Telemetry Framework for Research through Design

[![Ren'Py](https://img.shields.io/badge/Ren'Py-8.0.3-ff69b4)](https://www.renpy.org/)
[![Status](https://img.shields.io/badge/Status-Research_Prototype-blueviolet)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Research](https://img.shields.io/badge/Framework-Metamodern_Cosmotechnics-00ffff)]()

> "The price of data is context." — C. Thi Nguyen, *The Limits of Data*

## 📖 Abstract

**Neon Hearts of Kowloon** is not just a Cyberpunk visual novel; it is an **epistemic probe** disguised as a game. Developed as part of a **Research through Design (RtD)** practice, this project investigates **Techno-Animism** and **Post-Human Symbiosis** within the context of Hong Kong's hyper-dense urbanism.

Unlike traditional game analytics that treat players as data mines, this framework implements **Project ALETEIA**—a value-sensitive telemetry system designed to quantify "empathy labor" while respecting user autonomy. It challenges the "surveillance capitalism" model by making data collection visible, diegetic, and strictly opt-in.

---

## 🏗 Research Framework:

This codebase serves as a practical implementation of the following theoretical concepts:

* **Metamodern Cosmotechnics:** Reimagining the relationship between technology and the moral subject, inspired by Yuk Hui.
* **Anti-Reductionism in Data:** Responding to C. Thi Nguyen's critique that metrics strip away context. We solve this by implementing **"Thick Data"** collection methods (Hesitation Traces, Regret Metrics, Self-Reporting).
* **Value Sensitive Design (VSD):** Embedding ethical values (privacy, transparency, reversibility) directly into the code structure (`persistent.data_consent`).

---

## ⚡ Project ALETEIA: The Epistemic Probe

The core of this repository is the **ALETEIA Probe** (`telemetry.rpy`), a custom-built telemetry module for Ren'Py that captures the *process* of decision-making, not just the result.

### 1. The Regret Metric (Temporal Correction)
* **Theory:** Human ethical decisions are iterative, not linear. "Save scumming" (reloading) is often a sign of moral reflection.
* **Implementation:** The system uses `persistent.aleteia_history` to track unique decision IDs across save states. If a player rolls back time to change a decision, the system detects this "temporal anomaly" and logs it as an act of **Ethical Correction**.
* **Code:** `probe.check_regret(decision_id)`

### 2. The Hesitation Trace (The Road Not Taken)
* **Theory:** What a player *doesn't* choose is as important as what they do. Hovering over a choice without clicking indicates internal friction or "empathy labor."
* **Implementation:** Using Ren'Py's `hovered` hooks in `screens.rpy`, the system tracks mouse dwell time on unselected options.
* **Payload:** Captures the "Road Not Taken" (e.g., `hover_trace: {"Disconnect": 3.2s}`).

### 3. Epistemic Triangulation (Diegetic Interrogation)
* **Theory:** High latency (delay) in decision-making is ambiguous. It could be deep empathy, or just reading speed/lag. Data alone is insufficient.
* **Implementation:** When latency exceeds `LATENCY_THRESHOLD_HIGH` (e.g., 5s), the AI character (AI-09) breaks the fourth wall to ask the player *why* they hesitated.
* **Output:** Combines **Behavioral Data** (Time), **Intent Data** (Self-Report), and **Context Data** (Narrative) into a single rigorous JSON object.

---

## ⛩️ Value Sensitive Design (VSD) & Ethics
> **"Technology is not neutral; it embodies the values of its creators."**

This project strictly adheres to **Value Sensitive Design (VSD)** principles, translating the concept of "Data Sovereignty" into executable Python code. We reject the standard "surveillance capitalism" model in favor of a **Ritualistic Data Gift** model.

### 🛡️ Privacy by Design 
Our telemetry implementation prioritizes user autonomy through three architectural hard-stops:

* **🚫 Default Opt-Out :** The variable `persistent.data_consent` is hard-coded to `False`. No network socket is ever opened until the user explicitly performs the "Handshake Ritual" (clicks the toggle).
* **🎭 Radical Anonymity :** We do not collect IP addresses, hardware IDs, or Steam IDs. Users are assigned a random `UUIDv4` that persists only locally, representing a "relational entity" rather than a biological subject.
* **🎛️ Revocable Sovereignty :** A dedicated **Data Autonomy Panel** (included in `data_policy_ui.rpy`) allows users to sever the data link at any moment from the Settings menu, instantly halting all background threads.

> "We code not to control, but to commune."
> 

---
## Backend Setup (Google Cloud Shrine)

To replicate the data collection environment, you must deploy the Google Apps Script provided in `code.gs`:

1.  **Create Spreadsheet:** Create a new Google Sheet and name it `Neon_Hearts_Telemetry`.
2.  **Access Script Editor:** Go to `Extensions` > `Apps Script`.
3.  **Paste Code:** Replace the default code with the contents of `code.gs` from this repository.
4.  **Header Setup:** Ensure the first row of your sheet has the following headers to match the ALETEIA schema:
    * `A1: Server Timestamp`, `B1: Client Timestamp`, `C2: Player ID`, `D2: Event Type`, `E2: Details (JSON)`
5.  **Deploy as Web App:** * Click `Deploy` > `New Deployment`.
    * Select `Web App`.
    * **Execute as:** `Me`.
    * **Who has access:** `Anyone` (This is required for Ren'Py to send data without OAuth).
6.  **Connect:** Copy the `Web App URL` and paste it into the `TELEMETRY_URL` variable in `telemetry.rpy`.

---

## 🛠 Technical Architecture

The system is composed of three synchronized Ren'Py script files:

| File | Function |
| :--- | :--- |
| **`telemetry.rpy`** | **The Brain.** Contains the `AleteiaProbe` class, threaded network workers (`urllib`/`ssl`), and the `persistent` memory logic. |
| **`screens.rpy`** | **The Nervous System.** Modified `screen choice` to listen for `hovered`/`unhovered` events, capturing physical hesitation before a click occurs. |
| **`scripts.rpy`** | **The Interface.** The narrative layer that triggers specific probe events, handles the "AI Interrogation" logic, and manages the initial "Data Consent" flow. |
| **`data_policy_ui.rpy`** | **The Ethics Layer.** Provides a visual, clickable "Link Status" toggle, ensuring consent is reversible at any time. |

### Data Payload Example (JSON)
The system sends asynchronous POST requests to a Google Apps Script endpoint:


## 🛠️ Technical Architecture

The system utilizes a **Serverless Architecture** (Google Apps Script + Sheets) to ensure zero-cost deployment, high scalability, and thread-safe asynchronous execution.

```mermaid
sequenceDiagram
    participant Player as Ren'Py Client (Main Thread)
    participant Guard as Consent Gatekeeper
    participant Thread as Async Worker (Daemon)
    participant Cloud as Google Script API

    Note over Player: User faces Ethical Dilemma
    Player->>Player: Hesitates... (Time counting)
    Player->>Player: Makes Choice
    
    Player->>Guard: log_hcievent(event, latency)
    
    alt Consent == False
        Guard--xPlayer: RETURN IMMEDIATE (No Net-Op)
    else Consent == True
        Guard->>Thread: Spawn Thread (Daemon)
        Note right of Player: Game continues (No Lag)
        Thread->>Cloud: HTTPS POST (JSON Payload)
        Note over Thread: SSL Context Injection
        Cloud-->>Thread: 200 OK
    end
