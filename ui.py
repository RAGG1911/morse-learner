import tkinter as tk
from tkinter import ttk
from data import get_display_data, get_morse
from storage import load_favourites, load_mastery, get_mastery_level
from audio import play_char

MASTERY_COLORS = {
    'unseen': '#B4B2A9',
    'learning': '#EF9F27',
    'mastered': '#1D9E75',
}

class MorseDictionary(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Morse Code Dictionary')
        self.configure(bg='#f9f9f9')
        self.resizable(True, True)
        
        self._all_cards = get_display_data()
        self._favourites = load_favourites()
        self._mastery = load_mastery()
        self._card_size = 'expanded'

        self._build_ui()
        self._render_cards(self._all_cards)

    def _build_ui(self):
        toolbar = tk.Frame(self, bg='#f9f9f9', pady=8, padx=12)
        toolbar.pack(fill='x')

        tk.Label(toolbar, text='Morse Dictionary', 
                 font=('Helvetica', 16, 'bold'), 
                 bg='#f9f9f9').pack(side='left')
        
        self._size_btn = tk.Button(
            toolbar, text='Compact View',
            command=self._toggle_card_size,
            relief='groove', padx=8
        )

        self._size_btn.pack(side='right', padx=4)

        container = tk.Frame(self, bg='#f9f9f9')
        container.pack(fill='both', expand=True, padx=12, pady=4)

        canvas = tk.Canvas(container, bg='#f9f9f9', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        self._grid_frame = tk.Frame(canvas, bg='#f9f9f9')
        self._canvas_window = canvas.create_window(
            (0, 0), window=self._grid_frame, anchor='nw'
        )

        self._grid_frame.bind('<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
            lambda e: canvas.itemconfig(self._canvas_window, width=e.width))
        canvas.bind_all('<MouseWheel>',
            lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))
        
        self._canvas = canvas

    def _render_cards(self, data):
        for widget in self._grid_frame.winfo_children():
            widget.destroy()
        cols = 6 if self._card_size == 'compact' else 4

        for i, (char, morse, category) in enumerate(data):
            row, col = divmod(i, cols)
            card = self._make_card(char, morse, category)
            card.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')
        
        for c in range(cols):
            self._grid_frame.columnconfigure(c, weight=1)

    def _make_card(self, char, morse, category):
        mastery_data = self._mastery.get(char, {})
        mastery_level = get_mastery_level(mastery_data)
        mastery_color = MASTERY_COLORS[mastery_level]
        is_expanded = self._card_size == 'expanded'

        card = tk.Frame(
            self._grid_frame, bg='white', relief='solid',
            bd=1, padx=10, pady=8
        )

        tk.Label(
            card, text=char, 
            font=('Helvetica', 22 if is_expanded else 14, 'bold'),
            bg='white'
        ).pack()

        if is_expanded:
            dot_dash_frame = tk.Frame(card, bg='white')
            dot_dash_frame.pack(pady=4)
            self._draw_morse_symbols(dot_dash_frame, morse)

            tk.Label(
                card, text=morse, font=('Courier', 11),
                fg='#888780', bg='white'
            ).pack()

        tk.Frame(card, bg=mastery_color, height=4).pack(
            fill='x', side='bottom', pady=(6, 0)
        )

        tk.Button(
            card, text='▶',
            command=lambda c=char: play_char(c),
            relief='groove', font=('Helvetica', 10),
            bg='#f1efe8', padx=6
        ).pack(pady=(4, 0))

        card.bind('<Enter>', lambda e: card.configure(bg='#f1efe8'))
        card.bind('<Leave>', lambda e: card.configure(bg='white'))

        return card
    
    def _draw_morse_symbols(self, parent, morse):
        canvas = tk.Canvas(parent, bg='white', height=16, highlightthickness=0)
        canvas.pack()

        x = 4
        for symbol in morse:
            if symbol == '.':
                canvas.create_oval(x, 4, x + 10, 14, fill='#3d3d3a', outline='')
                x += 18
            elif symbol == '-':
                canvas.create_rectangle(x, 7, x + 26, 13, fill='#3d3d3a', outline='')
                x += 34
        canvas.configure(width=x)

    def _toggle_card_size(self):
        if self._card_size == 'expanded':
            self._card_size = 'compact'
            self._size_btn.configure(text='Expanded View')
        else:
            self._card_size = 'expanded'
            self._size_btn.configure(text='Compact View')
        self._render_cards(self._all_cards)

if __name__ == '__main__':
    app = MorseDictionary()
    app.mainloop()