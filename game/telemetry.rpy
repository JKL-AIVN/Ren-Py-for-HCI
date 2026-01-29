# telemetry.rpy

# Force default to False, implementing "Privacy by Design" ethics
default persistent.data_consent = False 
default persistent.player_id = None
# Added: Persistent memory to record player history, resistant to Rollback.
default persistent.aleteia_history = set()

# init -1 ensures functions are defined before the game starts, solving NameError
init -1 python:
    import json
    import threading
    import ssl
    import time
    import uuid

    # Determine Python version
    try:
        import urllib.request as urllib_req
        from urllib.error import URLError, HTTPError
        py3 = True
    except ImportError:
        import urllib2 as urllib_req
        from urllib2 import URLError, HTTPError
        py3 = False
        
    # Your Google Script API URL
    TELEMETRY_URL = "https://script.google.com/COPY_HERE"

    def _worker(payload):
        """
        Background worker thread: responsible for actual network transmission
        """
        try:
            # Use default=str to handle non-serializable objects gracefully
            data = json.dumps(payload, default=str)
            if py3:
                data = data.encode('utf-8')

            # Create a context that does not verify certificates (Windows fix)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            req = urllib_req.Request(TELEMETRY_URL, data, {'Content-Type': 'application/json'})
            
            # Send request (won't freeze the game even if it's slightly slow)
            with urllib_req.urlopen(req, context=ctx, timeout=10) as response:
                pass
            
        except Exception as e:
            # Fail silently in production, or just print to the console
            print("Telemetry Failed: " + str(e))

    # === ALETEIA PROBE MODULE ===
    class AleteiaProbe:
        def __init__(self):
            # Temporary storage for hover data (current decision)
            self.hover_log = {} 
            self.hover_start = {}

        def start_hover(self, item_id):
            """Starts timing: when the mouse enters an option"""
            self.hover_start[item_id] = time.time()

        def end_hover(self, item_id):
            """Ends timing: when the mouse leaves an option"""
            if item_id in self.hover_start:
                duration = time.time() - self.hover_start[item_id]
                # Accumulate time (prevents double-counting if the player enters/leaves the same option multiple times)
                self.hover_log[item_id] = self.hover_log.get(item_id, 0.0) + duration
                del self.hover_start[item_id]

        def get_and_clear_trace(self):
            """Retrieves data and clears it (for the next decision)"""
            trace_data = self.hover_log.copy()
            self.hover_log.clear()
            self.hover_start.clear()
            return trace_data

        def check_regret(self, decision_unique_id):
            """
            Checks for "regret" (Rollback).
            If the player rolls back time, persistent variables are not reset,
            allowing us to detect if 'decision_unique_id' already exists in the history.
            """
            if decision_unique_id in persistent.aleteia_history:
                return True
            else:
                persistent.aleteia_history.add(decision_unique_id)
                return False

    # Instantiate the probe (Global Object)
    probe = AleteiaProbe()

    # Slightly modified log_hcievent to support passing complex dictionaries (Dict)
    def log_hcievent(event_type, details):
        if not persistent.data_consent:
            return

        if persistent.player_id is None:
            persistent.player_id = str(uuid.uuid4())
        
        payload = {
            "player_id": persistent.player_id,
            "event_type": event_type,
            "details": details, # Now accepts complex dictionaries containing hover_trace
            "client_timestamp": time.time()
        }

        t = threading.Thread(target=_worker, args=(payload,))
        t.daemon = True 
        t.start()
