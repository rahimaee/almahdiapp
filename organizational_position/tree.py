class PositionNode:
    def __init__(self, name, label=None):
        self.name = name
        self.label = label or name
        self.children = []
        self.positions = []
        self.soldier = None
        self.soldiers_count = 0
        self.positions_count = 0

    def add_child(self, child_node):
        self.children.append(child_node)

    def add_position(self, position):
        self.positions.append(position)
        self.positions_count += 1
        self.soldiers_count += getattr(position, "soldiers", []).count() if hasattr(position, "soldiers") else 0


def build_organizational_tree(positions):
    """
    ساختار درختی بر اساس:
    position_parent_group > position_group > position_code
    """
    tree = {}
    parent_groups = {}

    for pos in positions:
        parent_name = pos.position_parent_group or "بدون سرگروه"
        group_name = pos.position_group or "بدون گروه"
        soldier = pos.soldier
        # نود والد
        if parent_name not in parent_groups:
            parent_groups[parent_name] = PositionNode(parent_name)

        parent_node = parent_groups[parent_name]

        # نود گروه
        group_node = next((g for g in parent_node.children if g.name == group_name), None)
        if not group_node:
            group_node = PositionNode(group_name)
            parent_node.add_child(group_node)
            
        # افزودن جایگاه به گروه
        group_node.add_position(pos)

        # ثبت کل درخت
        tree[parent_name] = parent_node

    # محاسبه مجموع‌ها
    for parent in tree.values():
        parent.positions_count = sum(c.positions_count for c in parent.children)
        parent.soldiers_count = sum(c.soldiers_count for c in parent.children)

    return tree