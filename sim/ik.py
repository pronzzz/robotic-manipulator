import pybullet as p

class IKSolver:
    def __init__(self, arm_id, end_effector_index):
        self.arm_id = arm_id
        self.ee_index = end_effector_index
        
        # Get the number of joints
        self.num_joints = p.getNumJoints(self.arm_id)
        # Assuming all joints before EE are revolute (0, 1, 2, 3)
        self.joint_indices = [i for i in range(self.num_joints) if p.getJointInfo(self.arm_id, i)[2] == p.JOINT_REVOLUTE]
    
    def solve(self, target_pos, target_orn=None):
        """
        Solves IK for position only, or position+orientation.
        For a 4-DOF arm, position-only is usually preferred unless the orientation is achievable.
        """
        if target_orn:
            joint_poses = p.calculateInverseKinematics(
                self.arm_id, 
                self.ee_index, 
                target_pos, 
                target_orn,
                maxNumIterations=100,
                residualThreshold=1e-4
            )
        else:
            joint_poses = p.calculateInverseKinematics(
                self.arm_id, 
                self.ee_index, 
                target_pos,
                maxNumIterations=100,
                residualThreshold=1e-4
            )
        return list(joint_poses[:len(self.joint_indices)])
