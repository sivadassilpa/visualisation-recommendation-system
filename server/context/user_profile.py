class UserProfile:
    def __init__(self, familiarity, profession, interest, country):
        self.familiarity = familiarity
        self.profession = profession
        self.interest = interest
        self.country =country

    def to_dict(self):
        return {
            "familiarity": self.familiarity,
            "profession": self.profession,
            "interests": self.interests,
            "country":self.country
        }