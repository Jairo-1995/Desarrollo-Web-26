(() => {
    const enlacesMenu = [
        { texto: "Inicio", href: "#inicio" },
        { texto: "Quiénes Somos", href: "#quienes-somos" },
        { texto: "Productos", href: "#servicios" },
        { texto: "Oferta", href: "#producto-dinamico" },
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
            imagen: "/static/img/maiz.webp",
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
    const checkoutProductoNombre = document.getElementById("checkoutProductoNombre");
    const checkoutProductoTotal = document.getElementById("checkoutProductoTotal");
    const compraAccesoModal = document.getElementById("compraAccesoModal");
    let bsCompraAccesoModal;
    const compraAccesoProducto = document.getElementById("compraAccesoProducto");

    const formularioProducto = null; // el registro de producto se hace desde /productos/crear

    const formularioContacto = document.getElementById("formulario-contacto");
    const contactoNombre = document.getElementById("contact-nombre");
    const contactoEmail = document.getElementById("contact-email");
    const contactoAsunto = document.getElementById("contact-asunto");
    const contactoMensaje = document.getElementById("contact-mensaje");


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

        if (menuPrincipal) menuPrincipal.innerHTML = plantillaMenu();
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
        // El botón "Comprar ahora" usa la misma ventana flotante de compra
        // que el resto del sitio (clase .btn-comprar + data-*).
        if (ofertaComprarAhora) {
            ofertaComprarAhora.classList.add("btn-comprar");
            ofertaComprarAhora.dataset.producto = producto.nombre;
            ofertaComprarAhora.dataset.precio = precioNumerico(producto.precio).toFixed(2);
            ofertaComprarAhora.dataset.unidad = unidadDeTextoPrecio(producto.precio);
            ofertaComprarAhora.dataset.origen = "inicio";
            ofertaComprarAhora.dataset.imagen = producto.imagen;
        }
    }

    // Extrae la unidad de un texto de precio tipo "$3.00 por kilogramo"
    function unidadDeTextoPrecio(textoPrecio) {
        const coincidencia = String(textoPrecio).match(/por\s+(\S+(?:\s+\S+)?)/i);
        return coincidencia ? coincidencia[1] : "unidad";
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

    function precioNumerico(textoPrecio) {
        // Convierte "$3,50 por kilogramo" o "$5.00" en un número
        const valor = parseFloat(String(textoPrecio).replace(",", ".").replace(/[^0-9.]/g, ""));
        return Number.isFinite(valor) ? valor : 0;
    }

    function abrirModalCheckout(producto) {
        checkoutProductName.textContent = producto.nombre;
        checkoutProductPrice.textContent = producto.precio;
        checkoutProductImage.src = producto.imagen;
        checkoutForm.dataset.productName = producto.nombre;
        checkoutForm.dataset.productPrice = producto.precio;
        // Campos que se envían al servidor (POST /comprar)
        checkoutProductoNombre.value = producto.nombre;
        checkoutProductoTotal.value = precioNumerico(producto.precio).toFixed(2);
        bsCheckoutModal.show();
    }

    // Antes de mostrar la ventana de compra: si no hay sesión, se pide
    // ingresar o registrarse en la ventana flotante de acceso.
    function intentarComprar(producto) {
        if (window.ESTA_AUTENTICADO) {
            abrirModalCheckout(producto);
        } else {
            compraAccesoProducto.textContent = producto.nombre;
            bsCompraAccesoModal.show();
        }
    }

    // Manejador de los botones de compra: lo controla el modal reutilizable
    // (templates/components/modal_compra.html), que se incluye desde base.html
    // en todas las páginas y registra su propio listener delegado. Aquí no
    // se duplica: los elementos del checkout antiguo solo existen en index.

    // El formulario de compra se envía de forma nativa a POST /comprar
    // (Flask registra el cliente y la factura y muestra el mensaje flash;
    // la validación "required" del HTML se aplica antes de enviar).

    function crearTarjetaDisponible(producto) {
        const columna = crearElemento("div", ["col-md-6", "col-lg-4", "mb-4"]);
        const tarjeta = crearElemento("div", ["card", "h-100", "shadow"]);
        const imagen = crearElemento("img", ["card-img-top"]);
        const cuerpo = crearElemento("div", ["card-body"]);
        const titulo = crearElemento("h5", ["card-title"], producto.nombre);
        const descripcion = crearElemento("p", ["card-text"], producto.descripcion);
        const precio = crearElemento("p", ["text-success", "fw-bold", "fs-5"], producto.precio);

        const botonera = crearElemento("div", ["d-flex", "gap-2"]);
        // El botón comprar abre la ventana flotante de compra (.btn-comprar):
        // el manejador global lo detecta con data-producto, data-precio, etc.
        const botonComprar = crearElemento("button", ["btn", "btn-success", "btn-sm", "btn-comprar"], "Comprar");
        const botonMasInfo = crearElemento("button", ["btn", "btn-outline-secondary", "btn-sm"], "Más Información");

        imagen.src = producto.imagen;
        imagen.alt = producto.alt;
        imagen.loading = "lazy";
        botonComprar.type = "button";
        botonComprar.dataset.producto = producto.nombre;
        botonComprar.dataset.precio = precioNumerico(producto.precio).toFixed(2);
        botonComprar.dataset.unidad = unidadDeTextoPrecio(producto.precio);
        botonComprar.dataset.origen = "inicio";
        botonComprar.dataset.imagen = producto.imagen;
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

    function inicializarFormularioContacto() {
        if (formularioContacto) {
            formularioContacto.addEventListener("submit", manejarEnvioContacto);
        }
    }

    function saltarAAnclaDirecto(instantaneo) {
        // Si la URL trae #quienes-somos, #productos-disponibles, etc.,
        // posiciona la sección de inmediato, sin animación. Se llama al
        // cargar y de nuevo al terminar de renderizar el contenido
        // dinámico, porque este cambia la altura de la página.
        if (!window.location.hash) return;
        const destino = document.getElementById(window.location.hash.slice(1));
        if (destino) {
            // behavior:"instant" siempre: nunca deslizar con animación
            destino.scrollIntoView({ behavior: "instant", block: "start" });
            if (instantaneo) window.scrollTo({ top: window.scrollY, behavior: "instant" });
        }
    }

    // Salto instantáneo al hacer clic en enlaces internos (#quienes-somos, etc.)
    // sin que el navegador deslice con animación hasta la sección.
    function configurarSaltoEnlaces() {
        document.addEventListener("click", (evento) => {
            const enlace = evento.target.closest('a[href*="#"]');
            if (!enlace) return;
            const url = new URL(enlace.href, window.location.href);
            if (url.pathname !== window.location.pathname) return; // otra página
            const destino = document.getElementById(url.hash.slice(1));
            if (!destino) return;
            evento.preventDefault();
            destino.scrollIntoView({ behavior: "instant", block: "start" });
            // Guarda el ancla en la URL sin provocar otro salto del navegador
            history.replaceState(null, "", url.hash);
        });
    }

    // Toasts flotantes (mensajes flash): cerrar con la "x" y autodescartar
    // tras unos segundos. Como son position:fixed, al aparecer NO mueven la
    // página: el usuario se queda viendo el producto comprado/agregado.
    function configurarToastsFlotantes() {
        const toasts = document.querySelectorAll(".toast-flotante");
        if (!toasts.length) return;
        toasts.forEach((toast) => {
            const cerrar = () => {
                toast.style.transition = "opacity .3s ease, transform .3s ease";
                toast.style.opacity = "0";
                toast.style.transform = "translateY(-.6rem)";
                setTimeout(() => toast.remove(), 320);
            };
            const boton = toast.querySelector(".toast-cerrar");
            if (boton) boton.addEventListener("click", cerrar);
            setTimeout(cerrar, 5000);
        });
    }

    // Mantener la posición de scroll tras enviar formularios (comprar, agregar,
    // editar): Flask redirige y la página se recarga, pero guardamos dónde
    // estaba el usuario y volvemos a ese punto exacto, sin deslizar hacia arriba.
    function configurarMantenerScroll() {
        // Al enviar cualquier formulario (compra, registros, etc.), recordamos
        // la posición vertical actual.
        document.addEventListener("submit", () => {
            try { sessionStorage.setItem("scrollTrasAccion", String(window.scrollY)); } catch (e) {}
        }, true);

        // Al cargar la página, si hay una posición guardada (venimos de una
        // acción), volvemos ahí de forma INSTANTÁNEA, sin animación.
        let yGuardado = null;
        try { yGuardado = sessionStorage.getItem("scrollTrasAccion"); } catch (e) {}
        if (yGuardado !== null) {
            try { sessionStorage.removeItem("scrollTrasAccion"); } catch (e) {}
            const y = parseInt(yGuardado, 10);
            if (!window.location.hash) {
                window.scrollTo({ top: y, behavior: "instant" });
            }
            // El contenido dinámico puede cambiar la altura de la página
            // después de cargar: repetimos el salto para asegurar la posición.
            setTimeout(() => {
                if (!window.location.hash) window.scrollTo({ top: y, behavior: "instant" });
            }, 300);
        }
    }

    function iniciarAplicacion() {
        configurarMantenerScroll();
        configurarToastsFlotantes();
        cargarPlantillasBase();
        mostrarGaleriaInicio();
        mostrarProductosDisponibles();
        mostrarResumenDinamico();
        mostrarEstadoDatos();
        mostrarTablaProductos();

        if (document.getElementById("producto-dinamico")) {
            inicializarProductoRecomendado();
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
        if (compraAccesoModal) {
            bsCompraAccesoModal = new bootstrap.Modal(compraAccesoModal);
        }
        if (checkoutModal) {
            bsCheckoutModal = new bootstrap.Modal(checkoutModal);
        }


        configurarSaltoEnlaces();
        saltarAAnclaDirecto();
    }

    // Iniciar la aplicación cuando el DOM esté completamente cargado
    document.addEventListener("DOMContentLoaded", iniciarAplicacion);
})();
