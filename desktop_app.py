import os

import customtkinter as ctk
import tkintermapview


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

    TEXT = {
        "ja": {
            "title": "防災支援システム", "user": "大阪 太郎", "role": "管理者", "logout": "ログアウト",
            "language": "🌐 EN / JP", "home": "ホーム", "shelter_search": "避難所検索", "results": "検索結果", "register": "避難所登録",
            "emergency_mode": "緊急モードへ", "normal_mode": "通常モードへ", "notice_title": "地域の防災情報", "status": "平常",
            "notices": "重要なお知らせ", "events": "イベント", "no_notice": "現在、地域からのお知らせはありません", "important": "重要", "notice": "お知らせ",
            "event_notice": "地域防災訓練のお知らせ", "event_detail": "近くの避難所で訓練を行います", "map_title": "マップ・交通情報",
            "hazard": "ハザードマップ", "road": "通行止め・道路状況", "hazard_map": "青森市 ハザードマップ", "register_location": "現在地を登録・更新",
            "zoom_map": "現在地周辺を拡大", "closed": "✖ 通行止め", "closed_reason_1": "中央交差点付近：土砂崩れのため通行不可",
            "closed_reason_2": "本町交差点付近：道路冠水のため通行不可", "closed_reason_3": "港町交差点付近：落石のため通行不可",
            "emergency_alert": "【緊急地震速報】青森市で災害発生！直ちに安全を確保してください", "safe_place": "まず安全な場所へ",
            "start_navigation": "一番近い避難所へナビ開始", "route_map": "避難経路マップ", "distance": "避難所まで 1.2 km",
            "walking": "徒歩 約15分　安全な経路を表示中", "nearby_roads": "周辺の通行止め情報", "help": "使い方", "close": "閉じる",
            "help_1": "近くの避難所を探します", "help_2": "青森市の危険な場所を確認します", "help_3": "災害時の避難操作を大きく表示します",
            "selected": "を選択しました", "tag_area": "地域", "today": "本日",
            "notice_1": "土砂災害の危険があるため避難してください", "notice_2": "B避難所の開設状況を確認できます",
            "marker_instruction": "：地図上のマーカーを選択してください",
        },
        "en": {
            "title": "Disaster Support System", "user": "Taro Osaka", "role": "Administrator", "logout": "Log out",
            "language": "🌐 EN / JP", "home": "Home", "shelter_search": "Shelters", "results": "Results", "register": "Register shelter",
            "emergency_mode": "Emergency mode", "normal_mode": "Normal mode", "notice_title": "Local disaster information", "status": "Clear",
            "notices": "Important notices", "events": "Events", "no_notice": "There are no local notices at this time", "important": "Important", "notice": "Notice",
            "event_notice": "Community disaster drill", "event_detail": "A drill will be held at a nearby shelter", "map_title": "Maps and traffic",
            "hazard": "Hazard map", "road": "Road closures", "hazard_map": "Aomori hazard map", "register_location": "Save or update location",
            "zoom_map": "Zoom to my area", "closed": "✖ Road closed", "closed_reason_1": "Chuo intersection: impassable due to landslide",
            "closed_reason_2": "Honcho intersection: impassable due to flooding", "closed_reason_3": "Minatomachi intersection: impassable due to falling rocks",
            "emergency_alert": "[Earthquake alert] Disaster reported in Aomori. Move to safety immediately.", "safe_place": "Move to safety first",
            "start_navigation": "Start navigation to the nearest shelter", "route_map": "Evacuation route map", "distance": "1.2 km to shelter",
            "walking": "About 15 min on foot　Showing a safe route", "nearby_roads": "Nearby road closures", "help": "Help", "close": "Close",
            "help_1": "Find nearby shelters", "help_2": "Check dangerous areas in Aomori", "help_3": "Show large evacuation controls during a disaster",
            "selected": " selected", "tag_area": "Area", "today": "Today",
            "notice_1": "Evacuate because of the landslide risk", "notice_2": "Check the opening status of Shelter B",
            "marker_instruction": ": select a marker on the map",
        },
    }

    def __init__(self):
        super().__init__()
        self.title("防災支援システム")
        self.geometry("1280x820")
        self.minsize(520, 680)
        self.mode = "normal"
        self.language = "ja"
        self.active_notice_tab = "notices"
        self.active_map_tab = "hazard"
        self._last_narrow = None
        self._build_shell()
        self.show_normal_mode()
        self.bind("<Configure>", self._on_resize)

    def t(self, key):
        return self.TEXT[self.language][key]

    def _build_shell(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        header = ctk.CTkFrame(self, height=88, corner_radius=0, fg_color=self.COLORS["surface"])
        header.grid(row=0, column=0, sticky="nsew")
        header.grid_columnconfigure(0, weight=1)
        header.grid_propagate(False)

        ctk.CTkLabel(
            header, text=self.t("title"), font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.COLORS["ink"],
        ).grid(row=0, column=0, padx=32, pady=22, sticky="w")

        user_area = ctk.CTkFrame(header, fg_color="transparent")
        user_area.grid(row=0, column=1, padx=30, pady=14, sticky="e")
        self._button(user_area, self.t("language"), self.toggle_language, height=40, width=112, corner_radius=9, font=ctk.CTkFont(size=14, weight="bold"), fg_color="transparent", hover_color=self.COLORS["surface_alt"], border_width=1, border_color=self.COLORS["teal"], text_color=self.COLORS["teal"]).grid(row=0, column=0, rowspan=2, padx=(0, 18))
        ctk.CTkLabel(user_area, text="●", font=ctk.CTkFont(size=30), text_color=self.COLORS["teal"]).grid(row=0, column=1, rowspan=2, padx=(0, 12))
        ctk.CTkLabel(user_area, text=self.t("user"), font=ctk.CTkFont(size=17, weight="bold"), text_color=self.COLORS["ink"]).grid(row=0, column=2, sticky="w")
        ctk.CTkLabel(user_area, text=self.t("role"), font=ctk.CTkFont(size=13, weight="bold"), text_color=self.COLORS["white"], fg_color=self.COLORS["teal"], corner_radius=10, padx=11, pady=3).grid(row=1, column=2, pady=(3, 0), sticky="w")
        self._button(user_area, self.t("logout"), self._logout, height=40, width=100, corner_radius=9, font=ctk.CTkFont(size=14, weight="bold"), fg_color="transparent", hover_color=self.COLORS["surface_alt"], border_width=1, border_color=self.COLORS["red"], text_color=self.COLORS["red"]).grid(row=0, column=3, rowspan=2, padx=(18, 0))

        self.content = ctk.CTkFrame(self, fg_color=self.COLORS["surface_alt"], corner_radius=0)
        self.content.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        self.nav = ctk.CTkFrame(self, height=92, corner_radius=0, fg_color=self.COLORS["surface"])
        self.nav.grid(row=2, column=0, sticky="nsew")
        self.nav.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.nav.grid_propagate(False)
        nav_items = [("⌂", "home"), ("⌕", "shelter_search"), ("▤", "results"), ("+", "register")]
        for column, (icon, label) in enumerate(nav_items):
            ctk.CTkButton(self.nav, text=f"{icon}  {self.t(label)}", height=58, corner_radius=12, font=ctk.CTkFont(size=16, weight="bold"), fg_color="transparent", hover_color=self.COLORS["surface_alt"], text_color=self.COLORS["ink"], command=lambda name=label: self._placeholder(self.t(name))).grid(row=0, column=column, padx=8, pady=17, sticky="ew")
        self.mode_button = ctk.CTkButton(self.nav, text=f"⚠  {self.t('emergency_mode')}", height=58, width=210, corner_radius=12, font=ctk.CTkFont(size=16, weight="bold"), fg_color=self.COLORS["red"], hover_color=self.COLORS["red_dark"], command=self.toggle_mode)
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
        self.mode_button.configure(text=f"⚠  {self.t('emergency_mode')}", fg_color=self.COLORS["red"])
        self.content.grid_rowconfigure(0, weight=1)
        wrapper = ctk.CTkFrame(self.content, fg_color="transparent")
        wrapper.grid(row=0, column=0, sticky="nsew", padx=28, pady=24)
        wrapper.grid_columnconfigure((0, 1), weight=1, uniform="columns")
        wrapper.grid_rowconfigure(0, weight=1)
        self.normal_wrapper = wrapper
        self.notice_card = self._build_notice_card(wrapper)
        self.map_card = self._build_map_card(wrapper)
        self.notice_card.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.map_card.grid(row=0, column=1, sticky="nsew", padx=(12, 0))
        self._apply_responsive_layout()

    def _card(self, parent, title):
        card = ctk.CTkFrame(parent, fg_color=self.COLORS["surface"], border_width=1, border_color=self.COLORS["line"], corner_radius=16)
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(2, weight=1)
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=21, weight="bold"), text_color=self.COLORS["ink"]).grid(row=0, column=0, padx=22, pady=(20, 14), sticky="w")
        return card

    def _build_notice_card(self, parent):
        card = self._card(parent, self.t("notice_title"))
        tabs = ctk.CTkSegmentedButton(card, values=[self.t("notices"), self.t("events")], height=46, font=ctk.CTkFont(size=16, weight="bold"), command=self._notice_tab_changed)
        tabs.set(self.t(self.active_notice_tab))
        tabs.grid(row=1, column=0, padx=20, pady=(0, 14), sticky="ew")
        scroll = ctk.CTkScrollableFrame(card, fg_color=self.COLORS["surface_alt"], corner_radius=10)
        scroll.grid(row=2, column=0, padx=16, pady=(0, 18), sticky="nsew")
        items = [("2026年07月14日", self.t("important"), self.t("notice_1")), ("2026年07月14日", self.t("notice"), self.t("notice_2")), ("2026年07月12日", self.t("tag_area"), self.t("event_notice"))]
        for date, tag, heading in items:
            item = ctk.CTkFrame(scroll, fg_color=self.COLORS["surface"], corner_radius=10)
            item.pack(fill="x", padx=4, pady=5)
            ctk.CTkLabel(item, text=date, font=ctk.CTkFont(size=13), text_color=self.COLORS["muted"]).pack(anchor="w", padx=14, pady=(12, 2))
            ctk.CTkLabel(item, text=tag, font=ctk.CTkFont(size=12, weight="bold"), text_color=self.COLORS["red"] if tag == self.t("important") else self.COLORS["teal"]).pack(anchor="w", padx=14)
            ctk.CTkLabel(item, text=heading, wraplength=430, justify="left", font=ctk.CTkFont(size=15, weight="bold"), text_color=self.COLORS["ink"]).pack(anchor="w", padx=14, pady=(3, 12))
        return card

    def _build_map_card(self, parent):
        card = self._card(parent, self.t("map_title"))
        tabs = ctk.CTkSegmentedButton(card, values=[self.t("hazard"), self.t("road")], height=46, font=ctk.CTkFont(size=16, weight="bold"), command=self._map_tab_changed)
        tabs.set(self.t(self.active_map_tab))
        tabs.grid(row=1, column=0, padx=20, pady=(0, 14), sticky="ew")
        preview = ctk.CTkFrame(card, fg_color=("#e6eff0", "#203740"), border_width=1, border_color=self.COLORS["line"], corner_radius=12)
        preview.grid(row=2, column=0, padx=20, pady=(0, 16), sticky="nsew")
        self.map_widget = tkintermapview.TkinterMapView(preview, corner_radius=12)
        self.map_widget.pack(fill="both", expand=True, padx=2, pady=2)
        self.map_widget.set_position(40.8244, 140.74)
        self.map_widget.set_zoom(14)
        self.map_widget.set_marker(40.8280, 140.7350, text=self.t("closed"), marker_color_circle="#c62828", marker_color_outside="#8e171b", text_color="#8e171b", command=lambda marker: self._show_closure("closed_reason_1"))
        self.map_widget.set_marker(40.8205, 140.7450, text=self.t("closed"), marker_color_circle="#c62828", marker_color_outside="#8e171b", text_color="#8e171b", command=lambda marker: self._show_closure("closed_reason_2"))
        self.map_widget.set_marker(40.8180, 140.7300, text=self.t("closed"), marker_color_circle="#c62828", marker_color_outside="#8e171b", text_color="#8e171b", command=lambda marker: self._show_closure("closed_reason_3"))
        self.map_detail = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=15, weight="bold"), text_color=self.COLORS["red"], anchor="w")
        self.map_detail.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        actions.grid_columnconfigure((0, 1), weight=1)
        self._button(actions, self.t("register_location"), lambda: self._placeholder(self.t("register_location")), fg_color=self.COLORS["teal"], hover_color=self.COLORS["teal_dark"]).grid(row=0, column=0, padx=(0, 6), sticky="ew")
        self._button(actions, self.t("zoom_map"), lambda: self._placeholder(self.t("zoom_map")), fg_color=self.COLORS["teal"], hover_color=self.COLORS["teal_dark"]).grid(row=0, column=1, padx=(6, 0), sticky="ew")
        return card

    def show_emergency_mode(self):
        self.mode = "emergency"
        self._clear_content()
        self.mode_button.configure(text=f"✓  {self.t('normal_mode')}", fg_color=self.COLORS["teal"])
        self.content.grid_rowconfigure(0, weight=0)
        banner = ctk.CTkFrame(self.content, fg_color=self.COLORS["red"], corner_radius=0, height=92)
        banner.grid(row=0, column=0, padx=0, pady=0, sticky="ew")
        banner.grid_propagate(False)
        ctk.CTkLabel(banner, text=self.t("emergency_alert"), font=ctk.CTkFont(size=23, weight="bold"), text_color=self.COLORS["white"]).pack(expand=True)
        body = ctk.CTkFrame(self.content, fg_color="transparent")
        body.grid(row=1, column=0, padx=28, pady=24, sticky="nsew")
        self.content.grid_rowconfigure(1, weight=1)
        body.grid_columnconfigure(0, weight=1, uniform="emergency")
        body.grid_columnconfigure(1, weight=2, uniform="emergency")
        body.grid_rowconfigure(0, weight=1)
        action = ctk.CTkFrame(body, fg_color=self.COLORS["orange"], corner_radius=16)
        action.grid(row=0, column=0, padx=(0, 14), sticky="nsew")
        ctk.CTkLabel(action, text=self.t("safe_place"), font=ctk.CTkFont(size=22, weight="bold"), text_color="#3b2500").pack(pady=(48, 18))
        self._button(action, self.t("start_navigation"), lambda: self._placeholder(self.t("start_navigation")), height=190, font=ctk.CTkFont(size=24, weight="bold"), fg_color=self.COLORS["white"], text_color="#5c3900", hover_color="#fff5dc").pack(fill="both", expand=True, padx=24, pady=(10, 34))
        map_area = ctk.CTkFrame(body, fg_color=self.COLORS["surface"], border_width=1, border_color=self.COLORS["line"], corner_radius=16)
        map_area.grid(row=0, column=1, padx=(14, 0), sticky="nsew")
        map_area.grid_rowconfigure(0, weight=1)
        map_area.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(map_area, text=f"⌖\n{self.t('route_map')}\n\n{self.t('distance')}", font=ctk.CTkFont(size=30, weight="bold"), text_color=self.COLORS["red"]).grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        ctk.CTkLabel(map_area, text=self.t("walking"), font=ctk.CTkFont(size=17, weight="bold"), text_color=self.COLORS["muted"]).grid(row=1, column=0, padx=22, pady=(0, 10))
        self._button(map_area, self.t("nearby_roads"), lambda: self._placeholder(self.t("nearby_roads")), fg_color=self.COLORS["white"], text_color=self.COLORS["red"], border_width=2, border_color=self.COLORS["red"], hover_color="#fff1f1").grid(row=2, column=0, padx=22, pady=(0, 22), sticky="ew")

    def toggle_mode(self):
        self.show_emergency_mode() if self.mode == "normal" else self.show_normal_mode()

    def _notice_tab_changed(self, value):
        self.active_notice_tab = value
        print(f"タブ切替: {value}")

    def _map_tab_changed(self, value):
        self.active_map_tab = "hazard" if value == self.t("hazard") else "road"
        self.map_detail.configure(text="" if self.active_map_tab == "hazard" else self.t("closed") + self.t("marker_instruction"))
        print(f"タブ切替: {value}")

    def _show_closure(self, reason_key):
        self.map_detail.configure(text=self.t(reason_key))

    def _on_resize(self, event):
        if event.widget is self:
            self._apply_responsive_layout()

    def _apply_responsive_layout(self):
        wrapper = getattr(self, "normal_wrapper", None)
        if not wrapper or self.mode != "normal":
            return
        narrow = self.winfo_width() < 900
        if narrow == self._last_narrow:
            return
        self._last_narrow = narrow
        if narrow:
            wrapper.grid_columnconfigure(1, weight=0)
            wrapper.grid_rowconfigure((0, 1), weight=1)
            self.notice_card.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 12), sticky="nsew")
            self.map_card.grid(row=1, column=0, columnspan=2, padx=0, pady=(12, 0), sticky="nsew")
        else:
            wrapper.grid_columnconfigure(1, weight=1)
            wrapper.grid_rowconfigure(1, weight=0)
            self.notice_card.grid(row=0, column=0, columnspan=1, padx=(0, 12), pady=0, sticky="nsew")
            self.map_card.grid(row=0, column=1, columnspan=1, padx=(12, 0), pady=0, sticky="nsew")

    def toggle_language(self):
        self.language = "en" if self.language == "ja" else "ja"
        self._last_narrow = None
        for child in self.winfo_children():
            child.destroy()
        self._build_shell()
        if self.mode == "normal":
            self.show_normal_mode()
        else:
            self.show_emergency_mode()

    def _logout(self):
        self._placeholder(self.t("logout"))

    def _placeholder(self, action):
        print(f"操作: {action}")


if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    BousaiHomeApp().mainloop()