; Auto-generated. Do not edit!


(cl:in-package move_canopy-srv)


;//! \htmlinclude MovePos-request.msg.html

(cl:defclass <MovePos-request> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0)
   (z
    :reader z
    :initarg :z
    :type cl:float
    :initform 0.0))
)

(cl:defclass MovePos-request (<MovePos-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MovePos-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MovePos-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name move_canopy-srv:<MovePos-request> is deprecated: use move_canopy-srv:MovePos-request instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <MovePos-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader move_canopy-srv:x-val is deprecated.  Use move_canopy-srv:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <MovePos-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader move_canopy-srv:y-val is deprecated.  Use move_canopy-srv:y instead.")
  (y m))

(cl:ensure-generic-function 'z-val :lambda-list '(m))
(cl:defmethod z-val ((m <MovePos-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader move_canopy-srv:z-val is deprecated.  Use move_canopy-srv:z instead.")
  (z m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MovePos-request>) ostream)
  "Serializes a message object of type '<MovePos-request>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'z))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MovePos-request>) istream)
  "Deserializes a message object of type '<MovePos-request>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'z) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MovePos-request>)))
  "Returns string type for a service object of type '<MovePos-request>"
  "move_canopy/MovePosRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MovePos-request)))
  "Returns string type for a service object of type 'MovePos-request"
  "move_canopy/MovePosRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MovePos-request>)))
  "Returns md5sum for a message object of type '<MovePos-request>"
  "65467c40f11db30d3240bc807e76bdf9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MovePos-request)))
  "Returns md5sum for a message object of type 'MovePos-request"
  "65467c40f11db30d3240bc807e76bdf9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MovePos-request>)))
  "Returns full string definition for message of type '<MovePos-request>"
  (cl:format cl:nil "float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MovePos-request)))
  "Returns full string definition for message of type 'MovePos-request"
  (cl:format cl:nil "float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MovePos-request>))
  (cl:+ 0
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MovePos-request>))
  "Converts a ROS message object to a list"
  (cl:list 'MovePos-request
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':z (z msg))
))
;//! \htmlinclude MovePos-response.msg.html

(cl:defclass <MovePos-response> (roslisp-msg-protocol:ros-message)
  ((reached
    :reader reached
    :initarg :reached
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass MovePos-response (<MovePos-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MovePos-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MovePos-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name move_canopy-srv:<MovePos-response> is deprecated: use move_canopy-srv:MovePos-response instead.")))

(cl:ensure-generic-function 'reached-val :lambda-list '(m))
(cl:defmethod reached-val ((m <MovePos-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader move_canopy-srv:reached-val is deprecated.  Use move_canopy-srv:reached instead.")
  (reached m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MovePos-response>) ostream)
  "Serializes a message object of type '<MovePos-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'reached) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MovePos-response>) istream)
  "Deserializes a message object of type '<MovePos-response>"
    (cl:setf (cl:slot-value msg 'reached) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MovePos-response>)))
  "Returns string type for a service object of type '<MovePos-response>"
  "move_canopy/MovePosResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MovePos-response)))
  "Returns string type for a service object of type 'MovePos-response"
  "move_canopy/MovePosResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MovePos-response>)))
  "Returns md5sum for a message object of type '<MovePos-response>"
  "65467c40f11db30d3240bc807e76bdf9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MovePos-response)))
  "Returns md5sum for a message object of type 'MovePos-response"
  "65467c40f11db30d3240bc807e76bdf9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MovePos-response>)))
  "Returns full string definition for message of type '<MovePos-response>"
  (cl:format cl:nil "bool reached~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MovePos-response)))
  "Returns full string definition for message of type 'MovePos-response"
  (cl:format cl:nil "bool reached~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MovePos-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MovePos-response>))
  "Converts a ROS message object to a list"
  (cl:list 'MovePos-response
    (cl:cons ':reached (reached msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'MovePos)))
  'MovePos-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'MovePos)))
  'MovePos-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MovePos)))
  "Returns string type for a service object of type '<MovePos>"
  "move_canopy/MovePos")