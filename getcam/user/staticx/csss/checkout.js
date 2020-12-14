console.log('attach')
var form = document.getElementById('formmms')


form.addEventListener('submit', function (e) {
e.preventDefault()

document.getElementById('formmmsbtn').style.visibility = "hidden";
document.getElementById("payment11").style.visibility = "unset";

});

var url = '/processorder/'
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productsid':productid,'action':action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data:',data)
        location.reload()
    })
 
}} 