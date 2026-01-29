# screens.rpy

screen data_autonomy_panel():
    style_prefix "data_ui"
    vbox:
        xalign 0.5
        yalign 0.4
        spacing 20

        text "HETEROTOPIA DATA LINK STATUS" size 30 color "#00ffff"
        
        # showing text
        if persistent.data_consent:
            text "[ LINK STATUS: SYNCING ]" color "#00ff00" xalign 0.5
        else:
            text "[ LINK STATUS: DISCONNECTED ]" color "#ff0000" xalign 0.5

        null height 20

        # switch
        textbutton "Toggle Neural Data Sync":
            action ToggleField(persistent, "data_consent")
            style "cyber_button"

        text "This will affect anonymous data uploads to the Cloud Shrine." size 16 italic True xalign 0.5

style cyber_button:
    background Frame(Solid("#00ffff33"), 4, 4)
    hover_background Solid("#00ffff66")
    padding (10, 10)
    text_size 22
    text_idle_color "#00ffff"
    text_hover_color "#ffffff"