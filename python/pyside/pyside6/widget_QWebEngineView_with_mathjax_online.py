#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# See http://doc.qt.io/qt-5/qwebengineview.html#details

# This class replace the deprecated QWebView (based on QtWebKit).
# See:
# - https://stackoverflow.com/questions/29055475/qwebview-or-qwebengineview
# - https://wiki.qt.io/QtWebEngine/Porting_from_QtWebKit

HTML = r'''<!DOCTYPE html>
<html>
    <!-- Source: https://github.com/mathjax/MathJax/blob/master/test/sample-tex.html -->
    <head>
        <title>MathJax TeX Example</title>

        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />

        <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
                tex2jax: {inlineMath: [["$","$"],["\\(","\\)"]]}
            });
        </script>

        <!-- Install MathJax on Debian: "aptitude install libjs-mathjax" -->
        <!-- <script type="text/javascript" src='/usr/share/javascript/mathjax/MathJax.js?config=TeX-AMS_HTML-full'></script> -->
        <!-- <script type="text/javascript" src='MathJax/MathJax.js?config=TeX-AMS_HTML-full'></script> -->
        <script type="text/javascript" src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML-full'></script>

    </head>
    <body>

        <h2>Basics</h2>

        <p>
            Inline maths with $\LaTeX$ : $x \lt y$.
        </p>

        <p>
            When $a \ne 0$, there are two solutions to \(ax^2 + bx + c = 0\) and they are
            $$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$
        </p>

        <p>
            $$P(B|A) = \frac{P(A|B).P(B)}{P(A)}$$
        </p>


        <p>
            One line math block:
            $$n_{\mathrm{offset}} = \sum_{k=0}^{N-1} s_k n_k$$
        </p>


        <p>
            Multiple lines math block:
            $$
            (a + b)^2 = a^2 + 2ab + b^2 \\
            (a - b)^2 = a^2 - 2ab + b^2 \\
            \int_a^b f(x)dx \\
            V(x) = \max_{a \in \Gamma (x) } \{ F(x,a) + \beta V(T(x,a)) \}
            $$
        </p>

        <p>
            Symbols: $\alpha \beta \gamma \delta \epsilon \zeta \eta \theta \iota \kappa \lambda \mu \nu \xi \omicron \pi \rho \sigma \tau \upsilon \phi \chi \psi \omega$
        </p>

        <p>
            Symbols: $A B \Gamma \Delta E Z H \Theta I K \Lambda M N \Xi O \Pi P \Sigma T \Upsilon \Phi X \Psi \Omega$
        </p>


        <h2>Equation array</h2>

        $$
        \begin{eqnarray*}
            \mbox{Expectation of N} & = & \sum_{i=1}^{n} \mathbb{E}(Z_i) \\
                                    & = & \sum_{i=1}^{n} \frac{\gamma}{d^{\beta/2}} \frac{ c(d)^\beta }{i^{\alpha\beta}} \\
                                    & = & \frac{\gamma}{d^{\beta/2}} c(d)^\beta \sum_{i=1}^{n} \frac{1}{i^{\alpha\beta}} \\
                                    & = & z
        \end{eqnarray*}
        $$


        <h2>Arrays</h2>

        $$
        \begin{array}{cc}
            a & b \\
            c & c
        \end{array}
        $$


        <h2>Matrices</h2>
    
        $$
        A = \begin{pmatrix}
            a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
            a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
            \vdots  & \vdots  & \ddots & \vdots  \\
            a_{m,1} & a_{m,2} & \cdots & a_{m,n}
        \end{pmatrix}
        $$

        $$
        A = \begin{bmatrix}
            a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
            a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
            \vdots  & \vdots  & \ddots & \vdots  \\
            a_{m,1} & a_{m,2} & \cdots & a_{m,n}
        \end{bmatrix}
        $$


        <h2>Mathematical programming</h2>

        $$
        \begin{align}
            \max        & \quad z = 4 x_1 + 7 x_2    \notag \\
            \text{s.t.} & \quad 3 x_1 + 5 x_2 \leq 6 \label{constraint1}\\
                        & \quad   x_1 + 2 x_2 \leq 8 \label{constraint2}\\
                        & \quad   x_1, x_2 \geq 0    \notag
        \end{align}
        $$


        <h2>Systems of equation array</h2>

        $$
        f(n) = \left\{
            \begin{array}{ll}
                n/2      & \text{if $n$ is even} \\
                -(n+1)/2 & \text{if $n$ is odd}
            \end{array}
        \right.
        $$


        <h2>$\LaTeX$ fonts</h2>

        <h3>mathbb</h3>

        $$\mathbb{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$$

        <h3>mathbf</h3>

        $$\mathbf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$$
        $$\mathbf{abcdefghijklmnopqrstuvwxyz}$$

        <h3>mathtt</h3>

        $$\mathtt{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$$
        $$\mathtt{abcdefghijklmnopqrstuvwxyz}$$

        <h3>mathrm</h3>

        $$\mathrm{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$$
        $$\mathrm{abcdefghijklmnopqrstuvwxyz}$$

        <h3>mathsf</h3>

        $$\mathsf{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$$
        $$\mathsf{abcdefghijklmnopqrstuvwxyz}$$

        <h3>mathcal</h3>

        $$\mathcal{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$$
        $$\mathcal{abcdefghijklmnopqrstuvwxyz}$$

        <h3>mathfrak</h3>

        $$\mathfrak{ABCDEFGHIJKLMNOPQRSTUVWXYZ}$$
        $$\mathfrak{abcdefghijklmnopqrstuvwxyz}$$

    </body>
</html>
'''

# The next two lines are a workaround to fix an issue with QWebEngineView (see https://github.com/ContinuumIO/anaconda-issues/issues/9199#issuecomment-383842265)
import ctypes
ctypes.CDLL("libGL.so.1", mode=ctypes.RTLD_GLOBAL)

import sys
from PySide6.QtCore import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)

web = QWebEngineView()
web.setHtml(HTML)
web.show()

# The mainloop of the application. The event handling starts from this point.
# The exec_() method has an underscore. It is because the exec is a Python keyword. And thus, exec_() was used instead.
exit_code = app.exec_()

# The sys.exit() method ensures a clean exit.
# The environment will be informed, how the application ended.
sys.exit(exit_code)
