import os

import customtkinter as ctk


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHELTERS_FILE = os.path.join(BASE_DIR, "bousai_app", "data", "shelters.json")


class BousaiHomeApp(ctk.CTk):
    """高齢者にも使いやすい防災支援システムのデスクトップホーム画面。"""

    COLORS = {
        "ink": ("#14202b", "#f3f7f8"),
        "muted": ("#5b6b76", "#b7c6cc"),
        "surface": ("#ffffff", "#1b2933"),
        "surface_alt": ("#eef4f5", "#243640"),
        "line": ("#d6e2e5", "#40535d"),
        "teal": ("#087f83", "#48c6c0"),
        "teal_dark": ("#066569", "#2fa7a2"),
        "orange": ("#f6a623", "#ffb83e"),
        "red": ("#c62828", "#ef5350"),
        "red_dark": ("#971c22", "#b72c32"),
        "white": "#ffffff",
    }

    def __init__(self):
        super().__init__()
        self.title("防災支援システム")
        self.geometry("1280x820")
        self.minsize(980, 680)
        self.mode = "normal"
        self.active_notice_tab = "重要なお知らせ"
        self.active_map_tab = "ハザードマップ"
        self._build_shell()
        self.show_normal_mode()

    def _build_shell(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        header = ctk.CTkFrame(self, height=88, corner_radius=0, fg_color=self.COLORS["surface"])
        header.grid(row=0, column=0, sticky="nsew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text="防災支援システム", font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.COLORS["ink"],
        ).grid(row=0, column=0, padx=32, pady=22, sticky="w")

        user_area = ctk.CTkFrame(header, fg_color="transparent")
        user_area.grid(row=0, column=1, padx=30, pady=14, sticky="e")
        ctk.CTkLabel(user_area, text="●", font=ctk.CTkFont(size=30), text_color=self.COLORS["teal"]).grid(row=0, column=0, rowspan=2, padx=(0, 12))
        ctk.CTkLabel(user_area, text="大阪 太郎", font=ctk.CTkFont(size=17, weight="bold"), text_color=self.COLORS["ink"]).grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(user_area, text="管理者", font=ctk.CTkFont(size=13, weight="bold"), text_color=self.COLORS["white"], fg_color=self.COLORS["teal"], corner_radius=10, padx=11, pady=3).grid(row=1, column=1, pady=(3, 0), sticky="w")

        self.content = ctk.CTkFrame(self, fg_color=self.COLORS["surface_alt"], corner_radius=0)
        self.content.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.nav = ctk.CTkFrame(self, height=92, corner_radius=0, fg_color=self.COLORS["surface"])
        self.nav.grid(row=2, column=0, sticky="nsew")
        self.nav.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.nav.grid_propagate(False)
        nav_items = [("⌂", "ホーム"), ("⌕", "避難所検索"), ("▤", "検索結果"), ("+", "避難所登録")]
        for column, (icon, label) in enumerate(nav_items):
            ctk.CTkButton(self.nav, text=f"{icon}  {label}", height=58, corner_radius=12, font=ctk.CTkFont(size=16, weight="bold"), fg_color="transparent", hover_color=self.COLORS["surface_alt"], text_color=self.COLORS["ink"], command=lambda name=label: self._placeholder(name)).grid(row=0, column=column, padx=8, pady=17, sticky="ew")
        self.mode_button = ctk.CTkButton(self.nav, text="⚠  緊急モードへ", height=58, width=210, corner_radius=12, font=ctk.CTkFont(size=16, weight="bold"), fg_color=self.COLORS["red"], hover_color=self.COLORS["red_dark"], command=self.toggle_mode)
        self.mode_button.grid(row=0, column=4, padx=(14, 26), pady=17)

    def _clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def _button(self, parent, text, command, **kwargs):
        defaults = {"height": 52, "corner_radius": 12, "font": ctk.CTkFont(size=16, weight="bold")}
        defaults.update(kwargs)
        return ctk.CTkButton(parent, text=text, command=command, **defaults)

    def show_normal_mode(self):
        self.mode = "normal"
        self._clear_content()
        self.mode_button.configure(text="⚠  緊急モードへ", fg_color=self.COLORS["red"])
        self.content.grid_rowconfigure(0, weight=1)
        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew", padx=28, pady=24)
        wrapper.grid_columnconfigure((0, 1), weight=1, uniform="columns")
        wrapper.grid_rowconfigure(0, weight=1)
        self._build_notice_card(wrapper).grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self._build_map_card(wrapper).grid(row=0, column=1, sticky="nsew", padx=(12, 0))

    def _card(self, parent, title):
        card = ctk.CTkFrame(parent, fg_color=self.COLORS["surface"], border_width=1, border_color=self.COLORS["line"], corner_radius=16)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=21, weight="bold"), text_color=self.COLORS["ink"]).grid(row=0, column=0, padx=22, pady=(20, 14), sticky="w")
        return card

    def _build_notice_card(self, parent):
        card = self._card(parent, "地域の防災情報")
        tabs = ctk.CTkSegmentedButton(card, values=["重要なお知らせ", "イベント"], height=42, font=ctk.CTkFont(size=15, weight="bold"), command=self._notice_tab_changed)
        tabs.set(self.active_notice_tab)
        tabs.grid(row=1, column=0, padx=20, pady=(0, 14), sticky="ew")
        scroll = ctk.CTkScrollableFrame(card, fg_color=self.COLORS["surface_alt"], corner_radius=10)
        scroll.grid(row=2, column=0, padx=16, pady=(0, 18), sticky="nsew")
        items = [("2026年07月14日", "重要", "土砂災害の危険があるため避難してください"), ("2026年07月14日", "お知らせ", "B避難所の開設状況を確認できます"), ("2026年07月12日", "地域", "防災訓練のお知らせ")]
        for date, tag, heading in items:
            item = ctk.CTkFrame(scroll, fg_color=self.COLORS["surface"], corner_radius=10)
            item.pack(fill="x", padx=4, pady=5)
            ctk.CTkLabel(item, text=date, font=ctk.CTkFont(size=13), text_color=self.COLORS["muted"]).pack(anchor="w", padx=14, pady=(12, 2))
            ctk.CTkLabel(item, text=tag, font=ctk.CTkFont(size=12, weight="bold"), text_color=self.COLORS["red"] if tag == "重要" else self.COLORS["teal"]).pack(anchor="w", padx=14)
            ctk.CTkLabel(item, text=heading, wraplength=430, justify="left", font=ctk.CTkFont(size=15, weight="bold"), text_color=self.COLORS["ink"]).pack(anchor="w", padx=14, pady=(3, 12))
        return card

    def _build_map_card(self, parent):
        card = self._card(parent, "マップ・交通情報")
        tabs = ctk.CTkSegmentedButton(card, values=["ハザードマップ", "通行止め・道路状況"], height=42, font=ctk.CTkFont(size=15, weight="bold"), command=self._map_tab_changed)
        tabs.set(self.active_map_tab)
        tabs.grid(row=1, column=0, padx=20, pady=(0, 14), sticky="ew")
        preview = ctk.CTkFrame(card, fg_color=("#e6eff0", "#203740"), border_width=1, border_color=self.COLORS["line"], corner_radius=12)
        preview.grid(row=2, column=0, padx=20, pady=(0, 16), sticky="nsew")
        ctk.CTkLabel(preview, text="⌖\n地図プレビュー", font=ctk.CTkFont(size=23, weight="bold"), text_color=self.COLORS["teal"]).place(relx=.5, rely=.5, anchor="center")
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        actions.grid_columnconfigure((0, 1), weight=1)
        self._button(actions, "現在地を登録・更新", lambda: self._placeholder("現在地を登録・更新"), fg_color=self.COLORS["teal"], hover_color=self.COLORS["teal_dark"]).grid(row=0, column=0, padx=(0, 6), sticky="ew")
        self._button(actions, "現在地周辺を拡大", lambda: self._placeholder("現在地周辺のハザードマップを拡大"), fg_color=self.COLORS["teal"], hover_color=self.COLORS["teal_dark"]).grid(row=0, column=1, padx=(6, 0), sticky="ew")
        return card

    def show_emergency_mode(self):
        self.mode = "emergency"
        self._clear_content()
        self.mode_button.configure(text="✓  通常モードへ", fg_color=self.COLORS["teal"])
        self.content.grid_rowconfigure(0, weight=0)
        banner = ctk.CTkFrame(self.content, fg_color=self.COLORS["red"], corner_radius=0, height=92)
        banner.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        banner.grid_propagate(False)
        ctk.CTkLabel(banner, text="【緊急地震速報】大阪市で災害発生！直ちに安全を確保してください", font=ctk.CTkFont(size=23, weight="bold"), text_color=self.COLORS["white"]).pack(expand=True)
        body = ctk.CTkFrame(self.content, fg_color="transparent")
        body.grid(row=1, column=0, padx=28, pady=24, sticky="nsew")
        self.content.grid_rowconfigure(1, weight=1)
        body.grid_columnconfigure(0, weight=1, uniform="emergency")
        body.grid_columnconfigure(1, weight=2, uniform="emergency")
        body.grid_rowconfigure(0, weight=1)
        action = ctk.CTkFrame(body, fg_color=self.COLORS["orange"], corner_radius=16)
        action.grid(row=0, column=0, padx=(0, 14), sticky="nsew")
        ctk.CTkLabel(action, text="まず安全な場所へ", font=ctk.CTkFont(size=20, weight="bold"), text_color="#3b2500").pack(pady=(48, 18))
        self._button(action, "避難所をすぐ探す", lambda: self._placeholder("避難所をすぐ探す"), height=82, font=ctk.CTkFont(size=22, weight="bold"), fg_color=self.COLORS["white"], text_color="#5c3900", hover_color="#fff5dc").pack(fill="x", padx=24, pady=10)
        self._button(action, "避難経路を表示", lambda: self._placeholder("避難経路を表示"), height=82, font=ctk.CTkFont(size=22, weight="bold"), fg_color=self.COLORS["white"], text_color="#5c3900", hover_color="#fff5dc").pack(fill="x", padx=24, pady=10)
        map_area = ctk.CTkFrame(body, fg_color=self.COLORS["surface"], border_width=1, border_color=self.COLORS["line"], corner_radius=16)
        map_area.grid(row=0, column=1, padx=(14, 0), sticky="nsew")
        map_area.grid_rowconfigure(0, weight=1)
        map_area.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(map_area, text="⌖\n避難経路マップ", font=ctk.CTkFont(size=25, weight="bold"), text_color=self.COLORS["red"]).grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        self._button(map_area, "周辺の通行止め情報", lambda: self._placeholder("周辺の通行止め情報"), fg_color=self.COLORS["red"], hover_color=self.COLORS["red_dark"]).grid(row=1, column=0, padx=22, pady=(0, 22), sticky="ew")

    def toggle_mode(self):
        self.show_emergency_mode() if self.mode == "normal" else self.show_normal_mode()

    def _notice_tab_changed(self, value):
        self.active_notice_tab = value
        print(f"タブ切替: {value}")

    def _map_tab_changed(self, value):
        self.active_map_tab = value
        print(f"タブ切替: {value}")

    def _placeholder(self, action):
        print(f"操作: {action}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    BousaiHomeApp().mainloop()