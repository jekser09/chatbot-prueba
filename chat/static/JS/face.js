let chat_modal=document.getElementById("chat-modal")
let boton_chat=document.getElementById("btn-chat")
let boton_chat_cerrar=document.getElementById("btn-cerrar-chat")

boton_chat.addEventListener("click",()=>{
    chat_modal.showModal()
})

boton_chat_cerrar.addEventListener("click",()=>{
    chat_modal.close()
})