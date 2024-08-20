import cv2

# Webcam initialisieren
cap = cv2.VideoCapture(0)


# Setze die Auflösung auf 1920x1080 Pixel

while True:
    # Frame von der Webcam lesen
    ret, frame = cap.read()

    # Überprüfen, ob das Frame korrekt gelesen wurde
    if not ret:
        print("Konnte das Frame nicht lesen. Beende...")
        break

    # Zeige das Frame in einem Fenster an
    cv2.imshow("Webcam", frame)
    cv2.resize(frame, (1920, 1080))

    # Warte auf die Taste 'q', um die Webcam zu schließen
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Freigeben der Webcam und Schließen aller Fenster
cap.release()
cv2.destroyAllWindows()
