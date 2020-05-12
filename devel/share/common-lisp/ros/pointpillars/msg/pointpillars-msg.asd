
(cl:in-package :asdf)

(defsystem "pointpillars-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "pointpillars" :depends-on ("_package_pointpillars"))
    (:file "_package_pointpillars" :depends-on ("_package"))
  ))