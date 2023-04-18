import pygame
import random


class Game:

    def __init__(self):
        # starting coordinates of robot1
        self.closest_obstacle = (0, 0)
        self.x = 0
        self.y = 0
        # grid square dimensions
        self.width = 60
        self.height = 60

        # playing area dimensions
        self.gridw = 600
        self.gridh = 600

        # target coordinates
        self.dest_x = 0
        self.dest_y = 0

        self.ob_coordinates = []
        pygame.init()

        # create a screen:
        self.screen = pygame.display.set_mode((self.gridw, self.gridh))
        self.main()

    def main(self):
        self.screen.fill((255, 255, 255))
        self.ob_coordinates = self.drawObstacles()
        self.closest_obstacle = self.detectObstacles(self.ob_coordinates)
        pygame.time.set_timer(pygame.USEREVENT, 500)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                elif event.type == pygame.USEREVENT:
                    self.move(self.closest_obstacle)
                    if self.x == self.dest_x and self.y == self.dest_y:
                        pygame.time.set_timer(pygame.USEREVENT, 0)
                        pygame.draw.rect(self.screen, "green", (self.x, self.y, self.width, self.height))
                        pygame.display.update()

            self.drawGrid()

    # create the grid environment
    def drawGrid(self):

        for x in range(0, 600, 60):
            pygame.draw.line(self.screen, 0, (1, x), (600, x), 2)
            pygame.draw.line(self.screen, 0, (x, 1), (x, 600), 2)
        pygame.display.update()

    # move the robot to the closest obstacle
    def move(self, closest_ob):
        vel = 60

        self.dest_x = closest_ob[0]
        self.dest_y = closest_ob[1]

        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.display.update()

        # clear robot's old position
        old_x = self.x
        old_y = self.y
        pygame.draw.rect(self.screen, (255, 255, 255), (old_x, old_y, self.width, self.height))

        if self.y > self.dest_y:
            self.y -= vel  # go up
        elif self.y < self.dest_y:
            self.y += vel  # go down
        else:
        # Only update x coordinate if the robot is not moving vertically
            if self.y == self.dest_y:
                if self.x < self.dest_x:
                    self.x += vel
                elif self.x > self.dest_x:
                    self.x -= vel

        pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        pygame.display.update()

    def genMap(self):

        rows = 10

        cols = 10

        # Generate the matrix with all 0's
        self.matrix = [[0 for j in range(cols)] for i in range(rows)]

        # alarm is not placed in robot starting position
        self.matrix[self.y // self.height][self.x // self.width] = 0

        # control number of total generated alarms
        for (i) in range(3):
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
            self.matrix[row][col] = 1

    def drawObstacles(self):
        self.genMap()  # generate random placement for alarms

        # paint obstacles to screen
        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[0])):
                if self.matrix[y][x] == 1:
                    rect = pygame.Rect(x * self.width, y * self.height, self.width, self.height)
                    pygame.draw.rect(self.screen, "blue", rect)
                    coords = (x * self.width, y * self.height)
                    self.ob_coordinates.append(coords)

        pygame.display.update()
        return self.ob_coordinates

    # given the set of obstacles find the closest obstacle to the robot
    def detectObstacles(self, ob_coordinates):
        player_pos = (self.x, self.y)

        print(ob_coordinates)

        # initialize the closest distance and obstacle to the first obstacle in the set
        closest_dist = ((ob_coordinates[0][0] - player_pos[0]) ** 2 +
                        (ob_coordinates[0][1] - player_pos[1]) ** 2) ** 0.5
        self.closest_obstacle = ob_coordinates[0]

        # iterate over all obstacles and update closest distance and obstacle if a closer one is found
        for coord in ob_coordinates:
            dist = ((coord[0] - player_pos[0]) ** 2 + (coord[1] - player_pos[1]) ** 2) ** 0.5
            if dist < closest_dist:
                closest_dist = dist
                self.closest_obstacle = coord

        return self.closest_obstacle

if __name__ == "__main__":
    Game()
