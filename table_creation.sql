-- Crear la tabla Cliente
CREATE TABLE Cliente (
    ClienteID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    Direccion VARCHAR(255)
);

-- Crear la tabla Producto
CREATE TABLE Producto (
    ProductoID INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(255) NOT NULL,
    CantidadAlmacenada INT DEFAULT 0
);

-- Crear la tabla Paquete
CREATE TABLE Paquete (
    PaqueteID INT PRIMARY KEY AUTO_INCREMENT,
    ClienteID INT,
    Estatus INT,
    FechaEntrega DATE,
    FOREIGN KEY (ClienteID) REFERENCES Cliente(ClienteID)
);

-- Crear la tabla Orden
CREATE TABLE Orden (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    PaqueteID INT,
    ProductoID INT,
    CantidadTotal INT,
    CantidadEscaneada INT DEFAULT 0,
    FOREIGN KEY (PaqueteID) REFERENCES Paquete(PaqueteID),
    FOREIGN KEY (ProductoID) REFERENCES Producto(ProductoID)
);