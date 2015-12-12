; Usage: guile factorielle_optim.scm

(define (fact n)
    (define (fact2 n m)
        (if (= n 1)
            m
            (fact2 (- n 1) (* m n))))
    (fact2 n 1))

(display (fact 10))
(newline)
