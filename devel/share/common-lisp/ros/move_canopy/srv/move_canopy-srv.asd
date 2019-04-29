
(cl:in-package :asdf)

(defsystem "move_canopy-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "MovePos" :depends-on ("_package_MovePos"))
    (:file "_package_MovePos" :depends-on ("_package"))
  ))