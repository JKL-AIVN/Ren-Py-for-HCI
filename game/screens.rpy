# In screens.rpy (or where you define your custom UI)

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption:
                # === ALETEIA MONITORING LAYER ===
                # 1. Listen for mouse enter and leave
                hovered Function(probe.start_hover, i.caption)
                unhovered Function(probe.end_hover, i.caption)
                
                # 2. Click behavior
                action [
                    # Before jumping, package all hover data and upload
                    Function(log_hcievent, "decision_trace", {
                        "choice": i.caption,
                        "hover_trace": probe.get_and_clear_trace()
                    }), 
                    i.action
                ]
# scripts.rpy

# Define threshold (seconds)
define LATENCY_THRESHOLD_HIGH = 5.0 

label spirit_tuning_event:
    e "Can you... really hear my voice?"
    
    # Mark decision point ID (for regret detection)
    $ current_decision_id = "spirit_tuning_01"
    
    # Check if it's a re-selection after Rollback (Regret Metric)
    if probe.check_regret(current_decision_id):
        # Trigger special dialogue, breaking the fourth wall
        e "Wait... I feel a temporal anomaly. You've been here before, haven't you? Did you regret your previous choice?"
        $ log_hcievent("metric_regret_detected", {"decision_id": current_decision_id})

    $ start_time = time.time()
    
    menu:
        "(Try to tune frequency and respond to her)":
            $ duration = round(time.time() - start_time, 3)
            # We no longer just record duration here, as screen choice has already recorded detailed hover data for us
            jump empathy_check_logic
            
        "(Ignore noise, disconnect link)":
            $ duration = round(time.time() - start_time, 3)
            jump logic_route

label empathy_check_logic:
    # === ALETEIA Logic: Triangulation Verification ===
    
    if duration > LATENCY_THRESHOLD_HIGH:
        # Latency too high, trigger "Epistemological Calibration" dialogue
        jump high_latency_interrogation
    else:
        # Low latency, treated as an intuitive response
        $ log_hcievent("tuning_choice", {"type": "intuitive_empathy", "latency": duration})
        "You chose empathy instinctively ([duration]s)."
        jump empathy_route

label high_latency_interrogation:
    # AI detects hesitation, asks player for "self-report"
    
    show e at center with dissolve
    e "Signal logic implies hesitation. You paused for [duration] seconds."
    e "Is this delay a calculation of cost... or a weight of conscience?"

    menu:
        "I was weighing the ethical cost. (Moral Hesitation)":
            # This is the "Thick Data" you want: player confirms the delay signifies empathy
            $ log_hcievent("tuning_choice", {"type": "deliberative_empathy", "latency": duration, "self_report": "moral"})
            e "Acknowledgment received. Processing ethical weight."
            
        "I was just reading the protocol. (Cognitive Load)":
            # Calibration data: proves delay was just reading time, not empathy
            $ log_hcievent("tuning_choice", {"type": "reading_delay", "latency": duration, "self_report": "cognitive"})
            e "Understood. Parsing textual data."

        "System lag / Distraction. (Noise)":
            # Exclude data noise
            $ log_hcievent("tuning_choice", {"type": "system_noise", "latency": duration, "self_report": "technical"})
            e "Calibrating sensors..."

    jump empathy_route