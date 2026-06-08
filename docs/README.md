---
icon: material/home
---

# notki

!!! Warning ":fontawesome-solid-person-digging: Uwaga! :fontawesome-solid-person-digging:"
	Ta strona jest praktycznie zwasze "Under construction" :wink:
	<br><br>
	![Under construction](assets/under-construction.svg) (1)
	{ .annotate }

	1. Tę grafikę ściągnąłem [stąd](https://freesvg.org/under-construction-road-sign)

Podczas mojej podnad cwierćwiecznej pracy w :IBM-bw: z [niebieskimi](https://ibm.com) technologiami, czy podczas wypasu pingwinów :fontawesome-brands-linux:, lub antylop GNU :gnu:, czasami wymyślę coś czego, nie chę wymyślać drugi raz. Wtedy wrzucam to tutaj. Kiedyś ten projekt leżał wyłącznie na GitHubie, ale postanowiłem go "ukompatybilnić" z `mkdocs`, stąd umieszczenie wszystkiego w podkatalogu `docs`.

Pliki `README.md` utrzymuję dla zgodnośći z GitHubem, ale struktura plików i katalogów jest dostosowana do serwowania moich mądrośći bezpośrednio z `mkdocs`, które samo robi np spis treśći i nawigację po nagłówkach. Niestety wkradł się tu lekki bałagan i gdzieniegdzie są pliki `index.md`, ale pewnie wrócę to `README.md`. 


## Ansible

Rożne [tricki ansiblowe](ansible/index.md), które wyłowiłem z internetów, podpowiedział mi AI, a czasem nawet coś z mojej głowy.

## AIX

Tu jeszcze nic nie ma 

## Git

Najcześciej zpaminane komeny [Gita](git/index.md) i GitHuba :fontawesome-brands-github:.

## IBM Storage Scale (GPFS)

Ostatnio sporo dłubię przy [Storage Scale/GPFS](GPFS/index.md). Sukcesywnie będę tu odkładać tę wiedzę.

## IBM Storage Protect (TSM)

TSM, Spectrum Protect, [Storage Protect](ISP/README.md), a kto wie... Może i Storage Defender. 
Na ADSM się nie załapałem :wink:. 


## Linux

[Linux](LNX/README.md)

## mkdocs

Cała ta dokumentacja jest stworzona przy pomocy pakietu [mkdocs/metrial](https://squidfunk.github.io/mkdocs-material/reference/). System wydaje się prosty, ale jest w nim kilka niebanalnych zadziorów, które staram się opisywać na bieżąco.

[mkdocs](mkdocs/index.md)

## Power

Zaczątki dokumentacji dla [IBM Power](Power/index.md)

## Wirtualizacja PC-XT

[KVM/Qemu/LibVirt](virt/README.md)

## WinDOS


## Pomysły na przyszłość

Zgłaszać jako _issues_ do [tego projektu](https://https://github.com/stecenator/notki)

# Technikalia

Rzeczy związane z prowadzeniem tego dzienniczka.

- Wszlekie pliki konfiguracyjne staram się trzymać/przenosić do katalogu `templates/` a potem odnosić się do nich w tekscie poprzez `---8<--- "templates/plik"`