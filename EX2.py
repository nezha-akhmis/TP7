
  import json
from datetime import datetime

# -----------------------------
# Mixins
# -----------------------------
class Serializable:
    """Mixin pour sérialiser un objet en JSON"""
    def to_json(self) -> str:
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)

class Historisable:
    """Mixin pour garder l'historique des états"""
    def __init__(self, *args, **kwargs):
        self.historique = []
        super().__init__(*args, **kwargs)

    def enregistrer_etat(self):
        self.historique.append((datetime.now(), self.__dict__.copy()))

class Journalisable:
    """Mixin pour journaliser les actions"""
    def journaliser(self, message: str):
        print(f"[Journal] {datetime.now()}: {message}")

class Horodatable:
    """Mixin pour ajouter un timestamp sur les actions"""
    def horodatage(self):
        now = datetime.now()
        print(f"[Horodatage] {now}")
        if hasattr(self, "historique"):
            self.historique.append(f"Horodatage: {now}")

# -----------------------------
# Classe métier
# -----------------------------
class Contrat(Serializable, Historisable, Journalisable, Horodatable):
    def __init__(self, id: int, description: str):
        Historisable.__init__(self)  # initialise l'historique
        self.id = id
        self.description = description

    def modifier(self, nouvelle_desc: str):
        self.journaliser(f"Modification du contrat {self.id}")
        self.horodatage()
        self.enregistrer_etat()
        self.description = nouvelle_desc

# -----------------------------
# Exemple d'utilisation
# -----------------------------
if __name__ == "__main__":
    c = Contrat(1, "Initial")
    c.modifier("Révisé")
    print("\nContrat JSON :", c.to_json())
    print("\nHistorique :", c.historique)

    # Reconstruction depuis JSON
    json_str = c.to_json()
    c2 = Contrat.from_json(json_str)
    print("\nContrat reconstruit :", c2.to_json())
