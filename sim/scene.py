import pybullet as p
import pybullet_data
import time

class Scene:
    def __init__(self, gui=True):
        self.client = p.connect(p.GUI if gui else p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)

        # Load plane and table
        self.plane = p.loadURDF("plane.urdf")
        self.table = p.loadURDF("table/table.urdf", basePosition=[0.5, 0, -0.65])

        # Load arm
        self.arm_start_pos = [0, 0, 0]
        self.arm_start_orientation = p.getQuaternionFromEuler([0, 0, 0])
        self.arm = p.loadURDF("sim/urdf/arm.urdf", self.arm_start_pos, self.arm_start_orientation, useFixedBase=True)

        # Load objects (red block and a visual shelf)
        self.red_block = p.loadURDF("cube_small.urdf", basePosition=[0.4, 0.2, 0.05])
        p.changeVisualShape(self.red_block, -1, rgbaColor=[1, 0, 0, 1])

        # Shelf is just a box
        shelf_half_extents = [0.15, 0.15, 0.02]
        col_shape_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=shelf_half_extents)
        vis_shape_id = p.createVisualShape(p.GEOM_BOX, halfExtents=shelf_half_extents, rgbaColor=[0.5, 0.3, 0.1, 1])
        self.shelf = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=col_shape_id, baseVisualShapeIndex=vis_shape_id, basePosition=[0.4, -0.3, 0.2])

        # Camera setup
        p.resetDebugVisualizerCamera(cameraDistance=1.5, cameraYaw=45, cameraPitch=-30, cameraTargetPosition=[0.5, 0, 0])

        # Registry for LLM parsing
        self.registry = {
            "red_block": p.getBasePositionAndOrientation(self.red_block)[0],
            "shelf": [0.4, -0.3, 0.22] # Slightly above the shelf
        }
        
    def step(self):
        p.stepSimulation()

    def get_object_position(self, obj_name):
        if obj_name == "red_block":
            return p.getBasePositionAndOrientation(self.red_block)[0]
        elif obj_name == "shelf":
            return self.registry["shelf"]
        return None

if __name__ == "__main__":
    scene = Scene()
    print("Scene loaded successfully!")
    for _ in range(100):
        scene.step()
        time.sleep(1/240.0)
    p.disconnect()
