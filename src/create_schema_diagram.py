import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def generate_schema_diagram(dimensions: dict, facts: dict, output_path: str):
    
    "Generates and saves a Star Schema diagram using Matplotlib." 

    fig, ax = plt.subplots(figsize=(20, 12))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 12)
    ax.axis('off')

    table_positions = {}
    table_sizes = {}
    
    fact_bridge_names = list(facts.keys())
    if 'fact_communication' in fact_bridge_names:
        table_positions['fact_communication'] = (8.5, 5.0)
        table_sizes['fact_communication'] = (3, 2.5)

    if 'bridge_comm_user' in fact_bridge_names:
        table_positions['bridge_comm_user'] = (4.5, 5.0)
        table_sizes['bridge_comm_user'] = (3, 2.0)

    # Draw fact and bridge tables
    for name, pos in table_positions.items():
        width, height = table_sizes[name]
        df = facts[name]
        column_text = '\n'.join(df.columns)
        
        ax.add_patch(patches.Rectangle(pos, width, height, facecolor='lightblue', edgecolor='blue', lw=2))
        ax.text(pos[0] + width / 2, pos[1] + height - 0.3, name, ha='center', va='center', fontsize=12, weight='bold')
        ax.text(pos[0] + width / 2, pos[1] + height / 2 - 0.2, column_text, ha='center', va='center', fontsize=8)

    num_dims = len(dimensions)
    radius = 7.0
    center_x, center_y = 10, 6 
    for i, (name, df) in enumerate(dimensions.items()):
        angle = 2 * math.pi * i / num_dims
        x = center_x + radius * math.cos(angle) - 1.5 
        y = center_y + (radius - 2) * math.sin(angle) - 1.0 
        
        width, height = (3, 2)
        column_text = '\n'.join(df.columns)
        
        ax.add_patch(patches.Rectangle((x, y), width, height, facecolor='lightyellow', edgecolor='darkgreen', lw=1.5))
        ax.text(x + width / 2, y + height - 0.3, name, ha='center', va='center', fontsize=10, weight='bold')
        ax.text(x + width / 2, y + height / 2 - 0.3, column_text, ha='center', va='center', fontsize=8)
        
        primary_key = df.columns[0]
        
        target_table_name = None
        for fact_name in facts:
            if primary_key in facts[fact_name].columns:
                target_table_name = fact_name
                break
        
        if target_table_name:
            target_pos = table_positions[target_table_name]
            target_size = table_sizes[target_table_name]
            
            start_point = (x + width / 2, y + height / 2)
            end_point = (target_pos[0] + target_size[0] / 2, target_pos[1] + target_size[1] / 2)
            
            ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='gray', linestyle='--')

    if 'bridge_comm_user' in table_positions and 'fact_communication' in table_positions:
        start_pos = table_positions['bridge_comm_user']
        start_size = table_sizes['bridge_comm_user']
        end_pos = table_positions['fact_communication']
        end_size = table_sizes['fact_communication']
        
        start_point = (start_pos[0] + start_size[0], start_pos[1] + start_size[1] / 2)
        end_point = (end_pos[0], end_pos[1] + end_size[1] / 2)
        
        ax.plot([start_point[0], end_point[0]], [start_point[1], end_point[1]], color='black', linestyle='-')

    fig.suptitle('Star Schema', fontsize=16)
    plt.savefig(output_path, bbox_inches='tight', dpi=150)
    plt.close(fig)
    print(f"Diagram saved to: {output_path}")