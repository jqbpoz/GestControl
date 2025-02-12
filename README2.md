# Sterowanie Głośnością i Jasnością Ekranu za Pomocą Dłoni

## Opis
Program umożliwia sterowanie głośnością lub jasnością ekranu za pomocą dłoni, bazując na odległości między palcem wskazującym a kciukiem, w zależności od wybranego trybu. Aplikacja oferuje możliwość pauzy oraz dynamicznej zmiany trybu działania. Użytkownik ma dostęp do GUI, w którym wyświetla się podgląd z kamerki, informacje oraz przyciski. Analiza obrazu (kształtu dłoni) jest realizowana na podstawie biblioteki OpenCV.

## Wymagania
- Python 3.x
- PyQt6
- opencv-python
- numpy
- mediapipe
- pycaw
- screen-brightness-control

## Instalacja
1. Zainstaluj wymagane biblioteki:
    ```sh
    pip install -r requirements.txt
    ```

## Uruchomienie
1. Uruchom aplikację:
    ```sh
    python main.py
    ```

2. W oknie aplikacji wybierz tryb (głośność lub jasność), a następnie użyj dłoni do sterowania.

## Autor
Jakub Poznański