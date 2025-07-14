import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random

# Configuration des couleurs disponibles
AVAILABLE_COLORS = [
    '#e91e63',  # rose
    '#9c27b0',  # violet
    '#2196f3',  # bleu
    '#4caf50',  # vert
    '#ff9800',  # orange
    '#f44336',  # rouge
    '#795548',  # marron
    '#607d8b',  # bleu-gris
    '#ffeb3b',  # jaune
    '#9e9e9e',  # gris
    '#3f51b5',  # indigo
    '#00bcd4',  # cyan
    '#8bc34a',  # vert clair
    '#ff5722',  # orange foncé
    '#673ab7',  # violet foncé
    '#009688',  # teal
    '#ff9999',  # rose clair
    '#90EE90'  # vert clair
]

# Nœuds prédéfinis basés sur l'image (sans les types)
PREDEFINED_NODES = [
    "Computer Science",
    "Modern Letter",
    "Teacher1",
    "Teacher2",
    "University1",
    "University2",
    "Course1",
    "Course2",
    "Student1",
    "Student2",
    "City1",
    "City2",
    "Burkina Faso",
    "Cameroun",
    "Afrique",
    "SEA"
]

# Relations prédéfinies avec labels automatiques basés sur l'image
PREDEFINED_RELATIONS = {
    # Relations spécifiques extraites de l'image
    ("Computer Science", "Teacher1"): "employs",
    ("Computer Science", "Course1"): "gives",
    ("Modern Letter", "Teacher1"): "employs",
    ("Modern Letter", "Teacher2"): "employs",
    ("Teacher1", "Course1"): "gives",
    ("Teacher1", "Course2"): "gives",
    ("Teacher1", "University1"): "teaches at",
    ("Teacher1", "University2"): "teaches at",
    ("Teacher1", "City1"): "lives in",
    ("Teacher1", "Cameroun"): "comes from",
    ("Teacher1", "Teacher2"): "co-works",
    ("Teacher2", "Course2"): "gives",
    ("Teacher2", "City2"): "lives in",
    ("Teacher2", "Burkina Faso"): "comes from",
    ("University1", "City1"): "is located in",
    ("University2", "City2"): "is located in",
    ("Course1", "Student2"): "is followed by",
    ("Course2", "Student1"): "is followed by",
    ("Student1", "Course2"): "follows",
    ("Student2", "Course1"): "follows",
    ("City1", "Burkina Faso"): "is in",
    ("City2", "Burkina Faso"): "is in",
    ("Burkina Faso", "Afrique"): "is in",
    ("Cameroun", "Afrique"): "is in",
    ("SEA", "Teacher2"): "employs",
    ("SEA", "Course2"): "gives",
    ("Modern Letter", "Course1"): "gives",
    ("Student1", "Univerity1"): "signed up",
    ("Student2", "Univerity2"): "signed up",
    ("Computer Science", "University2"): "belongs",
    ("Modern Letter", "University1"): "belongs",
    ("SEA", "University2"): "belongs",


    # Relations inverses possibles
    ("Teacher1", "Computer Science"): "teaches in",
    ("Course1", "Computer Science"): "is given in",
    ("Teacher1", "Modern Letter"): "teaches in",
    ("Teacher2", "SEA"): "teaches in",
    ("University1", "Teacher1"): "employs",
    ("University2", "Teacher1"): "employs",
    ("University2", "Teacher2"): "employs",
    ("City1", "Teacher1"): "hosts",
    ("Burkina Faso", "Teacher2"): "is home to",
    ("Teacher2", "Teacher1"): "co-works",
    ("City2", "Teacher2"): "hosts",
    ("Cameroun", "Teacher1"): "is home to",
    ("City1", "University1"): "hosts",
    ("City2", "University2"): "hosts",
    ("Student2", "Course1"): "attends",
    ("Student1", "Course2"): "attends",
    ("Burkina Faso", "City1"): "contains",
    ("Burkina Faso", "City2"): "contains",
    ("Afrique", "Burkina Faso"): "contains",
    ("Afrique", "Cameroun"): "contains",
    ("Teacher2", "SEA"): "teaches in",
    ("Course2", "SEA"): "is given in",
    ("Course1", "Modern Letter"): "is given in",
    ("University2", "Student2"): "contains",
    ("University1", "Student1"): "contains",
    ("University2", "SEA"): "contains",
    ("University1", "Modern Letter"): "contains",
    ("University1", "Computer Science"): "contains",
}

