#include <SimpleFOC.h>

// 1. Instanciar el Sensor (AS5600 usa I2C)
MagneticSensorI2C sensor = MagneticSensorI2C(AS5600_I2C);

// 2. Instanciar el Driver
// Para Arduino Mega, esta es una combinación muy estable:
BLDCDriver3PWM driver = BLDCDriver3PWM(2, 3, 5);

// 3. Instanciar el Motor
// El motor 2804 suele tener 7 pares de polos (compruébalo si es necesario)
BLDCMotor motor = BLDCMotor(7);

// Comandante para interactuar por el monitor serie
Commander command = Commander(Serial);
void doTarget(char* cmd) { command.scalar(&motor.target, cmd); }

void setup() {
  // Inicializar sensor
  sensor.init();
  motor.linkSensor(&sensor);

  // Configuración del Driver
  driver.voltage_power_supply = 12; // Ajusta a tu fuente de poder
  driver.init();
  motor.linkDriver(&driver);

  // Configuración de control (Velocidad en este caso)
  motor.controller = MotionControlType::velocity;
  
  // Límites y PID (Valores iniciales seguros)
  motor.voltage_limit = 6;   // Voltaje máximo (empieza bajo por seguridad)
  motor.PID_velocity.P = 0.2;
  motor.PID_velocity.I = 2;
  
  // Inicializar comunicación serie
  Serial.begin(115200);
  motor.useMonitoring(Serial);

  // Inicializar motor
  motor.init();
  motor.initFOC(); // Aquí el motor hará un pequeño movimiento para calibrarse

  // Añadir comando para cambiar velocidad desde el monitor serie
  command.add('T', doTarget, "target velocity");

  Serial.println("Motor listo. Escribe T + velocidad (ej. T2) en el monitor serie.");
}

void loop() {
  // Función principal de FOC (debe ejecutarse lo más rápido posible)
  motor.loopFOC();

  // Función de movimiento (según el target definido)
  motor.move();

  // Escuchar comandos serie
  command.run();
}