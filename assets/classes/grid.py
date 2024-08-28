import ursina as u
from scripts import manager

class Grid(u.Entity):
    """An entity which serves as a parent to a bunch of quad entities (lines).
    This can vary in size and even when not rendered and could be useful in placing other entities (or tiles)
    usage:
    var = Grid()
    var.render() if you need to render it"""
    
    #def set_properties(self, cell_size=1, width=5, height=5, position=(0,0,0)):
    def __init__(self, cell_size=1, width=5, height=5, position=(0,0,0), name="grid"):
        super().__init__()
        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.position = position
        self.name = name
    
    def grid_to_world(self, x, y, origin="center", coc=False):
        """Calculate the onscreen position of items based on the desired grid position.
        coc = center on cell. moves the object to the center of the cell relative to its positioning"""
        cell_size=self.cell_size
        if origin == "top left":
            world_y = (y + self.height / 2) * cell_size
            world_x = (x - self.width / 2) * cell_size
            if coc:
                world_y -= self.cell_size/2
                world_x += self.cell_size/2
        if origin == "top right":
            world_y = (y + self.height / 2) * cell_size
            world_x = (x + self.width / 2) * cell_size
            if coc:
                world_y -= self.cell_size/2
                world_x -= self.cell_size/2
        if origin == "bottom left":
            world_y = (y - self.height / 2) * cell_size
            world_x = (x - self.width / 2) * cell_size
            if coc:
                world_y += self.cell_size/2
                world_x += self.cell_size/2
        if origin == "bottom right":
            world_y = (y - self.height / 2) * cell_size
            world_x = (x + self.width / 2) * cell_size
            if coc:
                world_y += self.cell_size/2
                world_x -= self.cell_size/2
        if origin == "center":
            world_y = y * cell_size
            world_x = x * cell_size
        return u.Vec3(world_x, world_y, 0)

    
    def render(self):
        """Create line entities to render the grid"""
        for x in range(self.width + 1):  # +1 to include the last line
            for y in range(self.height + 1):
                # Vertical lines
                if x < self.width + 1:
                    line_vertical = u.Entity(
                        parent=self,
                        model='quad',
                        color=u.color.gray,
                        scale=(0.05, self.height * self.cell_size),
                        position=self.grid_to_world(x, self.height / 2, origin="bottom left") + (0, 0, 0.1) + self.position
                    )
                    line_vertical.tags['grid']=""
                # Horizontal lines
                if y < self.height + 1:
                    line_horizontal = u.Entity(
                        parent=self,
                        model='quad',
                        color=u.color.gray,
                        scale=(self.width * self.cell_size, 0.05),
                        position=self.grid_to_world(self.width / 2, y, origin="bottom left") + (0, 0, 0.1) + self.position
                    )
                    line_horizontal.tags['grid']=""
        return self
    def toggle_visibility(self):
        for entity in u.scene.entities:
            if 'grid' in entity.tags:
                entity.enabled = not entity.enabled
    def input(self, key):
        if manager.devmode:
            if key == "space":
                self.toggle_visibility()

