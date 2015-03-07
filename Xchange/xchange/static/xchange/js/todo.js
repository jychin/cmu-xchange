
var req;

// Sends a new request to update the to-do list
function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "/get_post_json", true);
    req.send(); 
}

// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }
    var list = document.getElementById("mylist");
    var oldLength = list.childElementCount;

    // Parses the response to get a list of JavaScript objects for 
    // the items.
    var items = JSON.parse(req.responseText);

    // Adds each new item to the list
    for (var i = 0; i < items.length - oldLength; i++) {
        // Extracts the item id and text from the response
        var itemid = items[i]["itemid"];
        var userid = items[i]["userid"];
        var username = items[i]["username"];
        var text = items[i]["text"];
        var time = items[i]["time"];
        var comments = items[i]["comments"];
        
        // Builds a new HTML list item for the todo-list item
        var newItem = document.createElement("div");
        newItem.innerHTML = "<p class=\"lead bg-info\">" +  text +
        "<p><img src=\"/photo/" + userid +"\" width=\"40px\">posted by <a href=\"/profile/" + userid + "\">" + username + "</a> on " + time + "</p>";
        
        newItem.innerHTML += "<hr><div ><p><img src=\""
                  + "/photo/" + c_userid
                  + "\" width=\"40px\"> Commented By <a href=\"/profile/" + c_userid
                  + "\">" + c_username + "</a> on " + c_created + "</p></div><div><p class=\"post\">" + c_text + "</p></div>";

        newItem.innerHTML += "</div>";
        newItem.className = "blog";
        
        // Adds the mylist item to the HTML list
        if(list.childNodes.length > 0) {
            list.insertBefore(newItem, list.firstChild);
        } else {
            list.appendChild(newItem);
        }
        
    }
}

// causes the sendRequest function to run every 5 seconds
//window.setInterval(sendRequest, 5000);
