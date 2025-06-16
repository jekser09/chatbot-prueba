function detectar_pantalla(){
    if(screen.width<750){
        document.getElementById("img-login").attributes['src'].value="/static/IMG/productos_pacos3.png"
    }else if(screen.width>=750){
        document.getElementById("img-login").attributes['src'].value="/static/IMG/productos_pacos2.png"
    }
}

function conexion_db(){
    let led=document.querySelector(".led-bd")
    try{
        fetch("/probar_db/").then(Response=>Response.json()).then(
            data=>{
                if(data.estado){
                    led.style.backgroundColor="green"
                    led.title=data.msg  
                }
                else{
                    led.style.backgroundColor="orange"
                    led.title=data.msg
                }
            }
        ).catch(error=>{
            led.style.backgroundColor="orange"
            led.title="Error: "+error
        })
    }catch(error){
        led.style.backgroundColor="red"
        led.title="Error: "+error
    }
}

function ocultar_error(){
    let errores=document.querySelector(".errors")
    let input_user=document.getElementById("id_usuario")
    let input_pass=document.getElementById("id_clave")
    if(errores != null){
        if(input_user.value!=="" || input_pass.value!==""){
            errores.style.display="none"
        }else{
            errores.style=""
        }
        
    }
}

//CARGA DE EVENTOS
window.addEventListener("orientationchange",detectar_pantalla)

//
document.getElementById("id_usuario").addEventListener("change",ocultar_error)
document.getElementById("id_clave").addEventListener("change",ocultar_error)

// Acciones iniciales de la pagina
detectar_pantalla()
conexion_db()
