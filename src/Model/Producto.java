package Model;

public class Producto {
    private String nombre;
    private int entraron;
    private double precioCompra;
    private double precioVenta;
    private String codigo;

    public Producto(String codigo, String nombre, int entraron, double precioCompra, double precioVenta) {
        this.codigo = codigo;
        this.nombre = nombre;
        this.entraron = entraron;
        this.precioCompra = precioCompra;
        this.precioVenta = precioVenta;
    }

    public String getCodigo() {
        return codigo;
    }

    public void setCodigo(String codigo) {
        this.codigo = codigo;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public int getEntraron() {
        return entraron;
    }

    public void setEntraron(int entraron) {
        this.entraron = entraron;
    }

    public double getPrecioCompra() {
        return precioCompra;
    }

    public void setPrecioCompra(double precioCompra) {
        this.precioCompra = precioCompra;
    }

    public double getPrecioVenta() {
        return precioVenta;
    }

    public void setPrecioVenta(double precioVenta) {
        this.precioVenta = precioVenta;
    }

    @Override
    public String toString() {
        return "PRODUCTO{" +
                "NOMBRE='" + nombre + '\'' +
                ", ENTRARON=" + entraron +
                ", PRECIO COMPRA=" + precioCompra +
                ", PRECIO VENTA=" + precioVenta +
                ", CODIGO=" + codigo +
                '}';
    }
}



    

    

