import tkinter as tk
from tkinter import ttk
import math
# ---------------------------
# Safe eval environment setup
# ---------------------------
def make_math_env(degrees_mode: tk.BooleanVar):
    """
    Return a dict of safe names for eval().
    sin/cos/tan obey degrees_mode.
    """
    def sin_fn(x):
        return math.sin(math.radians(x)) if degrees_mode.get() else math.sin(x)
    def cos_fn(x):
        return math.cos(math.radians(x)) if degrees_mode.get() else math.cos(x)
    def tan_fn(x):
        return math.tan(math.radians(x)) if degrees_mode.get() else math.tan(x)

    return {
        # math functions (safe)
        'sin': sin_fn,
        'cos': cos_fn,
        'tan': tan_fn,
        'sqrt': math.sqrt,
        'log': lambda x: math.log10(x),
        'ln': math.log,
        'abs': abs,
        'round': round,
        # constants
        'pi': math.pi,
        'e': math.e,
        # allow basic builtins if needed (kept minimal)
        '__builtins__': None
    }

# ---------------------------
# Calculator GUI
# ---------------------------
class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scientific Calculator")
        self.geometry("420x640")
        self.resizable(False, False)
        self.config(bg="#2C2F33")

        self.expression = ""        # displayed expression string
        self.screen_var = tk.StringVar()
        self.deg_mode = tk.BooleanVar(value=True)  # default: Degrees

        self._build_ui()

    def _build_ui(self):
        # Display
        entry = tk.Entry(self, textvariable=self.screen_var,
                         font=("Consolas", 22, "bold"), bd=10,
                         relief=tk.RIDGE, bg="#23272A", fg="white",
                         justify="right", insertbackground="white")
        entry.pack(padx=12, pady=(18, 8), ipady=14, fill="x")

        # Degree/Radian toggle
        mode_frame = tk.Frame(self, bg="#2C2F33")
        mode_frame.pack(fill="x", padx=12)
        deg_radio = ttk.Radiobutton(mode_frame, text="Degrees", value=True, variable=self.deg_mode,
                                    command=self._update_mode)
        rad_radio = ttk.Radiobutton(mode_frame, text="Radians", value=False, variable=self.deg_mode,
                                    command=self._update_mode)
        deg_radio.pack(side="left", padx=(0,8))
        rad_radio.pack(side="left")

        # Buttons area
        btn_frame = tk.Frame(self, bg="#2C2F33")
        btn_frame.pack(padx=12, pady=12, fill="both", expand=True)

        # Layout rows (button labels). Functions insertion should add '(' where appropriate.
        rows = [
            ['C', '(', ')', '/', 'sqrt'],
            ['7', '8', '9', '*', 'log'],
            ['4', '5', '6', '-', 'ln'],
            ['1', '2', '3', '+', 'abs'],
            ['0', '.', '=', '%', 'pi'],
            ['sin', 'cos', 'tan', 'e', 'Ans']
        ]

        # create buttons
        for r in rows:
            row_frame = tk.Frame(btn_frame, bg="#2C2F33")
            row_frame.pack(expand=True, fill="both")
            for label in r:
                self._make_button(row_frame, label).pack(side="left", expand=True, fill="both", padx=4, pady=4)

        # footer
        footer = tk.Label(self, text="Designed by Shreyash", font=("Arial", 9),
                          bg="#2C2F33", fg="#99AAB5")
        footer.pack(pady=(6,10))

        # keep last answer
        self.last_answer = None

    def _make_button(self, parent, text):
        color_map = {
            'C': "#FF6B6B",
            '=': "#4ECDC4",
            'pi': "#F6E05E",
            'e': "#F6E05E",
            'sin': "#57F287",
            'cos': "#57F287",
            'tan': "#57F287",
            'sqrt': "#57F287",
            'log': "#57F287",
            'ln': "#57F287",
            'Ans': "#9FA8DA",
        }
        bg = color_map.get(text, "#99AAB5")
        btn = tk.Button(parent, text=text, font=("Consolas", 14, "bold"),
                        bd=2, bg=bg, fg="black", relief=tk.GROOVE,
                        activebackground="#7289DA", activeforeground="white",
                        height=2)

        if text == 'C':
            btn.config(command=self._clear)
        elif text == '=':
            btn.config(command=self._evaluate)
        elif text in ('sin', 'cos', 'tan', 'sqrt', 'log', 'ln'):
            # insert function name with opening paren
            btn.config(command=lambda t=text: self._insert(f"{t}("))
        elif text in ('pi', 'e'):
            btn.config(command=lambda t=text: self._insert(t))
        elif text == 'Ans':
            btn.config(command=lambda: self._insert(str(self.last_answer) if self.last_answer is not None else "0"))
        else:
            btn.config(command=lambda t=text: self._insert(t))

        return btn

    def _insert(self, tok: str):
        """Insert token into expression and update display."""
        self.expression += str(tok)
        self.screen_var.set(self.expression)

    def _clear(self):
        self.expression = ""
        self.screen_var.set("")

    def _update_mode(self):
        # No action required except to change behavior in eval environment.
        mode = "Degrees" if self.deg_mode.get() else "Radians"
        # optional: show small suffix in display
        # we won't change expression; just print mode in title bar
        self.title(f"Scientific Calculator - {mode}")

    def _evaluate(self):
        if not self.expression:
            return
        # prepare safe eval environment based on current degree/radian mode
        env = make_math_env(self.deg_mode)
        try:
            # Replace percentage operator (%) with /100
            expr = self.expression.replace('%', '/100')
            # Evaluate expression safely
            result = eval(expr, env)
            # format result (avoid long floating repr)
            if isinstance(result, float):
                # trim trailing zeros
                result_str = f"{result:.12g}"
            else:
                result_str = str(result)
            self.screen_var.set(result_str)
            self.last_answer = result
            self.expression = result_str  # allow chaining
        except Exception as e:
            self.screen_var.set("Error")
            self.expression = ""

if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop()
