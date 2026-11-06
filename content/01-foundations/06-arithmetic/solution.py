total_seconds = int(input("Seconds: "))

hours = total_seconds // 3600
left_over = total_seconds % 3600
minutes = left_over // 60
seconds = left_over % 60

print(hours, "h", minutes, "m", seconds, "s")
