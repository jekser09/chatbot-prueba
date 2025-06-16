let botui = new BotUI('botui-app')
const chat_modal=document.getElementById("chat-modal")
/* const btn_iniciar=document.getElementById("btn-abrir")
const btn_precision=document.getElementById('btn-precision') */
const ventana_chat=document.getElementById('botui-app')

async function chatear(texto){
    try{
        let respuestaBot=await fetch(`/conversacion/${texto}`)
        if(!respuestaBot.ok) return 'Respuesta negativa del servidor'
        let respuesta=await respuestaBot.json()
        if(respuesta.estado){
            return respuesta.respuesta
        }else{
            return respuesta.error
        }
    }catch(error){
        return 'Ocurrio un error: '+error
    }
}

async function iniciarChat() {
    await botui.message.add({
        content: ventana_chat.dataset.msg
    })
    await preguntar()
}

async function preguntar() {
    let response = await botui.action.text({
        action:{
            placeholder:'Escribe algo...'
        }
    })
    let mubot=await chatear(response.value)
    response = await botui.message.add({
        type: 'html',
        content: mubot
    })
    preguntar()
}

async function precision() {
    try{
        let respuestaBot=await fetch(`/estadistica/`)
        if(!respuestaBot.ok) return 'Respuesta negativa del servidor'
        let respuesta=await respuestaBot.json()
        if(respuesta.estado){
            return respuesta.respuesta
        }else{
            return respuesta.error
        }
    }catch(error){
        return 'Ocurrio un error: '+error
    }   
}

/* btn_iniciar.addEventListener("click",()=>{
    ventana_chat.hidden=false
    iniciarChat()
})

btn_precision.addEventListener("click",async ()=>{
    console.log(await precision())
}) */

iniciarChat()
