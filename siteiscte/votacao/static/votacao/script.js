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

//Note to self: Ainda não percebi como isto funcionou
//Fiz pip do seguinto pacote: https://pypi.org/project/django-jquery/
//E adicionei 'jquery' no INSTALLED_APPS no settings.py, não estava a conseguir via import "{{ STATIC_URL }}js/jquery.js"
//Como aparece no link a cima
//No entanto, voltei a exprimentar com "https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js" e funcionou
//
$("#btt1").click(function(){
    var texto = $('#comentario').val();
    var palavras = texto.split(" ");
    arrayInsultos = ["abécula", "abentesma", "achavascado", "alimária", "andrajoso", "barregã", "biltre", "cacóstomo", "cuarra", "estólido", "estroso", "estultilóquio", "nefelibata", "néscio", "pechenga", "sevandija", "somítico", "tatibitate", "xexé", "cheché", "xexelento"]
    var existeInsulto = new Boolean(false);
    var insulto = 'nenhum';
    for (var i = 0; i < palavras.length; i++) {
        palavramin = palavras[i].toLowerCase();
        for (var z = 0; z < arrayInsultos.length; z++) {
            if (palavramin === arrayInsultos[z]) {
                existeInsulto = new Boolean(true);
                insulto = palavramin;
                break;
            }
        }
    }
    if (existeInsulto == true){
        $('#comentario').val("Por favor insira um comentário sem insultos.");
    } else {
        $('#alerta_comentario').text('Validado');
    }
});