# 1. Character and Environment Definitions
define e = Character("AI-09", color="#00ffff")

init python:
    import time # Must import Python time library

# 2. Data Collection Switch
default persistent.data_consent = False
default persistent.player_id = None

label start:
    "System booting... Initializing virtual Kowloon environment."

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

    # Proceed with game logic
    jump spirit_tuning_event

label spirit_tuning_event:
    e "Can you... really hear my voice?"
    
    # Use native Python timer
    $ start_time = time.time()
    
    menu:
        "(Try to tune frequency and respond to her)":
            # Calculate difference
            $ duration = round(time.time() - start_time, 3)
            $ log_hcievent("tuning_choice_empathy", {"duration": duration, "choice": "respond"})
            "You chose empathy; decision took [duration] seconds."
            jump empathy_route
            
        "(Ignore noise, disconnect link)":
            $ duration = round(time.time() - start_time, 3)
            $ log_hcievent("tuning_choice_ignore", {"duration": duration, "choice": "disconnect"})
            "You chose indifference; decision took [duration] seconds."
            jump logic_route

label empathy_route:
    "Data has been asynchronously synchronized to the cloud shrine."
    return

label logic_route:
    "Link disconnected."
    return
