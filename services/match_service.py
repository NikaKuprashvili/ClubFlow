class MatchService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MatchService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self):
        self._matches = [
            {"date": "28 აგვ, 18:00", "opponent": "vs Palies", "venue": "Barroal Club"},
            {"date": "30 აგვ, 13:00", "opponent": "vs Prarwarsi", "venue": "Bolnson Iberian"}
        ]

    def get_upcoming_matches(self):
        return self._matches