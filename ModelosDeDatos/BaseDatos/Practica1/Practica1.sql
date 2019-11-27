-- 1 Creacion de la tabla Director
create table Director(
    iddirector int not null primary key,
    dni char not null unique,
    nombre char not null,
    apellido1 char not null,
    apellido2 char null,
    fechaNacimiento date not null,
    fechaRegistro date not null,
    fechaDeceso date null,
    enActivo boolean not null,    
    check (iddirector > 0),
    check (fechaRegistro > fechaNacimiento),
    check (fechaDeceso > fechaNacimiento),
    check (enActivo in (0,1))
);


-- 2 Creacion de la tabla Pelicula
create table Pelicula(
    idpelicula int not null primary key,
    titulo char not null unique,
    fechaEstreno date not null,
    duracionMin real not null,    
    genero char not null,
    iddirector int not null,
    check (idpelicula > 0),
    check (duracionMin > 0),
    check (genero in ('terror','scifi','aventura')),
    foreign key (iddirector) references Director(iddirector)
);

-- 3 Insertar al menos 3 filas válidas en la tabla Director, y otras 3 filas válidas en la tabla
-- Película

insert into Director (iddirector, dni, nombre, apellido1, apellido2, fechaNacimiento, fechaRegistro, fechaDeceso, enActivo)
values(1, '87939507L', 'Francisco', 'Plaza', 'Trinidad', '1973-02-08', '2009-12-11', null, 1);
insert into Director (iddirector, dni, nombre, apellido1, apellido2, fechaNacimiento, fechaRegistro, fechaDeceso, enActivo)
values(2, '10809094Z', 'Gabe', 'Ibanez', null , '1971-06-07', '2000-15-07', null, 1);
insert into Director (iddirector, dni, nombre, apellido1, apellido2, fechaNacimiento, fechaRegistro, fechaDeceso, enActivo)
values(3, '23903550H', 'Juan Antonio', 'Bardem', 'Munioz' , '1922-06-02', '1974-22-11', '2002-10-30', 0);

insert into Pelicula (idpelicula, titulo, fechaEstreno, duracionMin, genero, iddirector)
values(1, 'REC', '2007-11-23', 78, 'terror', 1);
insert into Pelicula (idpelicula, titulo, fechaEstreno, duracionMin, genero, iddirector)
values(2, 'Automata', '2014-09-20', 109, 'scifi', 2);
insert into Pelicula (idpelicula, titulo, fechaEstreno, duracionMin, genero, iddirector)
values(3, 'La isla misteriosa y el Capitan Nemo', '1973-03-17', 120, 'aventura', 3);

-- 4 Añadir a la tabla Película una nueva columna que almacene la recaudación, que no
-- pueda tomar un valor negativo, que no pueda ser nula, y que por defecto su valor sea 0

alter table Pelicula add recaudacion real not null check (recaudacion >= 0) default 0;

-- 5 ¿Se te ocurre un método mejor para almacenar los géneros de las películas? 
-- Por ejemplo, ¿qué pasaría si quisiésemos ampliar los géneros posibles y añadir uno nuevo?
-- Impleméntalo

-- Para esto, hay que cambiar la estructura de la tabla Pelicula, haciendo que la
-- columna genero sea sustituida por idgenero, de tipo int, y que esa columna sea una foreign key apuntando a
-- una nueva tabla, Genero, que tiene dos columnas: idgenero, descrgenero.

create table Genero(
    idgenero int not null primary key,
    descrgenero char not null unique,
    check (idgenero > 0)
);

insert into Genero (idgenero, descrgenero)
values(1, 'terror');
insert into Genero (idgenero, descrgenero)
values(2, 'scifi');
insert into Genero (idgenero, descrgenero)
values(3, 'aventura');

drop table Pelicula;

create table Pelicula(
    idpelicula int not null primary key,
    titulo char not null unique,
    fechaEstreno date not null,
    duracionMin real not null,    
    idgenero int not null,
    iddirector int not null,
    recaudacion real not null default 0,
    check (idpelicula > 0),
    check (duracionMin > 0),
    check (recaudacion >= 0),
    foreign key (idgenero) references Genero(idgenero),
    foreign key (iddirector) references Director(iddirector)
);

insert into Pelicula (idpelicula, titulo, fechaEstreno, duracionMin, idgenero, iddirector, recaudacion)
values(1, 'REC', '2007-11-23', 78, 1, 1, 32.5);
insert into Pelicula (idpelicula, titulo, fechaEstreno, duracionMin, idgenero, iddirector, recaudacion)
values(2, 'Automata', '2014-09-20', 109, 2, 2, 0.5);
insert into Pelicula (idpelicula, titulo, fechaEstreno, duracionMin, idgenero, iddirector, recaudacion)
values(3, 'La isla misteriosa y el Capitan Nemo', '1973-03-17', 120, 3, 3, 11);

--6 Imaginemos que, además, queremos almacenar los datos de los actores que participan
-- en las películas, sabiendo que un actor puede participar en varias películas, y una
-- película tiene varios actores. Implementa una solución a este problema. 
create table Actor(
    idactor int not null primary key,
    dni char not null unique,
    nombre char not null,
    apellido1 char not null,
    apellido2 char null,
    fechaNacimiento date not null,
    fechaRegistro date not null,
    fechaDeceso date null,
    enActivo boolean not null,    
    check (idactor > 0),
    check (fechaRegistro > fechaNacimiento),
    check (fechaDeceso > fechaNacimiento),
    check (enActivo in (0,1))
);

-- Ya que la relacion entre Pelicula y Actor es N a N,
-- se necesita una tabla de soporte 'PeliActor' con 
-- primary key 'compuesta' (o doble) para conectar las
-- dos tablas principales
create table PeliActor(
    idactor int not null,
    idpelicula int not null,
    foreign key (idactor) references Actor(idactor),
    foreign key (idpelicula) references Pelicula(idpelicula),
    primary key (idactor, idpelicula)
);

-- Para comprobar que la solucion funcione, hay que insertar unos valores 
-- en la tabla Actor
insert into Actor (idactor, dni, nombre, apellido1, apellido2, fechaNacimiento, fechaRegistro, fechaDeceso, enActivo)
values(1, '36827404B', 'Manuela', 'Velasco', 'Diez', '1975-10-23', '2007-05-21', null, 1);
insert into Actor (idactor, dni, nombre, apellido1, apellido2, fechaNacimiento, fechaRegistro, fechaDeceso, enActivo)
values(2, '00000000A', 'Connor', 'MacLeod', null, '1518-04-01', '1986-09-01', null, 1);

-- Una vez insertados los valores en la tabla Actor,
-- se puede rellenar la tabla PeliActor

-- Manuela Velasco actuo en REC
insert into PeliActor(idactor, idpelicula)
values(1,1); 

-- Mientras que Connor MacLeod actuo en todas
insert into PeliActor(idactor, idpelicula)
values(2,1);
insert into PeliActor(idactor, idpelicula)
values(2,2);
insert into PeliActor(idactor, idpelicula)
values(2,3);


-- drop table Actor;
-- drop table Director;
-- drop table Genero;
-- drop table PeliActor;
-- drop table Pelicula;