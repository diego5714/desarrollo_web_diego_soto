package com.diego5714.tarea4.models;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;
import java.util.List;

@Entity
@Table(name = "region")
public class Region {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "nombre", nullable = false, length = 200)
    private String nombre;

    // Relacion inversa: Una region puede tener muchas Comunas
    // Comuna tiene un campo region que gestiona la relacion inversa
    @OneToMany(mappedBy = "region")
    private List<Comuna> comunas;

    // Constructores
    public Region() {}

    // Getters
    public Integer getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public List<Comuna> getComunas() {
        return comunas;
    }
}
