import pandas as pd

from utilities.road_data import RoadData
from utilities.object_data import ObjectData


class SceneData:
    # Constructor
    def __init__(self, road_boundaries):
        self.roads = []
        self.objects = {}
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
            df.append(
                {
                    "id": self.roads[i].get_id(),
                    "boundary": self.roads[i].get_boundaries(),
                    "speed": self.roads[i].get_median_speed(),
                    "direction": self.roads[i].get_median_direction(),
                    "traffic": self.roads[i].get_median_traffic(),
                }
            )

        df = pd.DataFrame(df)
        df.to_csv(f'{data_path}/data.txt')
