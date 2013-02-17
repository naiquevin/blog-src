window.onload = function () {
    var emails = document.getElementsByTagName("email");
    for (var i=0; i<emails.length; i++) {
        var val = emails[i].textContent;
        emails[i].textContent = val.replace(/[a-zA-Z]/g, function (c) {
            return String.fromCharCode((c<="Z"?90:122)>=(c=c.charCodeAt(0)+13)?c:c-26);
        });
    }
}

