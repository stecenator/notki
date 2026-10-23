#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IBM Storage Protect (TSM) Post-Installation Documentation Command Executor
-------------------------------------------------------------------------
Ten skrypt automatyzuje uruchamianie listy poleceń administracyjnych w jednej
sesji dsmadmc, co pozwala na jednorazowe uwierzytelnienie za pomocą hasła i 2FA (MFA).
Wyniki poleceń są przechwytywane i zapisywane do czytelnego pliku raportu,
który stanowi część generatora dokumentacji poinstalacyjnej.

Bezpieczeństwo:
- Hasło i token TOTP (2FA) NIE są przekazywane jako argumenty linii poleceń (CLI).
- Są one pobierane ze zmiennych środowiskowych (DSM_PASSWORD, DSM_TOTP) lub
  interaktywnie od użytkownika w bezpieczny sposób (getpass).
"""

import os
import sys
import re
import getpass
import argparse
from datetime import datetime

try:
    import pexpect
except ImportError:
    print("Błąd: Biblioteka 'pexpect' jest wymagana do uruchomienia tego skryptu.", file=sys.stderr)
    print("Zainstaluj ją za pomocą: pip install pexpect", file=sys.stderr)
    sys.exit(1)


def clean_ansi_codes(text):
    """
    Usuwa kody kontrolne ANSI i sekwencje sterujące terminala z tekstu,
    aby wynikowy plik raportu był czystym tekstem ASCII/UTF-8.
    """
    if not text:
        return ""
    # Regex usuwający standardowe sekwencje ANSI Escape
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    cleaned = ansi_escape.sub('', text)
    
    # Dodatkowe oczyszczenie z powrotów karetki (\r) bez nowej linii
    cleaned = cleaned.replace('\r\n', '\n').replace('\r', '\n')
    return cleaned


def read_commands_file(filepath):
    """
    Odczytuje polecenia do wykonania z pliku, ignorując puste linie oraz komentarze.
    """
    if not os.path.exists(filepath):
        print(f"Błąd: Plik z komendami '{filepath}' nie istnieje.", file=sys.stderr)
        sys.exit(1)
        
    commands = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()
                if line_stripped and not line_stripped.startswith('#'):
                    commands.append(line_stripped)
    except Exception as e:
        print(f"Błąd podczas odczytu pliku '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)
        
    if not commands:
        print(f"Ostrzeżenie: Plik '{filepath}' nie zawiera żadnych poleceń do wykonania.", file=sys.stderr)
        
    return commands


def run_dsmadmc_session(dsm_path, user_id, password, totp, commands, dsm_args, prompt_regex):
    """
    Uruchamia jedną sesję dsmadmc przy użyciu pexpect, loguje się (hasło + 2FA),
    wykonuje podane polecenia i zbiera ich wyjście.
    """
    # Zgodnie z dokumentacją IBM Storage Protect:
    # TOTP (Time-based One-Time Password) jest doklejany bezpośrednio na końcu hasła administratora:
    # dsmadmc -id=admin -password=<adminpwd><authentication_token>
    # Ze względów bezpieczeństwa nie podajemy hasła w CLI (by nie było widoczne w 'ps'),
    # lecz przesyłamy je bezpiecznie do procesu dsmadmc w odpowiedzi na prompt o hasło.
    full_password = password + totp
    
    # Przygotowanie argumentów do dsmadmc
    cmd_args = []
    if user_id:
        cmd_args.append(f"-id={user_id}")
    
    # Dodatkowe argumenty dla dsmadmc przekazane przez użytkownika
    if dsm_args:
        import shlex
        cmd_args.extend(shlex.split(dsm_args))
        
    print(f"[*] Uruchamianie klienta administracyjnego: {dsm_path} {' '.join(cmd_args)}")
    
    # Wymuszamy angielskie locale (en_US.UTF-8), aby dsmadmc komunikował się w standardowym języku angielskim
    import os
    env = os.environ.copy()
    env["LC_ALL"] = "en_US.UTF-8"
    env["LANG"] = "en_US.UTF-8"
    
    try:
        # Uruchamiamy proces w pexpect z kodowaniem UTF-8 i wymuszonym en_US locale
        child = pexpect.spawn(dsm_path, cmd_args, encoding='utf-8', timeout=30, env=env)
        # Ustawiamy ogromny rozmiar okna wirtualnego terminala, aby wyeliminować paginację (scroll prompt)
        child.setwinsize(10000, 200)
    except pexpect.exceptions.ExceptionPexpect as e:
        print(f"[-] Krytyczny błąd podczas próby uruchomienia '{dsm_path}': {e}", file=sys.stderr)
        return None

    # Prompty logowania i oczekiwane zdarzenia
    # 0: Prompt o hasło
    # 1: Prompt o hasło (niemiecki/inne wersje językowe)
    # 2: Prompt o login (jeśli dsmadmc nie dostał go w parametrze)
    # 3: Pomyślne zalogowanie (wykrycie promptu administracyjnego)
    # 4: Błędy uwierzytelniania lub połączenia (np. kody ANSxxxxx)
    # 5: Błąd "invalid" w tekście
    # 6: EOF (nieoczekiwany koniec procesu)
    login_prompts = [
        r'(?i)password\s*:', 
        r'(?i)passwort\s*:', 
        r'(?i)user\s*id\s*:',
        prompt_regex,
        r'ANS[0-9]+[EW]',
        r'(?i)invalid',
        pexpect.EOF
    ]
    
    logged_in = False
    
    while not logged_in:
        try:
            index = child.expect(login_prompts, timeout=15)
            if index in (0, 1):
                print("[*] Wykryto prompt o hasło. Wysyłanie skonsolidowanego hasła z tokenem 2FA...")
                child.sendline(full_password)
            elif index == 2:
                print(f"[*] Wykryto prompt o User ID. Wysyłanie: {user_id}")
                child.sendline(user_id)
            elif index == 3:
                print("[+] Uwierzytelnienie powiodło się! Wykryto sesję administracyjną.")
                logged_in = True
            elif index in (4, 5):
                # Błąd logowania lub połączenia
                error_output = child.before + child.after if child.after else child.before
                cleaned_error = clean_ansi_codes(error_output).strip()
                print(f"[-] Błąd logowania lub błąd serwera: {cleaned_error}", file=sys.stderr)
                child.close()
                return None
            elif index == 6:
                # EOF przed zalogowaniem
                output = child.before if child.before else ""
                cleaned_output = clean_ansi_codes(output).strip()
                print(f"[-] Proces dsmadmc zakończył się nieoczekiwanie przed zalogowaniem:\n{cleaned_output}", file=sys.stderr)
                return None
        except pexpect.exceptions.TIMEOUT:
            print("[-] Przekroczono limit czasu (timeout) podczas oczekiwania na logowanie.", file=sys.stderr)
            child.close()
            return None
            
    # Słownik na wyniki komend
    results = {}
    
    # Wykonujemy komendy kolejno
    for cmd in commands:
        cmd_stripped = cmd.strip()
        print(f"[*] Wykonuję polecenie: '{cmd_stripped}'...")
        
        # Wysyłamy polecenie do dsmadmc
        child.sendline(cmd_stripped)
        
        try:
            # Czekamy na powrót promptu administracyjnego (z dużym timeoutem na ciężkie zapytania)
            child.expect(prompt_regex, timeout=120)
            
            # child.before zawiera cały output polecenia wygenerowany przed pojawieniem się nowego promptu
            raw_output = child.before
            clean_output = clean_ansi_codes(raw_output)
            
            # Pexpect emuluje tty, więc pierwsza linia wyjścia to zazwyczaj echo naszej komendy.
            # Usuwamy echo polecenia z początku wyjścia, aby raport był czysty.
            lines = clean_output.splitlines()
            if lines:
                # Jeśli pierwsza linia zawiera polecenie, usuwamy ją
                if cmd_stripped in lines[0] or (len(lines) > 1 and cmd_stripped in lines[1]):
                    # Bezpieczne usunięcie linii echa
                    start_idx = 1 if cmd_stripped in lines[0] else 2
                    lines = lines[start_idx:]
                    
            # Zapisujemy oczyszczony wynik
            results[cmd_stripped] = "\n".join(lines).strip()
            print(f"[+] Polecenie '{cmd_stripped}' zakończone sukcesem.")
            
        except pexpect.exceptions.TIMEOUT:
            print(f"[!] Ostrzeżenie: Przekroczono limit czasu dla polecenia: {cmd_stripped}", file=sys.stderr)
            results[cmd_stripped] = "[BŁĄD: Przekroczono limit czasu (timeout) wykonania polecenia]"
        except pexpect.exceptions.EOF:
            print(f"[-] Krytyczny błąd: Proces dsmadmc zakończył się nieoczekiwanie podczas polecenia: {cmd_stripped}", file=sys.stderr)
            results[cmd_stripped] = "[BŁĄD: Proces dsmadmc zakończył się nieoczekiwanie]"
            break

    # Prawidłowe wyjście z sesji dsmadmc
    print("[*] Zamykanie sesji dsmadmc...")
    try:
        child.sendline("quit")
        child.expect(pexpect.EOF, timeout=5)
    except Exception:
        pass
    finally:
        child.close()
        
    return results


def write_results_to_file(filepath, results):
    """
    Zapisuje zebrane wyniki poleceń do pliku wyjściowego w czytelnym formacie.
    """
    try:
        # Tworzenie pliku z uprawnieniami tylko dla właściciela (0o600) ze względów bezpieczeństwa
        mode = 0o600
        flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
        
        def opener(path, flags):
            return os.open(path, flags, mode)
            
        with open(filepath, 'w', encoding='utf-8', opener=opener) as f:
            f.write("=" * 80 + "\n")
            f.write("IBM Storage Protect (TSM) - Raport z wykonania poleceń poinstalacyjnych\n")
            f.write(f"Wygenerowano: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for cmd, output in results.items():
                f.write("=" * 80 + "\n")
                f.write(f"POLECENIE: {cmd}\n")
                f.write("=" * 80 + "\n")
                f.write(output + "\n\n")
                
        print(f"[+] Wyniki zostały pomyślnie zapisane do pliku: {filepath}")
    except Exception as e:
        print(f"[-] Błąd podczas zapisu raportu do pliku '{filepath}': {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Automatyczne wykonywanie poleceń IBM Storage Protect (TSM) w jednej sesji dsmadmc (obsługa 2FA).",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "-u", "--user",
        help="ID administratora (domyślnie: pobierane ze zmiennej środowiskowej DSM_USER lub pytane interaktywnie)"
    )
    parser.add_argument(
        "-i", "--input",
        default="dsm_cmd.txt",
        help="Ścieżka do pliku z poleceniami (domyślnie: dsm_cmd.txt)"
    )
    parser.add_argument(
        "-o", "--output",
        default="dsm_out.txt",
        help="Ścieżka do pliku wynikowego (domyślnie: dsm_out.txt)"
    )
    parser.add_argument(
        "--dsm-path",
        default="dsmadmc",
        help="Ścieżka do pliku wykonywalnego dsmadmc (domyślnie: dsmadmc)"
    )
    parser.add_argument(
        "--args",
        default="-dataonly=yes -scrollprompt=no",
        help="Dodatkowe argumenty przekazywane do dsmadmc (domyślnie: '-dataonly=yes -scrollprompt=no')"
    )
    parser.add_argument(
        "--prompt-regex",
        default=r'(?i)(tsm:\s*[a-z0-9_\-]+>|protect:\s*[a-z0-9_\-]+>|tsm>|protect>)\s*$',
        help="Niestandardowy regex do wykrywania promptu dsmadmc"
    )

    args = parser.parse_args()

    # 1. Pobranie nazwy użytkownika
    user_id = args.user or os.environ.get("DSM_USER")
    if not user_id:
        user_id = input("Podaj ID administratora TSM: ").strip()
        if not user_id:
            print("[-] ID administratora nie może być puste.", file=sys.stderr)
            sys.exit(1)

    # 2. Pobranie hasła (zmienna środowiskowa lub interaktywnie)
    password = os.environ.get("DSM_PASSWORD")
    if not password:
        password = getpass.getpass("Podaj hasło administratora TSM: ")
        if not password:
            print("[-] Hasło nie może być puste.", file=sys.stderr)
            sys.exit(1)

    # 3. Pobranie tokenu 2FA/TOTP (zmienna środowiskowa lub interaktywnie)
    totp = os.environ.get("DSM_TOTP")
    if totp is None:
        totp = getpass.getpass("Podaj kod TOTP (MFA/2FA) [wciśnij Enter jeśli brak]: ").strip()

    # 4. Odczyt poleceń z pliku dsm_cmd.txt
    commands = read_commands_file(args.input)
    if not commands:
        print("[-] Brak poleceń do wykonania. Zakończono.", file=sys.stderr)
        sys.exit(0)

    print(f"[*] Wczytano {len(commands)} poleceń do wykonania.")

    # 5. Uruchomienie sesji dsmadmc i wykonanie poleceń
    results = run_dsmadmc_session(
        dsm_path=args.dsm_path,
        user_id=user_id,
        password=password,
        totp=totp,
        commands=commands,
        dsm_args=args.args,
        prompt_regex=args.prompt_regex
    )

    # 6. Zapisanie wyników do pliku dsm_out.txt
    if results:
        write_results_to_file(args.output, results)
        print("[+] Zadanie zakończone sukcesem!")
    else:
        print("[-] Nie udało się wygenerować raportu z powodu wcześniejszych błędów.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
