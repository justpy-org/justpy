# Justpy Tutorial demo eq_test from docs/tutorial/equations.md
import justpy as jp

integral = r"""
\f\relax{x} = \int_{-\infty}^\infty \f\hat\xi\,e^{2 \pi i \xi x} \,d\xi
"""

f1 = r"""
     a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
     \sum_{k=0}^{n-1} ar^k =
     a \left(\frac{1-r^{n}}{1-r}\right)
     """

f2 = r"""
\displaystyle \frac{1}{\Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}} = 1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}} {1+\frac{e^{-8\pi}} {1+\cdots} } } }
"""


async def button_click(self, msg):
    wp = msg.page
    wp.eq1.equation += " +  \\sqrt{d} + 1"


def eq_test(request):
    wp = jp.WebPage()
    wp.btn = jp.Button(
        text="Modify Equation",
        click=button_click,
        a=wp,
        classes=jp.Styles.button_simple + " m-2 p-2",
    )
    wp.eq1 = jp.Equation(
        equation="c = \\pm\\sqrt{a^2 + b^2 + c^2}", classes="text-3xl m-2 p-2", a=wp
    )
    # Add a macro
    eq2 = jp.Equation(equation=integral, classes="text-3xl m-2 p-2", a=wp)
    eq2.options["macros"]["\\f"] = "#1f(#2)"
    jp.Equation(equation=f1, classes="text-3xl m-2 p-2", a=wp)
    jp.Equation(equation=f2, classes="text-3xl m-2 p-2", a=wp)
    # Use raw strings when convenient
    jp.Equation(
        equation="c = \\pm\\sqrt{a^2 + b^2}\\in\\RR",
        options={"macros": {"\\RR": "\\mathbb{R}"}},
        classes="text-3xl m-2 p-2",
        a=wp,
    )
    jp.Equation(
        equation=r"e = \pm\sqrt{c^2 + d^2}\in\RR",
        options={"macros": {"\\RR": "\\mathbb{R}"}},
        classes="text-3xl m-2 p-2",
        a=wp,
    )
    # You can also add equations using the WebPage equation method
    wp.equation(r"e^{i\pi}+1=0")
    a = wp.equation(r"e^{i\pi}+1=0")
    a.classes = "bg-blue-500 text-5xl text-white m-2 p-4 inline-block"
    return wp


# You can also add KATEX = True to justpy.env instead of specifying below
# initialize the demo
from examples.basedemo import Demo

Demo("eq_test", eq_test, KATEX=True)
