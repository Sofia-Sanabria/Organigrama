import networkx as nx
import matplotlib.pyplot as plt

def draw_org_chart():
    # Crear un grafo dirigido (DiGraph)
    G = nx.DiGraph()

    # Añadir nodos al grafo
    G.add_nodes_from(["CEO", "Gerente de Desarrollo de Aplicaciones", "Back-End Developer", "Front-end Developer", "Administración de Bases de Datos", "Diseñador Web"])

    # Añadir aristas que representan las relaciones jerárquicas
    G.add_edges_from([("CEO", "Gerente de Desarrollo de Aplicaciones"), ("CEO", "Back-End Developer"),
                      ("Gerente de Desarrollo de Aplicaciones", "Administración de Bases de Datos"), ("Gerente de Desarrollo de Aplicaciones", "Diseñador Web"),
                      ("Back-End Developer", "Front-end Developer")])

    # Definir posiciones para los nodos
    pos = {"CEO": (0, 0), "Gerente de Desarrollo de Aplicaciones": (-1, -1), "Back-End Developer": (1, -1),
           "Administración de Bases de Datos": (-2, -2), "Diseñador Web": (0, -2), "Front-end Developer": (2, -2)}

    # Crear una figura explícita con un número específico
    plt.figure(num="Organigrama Aplicacion Web")

    # Dibujar el grafo
    nx.draw(G, pos, with_labels=True, arrowsize=20, node_size=3000, node_color="mistyrose", font_size=8, font_color="black", font_weight="bold")

    # Mostrar el organigrama
    plt.show()

if __name__ == "__main__":
    draw_org_chart()
