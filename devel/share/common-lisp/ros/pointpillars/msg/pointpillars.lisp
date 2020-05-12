; Auto-generated. Do not edit!


(cl:in-package pointpillars-msg)


;//! \htmlinclude pointpillars.msg.html

(cl:defclass <pointpillars> (roslisp-msg-protocol:ros-message)
  ((message
    :reader message
    :initarg :message
    :type cl:string
    :initform "")
   (count
    :reader count
    :initarg :count
    :type cl:integer
    :initform 0))
)

(cl:defclass pointpillars (<pointpillars>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <pointpillars>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'pointpillars)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pointpillars-msg:<pointpillars> is deprecated: use pointpillars-msg:pointpillars instead.")))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <pointpillars>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pointpillars-msg:message-val is deprecated.  Use pointpillars-msg:message instead.")
  (message m))

(cl:ensure-generic-function 'count-val :lambda-list '(m))
(cl:defmethod count-val ((m <pointpillars>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pointpillars-msg:count-val is deprecated.  Use pointpillars-msg:count instead.")
  (count m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <pointpillars>) ostream)
  "Serializes a message object of type '<pointpillars>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'count)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'count)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'count)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'count)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <pointpillars>) istream)
  "Deserializes a message object of type '<pointpillars>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'count)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'count)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'count)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'count)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<pointpillars>)))
  "Returns string type for a message object of type '<pointpillars>"
  "pointpillars/pointpillars")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'pointpillars)))
  "Returns string type for a message object of type 'pointpillars"
  "pointpillars/pointpillars")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<pointpillars>)))
  "Returns md5sum for a message object of type '<pointpillars>"
  "89498e8c3e7e4e4d3ec5e32aa108f04d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'pointpillars)))
  "Returns md5sum for a message object of type 'pointpillars"
  "89498e8c3e7e4e4d3ec5e32aa108f04d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<pointpillars>)))
  "Returns full string definition for message of type '<pointpillars>"
  (cl:format cl:nil "string message~%uint32 count~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'pointpillars)))
  "Returns full string definition for message of type 'pointpillars"
  (cl:format cl:nil "string message~%uint32 count~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <pointpillars>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'message))
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <pointpillars>))
  "Converts a ROS message object to a list"
  (cl:list 'pointpillars
    (cl:cons ':message (message msg))
    (cl:cons ':count (count msg))
))
