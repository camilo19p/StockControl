import streamlit as st
import pandas as pd

# ── Configuración de la página ──────────────────────────────────────────────
st.set_page_config(
    page_title="StockControl",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0f1117; }
    div[data-testid="stSidebar"] { background-color: #1a1a2e; }

    .sc-title {
        font-size: 2rem;
        font-weight: 800;
        color: #f0a500;
        margin-bottom: 0.2rem;
    }
    .sc-subtitle {
        color: #8888aa;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }
    .sc-card {
        background: #16161f;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.75rem;
        color: #f0f0f5;
    }
    .sc-card strong { color: #f0a500; }
    .sc-badge {
        display: inline-block;
        background: rgba(240,165,0,0.12);
        color: #f0a500;
        border-radius: 100px;
        padding: 2px 10px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .sc-badge-green {
        display: inline-block;
        background: rgba(0,229,160,0.12);
        color: #00e5a0;
        border-radius: 100px;
        padding: 2px 10px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .sc-badge-red {
        display: inline-block;
        background: rgba(255,61,107,0.12);
        color: #ff3d6b;
        border-radius: 100px;
        padding: 2px 10px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .sc-empty {
        color: #555570;
        font-style: italic;
        padding: 1.5rem;
        text-align: center;
        background: #16161f;
        border-radius: 12px;
        border: 1px dashed rgba(255,255,255,0.08);
    }
    .success-msg {
        background: rgba(0,229,160,0.1);
        border: 1px solid rgba(0,229,160,0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #00e5a0;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    .warning-msg {
        background: rgba(240,165,0,0.1);
        border: 1px solid rgba(240,165,0,0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #f0a500;
        font-weight: 600;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: #16161f;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: #f0a500;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #8888aa;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .stButton > button {
        background: #f0a500 !important;
        color: #000 !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        width: 100%;
    }
    .stButton > button:hover { background: #ffc200 !important; }
    div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Inicializar datos en session_state ───────────────────────────────────────
def init_data():
    if "productos" not in st.session_state:
        st.session_state.productos = [
            {"codigo": "LIC001", "nombre": "Ron Medellín",      "entraron": 24, "precio_compra": 18000.0, "precio_venta": 25000.0, "salieron": 10},
            {"codigo": "LIC002", "nombre": "Aguardiente Blanco", "entraron": 48, "precio_compra": 8000.0,  "precio_venta": 12000.0, "salieron": 20},
            {"codigo": "LIC003", "nombre": "Cerveza Club",       "entraron": 120,"precio_compra": 2500.0,  "precio_venta": 4000.0,  "salieron": 60},
            {"codigo": "LIC004", "nombre": "Vino Tinto",         "entraron": 12, "precio_compra": 22000.0, "precio_venta": 35000.0, "salieron": 3},
        ]
    if "deuda" not in st.session_state:
        st.session_state.deuda = 150000.0
    if "capital" not in st.session_state:
        st.session_state.capital = 800000.0

init_data()

# ── Helpers ──────────────────────────────────────────────────────────────────
def get_producto_by_codigo(codigo):
    for i, p in enumerate(st.session_state.productos):
        if p["codigo"].upper() == codigo.upper():
            return i, p
    return -1, None

def calcular_vendido_total():
    return sum(p["salieron"] * p["precio_venta"] for p in st.session_state.productos)

def calcular_ganancia_total():
    return sum(p["salieron"] * (p["precio_venta"] - p["precio_compra"]) for p in st.session_state.productos)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sc-title">📦 StockControl</div>', unsafe_allow_html=True)
    st.markdown('<div class="sc-subtitle">Sistema de Control de Inventario</div>', unsafe_allow_html=True)
    st.divider()

    menu = st.radio(
        "Navegación",
        [
            "🏠  Inicio",
            "📋  Mostrar Productos",
            "🔍  Buscar Producto",
            "➕  Ingresar Producto",
            "💰  Ganancias",
            "✏️  Actualizar Producto",
            "❌  Eliminar Producto",
            "📊  Registro de Inventario",
        ],
        label_visibility="collapsed"
    )

    st.divider()
    total_prod = len(st.session_state.productos)
    total_unidades = sum(p["entraron"] for p in st.session_state.productos)
    st.metric("📦 Productos", total_prod)
    st.metric("🗂️ Unidades totales", total_unidades)

# ── INICIO ───────────────────────────────────────────────────────────────────
if menu == "🏠  Inicio":
    st.markdown('<div class="sc-title">Sistema Control de Inventario</div>', unsafe_allow_html=True)
    st.markdown('<div class="sc-subtitle">Gestión de productos, ventas y ganancias para tu negocio</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.productos)}</div><div class="metric-label">Productos</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{sum(p["entraron"] for p in st.session_state.productos)}</div><div class="metric-label">Unidades en stock</div></div>', unsafe_allow_html=True)
    with col3:
        vendido = calcular_vendido_total()
        st.markdown(f'<div class="metric-card"><div class="metric-value">${vendido:,.0f}</div><div class="metric-label">Total vendido</div></div>', unsafe_allow_html=True)
    with col4:
        ganancia = calcular_ganancia_total()
        st.markdown(f'<div class="metric-card"><div class="metric-value">${ganancia:,.0f}</div><div class="metric-label">Ganancias</div></div>', unsafe_allow_html=True)

    st.divider()
    st.markdown("### ¿Qué puedes hacer?")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Productos** — Ingresar, mostrar, buscar, actualizar y eliminar productos del inventario.")
    with col2:
        st.info("**Ganancias** — Visualiza la ganancia por producto calculada automáticamente.")
    with col3:
        st.info("**Inventario** — Resumen de ventas, ganancias, deuda y capital del negocio.")
    st.caption("💡 Usa el menú de la izquierda para navegar entre las funciones del sistema.")

# ── MOSTRAR PRODUCTOS ────────────────────────────────────────────────────────
elif menu == "📋  Mostrar Productos":
    st.markdown('<div class="sc-title">Lista de Productos</div>', unsafe_allow_html=True)

    if st.session_state.productos:
        for p in st.session_state.productos:
            ganancia_unit = p["precio_venta"] - p["precio_compra"]
            st.markdown(f"""
            <div class="sc-card">
                <span class="sc-badge">{p['codigo']}</span><br>
                <strong>{p['nombre']}</strong><br>
                Cantidad: {p['entraron']} und &nbsp;|&nbsp;
                Compra: ${p['precio_compra']:,.0f} &nbsp;|&nbsp;
                Venta: ${p['precio_venta']:,.0f} &nbsp;|&nbsp;
                <span class="sc-badge-green">Ganancia: ${ganancia_unit:,.0f}</span>
            </div>
            """, unsafe_allow_html=True)
        st.caption(f"Total: {len(st.session_state.productos)} producto(s) registrados")
    else:
        st.markdown('<div class="sc-empty">No hay productos registrados.</div>', unsafe_allow_html=True)

# ── BUSCAR PRODUCTO ──────────────────────────────────────────────────────────
elif menu == "🔍  Buscar Producto":
    st.markdown('<div class="sc-title">Buscar Producto</div>', unsafe_allow_html=True)

    busqueda = st.text_input("Escribe el código o nombre del producto", placeholder="Ej: LIC001 o Ron...")

    if busqueda:
        resultados = [p for p in st.session_state.productos
                      if busqueda.lower() in p["codigo"].lower() or busqueda.lower() in p["nombre"].lower()]
        if resultados:
            st.success(f"Se encontraron {len(resultados)} resultado(s):")
            for p in resultados:
                ganancia_unit = p["precio_venta"] - p["precio_compra"]
                st.markdown(f"""
                <div class="sc-card">
                    <span class="sc-badge">{p['codigo']}</span><br>
                    <strong>{p['nombre']}</strong><br>
                    Cantidad: {p['entraron']} und &nbsp;|&nbsp;
                    Compra: ${p['precio_compra']:,.0f} &nbsp;|&nbsp;
                    Venta: ${p['precio_venta']:,.0f} &nbsp;|&nbsp;
                    <span class="sc-badge-green">Ganancia: ${ganancia_unit:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="sc-empty">No se encontró ningún producto con ese criterio.</div>', unsafe_allow_html=True)

# ── INGRESAR PRODUCTO ────────────────────────────────────────────────────────
elif menu == "➕  Ingresar Producto":
    st.markdown('<div class="sc-title">Ingresar Producto</div>', unsafe_allow_html=True)

    with st.form("form_ingresar"):
        col1, col2 = st.columns(2)
        with col1:
            codigo  = st.text_input("Código del producto", placeholder="Ej: LIC005")
            nombre  = st.text_input("Nombre del producto", placeholder="Ej: Whisky Old Parr")
            entrada = st.number_input("Cantidad que entraron", min_value=1, value=1)
        with col2:
            p_compra = st.number_input("Precio de compra ($)", min_value=0.0, value=0.0, step=500.0)
            p_venta  = st.number_input("Precio de venta ($)",  min_value=0.0, value=0.0, step=500.0)
        submit = st.form_submit_button("✅ Guardar Producto")

    if submit:
        if codigo and nombre and p_compra > 0 and p_venta > 0:
            codigos = [p["codigo"].upper() for p in st.session_state.productos]
            if codigo.upper() in codigos:
                st.error("⚠️ Ya existe un producto con ese código.")
            elif p_venta <= p_compra:
                st.markdown('<div class="warning-msg">⚠️ El precio de venta debería ser mayor al de compra.</div>', unsafe_allow_html=True)
            else:
                st.session_state.productos.append({
                    "codigo": codigo.upper(),
                    "nombre": nombre,
                    "entraron": int(entrada),
                    "precio_compra": p_compra,
                    "precio_venta": p_venta,
                    "salieron": 0
                })
                st.markdown('<div class="success-msg">✅ PRODUCTO REGISTRADO CON ÉXITO</div>', unsafe_allow_html=True)
        else:
            st.error("⚠️ Por favor completa todos los campos correctamente.")

# ── GANANCIAS ────────────────────────────────────────────────────────────────
elif menu == "💰  Ganancias":
    st.markdown('<div class="sc-title">Ganancias por Producto</div>', unsafe_allow_html=True)

    if st.session_state.productos:
        ganancia_total = 0
        for i, p in enumerate(st.session_state.productos):
            ganancia = p["precio_venta"] - p["precio_compra"]
            ganancia_total += ganancia
            color_class = "sc-badge-green" if ganancia > 0 else "sc-badge-red"
            st.markdown(f"""
            <div class="sc-card">
                <strong>#{i+1} — {p['nombre']}</strong> &nbsp;
                <span class="sc-badge">{p['codigo']}</span><br>
                P. Compra: ${p['precio_compra']:,.0f} &nbsp;|&nbsp;
                P. Venta: ${p['precio_venta']:,.0f} &nbsp;|&nbsp;
                <span class="{color_class}">Ganancia unitaria: ${ganancia:,.0f}</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">${ganancia_total:,.0f}</div><div class="metric-label">Ganancia total acumulada</div></div>', unsafe_allow_html=True)
        with col2:
            vendido = calcular_vendido_total()
            st.markdown(f'<div class="metric-card"><div class="metric-value">${vendido:,.0f}</div><div class="metric-label">Total vendido</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sc-empty">No hay productos registrados.</div>', unsafe_allow_html=True)

# ── ACTUALIZAR PRODUCTO ──────────────────────────────────────────────────────
elif menu == "✏️  Actualizar Producto":
    st.markdown('<div class="sc-title">Actualizar Producto</div>', unsafe_allow_html=True)

    if st.session_state.productos:
        opciones = {f"{p['nombre']} ({p['codigo']})": p["codigo"] for p in st.session_state.productos}
        seleccion = st.selectbox("Selecciona el producto a actualizar", list(opciones.keys()))
        codigo_sel = opciones[seleccion]
        idx, prod = get_producto_by_codigo(codigo_sel)

        if prod:
            with st.form("form_actualizar"):
                col1, col2 = st.columns(2)
                with col1:
                    nueva_cantidad = st.number_input("Nueva cantidad (entraron)", min_value=0, value=prod["entraron"])
                    nuevo_p_compra = st.number_input("Nuevo precio de compra ($)", min_value=0.0, value=prod["precio_compra"], step=500.0)
                with col2:
                    nuevo_p_venta = st.number_input("Nuevo precio de venta ($)", min_value=0.0, value=prod["precio_venta"], step=500.0)
                submit = st.form_submit_button("✅ Actualizar")

            if submit:
                st.session_state.productos[idx]["entraron"]      = int(nueva_cantidad)
                st.session_state.productos[idx]["precio_compra"] = nuevo_p_compra
                st.session_state.productos[idx]["precio_venta"]  = nuevo_p_venta
                st.markdown('<div class="success-msg">✅ PRODUCTO ACTUALIZADO CON ÉXITO</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="sc-empty">No hay productos registrados.</div>', unsafe_allow_html=True)

# ── ELIMINAR PRODUCTO ────────────────────────────────────────────────────────
elif menu == "❌  Eliminar Producto":
    st.markdown('<div class="sc-title">Eliminar Producto</div>', unsafe_allow_html=True)

    if st.session_state.productos:
        opciones = {f"{p['nombre']} ({p['codigo']})": p["codigo"] for p in st.session_state.productos}
        seleccion = st.selectbox("Selecciona el producto a eliminar", list(opciones.keys()))
        codigo_sel = opciones[seleccion]
        idx, prod = get_producto_by_codigo(codigo_sel)

        if prod:
            st.markdown(f"""
            <div class="sc-card">
                <span class="sc-badge">{prod['codigo']}</span><br>
                <strong>{prod['nombre']}</strong><br>
                Cantidad: {prod['entraron']} und &nbsp;|&nbsp;
                Compra: ${prod['precio_compra']:,.0f} &nbsp;|&nbsp;
                Venta: ${prod['precio_venta']:,.0f}
            </div>
            """, unsafe_allow_html=True)

            if st.button("❌ Confirmar eliminación"):
                st.session_state.productos.pop(idx)
                st.markdown('<div class="success-msg">✅ PRODUCTO ELIMINADO CON ÉXITO</div>', unsafe_allow_html=True)
                st.rerun()
    else:
        st.markdown('<div class="sc-empty">No hay productos registrados.</div>', unsafe_allow_html=True)

# ── REGISTRO DE INVENTARIO ───────────────────────────────────────────────────
elif menu == "📊  Registro de Inventario":
    st.markdown('<div class="sc-title">Registro de Inventario</div>', unsafe_allow_html=True)

    if st.session_state.productos:
        # Tabla de inventario
        filas = []
        for p in st.session_state.productos:
            cantidad_quedaron = p["entraron"] - p["salieron"]
            p_vendido = p["salieron"] * p["precio_venta"]
            p_ganancia = p["salieron"] * (p["precio_venta"] - p["precio_compra"])
            filas.append({
                "Producto": p["nombre"],
                "C. Entraron": p["entraron"],
                "C. Quedaron": max(0, cantidad_quedaron),
                "C. Salieron": p["salieron"],
                "P. Vendido ($)": f"${p_vendido:,.0f}",
                "P. Ganancia ($)": f"${p_ganancia:,.0f}"
            })

        df = pd.DataFrame(filas)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.divider()

        # Métricas generales
        vendido_total  = calcular_vendido_total()
        ganancia_total = calcular_ganancia_total()
        deuda_restante = max(0, st.session_state.deuda - ganancia_total)
        capital        = st.session_state.capital + ganancia_total

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-value">${vendido_total:,.0f}</div><div class="metric-label">Vendido General</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card"><div class="metric-value">${st.session_state.deuda:,.0f}</div><div class="metric-label">Deuda inicial</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-value">${ganancia_total:,.0f}</div><div class="metric-label">Ganancias Generales</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card"><div class="metric-value">${capital:,.0f}</div><div class="metric-label">Capital actual</div></div>', unsafe_allow_html=True)

        st.divider()
        st.markdown("### ⚙️ Ajustar deuda y capital inicial")
        col1, col2 = st.columns(2)
        with col1:
            nueva_deuda = st.number_input("Deuda ($)", min_value=0.0, value=st.session_state.deuda, step=10000.0)
        with col2:
            nuevo_capital = st.number_input("Capital inicial ($)", min_value=0.0, value=st.session_state.capital, step=10000.0)
        if st.button("💾 Guardar valores"):
            st.session_state.deuda = nueva_deuda
            st.session_state.capital = nuevo_capital
            st.markdown('<div class="success-msg">✅ Valores actualizados.</div>', unsafe_allow_html=True)
            st.rerun()
    else:
        st.markdown('<div class="sc-empty">No hay productos registrados.</div>', unsafe_allow_html=True)
