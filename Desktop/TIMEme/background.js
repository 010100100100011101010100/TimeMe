//This is going to notify the user that the chrome extension has been installed 
chrome.runtime.onInstalled.addListener(()=>{
        console.log("The chrome extension has been installed");
});