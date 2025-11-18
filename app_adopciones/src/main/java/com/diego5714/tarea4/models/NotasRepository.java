package com.diego5714.tarea4.models;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface NotasRepository extends JpaRepository<Nota, Integer> {}
