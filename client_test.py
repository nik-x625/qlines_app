import subprocess

def run_command_in_cli(command):
    try:
        # Run the command in the shell, capture the output
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

        # Return the result
        return result.strip()
    except subprocess.CalledProcessError as e:
        # Handle command execution errors
        return f"Error: {e}"

# Example usage:
cli_command = "ls -l"  # Replace with your desired command
output = run_command_in_cli(cli_command)
print(output)
