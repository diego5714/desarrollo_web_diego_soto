package com.diego5714.tarea4.services;

import com.diego5714.tarea4.models.AvisoAdopcion;
import com.diego5714.tarea4.models.AvisoDTO;
import com.diego5714.tarea4.models.AvisosRepository;
import com.diego5714.tarea4.models.Nota;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AvisoService {

    @Autowired
    private AvisosRepository avisoRepository;

    @Transactional(readOnly = true)
    public List<AvisoDTO> getAllAvisos() {
        // Obtenemos todas las entidades de aviso en el repositorio
        List<AvisoAdopcion> avisos = avisoRepository.findAll();

        // Convertimos cada entidad en un DTO que es mas facil de enviar
        return avisos.stream().map(this::convertirAvisoDTO).collect(Collectors.toList());
    }

    // Método auxiliar para la conversion a DTO
    private AvisoDTO convertirAvisoDTO(AvisoAdopcion aviso) {
        // Formateamos "Cantidad/Tipo/Edad"
        String ctdTipoEdad = String.format(
            "%d %s(s) de %d %s",
            aviso.getCantidad(),
            aviso.getTipo().toString(),
            aviso.getEdad(),
            aviso.getUnidadMedida().toString().equals("a") ? "años" : "meses"
        );

        // Calculamos el promedio de las notas
        Double notaPromedio = aviso
            .getNotas()
            .stream()
            .mapToInt(Nota::getNota)
            .average()
            .orElse(0.0);

        // Creamos y devolvemos el DTO
        return new AvisoDTO(
            aviso.getID(),
            aviso.getFechaIngreso(),
            aviso.getSector(),
            ctdTipoEdad,
            aviso.getComuna().getNombre(),
            notaPromedio
        );
    }
}
