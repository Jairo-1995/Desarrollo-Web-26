(() => {
    const enlacesMenu = [
        { texto: "Inicio", href: "#inicio" },
        { texto: "Quiénes Somos", href: "#quienes-somos" },
        { texto: "Productos", href: "#servicios" },
        { texto: "Oferta", href: "#producto-dinamico" },
        { texto: "Registro", href: "#registro-producto" },
        { texto: "Contacto", href: "#contacto" }
    ];

    const productos = {
        artesania: {
            nombre: "Collares y Aretes Artesanales",
            descripcion: "Cestas, tejidos y artículos decorativos elaborados a mano por artesanos de la Amazonía, ideales para dar un toque cultural a tu hogar.",
            precio: "$7.00",
            imagen: "/static/img/aretes.jpg",
            alt: "Artesanías amazonicas"
        },
        miel: {
            nombre: "Miel Orgánica",
            descripcion: "Miel pura recolectada en la Amazonía, ideal para endulzar tus bebidas y disfrutar de un producto natural y aromático.",
            precio: "$4.50",
            imagen: "/static/img/miel.jpg",
            alt: "Miel orgánica amazónica"
        },
        aceite: {
            nombre: "Aceite de Coco",
            descripcion: "Aceite de coco virgen prensado en frío, perfecto para cocina, cuidado personal y una alternativa natural en tu día a día.",
            precio: "$3.50",
            imagen: "/static/img/coco.jpg",
            alt: "Aceite de coco amazónico"
        },
        chocolate: {
            nombre: "Chocolate Artesanal",
            descripcion: "Chocolate elaborado con cacao amazónico de alta calidad, un sabor auténtico y una delicia para los amantes de lo natural.",
            precio: "$3.50",
            imagen: "/static/img/chocolate.jpg",
            alt: "Chocolate artesanal amazónico"
        }
    };

    const productosOferta = [
        { clave: "artesania", texto: "Artesanías" },
        { clave: "miel", texto: "Miel Orgánica" },
        { clave: "aceite", texto: "Aceite de Coco" },
        { clave: "chocolate", texto: "Chocolate Artesanal" }
    ];

    const galeriaInicioItems = [
        {
            titulo: "Cosecha local",
            descripcion: "Productos frescos y tradicionales de la Amazonía ecuatoriana.",
            imagen: "/static/img/fruta.jpeg",
            alt: "Caña amazónica"
        },
        {
            titulo: "Artesanías auténticas",
            descripcion: "Diseños elaborados a mano que conservan la identidad cultural.",
            imagen: "/static/img/artesania.jpg",
            alt: "Artesanías amazónicas"
        },
        {
            titulo: "Productos naturales",
            descripcion: "Ingredientes y alimentos provenientes de la selva amazónica, cultivados de manera sostenible.",
            imagen: "/static/img/producto.jpeg",
            alt: "Chocolate artesanal"
            
            
        
        }
    ];

    const productosDisponibles = [
        {
            nombre: "Caña",
            descripcion: "Caña de la región amazónica, ideal para preparar bebidas tradicionales y dulces.",
            precio: "$1.00",
            imagen: "/static/img/caña.jpg",
            alt: "Caña"
        },
        {
            nombre: "Morete",
            descripcion: "Morete amazónico, un producto tradicional con múltiples usos culinarios y medicinales.",
            precio: "$3.00 por kilogramo",
            imagen: "/static/img/morete.jpg",
            alt: "Morete"
        },
        {
            nombre: "Ungurahua",
            descripcion: "Ungurahua amazónica, utilizada en la medicina tradicional para diversos fines terapéuticos.",
            precio: "$3,50 por kilogramo",
            imagen: "/static/img/ungurahua.jpg",
            alt: "Ungurahua"
        },
        {
            nombre: "Miel Amazónica",
            descripcion: "Miel pura y orgánica recolectada de colmenas silvestres.",
            precio: "$5.00 por frasco",
            imagen: "/static/img/miel.jpg",
            alt: "Miel Amazónica"
        },
        {
            nombre: "Yuca Fresca",
            descripcion: "Tubérculo amazónico nutritivo y versátil para tus comidas.",
            precio: "$5.00 por kg",
            imagen: "/static/img/yuca.jpg",
            alt: "Yuca Fresca"
        },
        {
            nombre: "Plátanos Amazónicos",
            descripcion: "Plátanos frescos y naturales de nuestros campos.",
            precio: "$6.00 por cabezas",
            imagen: "/static/img/platanos.jpg",
            alt: "Plátanos Amazónicos"
        },
        {
            nombre: "Maní Tostado",
            descripcion: "Maní 100% natural tostado al fuego tradicional.",
            precio: "$10.00 por kg",
            imagen: "/static/img/mani.jpg",
            alt: "Maní Tostado"
        },
        {
            nombre: "Aceite de Coco",
            descripcion: "Aceite de coco virgen prensado en frío, puro y natural.",
            precio: "$4.00 por litro",
            imagen: "/static/img/coco.jpg",
            alt: "Aceite de Coco"
        },
        {
            nombre: "Chocolate Artesanal",
            descripcion: "Chocolate elaborado con cacao amazónico de alta calidad.",
            precio: "$2.00 por barra",
            imagen: "/static/img/chocolate.jpg",
            alt: "Chocolate Artesanal"
        },
        {
            nombre: "Papaya",
            descripcion: "Fruta tropical de sabor delicioso y alta en vitaminas.",
            precio: "$1.00 por unidad",
            imagen: "/static/img/papaya.jpg",
            alt: "Papaya"
        },
        {
            nombre: "Choclo",
            descripcion: "Maíz fresco de la región amazónica, ideal para preparar platos tradicionales.",
            precio: "$3.00 por kg",
            imagen: "/static/img/choclo.jpg",
            alt: "Choclo"
        },
        {
            nombre: "Hoja de Guayusa",
            descripcion: "Infusión tradicional amazónica con propiedades energizantes y antioxidantes.",
            precio: "$4.00 por kilogramo",
            imagen: "/static/img/guayusa.jpg",
            alt: "Hoja de Guayusa"
        },
        {
            nombre: "Naranjilla",
            descripcion: "Fruta exótica de sabor agridulce y alto contenido de vitamina C. Perfecta para jugos y postres.",
            precio: "$8.00 por caja",
            imagen: "/static/img/naranjilla.jpg",
            alt: "Naranjilla"
        },
        {
            nombre: "Uvas Amazónicas",
            descripcion: "Uvas de la región amazónica, ideales para consumo directo o en la preparación de jugos y postres.",
            precio: "$6.50",
            imagen: "/static/img/uva.jpg",
            alt: "Uvas Amazónicas",
        },
        {
            nombre: "Chonta Amazónica",
            descripcion: "Chonta amazónica fresca, un fruto tradicional con múltiples usos culinarios y medicinales.",
            precio: "$4.00 por 500g",
            imagen: "/static/img/chonta.jpg",
            alt: "Chonta Amazónica",
        }
    ];

    const categoriasProyecto = ["Artesanías", "Frutas", "Productos naturales"];

    const contenedorProductos = document.getElementById("productos-lista");
    const galeriaInicio = document.getElementById("galeria-inicio");
    const resumenDinamico = document.getElementById("resumen-dinamico");
    const estadoDatos = document.getElementById("estado-datos");
    const tablaProductos = document.getElementById("tabla-productos");
    const botonesProductoOferta = document.getElementById("botones-productos-oferta");
    let botonesProducto = [];
    const productoNombre = document.getElementById("producto-nombre");
    const productoDescripcion = document.getElementById("producto-descripcion");
    const productoPrecio = document.getElementById("producto-precio");
    const productoImagen = document.getElementById("producto-imagen");
    const ofertaComprarAhora = document.getElementById("oferta-comprar-ahora");

    const modalConfirmacion = document.getElementById("confirmacionModal");
    const modalConfirmacionCuerpo = document.getElementById("confirmacionModalBody");
    const btnConfirmarAccion = document.getElementById("btn-confirmar-accion");
    let bsModal;

    const detalleProductoModal = document.getElementById("detalleProductoModal");
    let bsDetalleModal;
    const detalleProductoNombre = document.getElementById("detalleProductoNombre");
    const detalleProductoDescripcion = document.getElementById("detalleProductoDescripcion");
    const detalleProductoPrecio = document.getElementById("detalleProductoPrecio");
    const detalleProductoImagen = document.getElementById("detalleProductoImagen");
    const detalleProductoSpinner = document.getElementById("detalleProductoSpinner");
    const detalleProductoContenido = document.getElementById("detalleProductoContenido");

    const checkoutModal = document.getElementById("checkoutModal");
    let bsCheckoutModal;
    const checkoutForm = document.getElementById("checkoutForm");
    const checkoutProductName = document.getElementById("checkoutProductName");
    const checkoutProductPrice = document.getElementById("checkoutProductPrice");
    const checkoutProductImage = document.getElementById("checkoutProductImage");
    const checkoutName = document.getElementById("checkoutName");
    const checkoutAddress = document.getElementById("checkoutAddress");

    const formularioProducto = document.getElementById("formulario-producto");
    const mensajeProducto = document.getElementById("mensaje-producto");
    const campoNombre = document.getElementById("nombre-producto");
    const campoDescripcion = document.getElementById("descripcion-producto");
    const campoCategoria = document.getElementById("categoria-producto");
    const errorNombre = document.getElementById("error-nombre");
    const errorDescripcion = document.getElementById("error-descripcion");
    const errorCategoria = document.getElementById("error-categoria");
    const exitoNombre = document.getElementById("exito-nombre");
    const exitoDescripcion = document.getElementById("exito-descripcion");
    const exitoCategoria = document.getElementById("exito-categoria");
    const listaProductos = document.getElementById("lista-productos");
    const totalRegistros = document.getElementById("total-registros");
    const contadorDescripcion = document.getElementById("contador-descripcion");
    const botonRegistrar = document.getElementById("boton-registrar");

    const formularioContacto = document.getElementById("formulario-contacto");
    const contactoNombre = document.getElementById("contact-nombre");
    const contactoEmail = document.getElementById("contact-email");
    const contactoAsunto = document.getElementById("contact-asunto");
    const contactoMensaje = document.getElementById("contact-mensaje");

    const LONGITUD_MINIMA_NOMBRE = 3;
    const LONGITUD_MINIMA_DESCRIPCION = 15;
    const PALABRAS_MINIMAS_DESCRIPCION = 4;
    let contadorRegistros = 0;

    function plantillaMenu() {
        return enlacesMenu
            .map((enlace) => `
                        <li class="nav-item">
                            <a class="nav-link" href="${enlace.href}">${enlace.texto}</a>
                        </li>`)
            .join("");
    }

    function plantillaPiePagina() {
        return `
    <footer class="bg-dark text-white text-center p-3">
        <p>&copy; 2026 Productos Amazónicos</p>
        <p>Realizado por: Jairo Eliecer Mamallacta Andy</p>
        <p>Desarrollo de Aplicaciones Web</p>
    </footer>`;
    }

    function cargarPlantillasBase() {
        const menuPrincipal = document.getElementById("menu-principal");
        const piePagina = document.getElementById("app-footer");

        if (menuPrincipal) menuPrincipal.innerHTML = plantillaMenu();
        if (piePagina) piePagina.innerHTML = plantillaPiePagina();
    }

    function actualizarBotonesProducto(botonActivo) {
        botonesProducto.forEach((boton) => {
            boton.classList.remove("activo", "btn-success");
            boton.classList.add("btn-outline-success");
        });

        botonActivo.classList.add("activo", "btn-success");
        botonActivo.classList.remove("btn-outline-success");
    }

    function generarEnlaceWhatsApp(nombreProducto) {
        const numeroTelefono = "593991842412"; // Reemplaza con tu número de WhatsApp en formato internacional
        const mensaje = `¡Hola! Estoy interesado/a en comprar el producto: ${nombreProducto}. ¿Podrían darme más información?`;
        const urlMensaje = encodeURIComponent(mensaje);
        return `https://wa.me/${numeroTelefono}?text=${urlMensaje}`;
    }

    function mostrarProductoRecomendado(producto) {
        productoNombre.textContent = producto.nombre;
        productoDescripcion.textContent = producto.descripcion;
        productoPrecio.textContent = producto.precio;
        productoImagen.src = producto.imagen;
        productoImagen.alt = producto.alt;
        if (ofertaComprarAhora) ofertaComprarAhora.onclick = () => abrirModalCheckout(producto);
    }

    function manejarSeleccionProducto(evento) {
        const botonSeleccionado = evento.currentTarget;
        const productoSeleccionado = productos[botonSeleccionado.dataset.producto];

        mostrarProductoRecomendado(productoSeleccionado);
        actualizarBotonesProducto(botonSeleccionado);
    }

    function mostrarMensaje(texto, tipo) {
        mensajeProducto.textContent = texto;
        mensajeProducto.className = `alert ${tipo} mt-4`;
        mensajeProducto.classList.remove("d-none");

        if (tipo.includes("success")) {
            setTimeout(() => mensajeProducto.classList.add("d-none"), 4000);
        }
    }

    function crearElemento(etiqueta, clases, texto = "") {
        const elemento = document.createElement(etiqueta);
        elemento.classList.add(...clases);
        if (texto) elemento.textContent = texto;
        return elemento;
    }

    function mostrarDetalleProducto(producto) {
        // Mostrar spinner y ocultar contenido
        detalleProductoSpinner.classList.remove("d-none");
        detalleProductoContenido.classList.add("d-none");
        bsDetalleModal.show();

        // Simular carga de 2 segundos
        setTimeout(() => {
            detalleProductoNombre.textContent = producto.nombre;
            detalleProductoDescripcion.textContent = producto.descripcion;
            detalleProductoPrecio.textContent = producto.precio;
            detalleProductoImagen.src = producto.imagen;
            detalleProductoImagen.alt = producto.alt;
            detalleProductoSpinner.classList.add("d-none");
            detalleProductoContenido.classList.remove("d-none");
        }, 2000);
    }

    function abrirModalCheckout(producto) {
        checkoutProductName.textContent = producto.nombre;
        checkoutProductPrice.textContent = producto.precio;
        checkoutProductImage.src = producto.imagen;
        checkoutForm.dataset.productName = producto.nombre;
        checkoutForm.dataset.productPrice = producto.precio;
        bsCheckoutModal.show();
    }

    function manejarConfirmacionPedido(evento) {
        evento.preventDefault();
        const form = evento.target;

        const producto = {
            nombre: form.dataset.productName,
            precio: form.dataset.productPrice
        };

        const cliente = {
            nombre: checkoutName.value,
            direccion: checkoutAddress.value
        };

        const asunto = `Nuevo Pedido de Producto: ${producto.nombre}`;
        const cuerpoEmail = `
            ¡Se ha recibido un nuevo pedido!

            **Detalles del Cliente:**
            - Nombre: ${cliente.nombre}
            - Dirección de Envío: ${cliente.direccion}

            **Producto Solicitado:**
            - Producto: ${producto.nombre}
            - Precio: ${producto.precio}
        `;

        const mailtoLink = `mailto:amazonicoproduc@gmail.com?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpoEmail.trim())}`;
        window.location.href = mailtoLink;

        bsCheckoutModal.hide();
        form.reset();
    }

    function crearTarjetaDisponible(producto) {
        const columna = crearElemento("div", ["col-md-6", "col-lg-4", "mb-4"]);
        const tarjeta = crearElemento("div", ["card", "h-100", "shadow"]);
        const imagen = crearElemento("img", ["card-img-top"]);
        const cuerpo = crearElemento("div", ["card-body"]);
        const titulo = crearElemento("h5", ["card-title"], producto.nombre);
        const descripcion = crearElemento("p", ["card-text"], producto.descripcion);
        const precio = crearElemento("p", ["text-success", "fw-bold", "fs-5"], producto.precio);
        
        const botonera = crearElemento("div", ["d-flex", "gap-2"]);
        const botonComprar = crearElemento("button", ["btn", "btn-success", "btn-sm"], "Comprar");
        const botonMasInfo = crearElemento("button", ["btn", "btn-outline-secondary", "btn-sm"], "Más Información");

        imagen.src = producto.imagen;
        imagen.alt = producto.alt;
        imagen.loading = "lazy";
        botonComprar.addEventListener("click", () => abrirModalCheckout(producto));
        botonMasInfo.type = "button";
        botonMasInfo.addEventListener("click", () => mostrarDetalleProducto(producto));

        botonera.append(botonComprar, botonMasInfo);
        
        cuerpo.append(titulo, descripcion);
        if (producto.categoria) {
            cuerpo.appendChild(crearElemento("span", ["badge", "bg-success", "mb-3"], producto.categoria));
        }
        cuerpo.append(precio, botonera);
        tarjeta.append(imagen, cuerpo);
        columna.appendChild(tarjeta);

        return columna;
    }

    function crearTarjetaGaleria(item) {
        const columna = crearElemento("div", ["col-md-4"]);
        const tarjeta = crearElemento("div", ["card", "h-100", "shadow"]);
        const imagen = crearElemento("img", ["card-img-top"]);
        const cuerpo = crearElemento("div", ["card-body"]);
        const titulo = crearElemento("h5", ["card-title"], item.titulo);
        const descripcion = crearElemento("p", ["card-text"], item.descripcion);

        imagen.src = item.imagen;
        imagen.alt = item.alt;
        imagen.loading = "lazy";

        cuerpo.append(titulo, descripcion);
        tarjeta.append(imagen, cuerpo);
        columna.appendChild(tarjeta);

        return columna;
    }

    function mostrarGaleriaInicio() {
        if (!galeriaInicio) return;

        const tarjetas = galeriaInicioItems.map(crearTarjetaGaleria);
        galeriaInicio.replaceChildren(...tarjetas);
    }

    function renderBotonesProductoOferta() {
        if (!botonesProductoOferta) return;

        const estilosBotones = ["btn-success", "btn-primary", "btn-warning", "btn-info"];
        const botones = productosOferta.map(({ clave, texto }, index) => {
            const estilo = estilosBotones[index % estilosBotones.length];
            const boton = crearElemento("button", ["btn", estilo, "boton-producto"], texto);
            boton.type = "button";
            boton.dataset.producto = clave;
            return boton;
        });

        botonesProductoOferta.replaceChildren(...botones);
    }

    function mostrarProductosDisponibles() {
        if (!contenedorProductos) return;

        const tarjetas = productosDisponibles.map(crearTarjetaDisponible);
        contenedorProductos.replaceChildren(...tarjetas);
    }

    function crearTarjetaResumen(titulo, valor, detalle) {
        const columna = crearElemento("div", ["col-md-4"]);
        const tarjeta = crearElemento("div", ["card", "h-100", "shadow-sm", "text-center"]);
        const cuerpo = crearElemento("div", ["card-body"]);
        const encabezado = crearElemento("h5", ["card-title"], titulo);
        const numero = crearElemento("p", ["display-6", "text-success", "fw-bold", "mb-2"], valor);
        const texto = crearElemento("p", ["card-text"], detalle);

        cuerpo.append(encabezado, numero, texto);
        tarjeta.appendChild(cuerpo);
        columna.appendChild(tarjeta);

        return columna;
    }

    function mostrarResumenDinamico() {
        if (!resumenDinamico) return;

        const precios = productosDisponibles
            .map((producto) => parseFloat(producto.precio.replace(",", ".").replace(/[^0-9.]/g, "")))
            .filter((precio) => Number.isFinite(precio));
        const precioMenor = precios.length > 0 ? `$${Math.min(...precios).toFixed(2)}` : "Sin precio";
        const tarjetas = [
            crearTarjetaResumen("Productos cargados", productosDisponibles.length.toString(), "Cantidad de productos actualmente disponibles en el catálogo."),
            crearTarjetaResumen("Precio desde", precioMenor, "Valor calculado a partir de la lista de productos."),
            crearTarjetaResumen("Categorías", categoriasProyecto.length.toString(), categoriasProyecto.join(", "))
        ];

        resumenDinamico.replaceChildren(...tarjetas);
    }

    function mostrarEstadoDatos() {
        if (!estadoDatos) return;

        if (productosDisponibles.length === 0) {
            estadoDatos.textContent = "No hay productos disponibles para mostrar.";
            estadoDatos.className = "alert alert-warning";
        } else {
            estadoDatos.textContent = `Hay ${productosDisponibles.length} productos disponibles en el catálogo.`;
            estadoDatos.className = "alert alert-success";
        }
    }

    function crearFilaProducto(producto) {
        const fila = document.createElement("tr");
        const nombre = crearElemento("td", ["fw-bold"], producto.nombre);
        const descripcion = crearElemento("td", [], producto.descripcion);
        const precio = crearElemento("td", ["text-success", "fw-bold", "text-start"], producto.precio);

        fila.append(nombre, descripcion, precio);
        return fila;
    }

    function mostrarTablaProductos() {
        if (!tablaProductos) return;

        tablaProductos.replaceChildren();
        productosDisponibles.forEach((producto) => {
            tablaProductos.appendChild(crearFilaProducto(producto));
        });
    }

    function marcarCampo({ campo, errorEl, exitoEl, mensajeError, mensajeExito }) {
        errorEl.textContent = mensajeError || "";
        exitoEl.textContent = mensajeExito || "";
        campo.classList.toggle("is-invalid", !!mensajeError);
        campo.classList.toggle("is-valid", !!mensajeExito);
        return !mensajeError;
    }

    function validarNombreProducto() {
        const nombre = campoNombre.value.trim();
        const patronNombre = /^[a-zA-Z0-9\u00c0-\u017f\s]+$/;
        const opts = { campo: campoNombre, errorEl: errorNombre, exitoEl: exitoNombre };

        if (nombre === "") return marcarCampo({ ...opts, mensajeError: "Ingrese el nombre del producto." });
        if (nombre.length < LONGITUD_MINIMA_NOMBRE) return marcarCampo({ ...opts, mensajeError: `El nombre debe tener al menos ${LONGITUD_MINIMA_NOMBRE} caracteres.` });
        if (nombre.length > 40) return marcarCampo({ ...opts, mensajeError: "El nombre no debe superar los 40 caracteres." });
        if (!patronNombre.test(nombre)) return marcarCampo({ ...opts, mensajeError: "Use solo letras, numeros y espacios." });

        return marcarCampo({ ...opts, mensajeExito: "Nombre valido." });
    }

    function validarDescripcionProducto() {
        const descripcion = campoDescripcion.value.trim();
        const palabrasDescripcion = descripcion.split(/\s+/).filter(Boolean);
        const caracteresUnicos = new Set(descripcion.replace(/\s/g, "").toLowerCase()).size;
        contadorDescripcion.textContent = `${campoDescripcion.value.length}/160 caracteres. Minimo ${LONGITUD_MINIMA_DESCRIPCION}.`;
        const opts = { campo: campoDescripcion, errorEl: errorDescripcion, exitoEl: exitoDescripcion };

        if (descripcion === "") return marcarCampo({ ...opts, mensajeError: "Ingrese una descripcion del producto." });
        if (descripcion.length < LONGITUD_MINIMA_DESCRIPCION) return marcarCampo({ ...opts, mensajeError: `La descripcion debe tener al menos ${LONGITUD_MINIMA_DESCRIPCION} caracteres.` });
        if (palabrasDescripcion.length < PALABRAS_MINIMAS_DESCRIPCION) return marcarCampo({ ...opts, mensajeError: `La descripcion debe incluir al menos ${PALABRAS_MINIMAS_DESCRIPCION} palabras.` });
        if (caracteresUnicos < 5) return marcarCampo({ ...opts, mensajeError: "Escriba una descripcion mas detallada del producto." });
        if (descripcion.length > 160) return marcarCampo({ ...opts, mensajeError: "La descripcion no debe superar los 160 caracteres." });

        return marcarCampo({ ...opts, mensajeExito: "Descripcion suficiente." });
    }

    function validarCategoriaProducto() {
        const opts = { campo: campoCategoria, errorEl: errorCategoria, exitoEl: exitoCategoria };
        if (campoCategoria.value === "") return marcarCampo({ ...opts, mensajeError: "Seleccione una categoria, tipo o estado antes de registrar." });
        return marcarCampo({ ...opts, mensajeExito: "Categoria seleccionada." });
    }

    function actualizarEstadoBoton() {
        const esValido = campoNombre.classList.contains("is-valid") &&
            campoDescripcion.classList.contains("is-valid") &&
            campoCategoria.classList.contains("is-valid");
        botonRegistrar.disabled = !esValido;
    }

    function validarFormularioProducto() {
        const esValido = validarNombreProducto() && validarDescripcionProducto() && validarCategoriaProducto();
        actualizarEstadoBoton();
        return esValido;
    }

    function limpiarMensajesFormulario() {
        [errorNombre, errorDescripcion, errorCategoria, exitoNombre, exitoDescripcion, exitoCategoria].forEach(el => el.textContent = "");
        [campoNombre, campoDescripcion, campoCategoria].forEach(el => el.classList.remove("is-invalid", "is-valid"));
        contadorDescripcion.textContent = `0/160 caracteres. Minimo ${LONGITUD_MINIMA_DESCRIPCION}.`;
        botonRegistrar.disabled = true;
    }

    function actualizarTotalRegistros() {
        totalRegistros.textContent = contadorRegistros;
    }

    function confirmarEliminacionProducto(columna, nombre) {
        modalConfirmacionCuerpo.textContent = `¿Está seguro de que desea eliminar el producto "${nombre}"? Esta acción no se puede deshacer.`;
        bsModal.show();

        const ejecutarEliminacion = () => {
            columna.remove();
            contadorRegistros--;
            actualizarTotalRegistros();
            mostrarMensaje(`Producto eliminado: ${nombre}`, "alert-warning");
            bsModal.hide();
            btnConfirmarAccion.removeEventListener("click", ejecutarEliminacion);
        };

        btnConfirmarAccion.addEventListener("click", ejecutarEliminacion, { once: true });
    }

    function crearBotonEliminar(columna, nombre) {
        const botonEliminar = crearElemento("button", ["btn", "btn-danger", "btn-sm", "mt-3"], "Eliminar");
        botonEliminar.type = "button";
        botonEliminar.addEventListener("click", () => confirmarEliminacionProducto(columna, nombre));
        return botonEliminar;
    }

    function crearTarjetaProducto(nombre, descripcion, categoria) {
        const columna = crearElemento("div", ["col-md-4", "mb-3"]);
        const tarjeta = crearElemento("div", ["card", "h-100", "shadow"]);
        const cuerpo = crearElemento("div", ["card-body"]);
        const titulo = crearElemento("h5", ["card-title"], nombre);
        const textoDescripcion = crearElemento("p", ["card-text"], descripcion);
        const etiquetaCategoria = crearElemento("span", ["badge", "bg-success"], categoria);
        const botonEliminar = crearBotonEliminar(columna, nombre);

        cuerpo.append(titulo, textoDescripcion, etiquetaCategoria, botonEliminar);
        tarjeta.appendChild(cuerpo);
        columna.appendChild(tarjeta);

        return columna;
    }

    function agregarRegistroProducto(nombre, descripcion, categoria) {
        const tarjetaProducto = crearTarjetaProducto(nombre, descripcion, categoria);
        listaProductos.appendChild(tarjetaProducto);
        contadorRegistros++;
        actualizarTotalRegistros();
    }

    function agregarProductoDinamico(producto) {
        productosDisponibles.push({
            nombre: producto.nombre,
            descripcion: producto.descripcion,
            categoria: producto.categoria,
            precio: "Nuevo registro",
            imagen: "/static/img/producto.jpeg",
            alt: producto.nombre
        });

        mostrarProductosDisponibles();
        mostrarResumenDinamico();
        mostrarEstadoDatos();
        mostrarTablaProductos();
    }

    function validarCampoProducto(funcionValidacion) {
        funcionValidacion();
        actualizarEstadoBoton();
    }

    function obtenerDatosFormulario() {
        return {
            nombre: campoNombre.value.trim(),
            descripcion: campoDescripcion.value.trim(),
            categoria: campoCategoria.value
        };
    }

    function manejarEnvioFormulario(evento) {
        evento.preventDefault();

        if (!validarFormularioProducto()) {
            mostrarMensaje("Por favor, corrija los campos marcados antes de registrar.", "alert-danger");
            return;
        }

        const producto = obtenerDatosFormulario();
        agregarRegistroProducto(producto.nombre, producto.descripcion, producto.categoria);
        agregarProductoDinamico(producto);
        mostrarMensaje(`Producto registrado: ${producto.nombre} | Categoria: ${producto.categoria}`, "alert-success");

        formularioProducto.reset();
        limpiarMensajesFormulario();
    }

    function manejarEnvioContacto(evento) {
        evento.preventDefault();

        const nombre = contactoNombre.value;
        const email = contactoEmail.value;
        const asunto = contactoAsunto.value;
        const mensaje = contactoMensaje.value;

        const cuerpoEmail = `
            Nombre: ${nombre}
            Correo: ${email}
            --------------------------------
            Mensaje:
            ${mensaje}
        `;

        const mailtoLink = `mailto:amazonicoproduc@gmail.com?subject=${encodeURIComponent(asunto)}&body=${encodeURIComponent(cuerpoEmail.trim())}`;

        window.location.href = mailtoLink;
    }

    function inicializarProductoRecomendado() {
        renderBotonesProductoOferta();
        botonesProducto = Array.from(document.querySelectorAll(".boton-producto"));

        botonesProducto.forEach((boton) => {
            boton.addEventListener("click", manejarSeleccionProducto);
        });

        const botonActivo = document.querySelector('.boton-producto[data-producto="artesania"]') || botonesProducto[0];
        if (botonActivo) {
            mostrarProductoRecomendado(productos[botonActivo.dataset.producto]);
            actualizarBotonesProducto(botonActivo);
        }
    }

    function registrarEventosValidacion() {
        const campos = [
            { el: campoNombre, func: validarNombreProducto, events: ["input", "blur"] },
            { el: campoDescripcion, func: validarDescripcionProducto, events: ["input", "blur"] },
            { el: campoCategoria, func: validarCategoriaProducto, events: ["change", "blur"] }
        ];

        campos.forEach(({ el, func, events }) => {
            events.forEach(event => {
                el.addEventListener(event, () => validarCampoProducto(func));
            });
        });

        formularioProducto.addEventListener("submit", manejarEnvioFormulario);
    }

    function inicializarFormularioProducto() {
        registrarEventosValidacion();
        limpiarMensajesFormulario();
    }

    function inicializarFormularioContacto() {
        if (formularioContacto) {
            formularioContacto.addEventListener("submit", manejarEnvioContacto);
        }
    }

    function iniciarAplicacion() {
        cargarPlantillasBase();
        mostrarGaleriaInicio();
        mostrarProductosDisponibles();
        mostrarResumenDinamico();
        mostrarEstadoDatos();
        mostrarTablaProductos();

        if (document.getElementById("producto-dinamico")) {
            inicializarProductoRecomendado();
        }
        if (document.getElementById("registro-producto")) {
            inicializarFormularioProducto();
        }
        if (document.getElementById("contacto")) {
            inicializarFormularioContacto();
        }

        if (modalConfirmacion) {
            bsModal = new bootstrap.Modal(modalConfirmacion);
        }
        if (detalleProductoModal) {
            bsDetalleModal = new bootstrap.Modal(detalleProductoModal);
        }
        if (checkoutModal) {
            bsCheckoutModal = new bootstrap.Modal(checkoutModal);
        }
        if (checkoutForm) {
            checkoutForm.addEventListener("submit", manejarConfirmacionPedido);
        }
    }

    // Iniciar la aplicación cuando el DOM esté completamente cargado
    document.addEventListener("DOMContentLoaded", iniciarAplicacion);
})();
