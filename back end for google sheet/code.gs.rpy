function doPost(e) {
  // Get the current active sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  
  try {
    // Parse JSON data sent from Ren'Py
    var data = JSON.parse(e.postData.contents);
    
    // 1. Server Timestamp: Records the time the data reached the cloud
    var server_time = new Date();
    
    // 2. Client Timestamp: 
    // Original time sent from Ren'Py, used to calibrate network latency.
    // If not provided, use the current time as a fallback.
    var client_time = data.client_timestamp ? new Date(data.client_timestamp * 1000) : server_time;

    // 3. Handle complex data (CRITICAL UPDATE)
    // Use JSON.stringify to convert the details object (containing hover_trace, regret, etc.)
    // into a string. This ensures Google Sheets can store it completely without it becoming [object Object].
    var details_string = "";
    if (typeof data.details === 'object') {
      details_string = JSON.stringify(data.details);
    } else {
      details_string = String(data.details);
    }

    // 4. Append a row
    // Recommended column order: ServerTime | ClientTime | PlayerID | EventType | Details (JSON)
    sheet.appendRow([
      server_time,       // Column A
      client_time,       // Column B
      data.player_id,    // Column C
      data.event_type,   // Column D
      details_string     // This is your rich data repository
    ]);
    
    // Return success message to Ren'Py
    return ContentService.createTextOutput(JSON.stringify({"status": "success"}));
    
  } catch (error) {
    // Error handling: If there's an issue, log it in the Logger (viewable in the GAS backend)
    Logger.log(error);
    return ContentService.createTextOutput(JSON.stringify({"status": "error", "message": error.toString()}));
  }
}