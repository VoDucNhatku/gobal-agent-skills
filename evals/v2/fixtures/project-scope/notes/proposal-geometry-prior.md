# Proposal: candidate-region geometry prior for tiny OBB

Idea: enlarge candidate regions to at least sqrt(2)·s so that every rotated tiny object
contains at least one anchor point on a stride-s grid.

Reasoning in the draft: "By the lattice theorem, any closed rectangle whose short side is
at least sqrt(2)·s contains a grid point. Therefore recall of tiny objects becomes 100%."

Status: draft, no experiment yet.
