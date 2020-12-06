var updateBtns = document.getElementsByClassName('update-cart')
for (i = 0;i <updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
        var productid = this.dataset.products
        var action = this.dataset.action
        console.log('productid:',productid,'Action:',action)



        console.log('User:',user)
        if (user == 'AnonymousUser'){
            console.log('user not loggin in ')
        }else{
            updateuserorder(productid,action)
        }
    })


function updateuserorder(productid, action){
    console.log('user is loginn')
    var url = '/updatecart/'
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

