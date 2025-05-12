const chat_modal=document.getElementById("chat-modal")
const btn_abrir_modal=document.getElementById("btn-abrir")

function chatear(texto){
    let p_respuesta=chat_modal.querySelector('#id-respuesta')
    fetch(`/conversacion/${texto}`).then(respose=>respose.json()).then(
        respuesta=>{
            if (respuesta.estado){
                p_respuesta.textContent=respuesta.respuesta
            }else{
                p_respuesta.textContent=respuesta.error
            }
        }
    ).catch(error=>{console.error("Error al realizar fetch: "+error)})
}

btn_abrir_modal.addEventListener("click",()=>{
    chat_modal.showModal()
})

chat_modal.addEventListener("click",e=>{
    let elemento=e.target
    if(elemento.classList.contains('btn-cerrar')){
        chat_modal.close()
    }else if(elemento.classList.contains('btn-chatear')){
        let texto=chat_modal.querySelector("#input-texto").value
        console.log(texto)
        if(texto!=='') chatear(texto)
    }
})


