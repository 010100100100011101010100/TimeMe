document.getElementById('SaveTimeZone').addEventListener("click", function() {
    // Get the value of the selected timezone from the input field with ID "timezone"
    let selectedTimeZone = document.getElementById("timezone").value;
    
    // Save the selected timezone to Chrome's storage (synchronized across devices)
    chrome.storage.sync.set({ userTimezone: selectedTimeZone }, function() {
        // Log the saved timezone to the console
        console.log("Timezone saved", selectedTimeZone);
        
        // Show an alert to the user confirming the timezone has been saved
        alert("Timezone Saved");
    });
});
