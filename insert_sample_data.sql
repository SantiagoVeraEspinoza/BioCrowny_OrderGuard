INSERT INTO Cliente (Nombre, Direccion) VALUES
('Juan Pérez', 'Calle Falsa 123, Ciudad A'),
('María Gómez', 'Avenida Siempre Viva 456, Ciudad B'),
('Carlos López', 'Boulevard de los Sueños 789, Ciudad C');

INSERT INTO Producto (Nombre, CantidadAlmacenada) VALUES
('Detergente Biocrowny - Limón', 100),
('Detergente Biocrowny - Lavanda', 150),
('Detergente Biocrowny - Manzana', 200);

INSERT INTO Paquete (ClienteID, Estatus, FechaEntrega) VALUES
(1, 1, '2023-10-15'),  -- En Progreso
(2, 2, '2023-10-16'),  -- Armado
(3, 3, '2023-10-17');  -- En tránsito

INSERT INTO Orden (PaqueteID, ProductoID, CantidadTotal, CantidadEscaneada) VALUES
(1, 1, 10, 5),  -- Paquete 1, Producto 1
(1, 2, 5, 5),   -- Paquete 1, Producto 2
(2, 3, 20, 15), -- Paquete 2, Producto 3
(3, 1, 15, 10); -- Paquete 3, Producto 1