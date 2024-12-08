const usernameField = document.querySelector('#usernameField')
const feedbackField = document.querySelector('.invalid-feedback')
const emailField = document.querySelector("#emailField")
const emailfeedbackField = document.querySelector('.invalid-emailfeedback')
const unameSuccessOutput = document.querySelector('.usernameSuccessOutput')
const emailSuccessOutput = document.querySelector('.emailSuccessOutput')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordfield =  document.querySelector('#passwordfield')
const submitBtn = document.querySelector('.submit-btn')

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



emailField.addEventListener('keyup',(e)=>{
    const emailVal = e.target.value
    emailSuccessOutput.style.display="block"
    emailSuccessOutput.textContent = `Cheking ${emailVal}`


emailField.classList.remove("is-invalid")
emailfeedbackField.style.display = 'none'



if (emailVal.length > 0) {
    fetch('/authentication/validate-email',{

    body: JSON.stringify({email:emailVal}),
    method: 'POST',
    })
    .then((res)=> res.json())
    .then((data)=> {
        console.log("data",data)
    emailSuccessOutput.style.display="none"

        if(data.email_error){
            submitBtn.setAttribute("disabled",'disabled')
            submitBtn.disabled = true
            emailField.classList.add("is-invalid")
            emailfeedbackField.style.display = 'block'
            emailfeedbackField.innerHTML =`<p>${data.email_error}</p>`
        }
        else{
            submitBtn.removeAttribute("disabled")
        }
    })
}

})


usernameField.addEventListener('keyup',(e)=>{
const usernameVal = e.target.value

unameSuccessOutput.style.display = 'block'

unameSuccessOutput.textContent = `Cheking ${usernameVal}`

usernameField.classList.remove("is-invalid")
feedbackField.style.display = 'none'



if (usernameVal.length > 0) {
    fetch('/authentication/validate-username',{

    body: JSON.stringify({username:usernameVal}),
    method: 'POST',
    })
    .then((res)=> res.json())
    .then((data)=> {
        console.log("data",data)
        unameSuccessOutput.style.display = 'none'
        if(data.username_error){
            usernameField.classList.add("is-invalid")
            feedbackField.style.display = 'block'
            feedbackField.innerHTML =`<p>${data.username_error}</p>`
            submitBtn.disabled = true

        }
        else{
            submitBtn.removeAttribute("disabled")
        }
    })
}
})