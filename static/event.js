keybutton = document.getElementById("keybutton")        
coverbutton = document.getElementById("coverbutton")
keydiv = document.getElementById("key")
convertdiv = document.getElementById("convertter")

//keybutton.addEventListener("click",keyfind)
//keydiv.style.display='none'

coverbutton.style.opacity="0.5"
convertdiv.style.display='none'


function keyfind() {
     coverbutton.style.opacity = "0.5"
     keydiv.style.display = ""
     keybutton.style.opacity='1'
     convertdiv.style.display='none'
}

function convertfind() {
    convertdiv.style.display = '' 
    keydiv.style.display = 'none'
    coverbutton.style.opacity='1'
    keybutton.style.opacity='0.5'
}
