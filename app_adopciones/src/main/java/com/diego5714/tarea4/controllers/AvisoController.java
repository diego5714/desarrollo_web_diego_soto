package com.diego5714.tarea4.controllers;

import com.diego5714.tarea4.models.AvisoDTO;
import com.diego5714.tarea4.services.AvisoService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/avisos")
public class AvisoController {

    @Autowired
    private AvisoService avisoService;

    // Manejamos las peticiones GET a /api/avisos
    @GetMapping
    public List<AvisoDTO> getAllAvisos() {
        return avisoService.getAllAvisos();
    }
}
