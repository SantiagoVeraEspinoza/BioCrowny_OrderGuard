# BioCrowny Order Guard

Aplicación que detecta qrs de momento

## Instalación Aplicación

1. Descargar el repositorio 
    ```
    git clone https://github.com/SantiagoVeraEspinoza/BioCrowny_OrderGuard.git
    ```
2. Crear el ambiente virtual
    - En Windows:
        ```
        cd BioCrowny_OrderGuard
        py -3 -m venv .venv
        ```
    - En Linux/Mac:
        ```
        cd BioCrowny_OrderGuard
        python3 -m venv .venv
        ```

3. Activar el ambiente virtual
    - En Windows:
        ```
        .venv\Scripts\activate
        ```
    - En Linux/Mac:
        ```
        . .venv/bin/activate
        ```

4. Installar dependencias
    ```
    pip install -r requirements.txt
    ```

5. Ejecutar la aplicación
    ```
    flask --app main run --reload
    ```

### Instalación API

1. Instala dependencias
    ```
    cd api
    npm install
    ```

2. Inicia la API
    ```
    node api.js
    ```

### Instalación Base de Datos

1. Entra a MySQL
    ```
    mysql -u root -p
    ```

2. Crear las tablas con el archivo `table_creation.sql`

3. Crear los datos de prueba con el archivo `insert_sample_data.sql`