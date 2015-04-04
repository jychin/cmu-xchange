var req;

// Sends a new request to update the to-do list
function sendRequest() {
    if (window.XMLHttpRequest) {
        req = new XMLHttpRequest();
    } else {
        req = new ActiveXObject("Microsoft.XMLHTTP");
    }
    req.onreadystatechange = handleResponse;
    req.open("GET", "/globalstreamjson", true);
    req.send(); 
}

// This function is called for each request readystatechange,
// and it will eventually parse the XML response for the request
function handleResponse() {
    if (req.readyState != 4 || req.status != 200) {
        return;
    }

    // Removes the old to-do list items
    var list = document.getElementById("postlist");
    var oldLength = 0;

    var c = document.getElementById("postlist").childNodes;
    for (var i = 0; i < c.length; i++) {
        if(c[i].nodeName == "DIV") {
            oldLength++;
        }
    }
    console.log(oldLength);

    /*
    while (list.hasChildNodes()) {
        list.removeChild(list.firstChild);
    }
    */

    // Parses the response to get a list of JavaScript objects for 
    // the items.
    var items = JSON.parse(req.responseText);

    // Adds each new todo-list item to the list
    for (var i = 0; i < items.length - oldLength; i++) {
        // Extracts the item id and text from the response
        var itemid = items[i]["itemid"];
        var userid = items[i]["userid"];
        var username = items[i]["username"];
        var created = items[i]["created"];
        var text = items[i]["text"];
        var comments = items[i]["comments"];
  
        // Builds a new HTML list item for the todo-list item

        var newItem = document.createElement("div");
        newItem.innerHTML = "<hr><div ><p class=\"lead bg-info\"><img src=\""
              + "/photo/" + userid
              + "\" width=\"40px\"> Posted By <a href=\"/profile/" + userid
              + "\">" + username + "</a> on " + created + "</p></div><div><p class=\"post\">" + text + "</p></div>";

        newItem.innerHTML += "<div><textarea class=\"field span10\" rows=\"3\" maxlength=\"50\" id=\"comment-content-" 
                    + itemid + "\"></textarea> <br> <br><input class=\"btn btn-large btn-primary offset7\" onclick=\"addcomment(" 
                    + itemid + ")\" value=\"Add Comment\" /></div>";
        newItem.innerHTML += "<div id=\"comment-" + itemid + "\">"; 
        for (var j = 0; j < comments.length; j++) {
            var c_itemid = comments[j]["itemid"];
            var c_userid = comments[j]["userid"];
            var c_username = comments[j]["username"];
            var c_created = comments[j]["created"];
            var c_text = comments[j]["text"];
      
            newItem.innerHTML += "<hr><div ><p><img src=\""
                  + "/photo/" + c_userid
                  + "\" width=\"40px\"> Commented By <a href=\"/profile/" + c_userid
                  + "\">" + c_username + "</a> on " + c_created + "</p></div><div><p class=\"post\">" + c_text + "</p></div>";
        }
        newItem.innerHTML += "</div>";
        newItem.className = "post-item";
        // Adds the todo-list item to the HTML list
        if(list.childNodes.length > 0) {
            list.insertBefore(newItem, list.firstChild);
        } else {
            list.appendChild(newItem);
        }
        
    }
}

// causes the sendRequest function to run every 5 seconds
window.setInterval(sendRequest, 5000);
