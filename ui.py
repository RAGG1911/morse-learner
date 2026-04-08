import tkinter as tk
import customtkinter as ctk
from data import get_display_data
from storage import load_favourites, load_mastery, get_mastery_level
from audio import play_char

ctk.set_appearance_mode('system')
ctk.set_default_color_theme('blue')

MASTERY_COLORS = {
    'unseen':   '#B4B2A9',
    'learning': '#EF9F27',
    'mastered': '#1D9E75',
}

class MorseDictionary(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Morse Learner — Dictionary')
        self.geometry('1000x700')

        self._all_cards     = get_display_data()
        self._favourites    = load_favourites()
        self._mastery       = load_mastery()
        self._card_size     = 'expanded'
        self._active_filter = 'all'
        self._search_query  = ''

        self._build_ui()
        self._render_cards(self._all_cards)

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Toolbar
        toolbar = ctk.CTkFrame(self, fg_color='transparent')
        toolbar.grid(row=0, column=0, sticky='ew', padx=16, pady=(16, 4))
        toolbar.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            toolbar, text='Morse Dictionary',
            font=ctk.CTkFont(size=20, weight='bold')
        ).grid(row=0, column=0, sticky='w')

        self._size_btn = ctk.CTkButton(
            toolbar, text='Compact view', width=120,
            command=self._toggle_card_size
        )
        self._size_btn.grid(row=0, column=1, sticky='e')

        # Search bar
        search_frame = ctk.CTkFrame(self, fg_color='transparent')
        search_frame.grid(row=1, column=0, sticky='ew', padx=16, pady=4)

        ctk.CTkLabel(search_frame, text='Search:').pack(side='left', padx=(0, 8))
        self._search_var = ctk.StringVar()
        self._search_var.trace_add('write', self._on_search)
        ctk.CTkEntry(
            search_frame, textvariable=self._search_var,
            width=260, placeholder_text='Letter or morse pattern...'
        ).pack(side='left')
        ctk.CTkButton(
            search_frame, text='✕', width=32,
            command=self._clear_search
        ).pack(side='left', padx=6)

        # Filter toggles
        filter_frame = ctk.CTkFrame(self, fg_color='transparent')
        filter_frame.grid(row=2, column=0, sticky='ew', padx=16, pady=4)

        self._filter_buttons = {}
        for label, value in [('All', 'all'), ('Letters', 'letter'),
                              ('Numbers', 'number'), ('Punctuation', 'punctuation')]:
            btn = ctk.CTkButton(
                filter_frame, text=label, width=100,
                command=lambda v=value: self._set_filter(v)
            )
            btn.pack(side='left', padx=(0, 8))
            self._filter_buttons[value] = btn
        self._update_filter_buttons()

        # Scrollable card area — all cards will be parented HERE
        self._scroll_frame = ctk.CTkScrollableFrame(self, fg_color='transparent')
        self._scroll_frame.grid(row=3, column=0, sticky='nsew', padx=16, pady=(4, 16))

    # ── Filtering ─────────────────────────────────────────────────────────────

    def _get_filtered_cards(self) -> list:
        data = self._all_cards
        if self._active_filter != 'all':
            data = [c for c in data if c[2] == self._active_filter]
        if self._search_query:
            q = self._search_query.lower()
            data = [c for c in data if q in c[0].lower() or q in c[1]]
        return data

    def _on_search(self, *args):
        self._search_query = self._search_var.get()
        self._render_cards(self._get_filtered_cards())

    def _clear_search(self):
        self._search_var.set('')

    def _set_filter(self, value: str):
        self._active_filter = value
        self._update_filter_buttons()
        self._render_cards(self._get_filtered_cards())

    def _update_filter_buttons(self):
        for value, btn in self._filter_buttons.items():
            if value == self._active_filter:
                btn.configure(fg_color=('#3d3d3a', '#ffffff'),
                              text_color=('#ffffff', '#000000'))
            else:
                btn.configure(fg_color=('gray75', 'gray25'),
                              text_color=('gray10', 'gray90'))

    # ── Card rendering ────────────────────────────────────────────────────────

    def _render_cards(self, data):
        for widget in self._scroll_frame.winfo_children():
            widget.destroy()

        cols = 6 if self._card_size == 'compact' else 4
        for i, (char, morse, category) in enumerate(data):
            row, col = divmod(i, cols)
            card = self._make_card(char, morse)          # ← parent is scroll_frame now
            card.grid(row=row, column=col, padx=6, pady=6, sticky='nsew')

        for c in range(cols):
            self._scroll_frame.grid_columnconfigure(c, weight=1)

    def _make_card(self, char: str, morse: str) -> ctk.CTkFrame:
        mastery_data  = self._mastery.get(char, {})
        mastery_level = get_mastery_level(mastery_data)
        mastery_color = MASTERY_COLORS[mastery_level]
        is_expanded   = self._card_size == 'expanded'

        # ↓ Parent is self._scroll_frame, not self
        card = ctk.CTkFrame(self._scroll_frame, corner_radius=10)

        ctk.CTkLabel(
            card, text=char,
            font=ctk.CTkFont(size=22 if is_expanded else 14, weight='bold')
        ).pack(pady=(10, 2))

        if is_expanded:
            self._draw_morse_symbols(card, morse)
            ctk.CTkLabel(
                card, text=morse,
                font=ctk.CTkFont(family='Courier', size=11),
                text_color='gray'
            ).pack(pady=(0, 4))

        # Mastery bar
        ctk.CTkFrame(
            card, height=4, fg_color=mastery_color, corner_radius=0
        ).pack(fill='x', pady=(4, 0))

        # Play button
        ctk.CTkButton(
            card, text='▶', width=48,
            command=lambda c=char: play_char(c)
        ).pack(pady=8)

        return card

    def _draw_morse_symbols(self, parent, morse: str):
        canvas = tk.Canvas(
            parent, height=18,
            bg=self._get_canvas_bg(),
            highlightthickness=0
        )
        canvas.pack(pady=4)
        x = 4
        for symbol in morse:
            if symbol == '.':
                canvas.create_oval(x, 4, x + 10, 14, fill='#888780', outline='')
                x += 18
            elif symbol == '-':
                canvas.create_rectangle(x, 7, x + 26, 13, fill='#888780', outline='')
                x += 34
        canvas.configure(width=x + 4)

    def _get_canvas_bg(self) -> str:
        return '#2b2b2b' if ctk.get_appearance_mode() == 'Dark' else '#ebebeb'

    def _toggle_card_size(self):
        if self._card_size == 'expanded':
            self._card_size = 'compact'
            self._size_btn.configure(text='Expanded view')
        else:
            self._card_size = 'expanded'
            self._size_btn.configure(text='Compact view')
        self._render_cards(self._get_filtered_cards())


if __name__ == '__main__':
    app = MorseDictionary()
    app.mainloop()