def generate_positions(self):
        """Génère des positions automatiques pour les nœuds"""
        nodes_list = list(self.nodes.keys())
        num_nodes = len(nodes_list)

        if num_nodes == 0:
            return

        # Calculer la disposition en grille
        cols = int(np.ceil(np.sqrt(num_nodes)))
        rows = int(np.ceil(num_nodes / cols))

        # Espacement entre les nœuds
        x_spacing = 14 / max(1, cols - 1) if cols > 1 else 0
        y_spacing = 8 / max(1, rows - 1) if rows > 1 else 0

        # Décalage pour centrer
        x_offset = 1
        y_offset = 1

        for i, node in enumerate(nodes_list):
            row = i // cols
            col = i % cols

            x = x_offset + col * x_spacing
            y = y_offset + row * y_spacing

            self.positions[node] = (x, y)

    def draw_node(self, ax, name, node_info, pos):
        """Dessine un nœud sur le graphique"""
        x, y = pos

        # Créer un rectangle arrondi pour les nœuds
        rect = patches.FancyBboxPatch((x - 0.8, y - 0.5), 1.6, 1.0,
                                      boxstyle="round,pad=0.1",
                                      facecolor=node_info['color'],
                                      edgecolor='black', linewidth=2)
        ax.add_patch(rect)

        # Ajout du texte
        text_color = 'white' if node_info['color'] not in ['#ffeb3b', '#90EE90'] else 'black'
        ax.text(x, y, node_info['text'], ha='center', va='center',
                fontsize=8, fontweight='bold', color=text_color)

    def draw_directed_relation(self, ax, start_pos, end_pos, label):
        """Dessine une relation orientée entre deux nœuds avec une flèche"""
        x1, y1 = start_pos
        x2, y2 = end_pos

        # Éviter les divisions par zéro
        if abs(x2 - x1) < 0.01 and abs(y2 - y1) < 0.01:
            return

        # Calcul du vecteur directionnel
        dx = x2 - x1
        dy = y2 - y1
        distance = np.sqrt(dx ** 2 + dy ** 2)

        if distance == 0:
            return

        # Normalisation
        dx_norm = dx / distance
        dy_norm = dy / distance

        # Points sur les bords des rectangles
        start_x = x1 + 0.8 * dx_norm
        start_y = y1 + 0.5 * dy_norm
        end_x = x2 - 0.8 * dx_norm
        end_y = y2 - 0.5 * dy_norm

        # Dessiner la ligne principale
        ax.plot([start_x, end_x], [start_y, end_y], 'k-', linewidth=2)

        # Calcul des points pour la flèche
        arrow_length = 0.3
        arrow_angle = np.pi / 6  # 30 degrés

        # Point de la pointe de la flèche
        arrow_tip_x = x2 - 0.9 * dx_norm
        arrow_tip_y = y2 - 0.6 * dy_norm

        # Calcul des deux branches de la flèche
        cos_angle = np.cos(arrow_angle)
        sin_angle = np.sin(arrow_angle)

        # Branche gauche
        arrow_left_x = arrow_tip_x - arrow_length * (dx_norm * cos_angle + dy_norm * sin_angle)
        arrow_left_y = arrow_tip_y - arrow_length * (dy_norm * cos_angle - dx_norm * sin_angle)

        # Branche droite
        arrow_right_x = arrow_tip_x - arrow_length * (dx_norm * cos_angle - dy_norm * sin_angle)
        arrow_right_y = arrow_tip_y - arrow_length * (dy_norm * cos_angle + dx_norm * sin_angle)

        # Dessiner la flèche
        ax.plot([arrow_tip_x, arrow_left_x], [arrow_tip_y, arrow_left_y], 'k-', linewidth=2)
        ax.plot([arrow_tip_x, arrow_right_x], [arrow_tip_y, arrow_right_y], 'k-', linewidth=2)

        # Ajouter le label au milieu de la relation
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        # Calculer l'angle de la ligne pour orienter le texte
        angle_rad = np.arctan2(dy, dx)
        angle_deg = np.degrees(angle_rad)

        # Ajuster l'angle pour que le texte soit toujours lisible
        if angle_deg > 90 or angle_deg < -90:
            angle_deg += 180

        ax.text(mid_x, mid_y, label, ha='center', va='center',
                fontsize=7, rotation=angle_deg, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3",
                          facecolor='lightblue', alpha=0.9, edgecolor='navy'))