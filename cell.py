class Cell:
    def __init__(self, bubble):
        self.owner = bubble

    # def pull_neighbors(self):
    #     for neighbor in neighbors:
    #         neighbor.forces_applied.append(())

    def calculate_force(self):
        for neighbor in neighbors:
            neighbor.rect.center

        # self.owner.