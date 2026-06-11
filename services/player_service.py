class PlayerService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PlayerService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self):
        self._players = [
            {"id": 1, "name": "Marcus Perez", "pos": "FW", "rating": 88, "wage": "€1,250,000", "vfm": "7.5 VFM", "vfm_color": "#2ecc71"},
            {"id": 2, "name": "Daniel Cannon", "pos": "MF", "rating": 85, "wage": "€1,360,000", "vfm": "7.1 VFM", "vfm_color": "#2ecc71"},
            {"id": 3, "name": "Leonard James", "pos": "DF", "rating": 82, "wage": "€1,380,000", "vfm": "6.8 VFM", "vfm_color": "#2ecc71"},
            {"id": 4, "name": "John Banker", "pos": "GK", "rating": 80, "wage": "€1,330,000", "vfm": "6.6 VFM", "vfm_color": "#2ecc71"},
            {"id": 5, "name": "Oliver Sanchez", "pos": "FW", "rating": 79, "wage": "€1,100,000", "vfm": "6.5 VFM", "vfm_color": "#2ecc71"}
        ]

    def get_all_players(self):
        return self._players

    def get_squad_kpi(self):
        return [
            ("მიმდინარე პოზიცია", "La Liga, 1st", "#2ecc71"),
            ("სატრანსფერო ბიუჯეტი", "€120,500,000", "#3498db"),
            ("გუნდის რეიტინგი", "88 OVR", "#9b59b6"),
            ("კონტრაქტების სტატუსი", "3 იწურება მალე", "#e74c3c")
        ]