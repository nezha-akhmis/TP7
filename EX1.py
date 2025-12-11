from datetime import datetime
import json
from abc import ABC, abstractmethod

# -----------------------------
# Mixins de base
# -----------------------------
class Horodatable:
    """Mixin pour ajouter un horodatage aux actions"""
    def horodatage(self):
        now = datetime.now()
        print(f"[LOG] Action à {now}")
        if hasattr(self, "_historique"):
            self._historique.append(f"Horodatage: {now}")

class Validable:
    """Mixin pour valider l'objet"""
    def valider(self):
        if not getattr(self, "titre", None):
            raise ValueError("Titre manquant")
        print("Validation OK")
        if hasattr(self, "_historique"):
            self._historique.append("Validation OK")

# -----------------------------
# Mixins avancés
# -----------------------------
class Serializable(ABC):
    """Mixin abstrait pour la sérialisation"""
    @abstractmethod
    def to_json(self) -> str:
        pass

class Historisable:
    """Mixin pour conserver un historique des actions"""
    def __init__(self, *args, **kwargs):
        self._historique = []
        super().__init__(*args, **kwargs)

    def historique(self):
        return self._historique

# -----------------------------
# Classe principale Document
# -----------------------------
class Document(Horodatable, Validable, Serializable, Historisable):
    def __init__(self, titre, contenu):
        self.titre = titre
        self.contenu = contenu
        super().__init__()  # initialise Historisable

    def sauvegarder(self):
        self.horodatage()
        self.valider()
        print(f"Document '{self.titre}' sauvegardé.")
        self._historique.append(f"Document '{self.titre}' sauvegardé.")

    def to_json(self) -> str:
        """Sérialisation du document en JSON"""
        data = {
            "titre": self.titre,
            "contenu": self.contenu,
            "historique": getattr(self, "_historique", [])
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

# -----------------------------
# Exemple d'utilisation
# -----------------------------
if __name__ == "__main__":
    doc = Document("Rapport", "Contenu important")
    doc.sauvegarder()
    print("\nHistorique des actions :", doc.historique())
    print("\nDocument en JSON :\n", doc.to_json())
