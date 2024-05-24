import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def create_radar_chart(labels, stats):
    num_vars = len(labels)

    # Winkel für die Diagrammberechnung
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Der Radarplot soll rund sein, also müssen wir die Liste schließen
    stats = np.concatenate((stats, [stats[0]]))
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    
    # Füllfarbe auf kräftiges Dunkelblau setzen
    ax.fill(angles, stats,alpha=0.7, color= "black", edgecolor='darkblue', linewidth=2)

    # Schönheitsverbesserungen
    ax.set_yticklabels([])  # Remove radial labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Remove the radial grid lines
    ax.set_rgrids([])

    # Remove the outer circle
    ax.spines['polar'].set_visible(False)

    # Ändern der Farbe der äußeren Linien zu einer helleren Farbe
    ax.xaxis.grid(True, color='darkgrey', linestyle=':', linewidth=1.5)

    return fig

def main():
    # Daten für das Diagramm
    labels = np.array(['Rücken', 'Brust', 'Core', 'Arme', 'Schultern', 'Beine', "Cardio"])
    stats = np.array([6, 2, 5, 3, 4, 5, 3])

    # Streamlit App
    fig = create_radar_chart(labels, stats)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
