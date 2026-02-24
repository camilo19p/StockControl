
package Control;

import Model.Producto;
import java.util.ArrayList;
import java.util.List;

public class GestorProductos {
    public List<Producto> listaProductos;

    public GestorProductos() {
        this.listaProductos = new ArrayList<>();
    }

    public void agregarProducto(Producto producto) {
        listaProductos.add(producto);
    }

    public void eliminarProducto(Producto producto) {
        listaProductos.remove(producto);
    }

    public List<Producto> getListaProductos() {
        return listaProductos;
    }
}


