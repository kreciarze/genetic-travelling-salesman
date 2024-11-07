# Przegląd projektu

**Temat:** Rozwiązanie problemu komiwojażera z wykorzystaniem algorytmu genetycznego

**Cele:** 

- Opracowanie bliskiego optimum rozwiązania problemu komiwojażera
- Implementacja algorytmu w Pythonie przy użyciu PyGAD i wizualizacja wyników
- Ocena i walidacja rozwiązania, porównanie z innymi metodami optymalizacji

**Stos technologiczny:** Python, PyGAD

# Programowanie i algorytmy genetyczne 

## Programowanie genetyczne

### Programowanie genetyczne, GP (ang. *genetic programming*)

Zautomatyzowana metoda mająca na celu tworzenie programów komputerowych w oparciu o ogólną definicję problemu. Innymi słowy programowanie genetyczne pozwala, w oparciu o wysokopoziomową definicję mówiącą co ma być zrobione, automatycznie stworzyć program, który owo zagadnienie rozwiąże. 

## Algorytmy genetyczne

::: columns
:::: {.column width=60%}

Algorytmy genetyczne to rodzaj algorytmów inspirowanych zasadami biologicznej ewolucji, które są wykorzystywane do rozwiązywania problemów optymalizacyjnych i poszukiwania rozwiązań w dużych przestrzeniach stanów. Działają one poprzez symulowanie procesu selekcji naturalnej, krzyżowania i mutacji, co pozwala na tworzenie coraz lepszych rozwiązań.

::::
:::: {.column width=40%}

![Algorytm genetyczny. \label{fig:alg-gen}](img/alg-genetyczny.png){width=85%}

::::
:::

---

Proces działania algorytmu genetycznego przedstawia rysunek \ref{fig:alg-gen} oraz może być opisany następująco:

- Inicjalizacja – na początku generuje się populację losowych rozwiązań (nazywanych osobnikami).
- Selekcja – wybiera się najlepsze osobniki na podstawie funkcji oceny, która określa ich jakość.
- Krzyżowanie (Crossover) – łączy się wybrane osobniki, tworząc nowe rozwiązania poprzez wymianę ich "genów".
- Mutacja – wprowadza się drobne, losowe zmiany do potomków, aby zapewnić różnorodność w populacji.
- Ewolucja – proces selekcji, krzyżowania i mutacji powtarza się wielokrotnie, aż do osiągnięcia zadowalającego rozwiązania.

Algorytmy genetyczne są szeroko stosowane w różnych dziedzinach, takich jak optymalizacja logistyczna, projektowanie, uczenie maszynowe, robotyka, a nawet sztuka. Pomimo że mogą wymagać dużej mocy obliczeniowej, są w stanie znaleźć dobre przybliżenia do rozwiązań nawet dla bardzo skomplikowanych problemów.

# Problem komiwojażera

### Problem komiwojażera (ang. Travelling Salesman Problem, TSP) 

Klasyczny problem optymalizacyjny, który polega na znalezieniu najkrótszej możliwej trasy, jaką musi pokonać komiwojażer (sprzedawca), aby odwiedzić każde z zadanych miast dokładnie raz i wrócić do punktu początkowego.

Formalnie, mając dany zbiór miast oraz odległości między każdą parą miast, należy wyznaczyć najkrótszy cykl Hamiltona w grafie, który reprezentuje połączenia między miastami. Przykładowe rozwiązanie prezentuje rysunek \ref{fig:komi-sample}. Problem komiwojażera jest zaliczany do klasy problemów NP-trudnych, co oznacza, że dla dużych zbiorów miast jego dokładne rozwiązanie staje się bardzo czasochłonne.

---

::: columns
:::: {.column width=60%}

**Zastosowanie**

Problem ten znajduje zastosowanie m.in. w logistyce, planowaniu tras transportowych i optymalizacji procesów produkcyjnych. Do jego rozwiązywania stosuje się różne podejścia, w tym algorytmy dokładne, przybliżone oraz heurystyczne, takie jak algorytmy genetyczne czy symulowane wyżarzanie.

::::
:::: {.column width=40%}

![Przykładowe rozwiązanie problemu komiwojażera \label{fig:komi-sample} ](img/traveling-salesman-problem.png){width=85%}

::::
:::


# Dziękujemy za uwagę

# Bibliografia

Leszek Rutkowski. Metody i techniki sztucznej inteligencji. PWN 2012
<!-- 
https://www.geeksforgeeks.org/genetic-algorithms/

[https://medium.com/@byanalytixlabs/a-complete-guide-to-genetic-algorithm-advantages-limitations-more-738e87427dbb](A Complete Guide to Genetic Algorithm — Advantages, Limitations & More) -->
