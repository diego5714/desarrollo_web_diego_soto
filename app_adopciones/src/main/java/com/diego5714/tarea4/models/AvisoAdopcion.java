package com.diego5714.tarea4.models;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDateTime;
import java.util.List;
import org.hibernate.annotations.Immutable;

//import org.springframework.cglib.core.Local;
//import org.springframework.web.multipart.MultipartFile;

@Entity
@Table(name = "aviso_adopcion")
@Immutable
public class AvisoAdopcion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @NotNull
    @Column(name = "fecha_ingreso", nullable = false)
    private LocalDateTime fechaIngreso;

    @Column(name = "sector", length = 100)
    private String sector;

    @NotNull
    @Column(name = "nombre", nullable = false, length = 200)
    private String nombre;

    @NotNull
    @Column(name = "email", nullable = false, length = 100)
    private String email;

    @Column(name = "celular", length = 15)
    private String celular;

    @NotNull
    @Enumerated(EnumType.STRING)
    @Column(name = "tipo", nullable = false)
    private TipoAnimal tipo;

    @NotNull
    @Column(name = "cantidad", nullable = false)
    private Integer cantidad;

    @NotNull
    @Column(name = "edad", nullable = false)
    private Integer edad;

    @NotNull
    @Enumerated(EnumType.STRING)
    @Column(name = "unidad_medida", nullable = false)
    private UnidadMedidaEdad unidadMedida;

    @NotNull
    @Column(name = "fecha_entrega", nullable = false)
    private LocalDateTime fechaEntrega;

    @Column(name = "descripcion", columnDefinition = "TEXT")
    private String descripcion;

    // Relacion: Muchos avisos pertenecen a una comuna
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "comuna_id", nullable = false)
    private Comuna comuna;

    // Relacion inversa: Un aviso puede tener muchas notas.
    // El campo 'aviso' de Nota se encargara de gestionar esta relacion.
    @OneToMany(mappedBy = "aviso")
    private List<Nota> notas;

    // Constructores ###########################################

    public AvisoAdopcion() {}

    // Getters
    public Integer getID() {
        return id;
    }

    public LocalDateTime getFechaIngreso() {
        return fechaIngreso;
    }

    public Comuna getComuna() {
        return comuna;
    }

    public String getSector() {
        return sector;
    }

    public String getNombre() {
        return nombre;
    }

    public String getEmail() {
        return email;
    }

    public String getCelular() {
        return celular;
    }

    public TipoAnimal getTipo() {
        return tipo;
    }

    public Integer getCantidad() {
        return cantidad;
    }

    public Integer getEdad() {
        return edad;
    }

    public UnidadMedidaEdad getUnidadMedida() {
        return unidadMedida;
    }

    public LocalDateTime getFechaEntrega() {
        return fechaEntrega;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public List<Nota> getNotas() {
        return notas;
    }
}
