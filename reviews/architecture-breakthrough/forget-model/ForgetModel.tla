---------------- MODULE ForgetModel ----------------
EXTENDS Naturals, FiniteSets, TLC

(*
  ABR-SESSION-0 candidate reference model.
  NOT CHECKED by TLC; NOT an implementation or Owner-approved contract.
  Finite abstraction: producer registration, fence capture, dependency
  registration, visibility, terminalization and restore high-water.
*)

CONSTANTS Producers, Artifacts, Targets, NoTarget

ASSUME Producers # {} /\ Artifacts # {} /\ Targets # {}

VARIABLES
  registered,
  terminal,
  artifactOwner,
  artifactTarget,
  dependencyRegistered,
  visible,
  fenceInstalled,
  fenceHighWater,
  registrationSeq,
  suppressed,
  inventorySealed,
  barrierClosed,
  restoreControlGeneration,
  currentControlGeneration

vars ==
  <<registered, terminal, artifactOwner, artifactTarget,
    dependencyRegistered, visible, fenceInstalled, fenceHighWater,
    registrationSeq, suppressed, inventorySealed, barrierClosed,
    restoreControlGeneration, currentControlGeneration>>

Init ==
  /\ registered = {}
  /\ terminal = {}
  /\ artifactOwner = [a \in Artifacts |-> CHOOSE p \in Producers : TRUE]
  /\ artifactTarget = [a \in Artifacts |-> CHOOSE t \in Targets : TRUE]
  /\ dependencyRegistered = {}
  /\ visible = {}
  /\ fenceInstalled = FALSE
  /\ fenceHighWater = 0
  /\ registrationSeq = [p \in Producers |-> 0]
  /\ suppressed = {}
  /\ inventorySealed = FALSE
  /\ barrierClosed = FALSE
  /\ restoreControlGeneration = 0
  /\ currentControlGeneration = 0

RegisterProducer(p) ==
  /\ p \in Producers
  /\ p \notin registered
  /\ ~fenceInstalled
  /\ registered' = registered \cup {p}
  /\ registrationSeq' = [registrationSeq EXCEPT ![p] = 1]
  /\ UNCHANGED <<terminal, artifactOwner, artifactTarget,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      suppressed, inventorySealed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

InstallFence ==
  /\ ~fenceInstalled
  /\ fenceInstalled' = TRUE
  /\ fenceHighWater' = Cardinality(registered)
  /\ currentControlGeneration' = currentControlGeneration + 1
  /\ UNCHANGED <<registered, terminal, artifactOwner, artifactTarget,
      dependencyRegistered, visible, registrationSeq, suppressed,
      inventorySealed, barrierClosed, restoreControlGeneration>>

RegisterDependency(a) ==
  /\ a \in Artifacts
  /\ artifactOwner[a] \in registered
  /\ a \notin dependencyRegistered
  /\ dependencyRegistered' = dependencyRegistered \cup {a}
  /\ UNCHANGED <<registered, terminal, artifactOwner, artifactTarget,
      visible, fenceInstalled, fenceHighWater, registrationSeq,
      suppressed, inventorySealed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

Publish(a) ==
  /\ a \in Artifacts
  /\ artifactOwner[a] \in registered
  /\ a \in dependencyRegistered
  /\ artifactTarget[a] \notin suppressed
  /\ visible' = visible \cup {a}
  /\ UNCHANGED <<registered, terminal, artifactOwner, artifactTarget,
      dependencyRegistered, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, inventorySealed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

Terminalize(p) ==
  /\ p \in registered
  /\ p \notin terminal
  /\ terminal' = terminal \cup {p}
  /\ UNCHANGED <<registered, artifactOwner, artifactTarget,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, inventorySealed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

SuppressTarget(t) ==
  /\ t \in Targets
  /\ fenceInstalled
  /\ suppressed' = suppressed \cup {t}
  /\ visible' = {a \in visible : artifactTarget[a] # t}
  /\ UNCHANGED <<registered, terminal, artifactOwner, artifactTarget,
      dependencyRegistered, fenceInstalled, fenceHighWater,
      registrationSeq, inventorySealed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

SealInventory ==
  /\ fenceInstalled
  /\ inventorySealed' = TRUE
  /\ UNCHANGED <<registered, terminal, artifactOwner, artifactTarget,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

CloseBarrier ==
  /\ fenceInstalled
  /\ inventorySealed
  /\ Cardinality(terminal) = Cardinality(registered)
  /\ barrierClosed' = TRUE
  /\ UNCHANGED <<registered, terminal, artifactOwner, artifactTarget,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, inventorySealed,
      restoreControlGeneration, currentControlGeneration>>

Restore(snapshotGeneration) ==
  /\ snapshotGeneration \in Nat
  /\ restoreControlGeneration' = snapshotGeneration
  /\ currentControlGeneration' = currentControlGeneration
  /\ UNCHANGED <<registered, terminal, artifactOwner, artifactTarget,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, inventorySealed, barrierClosed>>

Next ==
  \/ \E p \in Producers : RegisterProducer(p)
  \/ InstallFence
  \/ \E a \in Artifacts : RegisterDependency(a)
  \/ \E a \in Artifacts : Publish(a)
  \/ \E p \in Producers : Terminalize(p)
  \/ \E t \in Targets : SuppressTarget(t)
  \/ SealInventory
  \/ CloseBarrier
  \/ \E g \in Nat : Restore(g)

Spec == Init /\ [][Next]_vars

TypeOK ==
  /\ registered \subseteq Producers
  /\ terminal \subseteq registered
  /\ visible \subseteq Artifacts
  /\ dependencyRegistered \subseteq Artifacts
  /\ suppressed \subseteq Targets

NoVisibleSuppressedTarget ==
  \A a \in visible : artifactTarget[a] \notin suppressed

RegisterBeforeVisible ==
  \A a \in visible :
    artifactOwner[a] \in registered /\ a \in dependencyRegistered

TerminalSubsetRegistered ==
  terminal \subseteq registered

BarrierSoundness ==
  barrierClosed => inventorySealed /\ terminal = registered

RestoreDoesNotLowerControl ==
  restoreControlGeneration <= currentControlGeneration

====
