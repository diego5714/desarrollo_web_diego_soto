package com.diego5714.tarea4.models;

import java.time.LocalDateTime;

// Definimos un DTO (Direct Transfer Object) que se le enviará
// a JavaScript.

public record AvisoDTO(
    Integer id,
    LocalDateTime fechaPublicacion,
    String sector,
    String cantidadTipoEdad,
    String comuna,
    Double notaPromedio
) {}
