# BioCrowny Order Guard

Aplicación que detecta qrs de momento

## Instalación

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