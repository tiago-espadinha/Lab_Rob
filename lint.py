import numpy as np
import time

def move_to_pos_smooth(serial_port, target_pos, move_type, steps=100):
    current_pos = get_pos(serial_port)
    if not current_pos:
        print("Error getting current position.")
        return

    # Calculate step increments for linear interpolation
    step_size = [(target - current) / steps for current, target in zip(current_pos, target_pos)]

    for step in range(1, steps + 1):
        # Calculate the interpolated position
        interpolated_pos = [current + step * size for current, size in zip(current_pos, step_size)]

        # Set the new interpolated position
        if move_type == 'up' or move_type == 'down':
            set_pos_com = f"SETPVC A31 X {interpolated_pos[0]}\r"
        elif move_type == 'left' or move_type == 'right':
            set_pos_com = f"SETPVC A31 Y {interpolated_pos[1]}\r"
        elif move_type == 'forward' or move_type == 'backward':
            set_pos_com = f"SETPVC A31 Z {interpolated_pos[2]}\r"

        send_command(serial_port, set_pos_com)
        receive_command(serial_port)
        receive_command(serial_port)

        # Pause for a short time between each step to control the speed
        time.sleep(0.02)  # Adjust this value based on your desired speed

    # Move to the final target position after interpolation
    move_command = f"MOVE A31 100\r"
    send_command(serial_port, move_command)
    receive_command(serial_port)
    receive_command(serial_port)

    print("Smooth movement complete")

# Example usage:
target_position = [5200, 150, 8000, 0, 0]  # Update with your desired target position
move_type = 'up'  # Update with your desired move type
move_to_pos_smooth(serial_port, target_position, move_type)
