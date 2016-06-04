# Assistenzrobotik

## ROS-Anbindung

Möglicherweise ist das ROS_Interface doch besser geeignet als das ROS-Plugin, zumindest sollte das eine ganz gewöhnliche Publisher/Subscriber-Architektur in LUA ermöglichen. Habs aber noch nicht installiert bekommen, mehr dazu hoffentlich morgen (Samstag).

## Aktuelle Aufgaben

im childscript vom Arm:
 - subscribe zielpose
 - rufe Funktion zur IK-Berechnung auf

 - lese Momentum des Arms aus

in externem Skript:
 - subscribe Arm-Status
 - plane Posen (mit Kraftregelung)
 - publishe an VREP


modelliere Umgebung/Roboter

# Altes Zeug

## Troubleshooting

(Annahme: morse-Verzeichnis MORSE = /usr/lib/python3/dist-packages/morse)

### Armatures - ROS

In der initialen Konfiguration lassen sich die vorgegebenen Roboterarme nicht mit ROS ansteuern (oder auslesen). Dieses Problem wurde noch nicht behoben, allerdings wurden einige Erkenntnisse gewonnen:

* In MORSE/builder/data.py werden die middlewares konfiguriert. morse.actuators.armature.Armature besitzt dabei kein ros-Interface.
 * Diese Datei lässt sich bearbeiten, sodass eine middleware (erfolgreich) genutzt wird. Allerdings ist noch nicht klar, wie diese aussehen soll, oder ob bereits ein passendes File existiert.
 * Mit MORSE/middleware/ros/jointstate.py existiert zumindest ein Topic, welches der Arm subscribed. Allerdings verlief das publishen auf dieses Topic bei mir erfolglos, da keine Verbindung aufgebaut werden konnte. (Fehlermeldung: [WARN] [WallTime: 1463226552.770708] Inbound TCP/IP connection failed: connection from sender terminated before handshake header received. 0 bytes were received. Please check sender for additional details.)

* Bereits vorhandene ros-middleware-Module liegen in MORSE/middleware/ros.

* Angeblich lassen sich armatures über das JointTrajectoryAction interface ansprechen.
 * http://www.openrobots.org/morse/doc/latest/user/actuators/armature.html
 * http://wiki.ros.org/joint_trajectory_action
 * Es existiert ein file in MORSE/middleware/ros/overlays/armatures.py, welches angeblich dieses interface nutzt. Ich habe noch nicht verstanden, ob man das separat einbinden muss (über data.py geht es nicht), oder ob es als overlay irgendwo schon dabei ist.

