# Assistenzrobotik

## ROS-Anbindung

Möglicherweise ist das ROS_Interface doch besser geeignet als das ROS-Plugin, da es eine ganz gewöhnliche Publisher/Subscriber-Architektur in LUA ermöglicht. Das würde aber bedeuten, dass wir den Status des Arms selbst auslesen müssen, um ihn zu publishen. (@Felix: Du bist da hoffentlich der Experte. :) )

### Installation ROS-Interface

1. Möglichkeit:
 
 In $(VREP_DIR)/compiledRosPlugins liegt bereits das File libv_repExtRosInterface.so. Zieht das direkt in $(VREP_DIR) hinein, wo auch alle anderen .so-Dateien liegen. Vielleicht reicht das bei euch schon; bei mir musste ich den Kram aber selbst kompilieren.

2. Möglichkeit:

 In $(VREP_DIR)/programming/ros_packages liegt der Ordner vrep_ros_interface. Der muss erstmal kompiliert werden. Bei mir hat das nicht direkt vor Ort geklappt, also habe ich ihn in einen anderen Ordner (der auch ein catkin_workspace war, vielleicht ist das wichtig) verschoben. Die Struktur sah also so aus: catkin_ws/src/vrep_ros_interface.
 
 Ach ja, darin gibt es auch eine Readme, die euch empfiehlt, v_repSubsGen zu installieren. Macht das mal so, wie empfohlen; am Ende liegt der Ordner "external" bei mir innerhalb von vrep_ros_interface.

 Um catkin build durchzuführen, müsst ihr erstmal die catkin_tools installieren (mit catkin_make hats bei mir nicht geklappt). Das geht über "sudo pip install catkin_tools". Danach catkin build in catkin_ws ausführen.
 
 Das müsste die Ordner build, devel und logs generieren. In devel/lib sollte jetzt libv_repExtRosInterface.so liegen. Einfach in $(VREP_DIR) kopieren, dann hats zummindest bei mir geklappt.


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

