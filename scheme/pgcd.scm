; Usage: guile pgcd.scm

(define (pgcd a b)
    (display "a=") (display a) (display " - b=") (display b) (newline)
    (cond ((> b a) (pgcd b a))
        ((zero? b) a)
        (else (pgcd b (modulo a b)))))

(display (pgcd 80 120))
(newline)
