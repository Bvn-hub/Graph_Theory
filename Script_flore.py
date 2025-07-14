def create_diagram(self):
        """Crée et affiche le diagramme ERD orienté"""
        if not self.nodes:
            print("❌ Aucun nœud à afficher.")
            return

        # Générer les positions
        self.generate_positions()

        # Configuration de la figure
        fig, ax = plt.subplots(1, 1, figsize=(18, 14))
        ax.set_xlim(-1, 17)
        ax.set_ylim(-1, 12)
        ax.set_aspect('equal')
        ax.axis('off')

        # Dessiner tous les nœuds
        for node_name, node_info in self.nodes.items():
            if node_name in self.positions:
                self.draw_node(ax, node_name, node_info, self.positions[node_name])

        # Dessiner toutes les relations
        for source, target, label in self.relations:
            if source in self.positions and target in self.positions:
                start_pos = self.positions[source]
                end_pos = self.positions[target]
                self.draw_directed_relation(ax, start_pos, end_pos, label)

        # Titre personnalisé
        ax.text(8, 11.5, 'Diagramme ERD - Domaine Enseignement', fontsize=18, fontweight='bold', ha='center')
        ax.text(8, 11, 'Sous-domaine: Dispensation des cours', fontsize=14, ha='center', style='italic')

        # Statistiques
        ax.text(1, 0.5, f'📊 {len(self.nodes)} nœuds', fontsize=12, fontweight='bold', ha='left')
        ax.text(1, 0, f'🔗 {len(self.relations)} relations orientées', fontsize=12, fontweight='bold', ha='left')

        # Légende
        ax.text(15, 0.5, '→ Direction: Source → Destinataire', fontsize=10, fontweight='bold', ha='right',
                style='italic')
        ax.text(15, 0, '🤖 Labels générés automatiquement', fontsize=10, fontweight='bold', ha='right', style='italic')

        # Cadre principal
        rect = patches.Rectangle((0, 0), 16, 11, linewidth=3, edgecolor='black', facecolor='none')
        ax.add_patch(rect)

        plt.tight_layout()
        plt.show()

    def display_summary(self):
        """Affiche un résumé des données saisies"""
        print("\n" + "=" * 60)
        print("RÉSUMÉ DU DIAGRAMME ERD")
        print("=" * 60)

        print(f"\n📊 NŒUDS ({len(self.nodes)}):")
        for node_name, node_info in self.nodes.items():
            print(f"  • {node_name} - {node_info['color']}")

        print(f"\n🔗 RELATIONS ORIENTÉES ({len(self.relations)}):")
        for source, target, label in self.relations:
            print(f"  • {source} --[{label}]--> {target}")

        print("\n" + "=" * 60)

    def run(self):
        """Exécute le générateur ERD interactif"""
        print("🎓 GÉNÉRATEUR ERD - DOMAINE ENSEIGNEMENT")
        print("=" * 50)
        print("✨ Labels générés automatiquement selon les nœuds")
        print("🎯 Flèches orientées du nœud source vers le destinataire")
        print("📋 Nœuds basés sur l'image fournie")

        try:
            # Saisie des nœuds
            self.input_nodes()

            # Saisie des relations
            self.input_relations()

            # Affichage du résumé
            self.display_summary()

            # Génération du diagramme
            print("\n📈 Génération du diagramme...")
            self.create_diagram()

            # Option de sauvegarde
            save = input("\nVoulez-vous sauvegarder le diagramme? (o/n): ").lower().strip()
            if save in ['o', 'oui', 'y', 'yes']:
                filename = input("Nom du fichier (sans extension): ").strip()
                if not filename:
                    filename = "erd_enseignement"

                plt.savefig(f'{filename}.png', dpi=300, bbox_inches='tight')
                print(f"💾 Diagramme sauvegardé sous '{filename}.png'")

            print("\n✅ Génération terminée avec succès!")

        except KeyboardInterrupt:
            print("\n\n❌ Arrêt du programme par l'utilisateur.")
        except Exception as e:
            print(f"❌ Erreur inattendue: {e}")


def main():
    """Fonction principale"""
    generator = ERDGenerator()
    generator.run()


if __name__ == "__main__":
    main()