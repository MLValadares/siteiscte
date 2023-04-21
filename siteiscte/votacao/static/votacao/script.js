function hidePhoto(){
    var x = document.getElementById("fperfil")
    //if (x.style.display === "none") {
    //x.style.display = "block";
  //} else {
    x.style.display= "none"
  //}
}
function showPhoto() {
    var x = document.getElementById("fperfil")
    if (x.style.display === "none") {
        x.style.display = "initial";
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
$("botao_validar").click(function(){
    alert("fqf")
    // var texto = $('#comentario').val();
    // var palavras = texto.split(" ");
    // arrayInsultos = ["abécula", "abentesma", "achavascado", "alimária", "andrajoso", "barregã", "biltre", "cacóstomo", "cuarra", "estólido", "estroso", "estultilóquio", "nefelibata", "néscio", "pechenga", "sevandija", "somítico", "tatibitate", "xexé", "cheché", "xexelento"]
    // var existeInsulto = new Boolean(false);
    // var insulto = 'nenhum';
    // for (var i = 0; i < palavras.length; i++) {
    //     palavramin = palavras[i].toLowerCase();
    //     for (var z = 0; z < arrayInsultos.length; z++) {
    //         if (palavramin === arrayInsultos[z]) {
    //             existeInsulto = new Boolean(true);
    //             insulto = palavramin;
    //             break;
    //         }
    //     }
    // }
    // if (existeInsulto == true){
    //     //alert(insulto);
    //     $('#comentario').val("Por favor insira um comentário sem insultos.");
    // } else {
    //     $('#alerta_comentario').text('Validado');
    // }
});