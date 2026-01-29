
<div align="center">

# 🔮 Project Neon: HCI Telemetry Probe

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Ren'Py](https://img.shields.io/badge/Engine-Ren'Py_8.x-ff69b4.svg)](https://www.renpy.org/)
[![Status](https://img.shields.io/badge/Status-Research_Prototype-2ea44f.svg)]()
[![Methodology](https://img.shields.io/badge/Methodology-Value_Sensitive_Design-purple.svg)]()

> *"Quantifying empathy labor in post-human social dynamics."*
> *"量化後人類社會動態中的共情勞動。"*

<p align="center">
  <b>Project Neon Telemetry</b> is a lightweight, asynchronous HCI research probe for Ren'Py.<br>
  It captures <b>millisecond-level decision latency</b> to quantify user hesitation and ethical engagement,<br>
  bridging the gap between <b>Cultural Theory</b> and <b>Game Mechanics</b>.
</p>

[Report Bug](https://github.com/JKL-AIVN/project-neon-telemetry/issues) · [Request Feature](https://github.com/JKL-AIVN/project-neon-telemetry/issues)

</div>

---

## ⛩️ Value Sensitive Design (VSD) & Ethics
> **"Technology is not neutral; it embodies the values of its creators."**

This project strictly adheres to **Value Sensitive Design (VSD)** principles, translating the concept of "Data Sovereignty" into executable Python code. We reject the standard "surveillance capitalism" model in favor of a **Ritualistic Data Gift** model.

### 🛡️ Privacy by Design (PbD)
Our telemetry implementation prioritizes user autonomy through three architectural hard-stops:

* **🚫 Default Opt-Out (預設拒絕):** The variable `persistent.data_consent` is hard-coded to `False`. No network socket is ever opened until the user explicitly performs the "Handshake Ritual" (clicks the toggle).
* **🎭 Radical Anonymity (徹底匿名):** We do not collect IP addresses, hardware IDs, or Steam IDs. Users are assigned a random `UUIDv4` that persists only locally, representing a "relational entity" rather than a biological subject.
* **🎛️ Revocable Sovereignty (可撤回主權):** A dedicated **Data Autonomy Panel** (included in `data_policy_ui.rpy`) allows users to sever the data link at any moment from the Settings menu, instantly halting all background threads.

---

## 🔬 Research Capability

Built for the undergraduate thesis **"Rehearsing Techno-Animism"**, this tool operationalizes abstract philosophical concepts into measurable metrics:

| Metric | Code Implementation | Theoretical Basis |
| :--- | :--- | :--- |
| ⏱️ **Hesitation Latency** | `time.time() - start_time` | **Care Ethics:** Hesitation (`Δt`) implies emotional labor and internal conflict, differentiating "reflexive clicking" from "ethical pondering." |
| ⛩️ **Ritual Frequency** | `log_hcievent("shrine_visit")` | **Techno-Animism:** Measuring how often users engage with non-functional "spirit" objects (Digital Shrine) indicates a shift towards animistic ontology. |
| 🔀 **Choice Topology** | Branch Path Analysis | **Symbiosis:** Mapping the trajectory of user relationships with AI agents (09) to visualize the "Post-Human Convergent" point. |


📦 Modular Installation
This module is designed to be non-intrusive. It does not overwrite your existing screens.rpy or gui.rpy.
1. Copy Files
Drop the following files into your project's game/ folder:
 * telemetry.rpy (Core Logic)
 * data_policy_ui.rpy (The UI Panel)
2. Configure Endpoint
Open telemetry.rpy and replace the TELEMETRY_URL with your own Google Script deployment URL.
3. Integrate UI (The "Plug-in" Step)
To make the Data Autonomy Switch visible to players, edit your existing screens.rpy. Find the screen preferences(): section and add this single line where you want the panel to appear:
# In your game/screens.rpy

screen preferences():
    tag menu
    # ... existing code ...
    
    vbox:
        # ... your existing sliders ...
        
        # Add this line to inject the module:
        use data_autonomy_panel

> "We code not to control, but to commune."
> 


---

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
