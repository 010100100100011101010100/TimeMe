const root = document.body; // Get the root body element of the page

// Dynamically add the Luxon library script to the document head

// let script = document.createElement("script");
// script.src = "https://cdnjs.cloudflare.com/ajax/libs/luxon/3.3.0/luxon.min.js"; // Luxon library URL
// script.type = "text/javascript";
// script.onload = () => {
//     console.log("Luxon added successfully"); // Log success when the script loads
// };


// Extract all visible text nodes from the body
let allTextNodes = extractTextNodes(root);
// console.log("These are all the text nodes bro",allTextNodes);

const options = { timeZone: 'America/New_York', timeStyle: 'short', dateStyle: 'short' };
if(a !=[]){
    const newYorkTime = a.toLocaleString('en-US', options);
    console.log(newYorkTime);   
}
else if (b!=[]){
    const newYorkTime = b.toLocaleString('en-US', options);
    console.log(newYorkTime);
}

else if(c!=[]){
    const newYorkTime = c.toLocaleString('en-US', options);
    console.log(newYorkTime);
}



// document.head.appendChild(script); // Append the script to the head of the document

// Function to recursively extract all text nodes from a given node
function extractTextNodes(node) {
    let textNode = [];
    // If the node is a text node and contains non-empty text, add it to the array
    if (node.nodeType === Node.TEXT_NODE && node.nodeValue.trim() !== "") {
        textNode.push(node.nodeValue.trim());
    }
    // If the node is an element node, iterate through its children and extract text
    if (node.nodeType === Node.ELEMENT_NODE) {
        for (let child of node.childNodes) {
            textNode = textNode.concat(extractTextNodes(child));
        }
    }
    return textNode; // Return the collected text nodes
}

// Function to check if a node is visible on the page
function isVisible(node) {
    let style = window.getComputedStyle(node); // Get the computed styles of the node
    return style.display !== "none" && style.visibility !== "hidden"; // Check visibility and display
}


// Function to detect different time formats from an array of visible text
function detectTimeFormats(visibleTextArray) {
    let combined = visibleTextArray.join(" "); // Combine all extracted text into a single string

    // Regex pattern to match 12-hour time format with AM/PM
    let regex12 = /\b([1-9]|1[0-2]):([0-5][0-9])\s?(AM|PM)\b/g;
    
    // Regex pattern to match 24-hour time format (00:00 to 23:59)
    let regex24 = /\b([01]?[0-9]|2[0-3]):([0-5][0-9])\b/g;
    
    // Regex pattern to match date-time format (e.g., YYYY-MM-DD HH:MM)
    let regexDateTime = /\b(\d{4}-\d{2}-\d{2})\s([01]?[0-9]|2[0-3]):([0-5][0-9])\b/g;
    
    // Regex pattern to match timezone identifiers (e.g., UTC, PST, UTC+5)
    let regexTimezone = /\b(UTC|PST|IST|EST|CET|[A-Z]{3,4})([-+]\d{1,2})?\b/g;

    // Match all patterns in the combined text and return results
    let match12hr = combined.match(regex12) || []; // Matches 12-hour times
    let match24hr = combined.match(regex24) || []; // Matches 24-hour times
    let matchDate = combined.match(regexDateTime) || []; // Matches date-time formats
    let matchTimezone = combined.match(regexTimezone) || []; // Matches timezones

    return {
        match12hr,
        match24hr,
        matchDate,
        matchTimezone
    };
}
