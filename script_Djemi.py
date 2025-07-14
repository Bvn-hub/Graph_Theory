def input_relations(self):
        """Permet à l'utilisateur de saisir les relations avec génération automatique des labels"""
        print("\n=== SAISIE DES RELATIONS ===")

        if len(self.nodes) < 2:
            print("❌ Il faut au moins 2 nœuds pour créer des relations.")
            return

        while True:
            try:
                num_relations = int(input("Combien de relations voulez-vous créer ? "))
                if num_relations >= 0:
                    break
                else:
                    print("❌ Veuillez entrer un nombre positif ou zéro.")
            except ValueError:
                print("❌ Veuillez entrer un nombre valide.")

        if num_relations == 0:
            print("Aucune relation ne sera créée.")
            return

        print(f"\nVous allez créer {num_relations} relations.")
        print("💡 Les labels seront générés automatiquement selon les nœuds.")
        print("\nNœuds disponibles:")
        node_list = list(self.nodes.keys())
        for i, node in enumerate(node_list, 1):
            print(f"  {i}. {node}")

        for i in range(num_relations):
            print(f"\n--- Relation {i + 1}/{num_relations} ---")

            # Sélection du nœud source
            while True:
                try:
                    source_idx = int(input(f"Nœud source (1-{len(node_list)}): ")) - 1
                    if 0 <= source_idx < len(node_list):
                        source_node = node_list[source_idx]
                        break
                    else:
                        print(f"❌ Veuillez entrer un nombre entre 1 et {len(node_list)}.")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide.")

            # Sélection du nœud destinataire
            while True:
                try:
                    target_idx = int(input(f"Nœud destinataire (1-{len(node_list)}): ")) - 1
                    if 0 <= target_idx < len(node_list):
                        target_node = node_list[target_idx]
                        break
                    else:
                        print(f"❌ Veuillez entrer un nombre entre 1 et {len(node_list)}.")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide.")

            # Génération automatique du label
            auto_label = self.get_automatic_label(source_node, target_node)

            print(f"\n🔄 Relation créée automatiquement:")
            print(f"   {source_node} --[{auto_label}]--> {target_node}")

            # Demander confirmation ou modification
            confirm = input("Confirmer ce label? (o/n, ou tapez un nouveau label): ").strip()

            if confirm.lower() in ['o', 'oui', 'y', 'yes', '']:
                selected_label = auto_label
            elif confirm.lower() in ['n', 'non', 'no']:
                selected_label = input("Entrez votre label personnalisé: ").strip()
                if not selected_label:
                    selected_label = auto_label
            else:
                selected_label = confirm if confirm else auto_label

            # Ajouter la relation
            self.relations.append((source_node, target_node, selected_label))
            print(f"✅ Relation confirmée: {source_node} --[{selected_label}]--> {target_node}")