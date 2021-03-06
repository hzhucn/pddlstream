(define (stream pr2-tamp)
  (:stream sample-pose
    :inputs (?o ?r)
    :domain (Stackable ?o ?r)
    :outputs (?p)
    :certified (and (Pose ?o ?p) (Supported ?o ?p ?r))
  )
  (:stream sample-grasp
    :inputs (?o)
    :domain (Graspable ?o)
    :outputs (?g)
    :certified (Grasp ?o ?g)
  )
  (:stream inverse-kinematics
    :inputs (?a ?o ?p ?g)
    :domain (and (Controllable ?a) (Pose ?o ?p) (Grasp ?o ?g))
    :outputs (?q ?t)
    :certified (and (BConf ?q) (ATraj ?t) (Kin ?a ?o ?p ?g ?q ?t))
  )
  (:stream plan-base-motion
    :inputs (?q1 ?q2)
    :domain (and (BConf ?q1) (BConf ?q2))
    :outputs (?t)
    :certified (and (BTraj ?t) (BaseMotion ?q1 ?t ?q2))
  )

  (:function (MoveCost ?t)
    (and (BTraj ?t))
  )
  (:predicate (TrajPoseCollision ?t ?o2 ?p2)
    (and (BTraj ?t) (Pose ?o2 ?p2))
  )
  (:predicate (TrajArmCollision ?t ?a ?q)
    (and (BTraj ?t) (AConf ?a ?q))
  )
  (:predicate (TrajGraspCollision ?t ?a ?o ?g)
    (and (BTraj ?t) (Arm ?a) (Grasp ?o ?g))
  )
)