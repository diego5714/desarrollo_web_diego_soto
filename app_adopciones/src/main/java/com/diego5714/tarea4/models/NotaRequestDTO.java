package com.diego5714.tarea4.models;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

public record NotaRequestDTO(
    @NotNull(message = "La nota debe ser un número válido")
    @Min(value = 1, message = "La nota debe ser al menos 1")
    @Max(value = 7, message = "La nota debe ser como máximo 7")
    Integer nota
) {}
