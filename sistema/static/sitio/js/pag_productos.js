var carritoVisible = false;

// Esta parte lo que dice es que estudien malparidos:V, mentiris
// Esta parte die que tienen que esperar que carguen todos los elementos para ejecutar el carrito
if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready);
} else {
    ready();
}

function ready() {
    
    // Aca esta el boton de eliminar un producto al darle clic al icono okeyyyyyy
    var botonesEliminarItem = document.getElementsByClassName('btn-eliminar');
    for (var i = 0; i < botonesEliminarItem.length; i++) {
        var button = botonesEliminarItem[i];
        button.addEventListener('click', eliminarItemCarrito);
    }

    // Sumar unidades, boton suma
    var botonesSumarCantidad = document.getElementsByClassName('sumar-cantidad');
    for (var i = 0; i < botonesSumarCantidad.length; i++) {
        var button = botonesSumarCantidad[i];
        button.addEventListener('click', sumarCantidad);
    }

    // Quitar unidades, boton resta
    var botonesRestarCantidad = document.getElementsByClassName('restar-cantidad');
    for (var i = 0; i < botonesRestarCantidad.length; i++) {
        var button = botonesRestarCantidad[i];
        button.addEventListener('click', restarCantidad);
    }

    // Esta parte es la que hace que al darle en agregar al carrito pues se agregue:V
    var botonesAgregarAlCarrito = document.getElementsByClassName('btn-agregar');
    for (var i = 0; i < botonesAgregarAlCarrito.length; i++) {
        var button = botonesAgregarAlCarrito[i];
        button.addEventListener('click', agregarAlCarritoClicked);
    }
}

// Despues de darle en finalizar o pagar, esta parte hace que se oculte la ventana emergente que salia del carrito bro's
function pagarClicked() {
    var carritoproductos = document.getElementsByClassName('carrito-productos')[0];
    while (carritoproductos.hasChildNodes()) {
        carritoproductos.removeChild(carritoproductos.firstChild);
    }
    actualizarTotalCarrito();
    ocultarCarrito();
}

function agregarAlCarritoClicked(event) {
    var button = event.target;
    var item = button.parentElement;
    var titulo = item.getElementsByClassName('card-title')[0].innerText;
    var precio = item.getElementsByClassName('card-text')[3].innerText;
    var imagenSrc = item.getElementsByTagName('img')[0].src;
    console.log(imagenSrc);

    agregarItemAlCarrito(titulo, precio, imagenSrc);

    hacerVisibleCarrito();
}

// Esta parte es cuando le de en agregar al carrito, que se muestre la ventana
function hacerVisibleCarrito() {
    carritoVisible = true;
    var carrito = document.getElementsByClassName('carrito')[0];
    carrito.style.marginRight = '0';
    carrito.style.opacity = '1';

    var productos = document.getElementsByClassName('container')[0];
    productos.style.width = '60%';
}

