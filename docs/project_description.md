# Opis Techniczny Projektu: Rozwiązanie problemu komiwojażera z wykorzystaniem algorytmu genetycznego

## 1. Cel Projektu

Projekt ma na celu znalezienie najkrótszej możliwej ścieżki podróży między szeregiem miast przy pomocy algorytmu genetycznego, który poszukuje optymalnego rozwiązania problemu komiwojażera.\
Kod jest implementacją algorytmu w Pythonie przy użyciu biblioteki `pygad`.

## 2. Struktura Kodu

Kod projektu składa się z następujących głównych elementów:

- **Klasa `TravelGraph`**:
  - Odpowiada za zarządzanie miastami, reprezentację macierzy odległości oraz implementację metod związanych z wyszukiwaniem najkrótszej ścieżki.
- **Metody algorytmu genetycznego**:
  - `pygad.GA` jest używany do przeprowadzenia procesu optymalizacji.
- **Funkcje pomocnicze**:
  - `generate_random_distance_matrix` generuje macierz odległości
  - `main` obsługuje główną logikę wywoływania algorytmu.

## 3. Szczegóły Techniczne i Algorytmiczne

### 3.1. Reprezentacja Danych
- **Lista Miast (`city_names`)**: 
  - Zawiera nazwy miast, które są odwiedzane w ramach ścieżki podróży.
- **Macierz Odległości (`distance_matrix`)**:
  - Dwuwymiarowa macierz zawierająca odległości między każdym miastem. Macierz jest symetryczna, a odległość z miasta do siebie samego jest zerowa.

### 3.2. Algorytm Genetyczny
- **Inicjalizacja**: 
  - Tworzona jest populacja rozwiązań reprezentujących różne ścieżki między miastami.
- **Funkcja Dopasowania (`fitness_function`)**:
  - Oblicza sumaryczną odległość dla danej ścieżki (rozwiązania). Im mniejsza odległość, tym lepsze rozwiązanie (wartość minimalizowana).
- **Selekcja Rodziców**: 
  - Typ selekcji ${SSS}$ (Steady-State Selection) pozwala wybrać najlepszych rodziców z każdej generacji, którzy są przekazywani do następnych pokoleń.
- **Krzyżowanie**: 
  - Wybór krzyżowania jednopunktowego (`single_point`) pozwala losowo łączyć sekwencje genów dwóch rodziców w celu stworzenia nowych rozwiązań.
- **Mutacja**: `mutation_type="random"` 
  - Modyfikuje losowo wybrane geny w populacji potomków, co zapobiega wpadaniu algorytmu w lokalne minima.

### 3.3. Zapewnienie Prawidłowego Rozwiązania
- **Początek Ścieżki w Pierwszym Mieście**:
  - Metoda `ensure_start_from_first_city` przesuwa rozwiązanie tak, aby zawsze zaczynało się od pierwszego miasta (indeks $0$ ), co wymusza spójność ścieżek.

## 4. Generowanie Macierzy Odległości
- Funkcja `generate_random_distance_matrix` tworzy losową macierz odległości dla miast. Dla każdej pary miast odległość jest liczona jako losowa wartość, co pozwala na generowanie losowych scenariuszy testowych.

## 5. Parametry Algorytmu i Optymalizacja
- **Liczba Generacji (`num_generations`)**: 
  - Określa maksymalną liczbę iteracji, przez które przechodzi algorytm.
- **Wielkość Populacji (`sol_per_pop`)**: 
  - Odpowiada za liczbę potencjalnych rozwiązań w każdej generacji.
- **Przestrzeń Genów (`gene_space`)**:
  - Zapewnia, że geny przyjmują wartości tylko w zakresie dostępnych indeksów miast, bez powtórzeń w ścieżce.

## 6. Wynik i Analiza Rozwiązania
Algorytm kończy swoje działanie, zwracając:
- **Najlepszą Ścieżkę**: 
  - Lista nazw miast w optymalnej kolejności.
- **Odległość Najlepszej Ścieżki**: 
  - Całkowita długość tej trasy.

## 7. Przykładowe Uruchomienie

Po uruchomieniu programu, wywołana zostaje funkcja `main`, która:
- Generuje losową listę miast i macierz odległości.
- Tworzy instancję klasy `TravelGraph`.
- Wywołuje metodę `find_shortest_path`, która uruchamia algorytm genetyczny i wyświetla najkrótszą znalezioną ścieżkę oraz jej odległość.