# Couleurs par nœud basées sur l'image
NODE_COLORS = {
    "Computer Science": "#e91e63",  # rose
    "Modern Letter": "#e91e63",  # rose
    "Teacher1": "#ff9999",  # rose clair
    "Teacher2": "#ff9999",  # rose clair
    "University1": "#9c27b0",  # violet
    "University2": "#9c27b0",  # violet
    "Course1": "#90EE90",  # vert clair
    "Course2": "#90EE90",  # vert clair
    "Student1": "#2196f3",  # bleu
    "Student2": "#2196f3",  # bleu
    "City1": "#ffeb3b",  # jaune
    "City2": "#ffeb3b",  # jaune
    "Burkina Faso": "#ff5722",  # orange foncé
    "Cameroon": "#ff5722",  # orange foncé
    "Afrique": "#f44336",  # rouge
    "SEA": "#2196f3"  # bleu
}


class ERDGenerator:
    def __init__(self):
        self.nodes = {}
        self.relations = []
        self.positions = {}
        self.used_colors = set()

    def get_unique_color(self):
        """Retourne une couleur unique non utilisée"""
        available = [color for color in AVAILABLE_COLORS if color not in self.used_colors]
        if not available:
            self.used_colors.clear()
            available = AVAILABLE_COLORS

        color = random.choice(available)
        self.used_colors.add(color)
        return color

    def get_automatic_label(self, source_node, target_node):
        """Génère automatiquement un label basé sur les nœuds source et destination"""
        # Vérifier d'abord les relations prédéfinies exactes
        key = (source_node, target_node)
        if key in PREDEFINED_RELATIONS:
            return PREDEFINED_RELATIONS[key]

        # Logique basée sur les noms des nœuds
        source_lower = source_node.lower()
        target_lower = target_node.lower()

        # Règles de déduction basées sur les patterns
        if "teacher" in source_lower:
            if "course" in target_lower: #or "computer" in target_lower or "letter" in target_lower:
                return "gives"
            elif "university" in target_lower:
                return "teaches at"
            elif "city" in target_lower:
                return "lives in"
            elif target_node in ["Burkina Faso", "Cameroun"]:
                return "comes from"
            elif "student" in target_lower:
                return "teaches"
            elif "teacher" in target_lower:
                return "co-works"
            elif "Computer Science" in target_lower or "Modern Letter" in target_lower or "SEA" in target_lower:
                return "teaches in"

        elif "student" in source_lower:
            if "course" in target_lower:
                return "follows"
            elif "university" in target_lower:
                return "signed up"
            elif "city" in target_lower:
                return "lives in"

        elif "university" in source_lower:
            if "teacher" in target_lower:
                return "employs"
            elif "city" in target_lower:
                return "is located in"
            elif "course" in target_lower:
                return "offers"
            elif "Computer Science" in target_lower or "Modern Letter" in target_lower or "SEA" in target_lower:
                return "contains"

        elif "city" in source_lower:
            if target_node in ["Burkina Faso", "Cameroun"]:
                return "is in"
            elif "teacher" in target_lower or "student" in target_lower or "university" in target_lower:
                return "hosts"

        elif source_node in ["Burkina Faso", "Cameroun"]:
            if target_node == "Afrique":
                return "is in"
            elif "city" in target_lower:
                return "contains"

        elif source_node == "Afrique":
            return "contains"

        elif "course" in source_lower:
            if "student" in target_lower:
                return "is followed by"
            elif "Computer" in target_lower or "Letter" in target_lower or "SEA" in target_lower:
                return "is given in"

        elif source_node in ["Computer Science", "Modern Letter", "SEA"]:
            if "teacher" in target_lower:
                return "employs"
            elif "course" in target_lower:
                return "offers"

        # Label générique si aucune règle ne s'applique
        return "relates to"

    def input_nodes(self):
        """Permet à l'utilisateur de saisir les nœuds ou d'utiliser les nœuds prédéfinis"""
        print("=== SAISIE DES NŒUDS ===")

        print("Voulez-vous utiliser :")
        print("1. Les nœuds prédéfinis de l'image (recommandé)")
        print("2. Créer vos propres nœuds")

        while True:
            try:
                choice = int(input("Votre choix (1-2): "))
                if choice in [1, 2]:
                    break
                else:
                    print("❌ Veuillez entrer 1 ou 2.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")

        if choice == 1:
            # Utiliser les nœuds prédéfinis
            print("\n📋 Nœuds prédéfinis disponibles:")
            for i, node in enumerate(PREDEFINED_NODES, 1):
                print(f"  {i}. {node}")

            print("\nVoulez-vous utiliser tous les nœuds ou en sélectionner quelques-uns ?")
            print("1. Tous les nœuds")
            print("2. Sélectionner des nœuds spécifiques")

            while True:
                try:
                    sub_choice = int(input("Votre choix (1-2): "))
                    if sub_choice in [1, 2]:
                        break
                    else:
                        print("❌ Veuillez entrer 1 ou 2.")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide.")

            if sub_choice == 1:
                # Tous les nœuds
                selected_nodes = PREDEFINED_NODES.copy()
            else:
                # Sélection spécifique
                selected_nodes = []
                print(f"\nSélectionnez les nœuds (1-{len(PREDEFINED_NODES)}). Tapez 0 pour terminer.")

                while True:
                    try:
                        node_idx = int(input(f"Nœud à ajouter (0-{len(PREDEFINED_NODES)}): "))
                        if node_idx == 0:
                            break
                        elif 1 <= node_idx <= len(PREDEFINED_NODES):
                            node_name = PREDEFINED_NODES[node_idx - 1]
                            if node_name not in selected_nodes:
                                selected_nodes.append(node_name)
                                print(f"✅ '{node_name}' ajouté")
                            else:
                                print("❌ Nœud déjà sélectionné")
                        else:
                            print(f"❌ Veuillez entrer un nombre entre 0 et {len(PREDEFINED_NODES)}")
                    except ValueError:
                        print("❌ Veuillez entrer un nombre valide.")

                if not selected_nodes:
                    print("❌ Aucun nœud sélectionné. Utilisation de tous les nœuds.")
                    selected_nodes = PREDEFINED_NODES.copy()

            # Créer les nœuds avec couleurs prédéfinies
            for node_name in selected_nodes:
                color = NODE_COLORS.get(node_name, self.get_unique_color())
                self.nodes[node_name] = {
                    'color': color,
                    'type': 'Predefined',
                    'text': node_name
                }
                print(f"✅ Nœud '{node_name}' créé (Couleur: {color})")

        else:
            # Création manuelle de nœuds
            while True:
                try:
                    num_nodes = int(input("Combien de nœuds voulez-vous créer ? "))
                    if num_nodes > 0:
                        break
                    else:
                        print("❌ Veuillez entrer un nombre positif.")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide.")

            for i in range(num_nodes):
                print(f"\n--- Nœud {i + 1}/{num_nodes} ---")

                while True:
                    node_name = input(f"Nom du nœud {i + 1}: ").strip()
                    if node_name and node_name not in self.nodes:
                        break
                    elif node_name in self.nodes:
                        print("❌ Ce nom de nœud existe déjà.")
                    else:
                        print("❌ Le nom ne peut pas être vide.")

                # Couleur automatique
                color = self.get_unique_color()

                self.nodes[node_name] = {
                    'color': color,
                    'type': 'Custom',
                    'text': node_name
                }

                print(f"✅ Nœud '{node_name}' créé (Couleur: {color})")
