function hidePhoto(){
    var x = document.getElementById("fperfil")
    //if (x.style.display === "none") {
    //x.style.display = "block";
  //} else {
    x.style.visibility= "hidden"
  //}
}
function showPhoto() {
    var x = document.getElementById("fperfil")
    if (x.style.visibility === "hidden") {
        x.style.visibility = "visible";
    }
}

function lista(){
    var x = document.getElementById("lista")
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {
        x.style.display = "none";
    }
}