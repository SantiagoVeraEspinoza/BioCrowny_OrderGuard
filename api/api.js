require('dotenv').config(); // Cargar variables de entorno desde .env
const express = require('express');
const mysql = require('mysql2');

const app = express();
const port = 3000;

// Configuración de la conexión a MySQL usando variables de entorno
const connection = mysql.createConnection({
    host: process.env.DB_HOST,      // Usar DB_HOST desde .env
    user: process.env.DB_USER,      // Usar DB_USER desde .env
    password: process.env.DB_PASSWORD, // Usar DB_PASSWORD desde .env
    database: process.env.DB_DATABASE // Usar DB_DATABASE desde .env
});

// Conectar a la base de datos
connection.connect((err) => {
    if (err) {
        console.error('Error al conectar a la base de datos:', err.message);
    } else {
        console.log('Conectado a la base de datos MySQL.');
    }
});

// Ruta para obtener un cliente por ID
app.get('/cliente/:id', (req, res) => {
    const id = req.params.id;
    const query = 'SELECT * FROM Cliente WHERE ClienteID = ?';

    connection.query(query, [id], (err, results) => {
        if (err) {
            res.status(500).json({ error: 'Error al consultar la base de datos' });
        } else if (results.length > 0) {
            res.json(results[0]); // Devuelve el primer resultado (el cliente)
        } else {
            res.status(404).json({ error: 'Producto no encontrado' });
        }
    });
});

// Ruta para obtener un producto por ID
app.get('/producto/:id', (req, res) => {
    const id = req.params.id;
    const query = 'SELECT * FROM Producto WHERE ProductoID = ?';

    connection.query(query, [id], (err, results) => {
        if (err) {
            res.status(500).json({ error: 'Error al consultar la base de datos' });
        } else if (results.length > 0) {
            res.json(results[0]); // Devuelve el primer resultado (el producto)
        } else {
            res.status(404).json({ error: 'Producto no encontrado' });
        }
    });
});

// Ruta para obtener una orden por ID
app.get('/orden/:id', (req, res) => {
    const id = req.params.id;
    const query = 'SELECT * FROM Orden WHERE OrderID = ?';

    connection.query(query, [id], (err, results) => {
        if (err) {
            res.status(500).json({ error: 'Error al consultar la base de datos' });
        } else if (results.length > 0) {
            res.json(results[0]); // Devuelve el primer resultado (la orden)
        } else {
            res.status(404).json({ error: 'Producto no encontrado' });
        }
    });
});

// Ruta para obtener un paquete por ID
app.get('/paquete/:id', (req, res) => {
    const id = req.params.id;
    const query = 'SELECT * FROM Paquete WHERE PaqueteID = ?';

    connection.query(query, [id], (err, results) => {
        if (err) {
            res.status(500).json({ error: 'Error al consultar la base de datos' });
        } else if (results.length > 0) {
            res.json(results[0]); // Devuelve el primer resultado (el paquete)
        } else {
            res.status(404).json({ error: 'Producto no encontrado' });
        }
    });
});

// Iniciar el servidor
app.listen(port, () => {
    console.log(`API escuchando en http://localhost:${port}`);
});