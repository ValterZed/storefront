function copy(text) {
    navigator.clipboard.writeText(text)
}
function redirect_home() {
    window.location.href = "/rewrite/"
}
function addDivToParent(parent, onNewLine, className, idName, text){
    var div = document.createElement('div');
    div.innerHTML = text.replaceAll("'","");
    div.className = className;
    div.id = idName;
    div.onclick = function() {copy(text.replaceAll("&#x27;+",""))}

    document.getElementById(parent).appendChild(div);
}
