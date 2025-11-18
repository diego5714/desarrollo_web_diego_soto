package com.diego5714.tarea4.controllers;

import com.diego5714.tarea4.models.Nota;
import com.diego5714.tarea4.models.NotaRequestDTO;
import com.diego5714.tarea4.services.NotaService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("api/avisos") //Se anida bajo la ruta de avisos
public class NotaController {

    // Cargamos el servicio de notas
    @Autowired
    private NotaService notaService;

    // Endpoint para crear una nueva nota
    // maneja requests POST
    @PostMapping("/{avisoId}/notas")
    public ResponseEntity<Nota> crearNotaParaAviso(
        @PathVariable Integer avisoId,
        @Valid @RequestBody NotaRequestDTO notaDTO
    ) {
        // Valid se asegura que la nota este entre 1 y 7

        // Llamamos al servicio para crear y gardar la nota
        Nota notaGuardada = notaService.crearNota(avisoId, notaDTO.nota());

        // Devolvemos la nota creada con un status 201 Created
        return ResponseEntity.status(HttpStatus.CREATED).body(notaGuardada);
    }
}
