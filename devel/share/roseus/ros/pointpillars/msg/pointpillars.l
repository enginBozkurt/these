;; Auto-generated. Do not edit!


(when (boundp 'pointpillars::pointpillars)
  (if (not (find-package "POINTPILLARS"))
    (make-package "POINTPILLARS"))
  (shadow 'pointpillars (find-package "POINTPILLARS")))
(unless (find-package "POINTPILLARS::POINTPILLARS")
  (make-package "POINTPILLARS::POINTPILLARS"))

(in-package "ROS")
;;//! \htmlinclude pointpillars.msg.html


(defclass pointpillars::pointpillars
  :super ros::object
  :slots (_message _count ))

(defmethod pointpillars::pointpillars
  (:init
   (&key
    ((:message __message) "")
    ((:count __count) 0)
    )
   (send-super :init)
   (setq _message (string __message))
   (setq _count (round __count))
   self)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:count
   (&optional __count)
   (if __count (setq _count __count)) _count)
  (:serialization-length
   ()
   (+
    ;; string _message
    4 (length _message)
    ;; uint32 _count
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;; uint32 _count
       (write-long _count s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint32 _count
     (setq _count (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get pointpillars::pointpillars :md5sum-) "89498e8c3e7e4e4d3ec5e32aa108f04d")
(setf (get pointpillars::pointpillars :datatype-) "pointpillars/pointpillars")
(setf (get pointpillars::pointpillars :definition-)
      "string message
uint32 count


")



(provide :pointpillars/pointpillars "89498e8c3e7e4e4d3ec5e32aa108f04d")


