from django.test import TestCase

from backend.lispy.core import cons, EmptyList, BinOp, Env, SpecialForm, Symbol, PredOp
from backend.lispy.input_handler import parse
from backend.lispy.outhput_handler import show, eval_lisp


class BestTestCase(TestCase):
    def test_core(self):
        l1 = cons(1, 2)
        l2 = cons(1, EmptyList())
        l3 = cons(cons(1, 2), cons(3, 4))
        l4 = cons(1, cons(2, EmptyList()))
        l5 = cons(BinOp('+'), cons(7, cons(4, EmptyList())))
        l6 = cons(PredOp('<'), cons(1, cons(2, EmptyList())))
        l7 = cons(PredOp('>'), cons(1, cons(2, EmptyList())))
        l8 = cons(PredOp('and'), cons(True, cons(True, EmptyList())))
        l9 = cons(PredOp('and'), cons(True, cons(False, EmptyList())))
        l10 = cons(PredOp('or'), cons(False, cons(False, EmptyList())))
        l11 = cons(PredOp('or'), cons(False, cons(True, EmptyList())))
        l12 = cons(PredOp('or'), cons(True, cons(False, EmptyList())))

        l13 = cons(BinOp('*'), cons(10, cons(cons(BinOp('+'), cons(2, cons(3, EmptyList()))), EmptyList())))

        l14 = cons(SpecialForm('def'), cons(Symbol('a'), cons(3, EmptyList())))
        l15 = cons(Symbol('a'), EmptyList())
        l16 = cons(SpecialForm('def'), cons(Symbol('a'), cons('asd', EmptyList())))
        l17 = cons(Symbol('a'), EmptyList())

        l18 = cons(BinOp('+'), cons(cons(BinOp('+'), cons(2, cons(3, EmptyList()))), cons(3, EmptyList())))

        pre1 = cons(PredOp('>'), cons(1, cons(2, cons(3, EmptyList()))))
        pre2 = cons(PredOp('>'), cons(2, cons(1, cons(3, EmptyList()))))
        pre3 = cons(PredOp('and'), cons(cons(PredOp('>'), cons(6, cons(2, EmptyList()))), cons(pre1, EmptyList())))

        self.assertEqual(show(l1), '(1 2)'),
        self.assertEqual(show(l2), '(1 ())'),
        self.assertEqual(show(l3), '((1 2) (3 4))'),
        self.assertEqual(show(l4), '(1 2 ())'),
        self.assertEqual(show(l5), '(+ 7 4 ())'),
        self.assertEqual(show(l6), '(< 1 2 ())'),
        self.assertEqual(show(l7), '(> 1 2 ())'),
        self.assertEqual(show(l8), '(and True True ())'),
        self.assertEqual(show(l9), '(and True False ())'),
        self.assertEqual(show(l10), '(or False False ())'),
        self.assertEqual(show(l11), '(or False True ())'),
        self.assertEqual(show(l12), '(or True False ())'),
        self.assertEqual(show(l13), '(* 10 (+ 2 3 ()) ())'),

        self.assertEqual(show(l14), '(def a 3 ())'),
        self.assertEqual(show(l16), '(def a "asd" ())'),

        self.assertEqual(show(l18), '(+ (+ 2 3 ()) 3 ())'),

        self.assertEqual(show(pre1), '(> 1 2 3 ())'),
        self.assertEqual(show(pre2), '(> 2 1 3 ())'),
        self.assertEqual(show(pre3), '(and (> 6 2 ()) (> 1 2 3 ()) ())'),

        e = Env()
        self.assertEqual(eval_lisp(l5, e), 11),
        self.assertTrue(eval_lisp(l6, e)),
        self.assertFalse(eval_lisp(l7, e)),
        self.assertTrue(eval_lisp(l8, e)),
        self.assertFalse(eval_lisp(l9, e)),
        self.assertFalse(eval_lisp(l10, e)),
        self.assertTrue(eval_lisp(l11, e)),
        self.assertTrue(eval_lisp(l12, e)),
        self.assertEqual(eval_lisp(l13, e), 50),
        self.assertEqual(eval_lisp(l14, e), 'OK'),
        self.assertEqual(eval_lisp(l15, e), 3),
        self.assertEqual(eval_lisp(l16, e), 'OK'),
        self.assertEqual(eval_lisp(l17, e), 'asd'),
        self.assertEqual(eval_lisp(l18, e), 8),
        self.assertFalse(eval_lisp(pre1, e)),
        self.assertFalse(eval_lisp(pre2, e)),
        self.assertFalse(eval_lisp(pre3, e)),

    def input_test(self):
        e = Env()

        inp1 = parse('(1 2)')
        self.assertEqual(show(inp1), '(1 2 ())')

        inp2 = parse('(+ 1 2)')
        self.assertEqual(show(inp2), '(+ 1 2 ())')
        self.assertEqual(eval_lisp(inp2, e), 3)

        inp3 = parse('(1 2 3 4)')
        self.assertEqual(show(inp3), '(1 2 3 4 ())')

        inp4 = parse('(+ (+ 3 2) 3)')
        self.assertEqual(eval_lisp(inp4, e), 8)
        self.assertEqual(show(inp4), '(+ (+ 3 2 ()) 3 ())')

        inp5 = parse('(1 (4 5))')
        self.assertEqual(show(inp5), '(1 (4 5 ()) ())')

        eval_lisp(parse('(def a 10)'), e)
        self.assertEqual(eval_lisp(parse('(+ a 3)'), e), 13)

        eval_lisp(parse('(def b (lambda (x) (* x x)))'), e)
        self.assertEqual(eval_lisp(parse('(b 3)'), e), 9)

    def test_if(self):
        self.assertEqual(eval_lisp(parse('(if (< 3 5) (12) (22))'), Env()), 12)

    def test_cond(self):
        e = Env()
        p = parse('(cond ((< 3 1) 1) ((< 2 3) 2))')
        self.assertEqual(eval_lisp(p, e), 2)

    def test_fib(self):
        e = Env()
        fib = parse('(def fib (lambda (n) ('
                    'cond ((== n 1) 1)'
                    ' ((== n 0) 0)'
                    ' (else (+ (fib (- n 1)) (fib (- n 2)))))'
                    '))')
        self.assertEqual(show(
            fib),
            '(def fib (lambda (n ()) (cond ((== n 1 ()) (1 ())) ((== n 0 ()) (0 ())) (else (+ (fib (- n 1 ()) ()) '
            '(fib (- n 2 ()) ()) ()) ()) ()) ()) ())')
        eval_lisp(fib, e)
        exec_fib = parse('(fib 10)')
        self.assertEqual(eval_lisp(exec_fib, e), 55)

    def test_simple_coms(self):
        e = Env()

        emp = parse('(defn empty? (x) (and (== (car x) None) (== (cdr x) None)))')
        f = parse('(empty? (` (1 2)))')
        t = parse('(empty? ())')
        qua = parse(
            '(defn qua (x)('
            'if (empty? x)'
            '()'
            '(cons (* 2 (car x)) (qua (cdr x)))'
            '))'
        )
        q = parse('(qua (qua (` (1 3))))')
        eval_lisp(emp, e)
        eval_lisp(qua, e)
        self.assertFalse(eval_lisp(f, e))
        self.assertTrue(eval_lisp(t, e))
        self.assertEqual(show(eval_lisp(q, e)), '(4 12 ())')

    def test_macro(self):
        e = Env()
        p = parse('(def t (macro (x) (+ x x)))')
        c = parse('(t (+ 1 2))')
        eval_lisp(p, e)
        self.assertEqual(eval_lisp(c, e), 6)

    def test_high_order_func(self):
        e = Env()
        p = parse('(defn a (x)'
                  ' ((defn g (z) (+ z x)) (` g))'
                  ')')
        eval_lisp(p, e)
        c = parse('((a 7) 3)')
        self.assertEqual(eval_lisp(c, e), 10)

        e = Env()
        p = parse('(defn a (x)'
                  ' ((defn g () (+ 3 x)) (` g))'
                  ')')
        eval_lisp(p, e)
        c = parse('((a 1))')
        self.assertEqual(eval_lisp(c, e), 4)

    def test_quote(self):
        e = Env()
        p = parse('(defn a (x)'
                  ' ((defn g (z) (+ z x)) (` g))'
                  ')')
        eval_lisp(p, e)
        c = parse('((a 7) 3)')
        self.assertEqual(eval_lisp(c, e), 10)

        e = Env()
        p = parse('(defn a (x)'
                  ' ((defn g (z) (+ z x)) `g)'
                  ')')
        eval_lisp(p, e)
        c = parse('((a 7) 3)')
        self.assertEqual(eval_lisp(c, e), 10)
