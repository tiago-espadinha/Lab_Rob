       if serial_port is not None:
            send_command(serial_port, set_pos_com)
            receive_command(serial_port)
            recv_com = receive_command(serial_port)
            # TODO: Check if position was set correctly

        # Debug mode
        else:
            print("Sent: " + set_pos_com)