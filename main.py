import sys
import time
from sim.scene import Scene
from sim.ik import IKSolver
from sim.executor import Executor
from llm.parser import LLMParser

def main(command):
    # 1. Initialize Scene
    print("Initializing Simulation...")
    scene = Scene(gui=True)
    time.sleep(1) # Let PyBullet settle
    
    # 2. Initialize IK & Executor
    # End effector index is 4 based on arm.urdf
    ik_solver = IKSolver(scene.arm, end_effector_index=4)
    executor = Executor(scene, ik_solver)
    
    # 3. Parse command with LLM
    print(f"Command: '{command}'")
    parser = LLMParser(list(scene.registry.keys()))
    plan = parser.parse_command(command)
    
    if not plan:
        print("Failed to generate a valid plan.")
        return

    print("Plan:", plan)
    
    # 4. Execute Plan
    for step in plan["steps"]:
        action = step["action"]
        target = step.get("target")
        
        if action == "move_to":
            print(f"Moving to {target}...")
            target_pos = scene.get_object_position(target)
            executor.move_to(target_pos)
            
        elif action == "grasp":
            # Grasping the last target we moved to
            executor.grasp(target if target else "red_block")
            
        elif action == "release":
            executor.release()
            
        time.sleep(0.5)

    print("Execution complete. Keeping simulation open for 5 seconds...")
    for _ in range(5 * 240):
        scene.step()
        time.sleep(1/240.0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = " ".join(sys.argv[1:])
    else:
        command = "pick up the red block and place it on the shelf"
    main(command)
