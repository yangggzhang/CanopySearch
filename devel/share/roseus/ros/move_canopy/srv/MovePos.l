;; Auto-generated. Do not edit!


(when (boundp 'move_canopy::MovePos)
  (if (not (find-package "MOVE_CANOPY"))
    (make-package "MOVE_CANOPY"))
  (shadow 'MovePos (find-package "MOVE_CANOPY")))
(unless (find-package "MOVE_CANOPY::MOVEPOS")
  (make-package "MOVE_CANOPY::MOVEPOS"))
(unless (find-package "MOVE_CANOPY::MOVEPOSREQUEST")
  (make-package "MOVE_CANOPY::MOVEPOSREQUEST"))
(unless (find-package "MOVE_CANOPY::MOVEPOSRESPONSE")
  (make-package "MOVE_CANOPY::MOVEPOSRESPONSE"))

(in-package "ROS")





(defclass move_canopy::MovePosRequest
  :super ros::object
  :slots (_x _y _z ))

(defmethod move_canopy::MovePosRequest
  (:init
   (&key
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    ((:z __z) 0.0)
    )
   (send-super :init)
   (setq _x (float __x))
   (setq _y (float __y))
   (setq _z (float __z))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:serialization-length
   ()
   (+
    ;; float64 _x
    8
    ;; float64 _y
    8
    ;; float64 _z
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _x
       (sys::poke _x (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _y
       (sys::poke _y (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _z
       (sys::poke _z (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _x
     (setq _x (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _y
     (setq _y (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _z
     (setq _z (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass move_canopy::MovePosResponse
  :super ros::object
  :slots (_reached ))

(defmethod move_canopy::MovePosResponse
  (:init
   (&key
    ((:reached __reached) nil)
    )
   (send-super :init)
   (setq _reached __reached)
   self)
  (:reached
   (&optional __reached)
   (if __reached (setq _reached __reached)) _reached)
  (:serialization-length
   ()
   (+
    ;; bool _reached
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _reached
       (if _reached (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _reached
     (setq _reached (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(defclass move_canopy::MovePos
  :super ros::object
  :slots ())

(setf (get move_canopy::MovePos :md5sum-) "65467c40f11db30d3240bc807e76bdf9")
(setf (get move_canopy::MovePos :datatype-) "move_canopy/MovePos")
(setf (get move_canopy::MovePos :request) move_canopy::MovePosRequest)
(setf (get move_canopy::MovePos :response) move_canopy::MovePosResponse)

(defmethod move_canopy::MovePosRequest
  (:response () (instance move_canopy::MovePosResponse :init)))

(setf (get move_canopy::MovePosRequest :md5sum-) "65467c40f11db30d3240bc807e76bdf9")
(setf (get move_canopy::MovePosRequest :datatype-) "move_canopy/MovePosRequest")
(setf (get move_canopy::MovePosRequest :definition-)
      "float64 x
float64 y
float64 z
---
bool reached
")

(setf (get move_canopy::MovePosResponse :md5sum-) "65467c40f11db30d3240bc807e76bdf9")
(setf (get move_canopy::MovePosResponse :datatype-) "move_canopy/MovePosResponse")
(setf (get move_canopy::MovePosResponse :definition-)
      "float64 x
float64 y
float64 z
---
bool reached
")



(provide :move_canopy/MovePos "65467c40f11db30d3240bc807e76bdf9")


