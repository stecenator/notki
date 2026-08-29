---
icon: material/robot-industrial
---

# IBM TS4500

Mądrości związane z biblioteką :IBM-bw: TS4500.

## Najważniejsze fakty

Rożnice w stosunku do wszelkiej maści magnetowidów w stylu TS4300.

- __Element address__ - nie jest już unikalny. W wirtualnych bibliotekach numeracja napędów zaczyna się od 257. Daltego, mając np dwie wirtualane biblioteki w jednej fizucznej mamy de-facto dwa napędy o element addressie 257. Dlatego z przeszedłem z konwencją nazewniczą na notację: `drv-f1c2r3`, która znaczy mniej więcej to:


    ```mermaid
    flowchart LR
        A["drv-f1c2r3"] --> B["drv\njakiś prefix, np. biblioteki wirtualnej"]
        A --> C["f1\nszafa 1"]
        A --> D["c2\nkolumna 2"]
        A --> E["r3\nrząd 3"]

    ```



    !!! tip 
        Taki zapis daje unikalną identyfikację napędu. Przy zachowaniu tej samej notacji w Protect, OS i zoningu daje spójny obraz całości, który łatwiej się debuguje.

- __Volrange zamiast slotów__ - Wszystkie sloty, wirtualne. Taśmy do biblioteki logicznej przypiuje się na podstawie zakresów etykiet, czyli _volrange_. 
- __Non Customer Setup__ - te pudła mogą być skręcane wyłącznie przez namaszczonych braminów. Ja wchodzę, gdzy wszystko jest pod prądem i ma IP. 
- __Przestrzeń serwisowa__ - jest bardzo ważna. Trzeba ją zaplanować ze sporym zapasem. I trzeba zaplanować wzrost, bo są to bodajże najczęściej rozbudowywane urządzenia jakie widziałem. 
- __Wkładanie taśm__ - w działającej bibliotece wyłacznie przez _I/O Station_. We wdrażanej, pewnie wygodniej wyłączyć, otworzyć i ręcznie powpychać do slotów. 

    !!! Warning "Uwaga!"
        Pogadaj z inżynierem i spytaj, do których kolumn można wkładać taśmy, bo w zależności od wyboru miejsca parkowania robota, niektóre kolumny będą niedostępne. __Nie ruszaj też taśm serwisowych!__

- __Partycje__ - czyli biblioteki logiczne tworzy się poprzez przypisanie do nich napędów i zakresów (_volrange_) taśm. 
- __Kompatybilność LTO__ - niestety nie jest już prawdą, że w nowych napędach LTO można czytać dwie generacje wstecz a pisać jedną. To było prawdą do LTO7, a potem się popieprzyło. Dlatego do LTO7 można było mieszać w jednej bibliotece logicznej napędy np LTO6 i LTO7 i taki TSM/Protect sobie z tym radził: wystarczyło stworzyć dwie _devclassy_: `format=ULTRIUM7` i `format=ULTRIUM6` i :guitar:. Teraz lepiej dla każdej klasy taśm stworzyć oddzielną bibliotekę logiczną.
- __VOLSER RANGE__ - przy pierwszym uruchomieniu, zwykle definiuje się jeden zakres: `000000` - `ZZZZZZ`, któ©y jest fajny bo łapie wszytkie taśmy. Kłopot pojawia się gdy trzeba przypisać inne taśmy do innej biblioteki. Wtedy trzeba zmodyfikować ten zakres, bo w przeciwnym wypadku będzie próbował np przypisać taśmy LTO10 do biblioteki z napędami LTO8.