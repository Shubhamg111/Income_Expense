const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordfield =  document.querySelector('#passwordfield')

const handleToggleInput=(e)=>{

    if(showPasswordToggle.textContent ==='SHOW'){
        showPasswordToggle.textContent = 'HIDE'
        passwordfield.setAttribute("type","text")
    }
    else{
        showPasswordToggle.textContent = 'SHOW'
        passwordfield.setAttribute('type','password')

    }

}

showPasswordToggle.addEventListener('click',handleToggleInput)

