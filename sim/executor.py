import pybullet as p
import time
import numpy as np

class Executor:
    def __init__(self, scene, ik_solver):
        self.scene = scene
        self.ik = ik_solver
        self.arm_id = self.scene.arm
        self.ee_index = self.ik.ee_index
        self.attached_object = None
        self.attach_constraint = None

    def move_to_joint_target(self, target_joints, duration=2.0, steps_per_sec=240):
        """Interpolates and steps joints."""
        current_joints = [p.getJointState(self.arm_id, i)[0] for i in self.ik.joint_indices]
        num_steps = int(duration * steps_per_sec)
        
        for step in range(num_steps):
            t = step / float(num_steps)
            # Smooth interpolation
            smooth_t = 0.5 * (1.0 - np.cos(t * np.pi))
            
            interp_joints = []
            for i in range(len(target_joints)):
                val = current_joints[i] + smooth_t * (target_joints[i] - current_joints[i])
                interp_joints.append(val)
                
            p.setJointMotorControlArray(
                self.arm_id, 
                self.ik.joint_indices, 
                p.POSITION_CONTROL, 
                targetPositions=interp_joints
            )
            self.scene.step()
            time.sleep(1.0 / steps_per_sec)
            
    def move_to(self, target_pos):
        """Moves end effector to target position (x, y, z)."""
        # We specify a default pitch for the gripper (e.g. pointing down)
        target_orn = p.getQuaternionFromEuler([0, 1.57, 0])
        joint_targets = self.ik.solve(target_pos, target_orn)
        self.move_to_joint_target(joint_targets)

    def grasp(self, target_obj_name):
        """Kinematic grasp of the nearest object."""
        if target_obj_name == "red_block":
            obj_id = self.scene.red_block
            
            # Check distance
            ee_pos = p.getLinkState(self.arm_id, self.ee_index)[0]
            obj_pos = p.getBasePositionAndOrientation(obj_id)[0]
            dist = np.linalg.norm(np.array(ee_pos) - np.array(obj_pos))
            
            if dist < 0.15: # Grab range
                print(f"Grasping {target_obj_name}...")
                self.attached_object = obj_id
                
                # Create a fixed constraint between EE and object
                self.attach_constraint = p.createConstraint(
                    self.arm_id, self.ee_index,
                    obj_id, -1,
                    p.JOINT_FIXED,
                    [0, 0, 0],
                    [0, 0, 0.05], # offset relative to EE
                    [0, 0, 0]  # offset relative to object
                )
            else:
                print(f"Failed to grasp {target_obj_name}. Too far: {dist:.2f}m")
        else:
            print(f"Cannot grasp {target_obj_name}")

    def release(self):
        """Release currently grasped object."""
        if self.attach_constraint is not None:
            print("Releasing object...")
            p.removeConstraint(self.attach_constraint)
            self.attach_constraint = None
            self.attached_object = None
        else:
            print("Nothing to release.")
