-- Nicolo Trevisani

-- 1. Crea una nueva tabla para almacenar las temporadas de las series (2 ptos). 

create table TEMPORADAS(
    idSerie int not null,
    numTemporada int not null,
    fechaEstreno date not null,
    fechaRegistro date not null,
    disponible boolean not null,        
    check (fechaRegistro > fechaEstreno),
    check (disponible in (0,1)),
    foreign key (idSerie) references SERIES(idSerie),
    primary key (idSerie, numTemporada)
);


-- 2. Añadir una nueva columna a la tabla "generos" para almacenar un campo
-- denominado "descripcion" (0.25 ptos).

alter table GENEROS add descripcion char;

-- 3. Crea un índice sobre el par de campos “titulo” y “anyoFin” de las series (0.25 ptos)

create index idx_tituloAnyoFin on SERIES (titulo, anyoFin);


-- 4. Mostrar el “idserie”, “titulo”, “titulo original” y “sinopsis” de todas las series,
-- ordenadas por título descendentemente (0.5 ptos)

select se.idserie, se.titulo, se.tituloOriginal, se.sinopsis 
    from SERIES se
        order by se.titulo desc;


-- 5. Retornar los datos de los usuarios franceses o noruegos (0.5 ptos)

select us.* 
    from USUARIOS us
        where us.pais in ('Noruega','Francia');


-- 6. Mostrar los datos de los actores junto con los datos de las series en las que actúan
-- (0.75 ptos)

select act.*, se.*
    from ACTORES act
        inner join REPARTO re on act.idActor = re.idActor
        inner join SERIES se on se.idSerie = re.idSerie;
    

-- 7. Mostrar los datos de los usuarios que no hayan realizado nunca ninguna valoración
-- (0.75 ptos)

select us.*
    from USUARIOS us
        where us.idUsuario not in (select val.idUsuario from VALORACIONES val);


-- 8. Mostrar los datos de los usuarios junto con los datos de su profesión, incluyendo las
-- profesiones que no estén asignadas a ningún usuario (0.75 ptos)

select us.*, pr.profesion
    from PROFESIONES pr
        left join USUARIOS us on us.idProfesion = pr.idProfesion;


-- 9. Retornar los datos de las series que estén en idioma español, y cuyo título comience
-- por E o G (1 pto)

select se.*
    from SERIES se
        inner join IDIOMAS id on id.ididioma = se.idIdioma
            where id.idioma = 'Español'
                and (se.titulo like ('E%') or se.titulo like ('G%'));
        

-- 10. Retornar los “idserie”, “titulo” y “sinopsis” de todas las series junto con la
-- puntuación media, mínima y máxima de sus valoraciones (1 pto)

select se.idSerie, se.titulo, se.sinopsis, avg(val.puntuacion) punt_media, min(val.puntuacion) punt_min, max(val.puntuacion) punt_max
    from SERIES se
        inner join VALORACIONES val on se.idSerie = val.idSerie
            group by se.idSerie;


-- 11. Actualiza al valor 'Sin sinopsis' la sinopsis de todas las series cuya sinopsis sea nula
-- y cuyo idioma sea el inglés (1 pto)

update SERIES set sinopsis = 'sin sinopsis'
    where sinopsis is null 
        and idIdioma in (
            select id.idIdioma from IDIOMAS id
                where id.idioma = 'Inglés');


-- 12. Utilizando funciones ventana, muestra los datos de las valoraciones junto al nombre
-- y apellidos (concatenados) de los usuarios que las realizan, y en la misma fila, el
-- valor medio de las puntuaciones realizadas por el usuario (1.25 ptos)

select us.nombre || " " || us.apellido1 || " " || us.apellido2 as usuario, val.puntuacion, avg(val.puntuacion)
    over (partition by us.idUsuario)
    from USUARIOS us
        inner join VALORACIONES val on us.idUsuario = val.idUsuario;