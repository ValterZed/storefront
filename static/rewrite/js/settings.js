var Tslider = document.getElementById("temperature");
        var Toutput = document.getElementById("tDisp");
        Toutput.innerHTML = Tslider.value;
    
        Tslider.oninput = function() {
        Toutput.innerHTML = this.value;
    }
    
    var MTslider = document.getElementById("max_tokens");
        var MToutput = document.getElementById("mtDisp");
        MToutput.innerHTML = MTslider.value;
    
        MTslider.oninput = function() {
        MToutput.innerHTML = this.value;
    }
    
    var FPslider = document.getElementById("frequency_penalty");
        var FPoutput = document.getElementById("fpDisp");
        FPoutput.innerHTML = FPslider.value;
    
        FPslider.oninput = function() {
        FPoutput.innerHTML = this.value;
    }
    
    var PPslider = document.getElementById("presence_penalty");
        var PPoutput = document.getElementById("ppDisp");
        PPoutput.innerHTML = PPslider.value;
    
        PPslider.oninput = function() {
        PPoutput.innerHTML = this.value;
    }

    
    function changeState(id) {
        var modeBtn = document.getElementById(id);
        if (modeBtn.textContent == "Rewrite") {
            modeBtn.textContent = "Free Use AI"
        }
    }

    function addDivToParent(parent, className, idName, text){
        var div = document.createElement('div');
        div.innerHTML = text.replaceAll("'","");
        div.className = className;
        div.id = idName;
        div.onclick = function() {copy(text)};


        document.getElementById(parent).appendChild(div);
    }
    ipt>
    function HomeAnyways() {
        window.location.href = "/rewrite/"
    }

    function copy(text) {
        Clipboard.write(text)
    }

    function home() {
        (async () => {
        const response = await fetch('/rewrite/settings?' + new URLSearchParams({
        t : document.getElementById('temperature').value,
        mt : document.getElementById('max_tokens').value,
        fp : document.getElementById('frequency_penalty').value,
        pp : document.getElementById('presence_penalty').value
    }))

    const data = await response.json()

    console.log(data)
    
})()
    }