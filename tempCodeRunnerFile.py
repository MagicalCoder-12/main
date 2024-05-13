        lasers_to_remove = []  # Create a list to store lasers that need to be removed
        for laser in player.lasers:
            for asteroid in asteroids:
                if check_collision_lasers_asteroid([laser], asteroid['x'], asteroid['y']):
                    print("Collision between laser and asteroid detected")
                    # Determine if a power-up should appear based on probabilities
                    for powerup_type, probability in powerup_probabilities.items():
                        if random.random() <= probability:
                            print(f"Random Number: {random.random()}")
                            print(f"Power-up Type: {powerup_type}, Probability: {probability}")
                            # Create a power-up at the asteroid's position
                            new_powerup_pos = [asteroid['x'], asteroid['y']]
                            random_powerup_image = os.path.join("Assets", "Items", "Fruits", f"{powerup_type.lower()}.png")
                            print(f"Selected Power-up Type: {powerup_type}")
                            new_powerup = PowerUp(random_powerup_image, 17, new_powerup_pos, scale_factor=2)
                            powerups.append(new_powerup)
                    lasers_to_remove.append(laser)  # Add the laser to the removal list
                    asteroids.remove(asteroid)  # Remove the collided asteroid
                    break  # Break out of the inner loop after collision detection