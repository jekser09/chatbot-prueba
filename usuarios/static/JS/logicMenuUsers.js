const menuToggle = document.querySelector('.menu-toggle')
const navMenu = document.querySelector('.navMenu')
const menuItems = document.querySelectorAll('.navMenu .contenedorEnlaces a')// Selector más específico.

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('abierto')
        menuToggle.classList.toggle('abierto') // Para animar el botón de hamburguesa
    })
}

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        navMenu.classList.remove('abierto')
        if (menuToggle.classList.contains('abierto')) {
            menuToggle.classList.remove('abierto') // Para revertir la animación del botón
        }
    });
});

function ajustarLayout() {
    if (window.innerWidth > 600) {
        navMenu.classList.remove('abierto')
        if (menuToggle && menuToggle.classList.contains('abierto')) {
            menuToggle.classList.remove('abierto') // Opcional: asegurar estado del botón
        }
    }
}

window.addEventListener('resize', ajustarLayout);

// Asegurar que el menú esté cerrado al cargar la página en dispositivos móviles
if (window.innerWidth <= 600) {
    navMenu.classList.remove('abierto')
    if (menuToggle && menuToggle.classList.contains('abierto')) {
        menuToggle.classList.remove('abierto')
    }
}

// Escucha el evento 'scroll' en toda la ventana
window.addEventListener('scroll', () => {
    // Comprueba si el menú está actualmente abierto (tiene la clase 'abierto')
    // y si el botón toggle existe (buena práctica)
    if (navMenu.classList.contains('abierto') && menuToggle) {
        
        // Si está abierto, quita la clase 'abierto' para cerrarlo
        navMenu.classList.remove('abierto')
        
        // También quita la clase 'abierto' del botón para resetear su estilo
        menuToggle.classList.remove('abierto')
    }
})

/* 
// --- INICIO CÓDIGO SCROLL INFINITO ---

// Variable para almacenar el HTML original del carrusel y su estado inicial
let originalScrollerHTML = '';
let originalItemsCount = 0;
let scrollerInstance = null; // Para guardar la referencia al elemento del carrusel
let scrollHandlerRef = null; // Para guardar la referencia del manejador de scroll

//Función debounce para optimizar la ejecución de eventos como resize.
//Limita la frecuencia con la que se ejecuta una función.
function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        var callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
}

//Inicializa o reinicializa la funcionalidad de scroll infinito.
function initInfiniteScroll() {
    scrollerInstance = document.querySelector('.contenedorEnlaces');
    if (!scrollerInstance) {
        console.warn('Contenedor .contenedorEnlaces no encontrado para scroll infinito.');
        return;
    }

    // Si ya hay un manejador de scroll, lo removemos antes de re-evaluar.
    if (scrollHandlerRef) {
        scrollerInstance.removeEventListener('scroll', scrollHandlerRef);
        scrollHandlerRef = null;
    }

    // Guardar el estado original la primera vez o restaurarlo
    if (!originalScrollerHTML) {
        originalScrollerHTML = scrollerInstance.innerHTML;
        originalItemsCount = scrollerInstance.children.length;
    } else {
        scrollerInstance.innerHTML = originalScrollerHTML; // Restaurar al original para recalcular
    }

    if (originalItemsCount === 0) {
        scrollerInstance.dataset.isInfinite = "false";
        return; // No hay items para hacer scroll
    }

    const items = Array.from(scrollerInstance.children); // Items originales

    // Calcular el ancho total del contenido original (items + márgenes)
    let currentOriginalContentWidth = 0;
    items.forEach(item => {
        const style = window.getComputedStyle(item);
        const marginLeft = parseFloat(style.marginLeft) || 0;
        const marginRight = parseFloat(style.marginRight) || 0;
        currentOriginalContentWidth += item.offsetWidth + marginLeft + marginRight;
    });

    // Si el contenido original no desborda el contenedor, no se necesita scroll infinito.
    if (currentOriginalContentWidth <= scrollerInstance.clientWidth) {
        scrollerInstance.dataset.isInfinite = "false";
        // console.log('Scroll infinito no necesario: el contenido no desborda.');
        return;
    }

    // Clonar los items originales y añadirlos al final
    items.forEach(item => {
        const clone = item.cloneNode(true);
        // Puedes añadir una clase a los clones si necesitas distinguirlos para depuración
        // clone.classList.add('cloned-item');
        scrollerInstance.appendChild(clone);
    });

    // Guardar el ancho original para usarlo en el manejador de scroll
    scrollerInstance.dataset.originalWidth = currentOriginalContentWidth;

    // Definir el manejador de scroll
    scrollHandlerRef = function() {
        const oWidth = parseFloat(this.dataset.originalWidth);
        // Si por alguna razón el ancho original es 0 o no es un número, o no es infinito, salir.
        if (!oWidth || this.dataset.isInfinite === "false") return;

        const scrollLeft = this.scrollLeft;

        // Si el scroll supera o iguala el ancho del contenido original (entramos en los clones)
        if (scrollLeft >= oWidth) {
            // "Teletransportar" el scroll restando el ancho del contenido original
            this.scrollLeft -= oWidth;
        }
        // Para un scroll infinito hacia la izquierda (más complejo, requiere prependar clones):
        // else if (scrollLeft <= 0) {
        //     // Esta condición se activaría si tuviéramos clones *antes* del contenido original
        //     // y el scroll llegara al inicio de la sección "original".
        //     // Habría que sumar oWidth para saltar al final de la sección original.
        //     // this.scrollLeft += oWidth; // Ejemplo conceptual para scroll izquierdo
        // }
    };

    scrollerInstance.addEventListener('scroll', scrollHandlerRef);
    scrollerInstance.dataset.isInfinite = "true";
    // console.log('Scroll infinito activado. Ancho original:', currentOriginalContentWidth);
}

// Asegurarse de que el DOM esté completamente cargado y los estilos aplicados
// para un cálculo correcto de anchos.
document.addEventListener('DOMContentLoaded', function() {
    // Un pequeño retraso puede ayudar a asegurar que todo esté renderizado,
    // especialmente si los items se cargan dinámicamente o los estilos tardan.
    setTimeout(initInfiniteScroll, 100);
});

// Re-inicializar en caso de cambio de tamaño de la ventana (con debounce)
window.addEventListener('resize', debounce(function() {
    // console.log('Ventana redimensionada, re-inicializando scroll infinito...');
    // Antes de re-inicializar, es buena idea limpiar el estado de isInfinite
    // si el scrollerInstance existe, para que no tome una decisión basada en data antigua.
    if (scrollerInstance) {
      scrollerInstance.dataset.isInfinite = "false"; // Forzar re-evaluación
    }
    initInfiniteScroll();
}, 250));

 */