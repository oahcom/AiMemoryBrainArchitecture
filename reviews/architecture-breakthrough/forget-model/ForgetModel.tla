---------------- MODULE ForgetModel ----------------
EXTENDS Naturals, FiniteSets, TLC

(*
  ABR-SESSION-0 candidate reference model.
  NOT CHECKED by TLC; NOT an implementation or Owner-approved contract.
  Finite abstraction: producer registration, fence capture, dependency
  registration, visibility, terminalization and safe restore overlay.
*)

CONSTANTS Producers, Artifacts, Targets, ArtifactProducer,
          ArtifactTarget, FenceTargets

ASSUME Producers # {}
ASSUME Artifacts # {}
ASSUME Targets # {}
ASSUME FenceTargets \subseteq Targets
ASSUME ArtifactProducer \in [Artifacts -> Producers]
ASSUME ArtifactTarget \in [Artifacts -> Targets]

VARIABLES
  registered,
  preFenceRegistered,
  terminal,
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
  <<registered, preFenceRegistered, terminal, dependencyRegistered,
    visible, fenceInstalled, fenceHighWater, registrationSeq,
    suppressed, inventorySealed, barrierClosed,
    restoreControlGeneration, currentControlGeneration>>

Init ==
  /\ registered = {}
  /\ preFenceRegistered = {}
  /\ terminal = {}
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
  /\ registrationSeq' =
       [registrationSeq EXCEPT ![p] = Cardinality(registered) + 1]
  /\ UNCHANGED <<preFenceRegistered, terminal, dependencyRegistered,
      visible, fenceInstalled, fenceHighWater, suppressed,
      inventorySealed, barrierClosed, restoreControlGeneration,
      currentControlGeneration>>

InstallFence ==
  /\ ~fenceInstalled
  /\ fenceInstalled' = TRUE
  /\ preFenceRegistered' = registered
  /\ fenceHighWater' = Cardinality(registered)
  /\ suppressed' = suppressed \cup FenceTargets
  /\ visible' = {a \in visible : ArtifactTarget[a] \notin FenceTargets}
  /\ currentControlGeneration' = currentControlGeneration + 1
  /\ UNCHANGED <<registered, terminal, dependencyRegistered,
      registrationSeq, inventorySealed, barrierClosed,
      restoreControlGeneration>>

RegisterDependency(a) ==
  /\ a \in Artifacts
  /\ ArtifactProducer[a] \in registered
  /\ a \notin dependencyRegistered
  /\ dependencyRegistered' = dependencyRegistered \cup {a}
  /\ UNCHANGED <<registered, preFenceRegistered, terminal,
      visible, fenceInstalled, fenceHighWater, registrationSeq,
      suppressed, inventorySealed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

Publish(a) ==
  /\ a \in Artifacts
  /\ ArtifactProducer[a] \in registered
  /\ ArtifactProducer[a] \notin terminal
  /\ a \in dependencyRegistered
  /\ ArtifactTarget[a] \notin suppressed
  /\ visible' = visible \cup {a}
  /\ UNCHANGED <<registered, preFenceRegistered, terminal,
      dependencyRegistered, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, inventorySealed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

Terminalize(p) ==
  /\ p \in registered
  /\ p \notin terminal
  /\ terminal' = terminal \cup {p}
  /\ UNCHANGED <<registered, preFenceRegistered, artifactOwner,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, inventorySealed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

SealInventory ==
  /\ fenceInstalled
  /\ inventorySealed' = TRUE
  /\ UNCHANGED <<registered, preFenceRegistered, terminal,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, barrierClosed,
      restoreControlGeneration, currentControlGeneration>>

CloseBarrier ==
  /\ fenceInstalled
  /\ inventorySealed
  /\ preFenceRegistered \subseteq terminal
  /\ {a \in Artifacts : ArtifactProducer[a] \in preFenceRegistered}
       \subseteq dependencyRegistered
  /\ barrierClosed' = TRUE
  /\ UNCHANGED <<registered, preFenceRegistered, terminal,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, inventorySealed,
      restoreControlGeneration, currentControlGeneration>>

Restore ==
  /\ restoreControlGeneration' = currentControlGeneration
  /\ UNCHANGED <<registered, preFenceRegistered, terminal,
      dependencyRegistered, visible, fenceInstalled, fenceHighWater,
      registrationSeq, suppressed, inventorySealed, barrierClosed,
      currentControlGeneration>>

Next ==
  \/ \E p \in Producers : RegisterProducer(p)
  \/ InstallFence
  \/ \E a \in Artifacts : RegisterDependency(a)
  \/ \E a \in Artifacts : Publish(a)
  \/ \E p \in Producers : Terminalize(p)
  \/ SealInventory
  \/ CloseBarrier
  \/ Restore

Spec == Init /\ [][Next]_vars

TypeOK ==
  /\ registered \subseteq Producers
  /\ preFenceRegistered \subseteq Producers
  /\ terminal \subseteq registered
  /\ visible \subseteq Artifacts
  /\ dependencyRegistered \subseteq Artifacts
  /\ suppressed \subseteq Targets

NoVisibleSuppressedTarget ==
  \A a \in visible : ArtifactTarget[a] \notin suppressed

RegisterBeforeVisible ==
  \A a \in visible :
    ArtifactProducer[a] \in registered /\ a \in dependencyRegistered

TerminalSubsetRegistered ==
  terminal \subseteq registered

BarrierSoundness ==
  barrierClosed =>
    inventorySealed /\ preFenceRegistered \subseteq terminal /\
    {a \in Artifacts : ArtifactProducer[a] \in preFenceRegistered}
      \subseteq dependencyRegistered

FenceHighWaterSoundness ==
  fenceInstalled => fenceHighWater = Cardinality(preFenceRegistered)

RestoreDoesNotLowerControl ==
  restoreControlGeneration <= currentControlGeneration

====
