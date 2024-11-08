# genetic-travelling-salesman

## Przegląd projektu 

**Temat:** Rozwiązanie problemu komiwojażera z wykorzystaniem algorytmu genetycznego

**Cele:** 

- Opracowanie bliskiego optimum rozwiązania problemu komiwojażera
- Implementacja algorytmu w Pythonie przy użyciu PyGAD i wizualizacja wyników
- Ocena i walidacja rozwiązania, porównanie z innymi metodami optymalizacji

**Stos technologiczny:** Python, PyGAD

## Opis Techniczny oraz Prezentacja

Opis techniczny projektu oraz prezentacja z przedstawieniem projektu znajdują się w folderach `docs/technical-description` oraz `docs/slides`.

## Uruchamianie

1. Budowa obrazu dockera:
    ```
    docker compose build genetic-travelling-salesman
    ```

2. Uruchamianie kontenera dockera:
    ```
    make dc_bash
    ```

3. Uruchamianie testów:
    ```
    make test
   ```

4. Uruchamianie algorytmu genetycznego:
    ```
    python src/driver.py
    ```
