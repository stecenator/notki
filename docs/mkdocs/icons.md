---
icon: fontawesome/solid/icons
---

# Ikony

Praca z ikonami ma dwa apstekyty:

=== "Ikona w tekscie"

	Jest prosta w uzyciu. Wystarczy użyć jej nazwy pomiedzy dwukropkami w tekscie, np: `:material-database-edit:` daje ikonę :material-database-edit:.

=== "Ikona dla strony"

	Trzeba ją podać w nagłówku dokumentu MarkDown:

    ``` title="Ustawianie ikony dla strony"
    ---
    icon: nazwa-ikony
    ---
    ```

## Ikony wbudowane

Używa się ich dość łatwo. Wystarczy znaleźć sobie coś wystarczająco ładnego [tutaj](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/) i kliknąć w wynik wyszukiwania. Samo się skopiuje i w normalnym tekscie MarkDown wystarczy to potem wkleić, np:

```
Pierdolnięty-uśmiechnięty :stuck_out_tongue_winking_eye:
```

Da taki efekt:

==Pierdolnięty-uśmiechnięty :stuck_out_tongue_winking_eye:==

### Ikony stron

Jeśli chcę mieć ikonę przy nawigacji (po lewej) na danej stronie muszę na poaczątku dokumentu MarkDown, umieścić sekcję:

``` title="Ustawianie ikony dla strony"
---
icon: nazwa-ikony
---
```

!!! Tip "Wskazówka"

	Jeśli w  [wyszukiwarce](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/) znalazłem np `:material-database-edit:` to  `material` jest nazwą kolekcji i de facto katalogiem, a `databse-edit` nazwą ikony, więc właściwa sekcja powinna wyglądać tak:

	```
	---
	icon: material/database-edit
	---
	```

	Czasem niestety katalogów jest więcej i trzeba trochę poeksperymentować, bo np ikona tej strony: :fontawesome-solid-icons:, w wyszukiwarce znajduej się jako `fontawesome-solid-icons` a w nagłówku strony trzeba było zastąpić wszystkie myślniki przez `/`:

	```
	---
	icon: fontawesome/solid/icons
	---
	```

## Własne ikony

Mogą trochę sprawić kłopotów, bo za osadzanie ikon dla stron i ikon w tekscie, odpowiadają inne mechanizmy w mkdocs. Żeby oba działały trzeba dodać poniższe elementy do `mkdocs.yml`:


```yaml hl_lines="3-9 12" title="Konfiguracja własnych ikon"
site_name: Marcinkowe mądrości
markdown_extensions:
    - pymdownx.emoji:
      emoji_index: !!python/name:material.extensions.emoji.twemoji
      emoji_generator: !!python/name:material.extensions.emoji.to_svg
      options:
        custom_icons:
          - overrides/.icons # (1)
          - .icons # (2)
theme:
  name: material
  custom_dir: overrides  # (3) Ważne! Włącza overrides dla seksji `icon:`s
```
{ .annotate. }

1. Z tego katalogu brane są ikony przy odwaołaniu w tekscie np `:ibm-eye-bee-m:` :ibm-eye-bee-m:.
2. Ten katalog jest sklejany z `custom_dir` przy wyszukiwaniu własnej ikony dla strony  w sekcji `icon:`.
3. Podstawowy katalog wyszukiwania katalogu z ikonami dla ston. 

!!! Warning "Ważne:"
    Jeśli ikony mają reagować na zmianę tematu pomiędzy ciemnym i jasnym, scieżki w SVG nie powinny mieć ustalonego koloru tylko atrybut `fill="currentColor"`. Przykładowa "pusta" ikona:

    ```xml
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="..." fill="currentColor"/>
    </svg>
    ```

### W tekscie

Własne ikony w tekscie  wstawia się tak samo jak wbudowane, czyli poprzez podanie ich nazwy, np ikonę `overrides/.icons/IBM-bw.svg`, czyli :IBM-bw:, wstawiam pisząc po prostu `:IBM-bw:` :shrug:. 

### Jako ikona strony

Mając skonfigurowany poprawnie `mkdocs.yml` własną ikonę dla strony ustawia się tak samo jak wbudowaną.