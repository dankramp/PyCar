# PyCar
Python car driving API for use with PyGame. See *bot.py* for an example of how to use car.py as an object in another file.

## To use car.py
car.py has its own main method. If you chose to run `python3 car.py`, you can use the arrow keys to practice driving the car around onscreen.

Otherwise, the Car class can be imported to another file and its methods used to control the car. The file you import into must initialize and instance of **pygame** and then the car can be controlled each tick of the clock. The following functions can be called to control the car:

### Controller functions
- `car.accelerate(value)`: This function changes the speed of the car when the car is updated at the end of the tick. *value* is a number in the range [-1,1] that essentially expresses how hard the gas pedal is pressed, 0 being not at all and 1 being all the way to the floor for max acceleration. A negative value indicates a negative acceleration (reversing). Any numbers outside of the range will be reduced to the unit value (1 or -1).
- `car.turn_wheels(clockwise)`: This function effectively turns the steering wheel so that the wheels turn 1 degree. *clockwise* is a boolean value that specifies which direction the wheels should rotate. The maxiumum angle that the wheels can turn from straight is specified by MAX_ANGLE at the top of the file.
- `car.brake(value)`: This function reduces the speed of the car towards 0. *value* is a number in the range (0,1] and specifies how hard the brake is pressed, 1 being all the way down. At 1, the car will lose 30% of its speed each tick.
- `car.get_turn_info(wheel_angle)`: This function returns an object with parameters 'center' and 'radius'. 'center' is the point about which the car will rotate if its wheels were turned to *wheel_angle* and 'radius' is the radius about which its back inside wheel rotates. This is useful for determining if a point is reachable given the current wheel angle or a speculative angle.

After all calculations and controller functions are called, the user must call `car.update()` followed by `car.draw(screen, color)` each tick. Calls to the controller functions do not take effect until `car.update()` is called, at which point the changes are applied then reset. If controller functions are called more than once before updating the car, only the last calls will have any effect (if they were valid calls).

### Other things to know
- You can check the values of the car's current state by accessing the variables, but do not alter them by any means other than through controller functions or else the car will not behave properly.
- The car's speed is reduced by 5% every update naturally, so it will eventually come to a stop if not accelerated.
- `car.angle` is the angle of deflection of the car's body from the vertical, with 0 degrees pointing upwards. This angle increases clockwise and is in **radians**.
- `car.wheel_angle` is the angle of deflection of the car's wheels from *the car's body*, with 0 degrees being straightly aligned. This angle also increases clockwise but is in **degrees**.
