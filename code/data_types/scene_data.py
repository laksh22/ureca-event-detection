import pandas as pd
import numpy as np

from data_types.road_data import RoadData
from data_types.object_data import ObjectData


class SceneData:
    # Constructor
    def __init__(self):
        self.roads = []
        self.objects = {}

    def make_testing_scene_data(self, scene_data_path):
        data = pd.read_csv(scene_data_path)
        for index, row in data.iterrows():
            boundary_0 = list(map(int, eval(row.boundary_0)))
            boundary_1 = list(map(int, eval(row.boundary_1)))
            boundary_2 = list(map(int, eval(row.boundary_2)))
            boundary_3 = list(map(int, eval(row.boundary_3)))
            road_boundaries = np.array(
                [boundary_0, boundary_1, boundary_2, boundary_3])

            road = RoadData(int(row.id), road_boundaries)
            road.set_trained_params(float(row.speed), float(
                row.direction), float(row.traffic))
            road.debug_trained()
            self.roads.append(road)

    def make_training_scene_data(self, road_boundaries):
        for i in range(len(road_boundaries)):
            self.roads.append(RoadData(i, road_boundaries[i]))

    # Take in objects of the scene and update object and road values
    def update_scene(self, frame_objects):
        # 1. Update the objects
        for index, row in frame_objects.iterrows():
            if row.obj_id in self.objects:  # If we already have data about this object
                row_object = self.objects[row.obj_id]
                row_object.update_object((row.x, row.y))
                # 2.a Update speed, direction, and traffic count for respective roads
                for road in self.roads:
                    if road.contains(row_object.curr_point):
                        road.add_speed(row_object.get_speed())
                        road.add_direction(row_object.get_direction())
                        road.update_traffic_count()
            else:  # Object just appeared on the scene
                row_object = self.objects[row.obj_id] = ObjectData(
                    (row.x, row.y))
                # 2.b Update traffic count for respective roads
                for road in self.roads:
                    if road.contains(row_object.curr_point):
                        road.update_traffic_count()

        # 3. For each road, add traffic count to list
        for road in self.roads:
            road.add_traffic()
            road.debug()

    # Save the scene data in CSV format

    def save(self, data_path):
        df = []
        for i in range(len(self.roads)):
            print(self.roads[i].get_boundaries())
            road_boundaries = self.roads[i].get_boundaries()
            df.append(
                {
                    "id": self.roads[i].get_id(),
                    "boundary_0": [road_boundaries[0][0], road_boundaries[0][1]],
                    "boundary_1": [road_boundaries[1][0], road_boundaries[1][1]],
                    "boundary_2": [road_boundaries[2][0], road_boundaries[2][1]],
                    "boundary_3": [road_boundaries[3][0], road_boundaries[3][1]],
                    "speed": self.roads[i].get_median_speed(),
                    "direction": self.roads[i].get_median_direction(),
                    "traffic": self.roads[i].get_median_traffic(),
                }
            )

        df = pd.DataFrame(df)
        df.to_csv(f'{data_path}/data.csv')