from generators import TerrainGenerator

class LatitudeClimateBands(TerrainGenerator):
    def __init__(self, minLatitude=-80.0, maxLatitude=80.0, equatorialTemperature=1, polarTemperature=-1, zeroAltitude=700.0):
        self.minLatitude=minLatitude
        self.maxLatitude=maxLatitude
        self.polarTemperature = polarTemperature
        self.equatorialTemperature = equatorialTemperature
        self.zeroAltitude = zeroAltitude

    def apply(self, grid):
        print "Applying climate bands"
        minX, minY, minZ = grid.min
        maxX, maxY, maxZ = grid.max

        temperatureRange = self.equatorialTemperature - self.polarTemperature
        temperatureDelta = temperatureRange / 90.0
        gridHeight = maxY - minY

        degreesPerUnit = (self.maxLatitude - self.minLatitude) / gridHeight

        for node in grid.nodes():
            nodeX, nodeY, nodeZ = node.location

            latitude = (nodeY - minY) * degreesPerUnit + self.minLatitude

            if node.contents.height > 0:
                altitudeFactor = (self.zeroAltitude - node.contents.height) / self.zeroAltitude
            else:
                altitudeFactor = 1.0

            node.contents.temperature = self.polarTemperature + (90 - abs(latitude)) * temperatureDelta * altitudeFactor

