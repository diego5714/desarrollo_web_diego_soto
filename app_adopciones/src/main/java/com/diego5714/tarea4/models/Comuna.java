package com.diego5714.tarea4.models;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;
import java.util.List;

@Entity
@Table(name = "comuna")
public class Comuna {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "nombre", nullable = false, length = 200)
    private String nombre;

    // Relacion: Muchas comunas pertenecen a una region
    @NotNull
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "region_id", nullable = false)
    private Region region;

    // Relacion inversa: Una comuna puede tener muchos avisos
    @OneToMany(mappedBy = "comuna")
    private List<AvisoAdopcion> avisos;

    // Constructores
    public Comuna() {}

    // Getters
    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public Region getRegion() {
        return region;
    }

    public List<AvisoAdopcion> getAvisos() {
        return avisos;
    }
}
