# script.rpy

# 1. Character and Environment Definitions
define e = Character("AI-09", color="#00ffff")
# Define high latency threshold (seconds) - used to trigger interrogation
define LATENCY_THRESHOLD_HIGH = 5.0 

init python:
    import time 

# 2. Data collection toggle and default values
default persistent.data_consent = False
default persistent.player_id = None

# Game Entry Point
label start:
    "System booting... Initializing virtual Kowloon environment."
    
    # === Phase 1: Data Consent Flow (Original) ===
    if not persistent.data_consent:
        e "New neural connection detected. To maintain the city's 'frequency tuning' stability, are you willing to share your interaction traces with HETEROTOPIA?"
        
        menu:
            "【Establish Link】Authorize data synchronization":
                $ persistent.data_consent = True
                $ log_hcievent("consent_granted", "Player accepted via start menu")
                e "Thank you for your trust. Data has begun flowing to the cloud shrine."
                
            "【Remain Isolated】Refuse data collection":
                $ persistent.data_consent = False
                e "Understood. Your frequency will remain on a private band, free from external interference."

    # Enter main measurement event
    jump spirit_tuning_event


# === Phase 2: Project ALETEIA Core Measurement Logic (Replaced old code) ===

label spirit_tuning_event:
    e "Can you... really hear my voice?"
    
    # Mark decision point ID (for detecting Rollback/Regret)
    $ current_decision_id = "spirit_tuning_01"
    
    # ALETEIA Mechanism 1: Check if it's a re-selection after Rollback (Regret Metric)
    # This function is defined in telemetry.rpy
    if probe.check_regret(current_decision_id):
        # Trigger special dialogue, breaking the fourth wall
        e "Wait... I feel a temporal anomaly. You've been here before, haven't you? Did you regret your previous choice?"
        $ log_hcievent("metric_regret_detected", {"decision_id": current_decision_id})

    $ start_time = time.time()
    
    menu:
        # Note: The choice screen in screens.rpy now automatically captures hover data (Hover Trace)
        
        "(Try to tune frequency and respond to her)":
            # Here we record total time spent; detailed hover traces are handled by screens.rpy
            $ duration = round(time.time() - start_time, 3)
            jump empathy_check_logic
            
        "(Ignore noise, disconnect link)":
            $ duration = round(time.time() - start_time, 3)
            jump logic_route

label empathy_check_logic:
    # ALETEIA Mechanism 2: Triangulation Verification
    
    if duration > LATENCY_THRESHOLD_HIGH:
        # Latency too high, jump to "Epistemological Calibration" dialogue
        jump high_latency_interrogation
    else:
        # Low latency, treated as intuitive response (Intuitive Empathy)
        $ log_hcievent("tuning_choice", {"type": "intuitive_empathy", "latency": duration, "choice": "respond"})
        "You chose empathy instinctively ([duration]s)."
        jump empathy_route

label high_latency_interrogation:
    # ALETEIA Mechanism 3: Self-Reporting
    # AI detects hesitation, asks player for explanation to eliminate data ambiguity
    
    show e at center with dissolve
    e "Signal logic implies hesitation. You paused for [duration] seconds."
    e "Is this delay a calculation of cost... or a weight of conscience?"

    menu:
        "I was weighing the ethical cost. (Moral Hesitation)":
            # This is the "Thick Data" you want: player confirms delay represents ethical deliberation
            $ log_hcievent("tuning_choice", {"type": "deliberative_empathy", "latency": duration, "self_report": "moral", "choice": "respond"})
            e "Acknowledgment received. Processing ethical weight."
            
        "I was just reading the protocol. (Cognitive Load)":
            # Calibration data: proves delay is just reading time
            $ log_hcievent("tuning_choice", {"type": "reading_delay", "latency": duration, "self_report": "cognitive", "choice": "respond"})
            e "Understood. Parsing textual data."

        "System lag / Distraction. (Noise)":
            # Exclude data noise
            $ log_hcievent("tuning_choice", {"type": "system_noise", "latency": duration, "self_report": "technical", "choice": "respond"})
            e "Calibrating sensors..."

    jump empathy_route

# === Ending Routes ===

label empathy_route:
    "Data has been asynchronously synchronized to the cloud shrine."
    # You can continue your story here...
    return

label logic_route:
    # Record cold choice
    $ log_hcievent("tuning_choice", {"type": "disconnection", "latency": duration, "choice": "disconnect"})
    "Link disconnected. The signal fades into the static."
    return