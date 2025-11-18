package com.diego5714.tarea4.services;

import com.diego5714.tarea4.models.AvisoAdopcion;
import com.diego5714.tarea4.models.AvisosRepository;
import com.diego5714.tarea4.models.Nota;
import com.diego5714.tarea4.models.NotasRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service //Servicio para gestionar la creacion de notas
public class NotaService {

    @Autowired
    private NotasRepository notaRepository;

    @Autowired
    private AvisosRepository avisoRepository;

    @Transactional // Transaccion atomica
    public Nota crearNota(Integer avisoId, int valorNota) {
        AvisoAdopcion aviso = avisoRepository.getReferenceById(avisoId);

        Nota nuevaNota = new Nota();
        nuevaNota.setAviso(aviso);
        nuevaNota.setNota(valorNota);

        return notaRepository.save(nuevaNota);
    }
}