// Agrega productos al carro desde el boton
function agregarItemAlCarrito(titulo, precio, imagenSrc) {
    var item = document.createElement('div');
    item.classList.add('item');
    var productosCarrito = document.getElementsByClassName('carrito-productos')[0];

    // Esta no permite que se agregue el mismo producto en filas distintas, y bota una alerta de que ya esta
    var nombresproductosCarrito = productosCarrito.getElementsByClassName('carrito-item-titulo');
    for (var i = 0; i < nombresproductosCarrito.length; i++) {
        if (nombresproductosCarrito[i].innerText == titulo) {
            alert("Este producto ya se encuentra en el carrito, si quiere mas sume las unidades");
            return;
        }
    }

    var itemCarritoContenido = `
        <div class="carrito-item">
            <img src="${imagenSrc}" width="80px" alt="">
            <div class="carrito-item-detalles">
                <span class="carrito-item-titulo">${titulo}</span>
                <div class="selector-cantidad">
                    <i class="fa-solid fa-minus restar-cantidad"></i>
                    <input type="text" value="1" class="carrito-item-cantidad" disabled>
                    <i class="fa-solid fa-plus sumar-cantidad"></i>
                </div>
                <span class="carrito-item-precio">${precio}</span>
            </div>
            <button class="btn-eliminar">
                <i class="fa-solid fa-trash"></i>
            </button>
        </div>
    `;
    item.innerHTML = itemCarritoContenido;
    productosCarrito.append(item);

    // Esto es lo de eliminar otra vez
    item.getElementsByClassName('btn-eliminar')[0].addEventListener('click', eliminarItemCarrito);

    // Resta unidades de producto
    var botonRestarCantidad = item.getElementsByClassName('restar-cantidad')[0];
    botonRestarCantidad.addEventListener('click', restarCantidad);

    // Esto suma cada que vaya poniendo un producto
    var botonSumarCantidad = item.getElementsByClassName('sumar-cantidad')[0];
    botonSumarCantidad.addEventListener('click', sumarCantidad);

    // Actualiza
    actualizarTotalCarrito();
}

// Esto es que sea auto incrementable, o sea que sume de 1 en 1 de las unidades
function sumarCantidad(event) {
    var buttonClicked = event.target;
    var selector = buttonClicked.parentElement;
    console.log(selector.getElementsByClassName('carrito-item-cantidad')[0].value);
    var cantidadActual = selector.getElementsByClassName('carrito-item-cantidad')[0].value;
    cantidadActual++;
    selector.getElementsByClassName('carrito-item-cantidad')[0].value = cantidadActual;
    actualizarTotalCarrito();
}

// Lo de arriba pero quitanto unidades
function restarCantidad(event) {
    var buttonClicked = event.target;
    var selector = buttonClicked.parentElement;
    console.log(selector.getElementsByClassName('carrito-item-cantidad')[0].value);
    var cantidadActual = selector.getElementsByClassName('carrito-item-cantidad')[0].value;
    cantidadActual--;
    if (cantidadActual >= 1) {
        selector.getElementsByClassName('carrito-item-cantidad')[0].value = cantidadActual;
        actualizarTotalCarrito();
    }
}

// Elimina item completo
function eliminarItemCarrito(event) {
    var buttonClicked = event.target;
    buttonClicked.parentElement.parentElement.remove();
    actualizarTotalCarrito();
    ocultarCarrito();
}

// Esto dice que si no hay elemntos dentro del carrito, se oculte es un tipo de verificacion, no se como decirlo
function ocultarCarrito() {
    var carritoproductos = document.getElementsByClassName('carrito-productos')[0];
    if (carritoproductos.childElementCount == 0) {
        var carrito = document.getElementsByClassName('carrito')[0];
        carrito.style.marginRight = '-100%';
        carrito.style.opacity = '0';
        carritoVisible = false;

        var productos = document.getElementsByClassName('container')[0];
        productos.style.width = '100%';
    }
}

function actualizarTotalCarrito() {
    var carritoContenedor = document.getElementsByClassName('carrito')[0];
    var carritoproductos = carritoContenedor.getElementsByClassName('carrito-item');
    var total = 0;
    // Esto es lo que enseño ese profesor de algoritmos, que recorra todo el arreglo para verificar
    for (var i = 0; i < carritoproductos.length; i++) {
        var item = carritoproductos[i];
        var precioElemento = item.getElementsByClassName('carrito-item-precio')[0];
        // Quita los signos que estan entre parentesis
        var precio = parseFloat(precioElemento.innerText.replace('$', '').replace('.', ''));
        var cantidadItem = item.getElementsByClassName('carrito-item-cantidad')[0];
        console.log(precio);
        var cantidad = cantidadItem.value;
        total = total + (precio * cantidad);
    }
    total = Math.round(total * 100) / 100;

    document.getElementsByClassName('carrito-precio-total')[0].innerText = '$' + total.toLocaleString("es") + ",00";

}
