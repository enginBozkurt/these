;; Auto-generated. Do not edit!


(when (boundp 'ouster_driver::PacketMsg)
  (if (not (find-package "OUSTER_DRIVER"))
    (make-package "OUSTER_DRIVER"))
  (shadow 'PacketMsg (find-package "OUSTER_DRIVER")))
(unless (find-package "OUSTER_DRIVER::PACKETMSG")
  (make-package "OUSTER_DRIVER::PACKETMSG"))

(in-package "ROS")
;;//! \htmlinclude PacketMsg.msg.html


(defclass ouster_driver::PacketMsg
  :super ros::object
  :slots (_buf ))

(defmethod ouster_driver::PacketMsg
  (:init
   (&key
    ((:buf __buf) (make-array 0 :initial-element 0 :element-type :char))
    )
   (send-super :init)
   (setq _buf __buf)
   self)
  (:buf
   (&optional __buf)
   (if __buf (setq _buf __buf)) _buf)
  (:serialization-length
   ()
   (+
    ;; uint8[] _buf
    (* 1    (length _buf)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8[] _buf
     (write-long (length _buf) s)
     (princ _buf s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8[] _buf
   (let ((n (sys::peek buf ptr- :integer))) (incf ptr- 4)
     (setq _buf (make-array n :element-type :char))
     (replace _buf buf :start2 ptr-) (incf ptr- n))
   ;;
   self)
  )

(setf (get ouster_driver::PacketMsg :md5sum-) "4f7b5949e76f86d01e96b0e33ba9b5e3")
(setf (get ouster_driver::PacketMsg :datatype-) "ouster_driver/PacketMsg")
(setf (get ouster_driver::PacketMsg :definition-)
      "uint8[] buf

")



(provide :ouster_driver/PacketMsg "4f7b5949e76f86d01e96b0e33ba9b5e3")


