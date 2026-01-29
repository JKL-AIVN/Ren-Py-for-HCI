# telemetry.rpy

# Force default to False, implementing "Privacy by Design" ethics
default persistent.data_consent = False 
default persistent.player_id = None

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

    def log_hcievent(event_type, details):
        """
        Main thread calling interface: non-blocking
        """
        # Check for player consent before proceeding
        if not persistent.data_consent:
            return

        # Generate ID
        if persistent.player_id is None:
            persistent.player_id = str(uuid.uuid4())
        
        payload = {
            "player_id": persistent.player_id,
            "event_type": event_type,
            "details": details,
            "client_timestamp": time.time()
        }

        # Start the thread, let _worker run in the background
        t = threading.Thread(target=_worker, args=(payload,))
        t.daemon = True # Ensure the thread closes when the game closes
        t.start()
