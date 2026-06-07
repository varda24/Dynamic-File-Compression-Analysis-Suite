import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import os


class Visualizer:
    """Visualize compression data"""

    def __init__(self):
        self.frequency = None
        self.huffman_tree = None

    def plot_frequency_distribution(self, text, output_path):
        """Plot character frequency distribution"""
        self.frequency = Counter(text)

        chars = list(self.frequency.keys())
        counts = list(self.frequency.values())

        # Sort by frequency
        sorted_data = sorted(zip(chars, counts), key=lambda x: x[1], reverse=True)
        chars, counts = zip(*sorted_data)

        plt.figure(figsize=(12, 6))
        plt.bar(chars, counts, color='steelblue')
        plt.title("Character Frequency Distribution", fontsize=16, fontweight='bold')
        plt.xlabel("Characters", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_huffman_tree(self, root, output_path):
        """Plot Huffman tree structure"""
        if root is None:
            return

        # Create networkx tree
        G = nx.DiGraph()
        labels = {}
        self._add_nodes_to_graph(G, root, labels)

        plt.figure(figsize=(14, 8))
        pos = nx.spring_layout(G, k=2, iterations=50)

        # Draw nodes
        node_colors = []
        for node in G.nodes():
            if G.nodes[node].get("is_leaf"):
                node_colors.append('lightblue')  # Leaf nodes
            else:
                node_colors.append('lightgray')  # Internal nodes

        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000)
        nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, edge_color='gray')

        nx.draw_networkx_labels(G, pos, labels, font_size=8)

        plt.title("Huffman Tree Diagram", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

    def _add_nodes_to_graph(self, G, node, labels, parent_id=None, counter=None):
        """Recursively add nodes to graph"""
        if node is None:
            return 0 if counter is None else counter

        if counter is None:
            counter = 0

        current_id = counter
        counter += 1
        is_leaf = node.char is not None
        G.add_node(current_id, is_leaf=is_leaf)
        labels[current_id] = (
            f"{repr(node.char)[1:-1]}\n({node.freq})"
            if is_leaf
            else f"({node.freq})"
        )

        if parent_id is not None:
            G.add_edge(parent_id, current_id)

        counter = self._add_nodes_to_graph(G, node.left, labels, current_id, counter)
        counter = self._add_nodes_to_graph(G, node.right, labels, current_id, counter)

        return counter

    def plot_compression_comparison(self, data, output_path):
        """Plot compression ratio comparison"""
        algorithms = list(data.keys())
        ratios = [data[algo]['ratio'] for algo in algorithms]

        plt.figure(figsize=(10, 6))
        colors = ['#1f77b4', '#ff7f0e']
        bars = plt.bar(algorithms, ratios, color=colors, edgecolor='black', linewidth=2)

        # Add value labels on bars
        for bar, ratio in zip(bars, ratios):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{ratio}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

        plt.title("Compression Ratio Comparison", fontsize=16, fontweight='bold')
        plt.ylabel("Compression Ratio (%)", fontsize=12)
        plt.xlabel("Algorithm", fontsize=12)
        plt.ylim(0, 100)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

    def plot_execution_time_comparison(self, data, output_path):
        """Plot execution time comparison"""
        algorithms = list(data.keys())
        encoding_times = [data[algo]['encoding_time'] for algo in algorithms]
        decoding_times = [data[algo]['decoding_time'] for algo in algorithms]

        x = range(len(algorithms))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))
        bars1 = ax.bar([i - width/2 for i in x], encoding_times, width, label='Encoding Time', color='skyblue')
        bars2 = ax.bar([i + width/2 for i in x], decoding_times, width, label='Decoding Time', color='lightcoral')

        ax.set_title('Execution Time Comparison', fontsize=16, fontweight='bold')
        ax.set_ylabel('Time (seconds)', fontsize=12)
        ax.set_xlabel('Algorithm', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(algorithms)
        ax.legend()

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

    @staticmethod
    def ensure_output_directory(path):
        """Ensure output directory exists"""
        os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
