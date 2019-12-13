-- Nicolo Trevisani

-- 1. Mostrar los datos de los pedidos realizados entre octubre y noviembre de 2018 (0.5 ptos)

select ped.* from Pedidos ped
    where fechaHoraPedido between '2018-10-01 00:00' and '2018-11-30 23:59';


-- 2. Devolver el id, nombre, apellido1, apellido2, fecha de alta y fecha de baja de todos
-- los miembros del personal que no estén de baja, ordenados descendentemente por
-- fecha de alta y ascendentemente por nombre (0.75 pto, 0.25 ptos adicionales si la
-- consulta se realiza con el nombre y apellidos concatenados).

select per.idpersonal, per.nombre || " " || per.apellido1 || " " || per.apellido2 persona, per.fechaAlta, per.fechaBaja from Personal per
    where per.fechaBaja is null
        order by fechaAlta desc, nombre asc; 


-- 3. Retornar los datos de todos los clientes cuyo nombre comience por G o J y que
-- además tengan observaciones (1 pto).
-- * NOTA sobre la pregunta 3: anteriormente se pedía que “Retornar los datos
-- de todos los clientes cuyo nombre de calle comience por G o J.”. Cualquiera
-- de las dos consultas se da como válida.

select cl.* from Clientes cl
    where (cl.nombre like ('G%') or cl.nombre like ('J%'))
        and cl.observaciones is not null;


-- 4. Devolver el id e importe de las pizzas junto con el id y descripción de todos sus
-- ingredientes, siempre que el importe de estas pizzas sea mayor de 3 (1 pto).

select pi.idpizza, pi.importeBase, ingrp.idingrediente, ingr.descripcion from Pizzas pi
    inner join IngredienteDePizza ingrp on pi.idpizza = ingrp.idpizza
    inner join Ingredientes ingr on ingrp.idingrediente = ingr.idingrediente
    where pi.importeBase > 3;


-- 5. Mostrar los datos de todas las pizzas que no hayan sido nunca pedidas, ordenados
-- por id ascendentemente (1 pto).

select pi.* from Pizzas pi
    where pi.idpizza not in (select li.idpizza from LineasPedidos li)
            order by pi.idpizza asc;


-- 6. Devolver los datos de las bases, junto con los datos de las pizzas en las que están
-- presentes, incluyendo los datos de las bases que no están en ninguna pizza (0.5 ptos)

select ba.*, pi.idpizza, pi.importeBase from Bases ba
    left join Pizzas pi on ba.idbase = pi.idbase;


-- 7. Retornar los datos de los pedidos realizados por el cliente con id 1, junto con los
-- datos de sus líneas y de las pizzas pedidas, siempre que el precio unitario en la línea
-- sea menor que el importe base de la pizza. (1.5 ptos)

select ped.*, lin.*, piz.* from Pedidos ped
    inner join LineasPedidos lin on lin.idpedido = ped.idpedido
    inner join Pizzas piz on piz.idpizza = lin.idpizza
        where ped.idpedido in (select cl.idcliente from Clientes cl where cl.idcliente = 1)
            and lin.precioUnidad < piz.importeBase;


-- 8. Mostrar el id y nif de todos los clientes, junto con el número total de pedidos
-- realizados (0.75 pto, 0.25 ptos adicionales si sólo se devuelven los datos de los que
-- hayan realizado más de un pedido).

select pe.idcliente, cl.nif, count(*) numero_pedidos from Clientes cl
    inner join Pedidos pe on cl.idcliente = pe.idcliente
        group by(pe.idcliente)
            having numero_pedidos > 1;


-- 9. Sumar 0.5 al importe base de todas las pizzas que contengan el ingrediente con id
-- ‘JAM’ (0.75 pto).

update Pizzas set importeBase = importeBase + 0.5
    where idpizza in (
        select pi.idpizza from Pizzas pi
            inner join IngredienteDePizza ingrp on pi.idpizza = ingrp.idpizza
                where ingrp.idingrediente = 'JAM');


-- 10. Eliminar las líneas de los pedidos anteriores a 2018 (0.75 pto).

delete from LineasPedidos where idpedido in (
    select pe.idpedido from Pedidos pe 
        where fechaHoraPedido < '2018-01-01 00:00'); 

delete from Pedidos where fechaHoraPedido < '2018-01-01 00:00'; 


-- 11. BONUS para el 10: Realizar una consulta que devuelva el número de pizzas totales
-- pedidas por cada cliente. En la consulta deberán aparecer el id y nif de los clientes,
-- además de su nombre y apellidos concatenados (1 pto).

select pe.idcliente, cl.nif, cl.nombre || " " || cl.apellido1 || " " || cl.apellido2 nombre_cliente, sum(li.cantidad) pizzas_pedidas from Clientes cl
    inner join Pedidos pe on cl.idcliente = pe.idcliente
    inner join LineasPedidos li on li.idpedido = pe.idpedido
        group by(cl.idcliente);