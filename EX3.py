
from datetime import datetime
import copy

# -----------------------------
# Mixins
# -----------------------------
class ValidationMixin:
    """Mixin pour valider que le titre n'est pas vide"""
    def valider_titre(self):
        if not getattr(self, "titre", None) or not self.titre.strip():
            raise ValueError("Le titre de la tâche est obligatoire et ne peut pas être vide.")

class HistoriqueMixin:
    """Mixin pour enregistrer l'historique des descriptions"""
    def __init__(self, *args, **kwargs):
        self._historique = []
        super().__init__(*args, **kwargs)

    def enregistrer_historique(self, description):
        self._historique.append((datetime.now(), copy.deepcopy(description)))

    def afficher_historique(self):
        for dt, desc in self._historique:
            print(f"[{dt}] {desc}")

class JournalisationMixin:
    """Mixin pour journaliser les actions dans la console"""
    def journaliser(self, message):
        print(f"[Journal] {datetime.now()}: {message}")

# -----------------------------
# Classe principale
# -----------------------------
class Tache(ValidationMixin, HistoriqueMixin, JournalisationMixin):
    def __init__(self, titre, description):
        self.titre = titre
        self.description = description
        self.date_creation = datetime.now()
        super().__init__()
        self.valider_titre()
        self.journaliser(f"Tâche créée : '{self.titre}'")
        self.enregistrer_historique(self.description)

    def mettre_a_jour(self, nouvelle_description):
        self.journaliser(f"Tâche '{self.titre}' mise à jour")
        self.enregistrer_historique(self.description)
        self.description = nouvelle_description
        self.valider_titre()

# -----------------------------
# Exemple d'utilisation
# -----------------------------
if __name__ == "__main__":
    tache = Tache("Rédiger rapport", "Préparer le rapport trimestriel")
    tache.mettre_a_jour("Préparer le rapport trimestriel et les annexes")
    tache.mettre_a_jour("Finaliser le rapport et l'envoyer au manager")

    print("\nHistorique des descriptions :")
    tache.afficher_historique()
